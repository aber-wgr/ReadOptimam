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
SAVEPATH = r"..\png_images\lesion_segments\"
input_file = r"..\dem1todem1200.xlsx"
data = pd.read_excel(input_file)
new_data = data[['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION']]
#new_data = data[['folder','studyID','seriesID','imageID','laterality','pixel_style','procedure','opinion_screen','opinion_mammog','opinion_ultra']]

folder = []

count_row = new_data.shape[0]  # gives number of row count
count_col = new_data.shape[1]

start_point = 0
end_point = count_row

for row in range(start_point, end_point):
    x1 = int(new_data['X1'][row])
    x2 = int(new_data['X2'][row])
    y1 = int(new_data['Y1'][row])
    y2 = int(new_data['Y2'][row])
    size = {x2-x1, y2-y1)
    print("lesion size:" + str(size))
    FOLDER_PATH = os.path.join(ROOTDIR, str(new_data['FOLDER'].iloc[row]))
    LESION_FOLDER = os.path.join(FOLDER_PATH, str(new_data['LESION_FOLDER'].iloc[row]))
    IMAGE_PATH = os.path.join(LESION_FOLDER, str(new_data['LESION_FILE'].iloc[row]) + ".dcm")

    file_output =  os.path.join(clabel_folder, str(new_data['LESION_FILE'].iloc[row]) + ".png")
    print("checking file:" + str(file_output))
    found = os.path.isfile(file_output)
    print("Found!" if found else "Not Found!")
#    if(not os.path.isfile(file_output)):        
#        try:
#            image = UTILS.diread(IMAGE_PATH)

#            label_folder = os.path.join(SAVEPATH, opinion)
#            image_output =  os.path.join(label_folder, str(new_data['LESION_FILE'].iloc[row]) + ".png")
            
#            Path(image_output).parents[0].mkdir(parents=True, exist_ok=True)

#            lesion = UTILS.segmented_image(x1,y1,x2,y2)



            
#            f = open(image_output, 'wb')
#            writer = png.Writer(width=size, height=size, bitdepth=16, greyscale=True)
#            writer.write(f, lesion)
#            f.close() 

#            print("Image " + str(row) + ", original type:" + str(image.dtype) + " reprocessed")            
#        except IOError as e:
#            print(str(e))
#            #print("Missing Image")
    else:
        print("rejected")
    



