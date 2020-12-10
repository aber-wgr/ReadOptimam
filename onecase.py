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

ImageList = {}


#modified version of the script to build the extraction CSV.
#In this we are interested in retrieving the casewise data and connecting that to the images
#Unlike the previous version (which is focused on retrieving marked-up lesion images) this version
#is intended for classification experiments

folder = "demd1"

ImageList = {"folder":[], "studyID":[], "seriesID":[], "imageID":[], "laterality":[]}
new_dir = os.path.join(ROOTDIR, folder)
imageDB_file = os.path.join(new_dir, "imagedb_" + folder + ".json")
nbss_file = os.path.join(new_dir, "nbss_" + folder + ".json")
imageDB_jsonfile = open(imageDB_file)
nbss_jsonfile = open(nbss_file)
imageDB = json.load(imageDB_jsonfile)
nbss = json.load(nbss_jsonfile)

studySet = imageDB['STUDIES']
for study in studySet:
    seriesSet = studySet[study]
    for series in seriesSet:
        # this can be a series entry, or the EpisodeID and StudyDate
        if series != "EpisodeID" and series != "StudyDate":
            sopSet = seriesSet[series]
            for sop in sopSet:
                if(sop != ""):
                    #We have an image identifier here
                    ImageList["studyID"].append(study)
                    ImageList["seriesID"].append(series)
                    ImageList["imageID"].append(sop)
                    ImageList["folder"].append(folder)

#folder is studyID, file is imageID
OutputList = {"folder":[], "studyID":[], "seriesID":[], "imageID":[], "laterality":[], "pixel_style":[]}
for i in range(len(ImageList["imageID"])):
    image_tags_file = os.path.join(new_dir, ImageList["studyID"][i], ImageList["imageID"][i] + ".json")
    image_tags_jsonfile = open(image_tags_file)
    image_tags = json.load(image_tags_jsonfile)
    #laterality value is at 0020,0062 and can be any one of "L", "R", "U" (Unpaired, shouldn't be in this set) or "B" (Both)
    laterality_section = image_tags["00200062"]
    laterality_value = laterality_section["Value"][0]
    #ImageList["laterality"].append(laterality_value)
    #Look up the pixel style. MONOCHROME2 is black-minimum (standard black image), MONOCHROME1 is white-minimum
    pixel_style_section = image_tags["00280004"]
    pixel_style = pixel_style_section["Value"][0]
    if(pixel_style=="MONOCHROME2"):
        OutputList["studyID"].append(ImageList["studyID"][i])
        OutputList["seriesID"].append(ImageList["seriesID"][i])
        OutputList["imageID"].append(ImageList["imageID"][i])
        OutputList["folder"].append(ImageList["folder"][i])
        OutputList["laterality"].append(laterality_value)
        OutputList["pixel_style"].append(pixel_style)

df = pd.DataFrame(OutputList)                        
#df = pd.DataFrame(list(zip(FOLDER,LESION_FOLDER,LESION_FILE,BENIGNCLASSIFICATION, MASSCLASSIFICATION,WIDTH,SUSPICIOUSCALCIFICATIONS,PLASMACELLMASTITIS,XONE,XTWO,WITHCALCIFICATION,MARKID,SUTURECALCIFICATION,OTHERBENIGNCLUSTER,FOCALASYMMETRY,MILKOFCALCIUM,DYSTROPHIC,LESIONID,CONSPICUITY,FATNECROSIS,HEIGHT,YONE,YTWO,VASCULAR,MASS,SKIN,ARCHITECTUREDISTORTION)), columns = ['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION'])
output = r"..\onecase.xlsx"
df.to_excel(output)
