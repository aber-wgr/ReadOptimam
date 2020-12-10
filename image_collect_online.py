import pandas as pd
import os 
import pydicom as dicom
import matplotlib.pyplot as plt
from skimage.transform import resize
import numpy as np
import cv2
import utils as UTILS
from pathlib import Path

ROOTDIR = r"\\groupspaces.dcs.aber.ac.uk\groupspaces\mammography\OPTIMAM_ORIGINAL_new\OPTIMAM_DB\image_db\sharing\omi-db\images"
SAVEPATH = r"..\png_images\lesions"
input_file = r"..\dem1todem1200.xlsx"
data = pd.read_excel(input_file)
new_data = data[['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION']]

scale_factor = 2

count_row = new_data.shape[0]  # gives number of row count
count_col = new_data.shape[1]


for row in range(0, count_row):
    print(row)
    FOLDER_PATH = os.path.join(ROOTDIR, str(new_data['FOLDER'].iloc[row]))
    LESION_FOLDER = os.path.join(FOLDER_PATH, str(new_data['LESION_FOLDER'].iloc[row]))
    IMAGE_PATH = os.path.join(LESION_FOLDER, str(new_data['LESION_FILE'].iloc[row]) + ".dcm")
    try:
        image = UTILS.diread(IMAGE_PATH)
        #scaled_image = resize(image, ( 4096 / scale_factor, 3328 / scale_factor), anti_aliasing=False)
        #image_output, mask_output, seg_output, maskseg_output, array_output, bound_output = UTILS.output_location(SAVEPATH, new_data['BENIGNCLASSIFICATION'].iloc[row], new_data['MARKID'].iloc[row], new_data['MASSCLASSIFICATION'].iloc[row], 1)
        #image_output =  os.path.join(SAVEPATH, str(new_data['MARKID'].iloc[row]) + ".png")
        #Path(image_output).parents[0].mkdir(parents=True, exist_ok=True)
        #plt.imsave(image_output, scaled_image, cmap = 'gray')
        print("Image " + str(row) + ", original type:" + str(image.dtype))
    except IOError:
        print("Missing Image")
    



