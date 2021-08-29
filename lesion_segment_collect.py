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
from random import random

ROOTDIR = r"\\groupspaces.dcs.aber.ac.uk\groupspaces\mammography\OPTIMAM_ORIGINAL_new\OPTIMAM_DB\image_db\sharing\omi-db\images"
SAVEPATH = r"..\png_images\lesion_segments"
input_file = r"..\dem1todem1200.xlsx"
data = pd.read_excel(input_file)
new_data = data[['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION']]
#new_data = data[['folder','studyID','seriesID','imageID','laterality','pixel_style','procedure','opinion_screen','opinion_mammog','opinion_ultra']]

folder = []

count_row = new_data.shape[0]  # gives number of row count
count_col = new_data.shape[1]

start_point = 0
end_point = count_row
#end_point = 1
max_size_x = 0
max_size_y = 0

lesion_count = 0

for row in range(start_point, end_point):
    x1 = int(new_data['X1'][row] / 4)
    x2 = int(new_data['X2'][row] / 4)
    y1 = int(new_data['Y1'][row] / 4)
    y2 = int(new_data['Y2'][row] / 4)
    size_x = (int)(x2-x1)
    size_y = (int)(y2-y1)
    size = (size_x, size_y)

    # screen out oversized lesions. We can probably center it inside a large one in a later variant
    if(size_x < 257 and size_y < 257):
        lesion_count = lesion_count + 1
        #expand outwards random amount
        padding_x = 256 - size_x
        padding_y = 256 - size_y

        
        print("lesion location:(" + str(x1) + "," + str(y1) + ")->(" + str(x2) + "," + str(y2) + ")")
        print("lesion size:" + str(size))
        FOLDER_PATH = os.path.join(ROOTDIR, str(new_data['FOLDER'].iloc[row]))
        LESION_FOLDER = os.path.join(FOLDER_PATH, str(new_data['LESION_FOLDER'].iloc[row]))
        IMAGE_PATH = os.path.join(LESION_FOLDER, str(new_data['LESION_FILE'].iloc[row]) + ".dcm")

        label_folder = os.path.join(SAVEPATH, "lesion")
    
        file_output =  os.path.join(label_folder, str(new_data['LESION_FILE'].iloc[row]) + ".png")
        print("checking file:" + str(file_output))
        found = os.path.isfile(file_output)
        print("Found!" if found else "Not Found!")
        if(not os.path.isfile(file_output)):        
            try:
                image = UTILS.diread(IMAGE_PATH)
                Path(file_output).parents[0].mkdir(parents=True, exist_ok=True)
                #lesion = UTILS.segmented_image(image,x1,x2,y1,y2)

                image_size = image.shape
                print("Base image size:" + str(image_size))
                image_size = tuple((int)(i/4) for i in image.shape)
                print("Scaled image size:" + str(image_size))
                proportion_x = random()
                proportion_y = random()

                left_proportion_x = (int)(proportion_x * padding_x)
                top_proportion_y = (int)(proportion_y * padding_y)
                right_proportion_x = padding_x - left_proportion_x
                bottom_proportion_y = padding_y - top_proportion_y

                print("corners are at:(" + str(x1) + "," + str(y1) + ")->(" + str(x2) + "," + str(y2) + ")")

                print(left_proportion_x)
                print(right_proportion_x)
                print(top_proportion_y)
                print(bottom_proportion_y)

                variance_x1 = 0 - (x1 - left_proportion_x)
                variance_x1 = max(variance_x1,0)
                left_proportion_x = left_proportion_x - variance_x1
                right_proportion_x = right_proportion_x + variance_x1

                variance_x2 = (image_size[1] - 1) - (x2 + right_proportion_x)
                variance_x2 = min(variance_x2,0)
                right_proportion_x = right_proportion_x + variance_x2
                left_proportion_x = left_proportion_x - variance_x2

                variance_y1 = 0 - (y1 - top_proportion_y)
                variance_y1 = max(variance_y1,0)
                top_proportion_y = top_proportion_y - variance_y1
                bottom_proportion_y = bottom_proportion_y + variance_y1

                variance_y2 = (image_size[0] - 1) - (y2 + bottom_proportion_y)
                variance_y2 = min(variance_y2,0)
                top_proportion_y = top_proportion_y + variance_y2
                bottom_proportion_y = bottom_proportion_y - variance_y2

                
                x1 = x1 - left_proportion_x
                x2 = x2 + right_proportion_x
                y1 = y1 - top_proportion_y
                y2 = y2 + bottom_proportion_y

                print(left_proportion_x)
                print(right_proportion_x)
                print(top_proportion_y)
                print(bottom_proportion_y)
                
                print("corners are at:(" + str(x1) + "," + str(y1) + ")->(" + str(x2) + "," + str(y2) + ")")

                scaled_image = resize(image,image_size,anti_aliasing=True) # comes out as 0-1 float64
  
                lesion = UTILS.segmented_image(scaled_image,x1,x2,y1,y2)

                lesion_z = (65535*((lesion - lesion.min())/lesion.ptp())).astype(np.uint16) # rescaled to 16-bit output
            
                f = open(file_output, 'wb')
                writer = png.Writer(width=256, height=256, bitdepth=16, greyscale=True)
                writer.write(f, lesion_z)
                f.close() 

                print("Image " + str(row) + ", original type:" + str(image.dtype) + " reprocessed")            
            except IOError as e:
                print(str(e))
        else:
            print("rejected")
    
SAVEPATH = r"..\png_images\lesion_segments"
input_file = r"..\casewise_nolesion.xlsx"
data = pd.read_excel(input_file)
#new_data = data[['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION']]
new_data = data[['folder','studyID','seriesID','imageID','laterality','pixel_style','procedure','opinion_screen','opinion_mammog','opinion_ultra']]

folder = []

count_row = new_data.shape[0]  # gives number of row count
count_col = new_data.shape[1]

start_point = 0
end_point = count_row

for row in range(start_point, end_point):
    print("row:" + str(row) + " type:" + str(new_data['procedure'][row]) + " opinion:" + str(new_data['opinion_mammog'][row]))
    procedure = str(new_data['procedure'][row])
    pf = procedure.find("/")
    if(pf != -1):
        procedure = procedure[0:pf-1]
    #mammog = procedure.find("Mammog") != -1
    mammog = (procedure != None) and (procedure != 'nan')
    if(mammog):
        FOLDER_PATH = os.path.join(ROOTDIR, str(new_data['folder'].iloc[row]))
        LESION_FOLDER = os.path.join(FOLDER_PATH, str(new_data['studyID'].iloc[row]))
        IMAGE_PATH = os.path.join(LESION_FOLDER, str(new_data['imageID'].iloc[row]) + ".dcm")

        procedure_folder = os.path.join(SAVEPATH, "clean")

        file_output =  os.path.join(procedure_folder, str(new_data['imageID'].iloc[row]) + ".png")
        print("checking file:" + str(file_output))
        found = os.path.isfile(file_output)
        print("Found!" if found else "Not Found!")
        if(not os.path.isfile(file_output)):        
            try:
                image = UTILS.diread(IMAGE_PATH)

                image_size = image.shape

                Path(file_output).parents[0].mkdir(parents=True, exist_ok=True)


                print("Base image size:" + str(image_size))
                image_size = tuple((int)(i/4) for i in image.shape)
                print("Scaled image size:" + str(image_size))

                ok = False
                timeout = 60
                lesion_z = None
                
                while(not ok and (timeout > 0)):
                    timeout = timeout - 1
                    proportion_x = random()
                    proportion_y = random()

                    x2 = int((proportion_x * (image_size[1] - 256)) + 256)
                    x1 = x2 - 256

                    y2 = int((proportion_y * (image_size[0] - 256)) + 256)
                    y1 = y2 - 256
                    
                    print("corners are at:(" + str(x1) + "," + str(y1) + ")->(" + str(x2) + "," + str(y2) + ")")

                    scaled_image = resize(image,image_size,anti_aliasing=True) # comes out as 0-1 float64
      
                    lesion = UTILS.segmented_image(scaled_image,x1,x2,y1,y2)

                    #check segment is not mostly black, reject if so

                    lesion_z = (65535*((lesion - lesion.min())/lesion.ptp())).astype(np.uint16) # rescaled to 16-bit output

                    z_mean = lesion_z.mean() / 65535.0
                    black_quotient = 1.0 - z_mean
                    print("image background quotient:"+str(black_quotient))
                    if(black_quotient < 0.80):
                        ok = True

                #lesion_z = (65535*((lesion - lesion.min())/lesion.ptp())).astype(np.uint16) # rescaled to 16-bit output
            
                f = open(file_output, 'wb')
                writer = png.Writer(width=256, height=256, bitdepth=16, greyscale=True)
                writer.write(f, lesion_z)
                f.close() 

                print("Image " + str(row) + ", original type:" + str(image.dtype) + " reprocessed")            
            except IOError as e:
                print(str(e))
                #print("Missing Image")
    else:
        print("rejected")


