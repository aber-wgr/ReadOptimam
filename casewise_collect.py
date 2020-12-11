import pandas as pd
import os 
import pydicom as dicom
import matplotlib.pyplot as plt
from skimage.transform import resize
import numpy as np
import cv2
import utils as UTILS
from pathlib import Path
import png

ROOTDIR = r"\\groupspaces.dcs.aber.ac.uk\groupspaces\mammography\OPTIMAM_ORIGINAL_new\OPTIMAM_DB\image_db\sharing\omi-db\images"
SAVEPATH = r"..\png_images\onecase"
input_file = r"..\onecase.xlsx"
data = pd.read_excel(input_file)
#new_data = data[['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION']]
new_data = data[['folder','studyID','seriesID','imageID','laterality','pixel_style','opinion_screen','opinion_mammog','opinion_ultra']]
scale_factor = 4

folder = []

count_row = new_data.shape[0]  # gives number of row count
count_col = new_data.shape[1]

count_row = 25

for row in range(0, count_row):
    print(row)
    FOLDER_PATH = os.path.join(ROOTDIR, str(new_data['folder'].iloc[row]))
    LESION_FOLDER = os.path.join(FOLDER_PATH, str(new_data['studyID'].iloc[row]))
    IMAGE_PATH = os.path.join(LESION_FOLDER, str(new_data['imageID'].iloc[row]) + ".dcm")
    try:
        image = UTILS.diread(IMAGE_PATH)
        x = int(4096 / scale_factor)
        y = int(3328 / scale_factor)
        scaled_image = resize(image, ( x, x), anti_aliasing=True) # comes out as 0-1 float64
        scaled_image_z = (65535*((scaled_image - scaled_image.min())/scaled_image.ptp())).astype(np.uint16)
        #scaled_image_z = scaled_image.astype(np.uint16) #convert back to 16-bit grayscale
        #image_output, mask_output, seg_output, maskseg_output, array_output, bound_output = UTILS.output_location(SAVEPATH, "", "", "", 1)
        image_output =  os.path.join(SAVEPATH, str(new_data['imageID'].iloc[row]) + ".png")
        Path(image_output).parents[0].mkdir(parents=True, exist_ok=True)

        print("Image " + str(row) + ", original type:" + str(image.dtype))

        f = open(image_output, 'wb')
        writer = png.Writer(width=x, height=x, bitdepth=16, greyscale=True)
        writer.write(f, scaled_image_z)
        #plt.imsave(image_output, scaled_image, cmap = 'gray')
        #print("Image " + str(row) + ", original type:" + str(image.dtype))
    except IOError:
        print("Missing Image")
    



