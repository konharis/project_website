#!/usr/bin/env python2.7

import pydicom
import re, sys, fnmatch, os
import shutil, cv2
import numpy as np
from drawcontours import read_draw_contrs

DPATH = r'/media/kostas/INTENSO/LV_segmentation_data_from_Tufvesson_et_al/LundTest100'
DPATH = r'/media/kostas/INTENSO/cardiac-segmentation-ubuntu/Lund_Tufvesson_val_submission_b'
DPATH = r'/media/kostas/INTENSO/cardiac-segmentation-ubuntu/Sunnybrook_val_submission'
DPATH = r'/media/kostas/INTENSO/cardiac-segmentation-ubuntu/Sunnybrook_online_submission'


def save_auto_manual_images(contour_path, contour_type,datasrc='LUND'):  
	''' Draws computed (auto) and manual contours on the original image and save the
	    resulted images. Currently supports LUND and SUNNYBROOK datasets.
	'''       
    imglist = [(dirpath, f)
        for dirpath, dirnames, files in os.walk(contour_path)
        for f in fnmatch.filter(files, '*.dcm')]
        #for f in fnmatch.filter(files, 'pat*.dcm')]

    if datasrc=='LUND':
        ctype='_inner' if contour_type=='i' else '_outer'  # for Lund data
    if datasrc=='SUNNYBROOK':
        ctype='-icontour' if contour_type=='i' else '-ocontour'  # for sunnybrook data
    for dname,fname in imglist:
        dn = dname[0:dname.rfind('/')]
        fn = fname[:fname.rfind('.')]
        print(dn,fn)
        imgname  = os.path.join(dname,fname)
        if datasrc=='LUND':
            mcntname = os.path.join(dn,'contours-manual',fn+ctype+'.txt')
            acntname = os.path.join(dn,'contours-auto',  fn+ctype+'.txt')
        if datasrc=='SUNNYBROOK':
            mcntname = os.path.join(dn,'contours-manual','IRCCI-expert',fn+ctype+'-manual.txt')
            acntname = os.path.join(dn,'contours-auto','FCN',  fn+ctype+'-auto.txt')
        
        cimg = read_draw_contrs(imgname,mcntname,acntname)
        if cimg != None:
            cv2.imwrite(os.path.join(dname,fn+ctype+'.png'), cimg)
        

if __name__== '__main__':
    la = len(sys.argv)
    if la != 4:
        print('Usage: python %s contour_type save_path crop_size ' % sys.argv[0])
        #sys.exit()
        crop_size =100
        datasrc = 'SUNNYBROOK'
        save_path = DPATH
        contour_type = 'i'
    else:     
        assert len(sys.argv)==4, "Required command-line args: contour_type save_path crop_size"
        contour_type = sys.argv[1]  
        assert contour_type=='i' or contour_type=='o', "Invalid contour type"
        save_path = sys.argv[2]        
        crop_size = int(sys.argv[3])

    if save_path.lower().find('lund')>-1:
        datasrc,crop_size = 'LUND',100
    if save_path.lower().find('sunnybrook')>-1:
        datasrc,crop_size = 'SUNNYBROOK',100

    print('contour type='+contour_type+'   crop size = '+str(crop_size))
    print('Results saving path='+save_path)
    save_auto_manual_images(save_path, contour_type,datasrc)
    
