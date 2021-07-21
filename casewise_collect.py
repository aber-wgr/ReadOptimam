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
SAVEPATH = r"..\png_images\casewise"
input_file = r"..\casewise.xlsx"
data = pd.read_excel(input_file)
#new_data = data[['FOLDER','LESION_FOLDER', 'LESION_FILE','BENIGNCLASSIFICATION', 'MASSCLASSIFICATION','WIDTH','SUSPICIOUSCALCIFICATIONS','PLASMACELLMASTITIS','X1','X2','WITHCALCIFICATION','MARKID','SUTURECALCIFICATION','OTHERBENIGNCLUSTER','FOCALASYMMETRY','MILKOFCALCIUM','DYSTROPHIC','LESIONID','CONSPICUITY','FATNECROSIS','HEIGHT','Y1','Y2','VASCULAR','MASS','SKIN','ARCHITECTUREDISTORTION']]
new_data = data[['folder','studyID','seriesID','imageID','laterality','pixel_style','procedure','opinion_screen','opinion_mammog','opinion_ultra']]
scale_factor = 8

sizes = [256,512,2048]

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
    opinion = str(new_data['opinion_mammog'][row])
    if(mammog and opinion != 'nan'):
        FOLDER_PATH = os.path.join(ROOTDIR, str(new_data['folder'].iloc[row]))
        LESION_FOLDER = os.path.join(FOLDER_PATH, str(new_data['studyID'].iloc[row]))
        IMAGE_PATH = os.path.join(LESION_FOLDER, str(new_data['imageID'].iloc[row]) + ".dcm")

        #procedure_folder = os.path.join(SAVEPATH, procedure)

        check_folder = os.path.join(SAVEPATH, str(sizes[0]))
        clabel_folder = os.path.join(check_folder, opinion)
        
        file_output =  os.path.join(clabel_folder, str(new_data['imageID'].iloc[row]) + ".png")
        print("checking file:" + str(file_output))
        found = os.path.isfile(file_output)
        print("Found!" if found else "Not Found!")
        if(not os.path.isfile(file_output)):        
            try:
                image = UTILS.diread(IMAGE_PATH)
                                                
                for size in sizes:                                
                    size_folder = os.path.join(SAVEPATH, str(size))
                    label_folder = os.path.join(size_folder, opinion)
                    image_output =  os.path.join(label_folder, str(new_data['imageID'].iloc[row]) + ".png")
                    
                    Path(image_output).parents[0].mkdir(parents=True, exist_ok=True)

                    scaled_image = resize(image,(size,size),anti_aliasing=True) # comes out as 0-1 float64
                    scaled_image_z = (65535*((scaled_image - scaled_image.min())/scaled_image.ptp())).astype(np.uint16) # rescaled to 16-bit output
            
                    f = open(image_output, 'wb')
                    writer = png.Writer(width=size, height=size, bitdepth=16, greyscale=True)
                    writer.write(f, scaled_image_z)
                    f.close() 

                print("Image " + str(row) + ", original type:" + str(image.dtype) + " reprocessed")            
            except IOError as e:
                print(str(e))
                #print("Missing Image")
    else:
        print("rejected")
    



