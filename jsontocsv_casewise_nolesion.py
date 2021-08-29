import pandas as pd
import os 
import pydicom as dicom
import matplotlib.pyplot as plt
import numpy as np
import cv2
import utils as UTILS
import json 
import pickle

ROOTDIR = r"..\data"

listdir = os.listdir(ROOTDIR)

Episodes = {}
ImageList = {"folder":[], "studyID":[], "seriesID":[], "imageID":[], "laterality":[], "pixel_style":[], "procedure":[], "opinion_screen":[], "opinion_mammog":[], "opinion_ultra":[]}

#modified version of the script to build the extraction CSV.
#In this we are interested in retrieving the casewise data and connecting that to the images
#Unlike the previous version (which is focused on retrieving marked-up lesion images) this version
#is intended for classification experiments

for folder in listdir:
    print(folder)
    Episodes[folder] = {}
    new_dir = os.path.join(ROOTDIR, folder)
    imageDB_file = os.path.join(new_dir, "imagedb_" + folder + ".json")
    nbss_file = os.path.join(new_dir, "nbss_" + folder + ".json")
    imageDB_jsonfile = open(imageDB_file)
    nbss_jsonfile = open(nbss_file)
    imageDB = json.load(imageDB_jsonfile)
    nbss = json.load(nbss_jsonfile)

    # first up, load up the list of Episodes. 
    # Every one of our Studies should be attached to a specific Episode of some kind. To this end, we will store 
    # the per-client results by EpisodeID, with the episodal info attached and a StudyList linking into the ImageDB info

    episodeSet = nbss
    for episodeID in episodeSet:
        if(episodeID!="ClientID" and episodeID!="Classification"):
            print("Resolving Episode " + episodeID)
            newEpisode = {}
            newEpisode["Id"] = episodeID
            episodeData = episodeSet[episodeID]
            # for each client there are many Episodes where there is no attached imaging data (and usually no images or screening either)
            # the distinction is StudyList being non-null
            # Note that this does not cover all cancer incidents. If it possible to have listed cancer incidents with no Studies attached
            # However we don't care about elements we don't have imaging for 
            studyList = episodeData["StudyList"]
            if(studyList!=None):
                # this is an interesting element. (Not all Studies attached to an Episode will have Marks)
                newEpisode["StudyList"] = studyList
                newEpisode["Opinions"] = { "L":{}, "R":{} }
                #Extract the various potential Opinions
                #Note these will not always be present
                assessment = episodeData.get("ASSESSMENT")
                if(assessment!=None):
                    # if we have an ASSESSMENT segment, we can potentially retrieve Ultrasound Survey and Mammographic opinions (Ux and Rx)
                    # these will be subgrouped for left/right, and will not always be present for both
                    left_assess = assessment.get("L")
                    right_assess = assessment.get("R")
                    # there can also be more than one assessment per breast too, although this virtually never happens
                    if(left_assess!=None):
                        for instance in left_assess:
                            newEpisode["Opinions"]["L"]["MammoOpinion"] = left_assess[instance]["MammoOpinion"]
                            newEpisode["Opinions"]["L"]["UssOpinion"] = left_assess[instance]["UssOpinion"]
                            break
                    if(right_assess!=None):
                        for instance in right_assess:
                            print(instance)
                            newEpisode["Opinions"]["R"]["MammoOpinion"] = right_assess[instance]["MammoOpinion"]
                            newEpisode["Opinions"]["R"]["UssOpinion"] = right_assess[instance]["UssOpinion"]
                            break

                screening = episodeData.get("SCREENING")
                if(screening!=None):
                    # We can have both SCREENING and ASSESSMENT and they're both radiological opinions, grump
                    left_screen = screening.get("L")
                    right_screen = screening.get("R")
                    if(left_screen!=None):
                        newEpisode["Opinions"]["L"]["ScreenOpinion"] = left_screen["Opinion"]
                    if(right_screen!=None):
                        newEpisode["Opinions"]["R"]["ScreenOpinion"] = right_screen["Opinion"]
            
                newEpisode["studyID"] = []
                newEpisode["seriesID"] = []
                newEpisode["imageID"] = []
                # now we've constructed the opinions set we should add this to the Big List
                Episodes[folder][episodeID] = newEpisode;


    studySet = imageDB['STUDIES'] #layer1
    for study in studySet:
        seriesSet = studySet[study] #layer2
        epID = seriesSet.get("EpisodeID")
        if(epID!=None):
            episode = Episodes[folder].get(epID)
            # we only care about studies that have attached Episodes
            if(episode!=None):
                for series in seriesSet: 
                    # this can be a series entry, or the EpisodeID and StudyDate
                    if series != "EpisodeID" and series != "StudyDate":
                        sopSet = seriesSet[series] #layer3
                        for sop in sopSet:
                            if(sop != ""):
                                #We have an image identifier here
                                    episode["studyID"].append(study)
                                    episode["seriesID"].append(series)
                                    episode["imageID"].append(sop)

                                    markSet = sopSet[sop] #layer4
                                    if(markSet == None) or (len(markSet)==0):
                                        image_tags_file = os.path.join(new_dir, study, sop + ".json")
                                        image_tags_jsonfile = None
                                        try:
                                            image_tags_jsonfile = open(image_tags_file)
                                        except:
                                            image_tags_file = os.path.join(new_dir, study, sop + ".dcm.json")
                                            try:
                                                image_tags_jsonfile = open(image_tags_file)
                                            except:
                                                # if we can't load the thing, it's one of the weird unconnected entries
                                                break
                                            finally:
                                                dd = ""
                                        if(image_tags_jsonfile!=None):
                                            print("Loading image tags from:" + image_tags_file)
                                            image_tags = None
                                            try:
                                                image_tags = json.load(image_tags_jsonfile)
                                            except:
                                                image_tags_jsonfile.close()
                                                break
                                            #laterality value is at 0020,0062 and can be any one of "L", "R", "U" (Unpaired, shouldn't be in this set) or "B" (Both)
                                            laterality_section = image_tags.get("00200062")
                                            if(laterality_section!=None):
                                                laterality_value = laterality_section.get("Value")
                                                if(laterality_value!=None):
                                                    laterality = laterality_value[0]
                                                    #Look up the pixel style. MONOCHROME2 is black-minimum (standard black image), MONOCHROME1 is white-minimum
                                                    pixel_style_section = image_tags["00280004"]
                                                    pixel_style = pixel_style_section["Value"][0]
                                                    procedure_section = image_tags.get("00400254")
                                                    procedure = None
                                                    if(procedure_section != None):
                                                        procedure_value = procedure_section.get("Value")
                                                        if(procedure_value!= None):
                                                            procedure = procedure_value[0]
                                                    if(pixel_style=="MONOCHROME2"):
                                                        if(laterality=="L" or laterality=="R"):
                                                            ImageList["studyID"].append(study)
                                                            ImageList["seriesID"].append(series)
                                                            ImageList["imageID"].append(sop)
                                                            ImageList["folder"].append(folder)
                                                            ImageList["laterality"].append(laterality)
                                                            ImageList["pixel_style"].append(pixel_style)
                                                            ImageList["procedure"].append(procedure)
                                                            ImageList["opinion_screen"].append(episode["Opinions"][laterality].get("ScreenOpinion"))
                                                            ImageList["opinion_mammog"].append(episode["Opinions"][laterality].get("MammoOpinion"))
                                                            ImageList["opinion_ultra"].append(episode["Opinions"][laterality].get("UssOpinion"))
                                            image_tags_jsonfile.close()

                            
#df = pd.DataFrame(list(zip(FOLDER,LESION_FOLDER,LESION_FILE,BENIGNCLASSIFICATION, MASSCLASSIFICATION,WIDTH,SUSPICIOUSCALCIFICATIONS,PLASMACELLMASTITIS,XONE,XTWO,WITHCALCIFICATION,MARKID,SUTURECALCIFICATION,OTHERBENIGNCLUSTER,FOCALASYMMETRY,MILKOFCALCIUM,DYSTROPHIC,LESIONID,CONSPICUITY,FATNECROSIS,HEIGHT,YONE,YTWO,VASCULAR,MASS,SKIN,ARCHITECTUREDISTORTION)), columns = ['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION'])
df = pd.DataFrame(ImageList)
output = r"..\casewise_nolesion.xlsx"
df.to_excel(output)
