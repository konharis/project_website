#!/usr/bin/env python2.7

import pydicom
import re, sys, os
import shutil, cv2
import numpy as np
from pathlib import Path


DPATH = r'/media/kostas/INTENSO/LV_segmentation_data_from_Tufvesson_et_al/Lund100'

def draw_contrs(img,icoords,ocoords):
    """
    Draws the contours icoords and ocoords on image img.
    The resulting color image cimg is returned.
    """
    cimg = np.zeros((img.shape[0],img.shape[1],3), np.int32)
    cimg[:,:,0],cimg[:,:,1],cimg[:,:,2] = img,img,img
    #cv2.imwrite('images/masktest.png', mask)
    if icoords.size>0:    
        cv2.drawContours(cimg, [icoords],-1,(0,0,255),1)  # RED
    if ocoords.size>0:
        cv2.drawContours(cimg, [ocoords],-1,(0,255,0),1) #GREEN
    return cimg


def read_draw_contrs(imgname,icntname,ocntname):
    """
    Reads the DICOM image imgname, the contour text files icntname,ocntname
    and draws the contours on the image.
    """
    if Path(icntname).exists() == False or Path(ocntname).exists()==False:
        return None
    f    = pydicom.read_file(imgname)
    img = f.pixel_array.astype('int')
    icoords = np.loadtxt(icntname, delimiter=' ')
    icoords = np.round(icoords).astype('int')
    ocoords = np.loadtxt(ocntname, delimiter=' ')
    ocoords = np.round(ocoords).astype('int')   
    return draw_contrs(img,icoords,ocoords)
