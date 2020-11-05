import pandas as pd
import os 
import pydicom as dicom
import matplotlib.pyplot as plt
import numpy as np
import cv2
import utils as UTILS
from pathlib import Path

ROOTDIR = r"..\images"
SAVEPATH = r"..\new_data"
input_file = r"..\dem1todem1200.xlsx"
data = pd.read_excel(input_file)
new_data = data[['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION']]

count_row = new_data.shape[0]  # gives number of row count
count_col = new_data.shape[1]


for row in range(count_row-40, count_row):
    #print(new_data['X1'].iloc[row], new_data['X2'].iloc[row], new_data['Y1'].iloc[row], new_data['Y2'].iloc[row])
    print(row)
    FOLDER_PATH = os.path.join(ROOTDIR, str(new_data['FOLDER'].iloc[row]))
    LESION_FOLDER = os.path.join(FOLDER_PATH, str(new_data['LESION_FOLDER'].iloc[row]))
    IMAGE_PATH = os.path.join(LESION_FOLDER, str(new_data['LESION_FILE'].iloc[row]) + ".dcm")
    #print(IMAGE_PATH)
    if new_data['X1'].iloc[row] < new_data['X2'].iloc[row]:
        image = UTILS.diread(IMAGE_PATH)
        mask = UTILS.create_mask(image, new_data['X1'].iloc[row], new_data['X2'].iloc[row], new_data['Y1'].iloc[row], new_data['Y2'].iloc[row])
        seg_image = UTILS.segmented_image(image, new_data['X1'].iloc[row], new_data['X2'].iloc[row], new_data['Y1'].iloc[row], new_data['Y2'].iloc[row])
        segmented_image = UTILS.IMAGE_THREASHOLD_OTSU(seg_image)
        maskseg_image = UTILS.create_segmask(image,new_data['X1'].iloc[row], new_data['X2'].iloc[row], new_data['Y1'].iloc[row], new_data['Y2'].iloc[row], segmented_image)
        image_output, mask_output, seg_output, maskseg_output, array_output, bound_output = UTILS.output_location(SAVEPATH, new_data['BENIGNCLASSIFICATION'].iloc[row], new_data['MARKID'].iloc[row], new_data['MASSCLASSIFICATION'].iloc[row], 1)

        Path(image_output).parents[0].mkdir(parents=True, exist_ok=True)
        plt.imsave(image_output, image, cmap = 'gray')
        Path(mask_output).parents[0].mkdir(parents=True, exist_ok=True)
        plt.imsave(mask_output, mask, cmap = 'gray')
        Path(seg_output).parents[0].mkdir(parents=True, exist_ok=True)
        plt.imsave(seg_output, segmented_image, cmap = 'gray')
        Path(maskseg_output).parents[0].mkdir(parents=True, exist_ok=True)
        plt.imsave(maskseg_output, maskseg_image, cmap = 'gray')
        Path(bound_output).parents[0].mkdir(parents=True, exist_ok=True)
        plt.imsave(bound_output, seg_image, cmap = 'gray')
        Path(array_output).parents[0].mkdir(parents=True, exist_ok=True)
        np.save(array_output, segmented_image)
        



