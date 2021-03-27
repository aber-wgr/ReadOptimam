import pandas as pd
import os 
import pydicom as dicom
import matplotlib.pyplot as plt
import numpy as np
import utils as UTILS
import json 
import pickle

ROOTDIR = r"\\path\to\optimam\install"

listdir = os.listdir(ROOTDIR)

FOLDER = []
LESION_FOLDER = []
LESION_FILE = []
LINKEDNBSSLESIONUMBER = []
BENIGNCLASSIFICATION = []
MASSCLASSIFICATION = []
WIDTH = []
SUSPICIOUSCALCIFICATIONS = []
PLASMACELLMASTITIS = []
XONE = []
XTWO = []
WITHCALCIFICATION = []
MARKID = []
SUTURECALCIFICATION = []
OTHERBENIGNCLUSTER = []
FOCALASYMMETRY = []
MILKOFCALCIUM = []
DYSTROPHIC = []
LESIONID = []
CONSPICUITY = []
FATNECROSIS = []
HEIGHT = []
YONE = []
YTWO = []
VASCULAR = []
MASS = []
SKIN = []
ARCHITECTUREDISTORTION = []


for folder in listdir:
    print(folder)
    new_dir = os.path.join(ROOTDIR, folder)
    file = os.path.join(new_dir, "imagedb_" + folder + ".json")
    jsonfile = open(file)
    jsondata = json.load(jsonfile)
    layer1 = jsondata['STUDIES']
    for lay1 in layer1:
        layer2 = layer1[lay1]
        for lay2 in layer2:
            if lay2 != "EpisodeID" and lay2 != "StudyDate":
                layer3 = layer2[lay2]
                for lay3 in layer3:
                    if(lay3 != ""):
                        layer4 = layer3[lay3]
                        if layer4 != None:
                            for lay4 in layer4:
                                print("Study ID:" + lay1)
                                print("Series ID:" + lay2)
                                print("SOP ID:" + lay3)
                                print("Mark ID:" + lay4)
                                layer5 = layer4[lay4]
                                FOLDER.append(folder)
                                LESION_FOLDER.append(lay1)
                                LESION_FILE.append(lay3)
                                #LINKEDNBSSLESIONUMBER.append(layer5['LinkedNBSSLesionNumber'])
                                BENIGNCLASSIFICATION.append(layer5['BenignClassification'])
                                if layer5['MassClassification'] == "ill_defined" or layer5['MassClassification'] == "spiculated":
                                    MASSCLASSIFICATION.append(layer5['MassClassification'])
                                else:
                                    MASSCLASSIFICATION.append('other')
                                WIDTH.append(layer5['Width'])
                                SUSPICIOUSCALCIFICATIONS.append(layer5['SuspiciousCalcifications'])
                                PLASMACELLMASTITIS.append(layer5['PlasmaCellMastitis'])
                                XONE.append(layer5['X1'])
                                XTWO.append(layer5['X2'])
                                WITHCALCIFICATION.append(layer5['WithCalcification'])
                                MARKID.append(layer5['MarkID'])
                                SUTURECALCIFICATION.append(layer5['SutureCalcification'])
                                OTHERBENIGNCLUSTER.append(layer5['OtherBenignCluster'])
                                FOCALASYMMETRY.append(layer5['FocalAsymmetry'])
                                MILKOFCALCIUM.append(layer5['MilkOfCalcium'])
                                DYSTROPHIC.append(layer5['Dystrophic'])
                                LESIONID.append(layer5['LesionID'])
                                CONSPICUITY.append(layer5['Conspicuity'])
                                FATNECROSIS.append(layer5['FatNecrosis'])
                                HEIGHT.append(layer5['Height'])
                                YONE.append(layer5['Y1'])
                                VASCULAR.append(layer5['Vascular'])
                                MASS.append(layer5['Mass'])
                                SKIN.append(layer5['Skin'])
                                ARCHITECTUREDISTORTION.append(layer5['ArchitecturalDistortion'])
                                YTWO.append(layer5['Y2'])
                            
df = pd.DataFrame(list(zip(FOLDER,LESION_FOLDER,LESION_FILE,BENIGNCLASSIFICATION, MASSCLASSIFICATION,WIDTH,SUSPICIOUSCALCIFICATIONS,PLASMACELLMASTITIS,XONE,XTWO,WITHCALCIFICATION,MARKID,SUTURECALCIFICATION,OTHERBENIGNCLUSTER,FOCALASYMMETRY,MILKOFCALCIUM,DYSTROPHIC,LESIONID,CONSPICUITY,FATNECROSIS,HEIGHT,YONE,YTWO,VASCULAR,MASS,SKIN,ARCHITECTUREDISTORTION)), columns = ['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION'])
output = r"..\dem1todem1200.xlsx"
df.to_excel(output)
