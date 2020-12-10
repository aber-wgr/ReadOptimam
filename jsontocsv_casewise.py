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
                newEpisode["Opinions"] = { "Left":{}, "Right":{} }
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
                            newEpisode["Opinions"]["Left"]["MammoOpinion"] = left_assess[instance]["MammoOpinion"]
                            newEpisode["Opinions"]["Left"]["UssOpinion"] = left_assess[instance]["UssOpinion"]
                            break
                    if(right_assess!=None):
                        for instance in right_assess:
                            print(instance)
                            newEpisode["Opinions"]["Right"]["MammoOpinion"] = right_assess[instance]["MammoOpinion"]
                            newEpisode["Opinions"]["Right"]["UssOpinion"] = right_assess[instance]["UssOpinion"]
                            break

                screening = episodeData.get("SCREENING")
                if(screening!=None):
                    # We can have both SCREENING and ASSESSMENT and they're both radiological opinions, grump
                    left_screen = screening.get("L")
                    right_screen = screening.get("R")
                    if(left_screen!=None):
                        newEpisode["Opinions"]["Left"]["ScreenOpinion"] = left_screen["Opinion"]
                        break
                    if(right_screen!=None):
                        newEpisode["Opinions"]["Right"]["ScreenOpinion"] = instance["Opinion"]
                        break
            
                newEpisode["studyID"] = []
                newEpisode["seriesID"] = []
                newEpisode["imageID"] = []
                # now we've constructed the opinions set we should add this to the Big List
                Episodes[folder][episodeID] = newEpisode;


    studySet = imageDB['STUDIES']
    for study in studySet:
        seriesSet = studySet[study]
        epID = seriesSet.get("EpisodeID")
        if(epID!=None):
            episode = Episodes[folder].get(epID)
            # we only care about studies that have attached Episodes
            if(episode!=None):
                for series in seriesSet:
                    # this can be a series entry, or the EpisodeID and StudyDate
                    if series != "EpisodeID" and series != "StudyDate":
                        sopSet = seriesSet[series]
                        for sop in sopSet:
                            if(sop != ""):
                                #We have an image identifier here
                                    episode["studyID"].append(study)
                                    episode["seriesID"].append(series)
                                    episode["imageID"].append(sop)
                            
#df = pd.DataFrame(list(zip(FOLDER,LESION_FOLDER,LESION_FILE,BENIGNCLASSIFICATION, MASSCLASSIFICATION,WIDTH,SUSPICIOUSCALCIFICATIONS,PLASMACELLMASTITIS,XONE,XTWO,WITHCALCIFICATION,MARKID,SUTURECALCIFICATION,OTHERBENIGNCLUSTER,FOCALASYMMETRY,MILKOFCALCIUM,DYSTROPHIC,LESIONID,CONSPICUITY,FATNECROSIS,HEIGHT,YONE,YTWO,VASCULAR,MASS,SKIN,ARCHITECTUREDISTORTION)), columns = ['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION'])
df = pd.DataFrame(Episodes)
output = r"..\casewise.xlsx"
df.to_excel(output)
