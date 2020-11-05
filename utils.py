import numpy as np
import pydicom as dicom
import random
import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import gaussian_filter
import os

def diread(path):
    Beginning_image = dicom.dcmread(path)
    beginning_image = Beginning_image.pixel_array
    
    return beginning_image

def create_mask(image, x1, x2, y1, y2):
    mask = np.zeros((image.shape))
    for kk in range(y1, y2):
        for ii in range(x1, x2):
            mask[kk,ii] = 255
    return mask 

def segmented_image(image, x1, x2, y1, y2):
    diffzml, diffxml = y2 - y1, x2 - x1
    array = np.zeros((diffzml, diffxml))
    for j in range(y1, y2):
        for k in range(x1, x2):
            array[j-y1,k-x1] = image[j,k]
    return array



def output_location(SAVEPATH, status, name, classification, val):
    # for "val" type = 0, shape = 1 
    image_name = str(name)
    if val == 0:
        if status == "B2":
            image_output =  os.path.join(SAVEPATH, "B2", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "B2", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "B2", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "B2", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "B2", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "B2", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output
        elif status == "B3":
            image_output =  os.path.join(SAVEPATH, "B3", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "B3", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "B3", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "B3", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "B3", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "B3", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output
        
        elif status == "B4":
            image_output =  os.path.join(SAVEPATH, "B4", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "B4", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "B4", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "B4", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "B4", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "B4", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output
        
        elif status == "B5":
            image_output =  os.path.join(SAVEPATH, "B5", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "B5", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "B5", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "B5", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "B5", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "B5", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output
        
        elif status == "Benign":
            image_output =  os.path.join(SAVEPATH, "Benign", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "Benign", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "Benign", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "Benign", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "Benign", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "Benign", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output
        
        elif status == "Malignant":
            image_output =  os.path.join(SAVEPATH, "Malignant", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "Malignant", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "Malignant", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "Malignant", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "Malignant", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "Malignant", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output
    elif val == 1:
        if classification == "spiculated":
            image_output =  os.path.join(SAVEPATH, "spiculated", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "spiculated", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "spiculated", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "spiculated", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "spiculated", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "spiculated", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output
        
        elif classification == "ill_defined":
            image_output =  os.path.join(SAVEPATH, "ill_defined", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "ill_defined", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "ill_defined", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "ill_defined", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "ill_defined", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "ill_defined", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output
        
        elif classification == "well_defined":
            image_output =  os.path.join(SAVEPATH, "well_defined", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "well_defined", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "well_defined", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "well_defined", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "well_defined", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "well_defined", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output
        
        elif classification == "other":
            image_output =  os.path.join(SAVEPATH, "other", "image", image_name + ".png")
            mask_output = os.path.join(SAVEPATH, "other", "mask", image_name + ".png")
            seg_output = os.path.join(SAVEPATH, "other", "seg", image_name + ".png")
            maskseg_output = os.path.join(SAVEPATH, "other", "maskseg", image_name + ".png")
            array_output = os.path.join(SAVEPATH, "other", "segnp", image_name)
            bound_output = os.path.join(SAVEPATH, "other", "bound_seg", image_name + ".png")
            return image_output, mask_output, seg_output, maskseg_output, array_output, bound_output

def IMAGE_THREASHOLD_OTSU(image):
    output = r"..\image.png"
    blur_image = gaussian_filter(image, sigma=5)
    plt.imsave(output, blur_image)
    img = cv2.imread(output, 0)
    ret,thr = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    threas_img = np.zeros((thr.shape))
    for kk in range(0, thr.shape[0]):
        for ii in range(0, thr.shape[1]):
            if thr[kk,ii] > 1:
                threas_img[kk,ii] = image[kk,ii]
    threashold_image = grow_region(image, threas_img)
    return threashold_image
        
def grow_region(image, threashold_image):
    Centre_start = centre_start(threashold_image)
    container = np.zeros((image.shape))
    listx = []
    listz = []
    listx.append(Centre_start[1])
    listz.append(Centre_start[0])
    while len(listx) > 0:
        x = listx[0]
        z = listz[0]
        Patch = patch(image, x,z)
        for rr in range(0, len(Patch[0])):
            if 2 <= Patch[0][rr] <= image.shape[0]-2 and 2 <= Patch[1][rr] <= image.shape[1] - 2:
                if threashold_image[Patch[0][rr], Patch[1][rr]] > 0 and container[Patch[0][rr], Patch[1][rr]] == 0:
                    container[Patch[0][rr], Patch[1][rr]] = 1
                    listx.append(Patch[1][rr])
                    listz.append(Patch[0][rr])
        listx.pop(0)
        listz.pop(0)
    for kk in range(0, image.shape[0]):
        for ii in range(0, image.shape[1]):
            if container[kk,ii] == 0:
                threashold_image[kk,ii] = 0
                
    return threashold_image

def patch(image, x,z):
    xlist = []
    zlist = []
    for kk in range(-1,2):
        for ii in range(-1,2):
            z_new = z + kk
            x_new = x + ii
            if image[z_new,x_new] > 0:
                zlist.append(z_new)
                xlist.append(x_new)
                
    return zlist, xlist

def centre_start(threashold_image):
    X_list = []
    Y_list = []
    for kk in range(0, threashold_image.shape[0]):
        for ii in range(0, threashold_image.shape[1]):
            if threashold_image[kk,ii] >= 1:
                X_list.append(ii)
                Y_list.append(kk)
    Xc = int(round(np.mean(X_list),0))
    Yc = int(round(np.mean(Y_list),))
    return Yc, Xc

def create_segmask(image, x1,x2,y1, y2, seg):
    base = np.zeros(image.shape)
    for kk in range(y1, y2):
        for ii in range(x1, x2):
            if seg[kk - y1, ii - x1] > 0:
                base[kk,ii] = 255
    return base 
            
