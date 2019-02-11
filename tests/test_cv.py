
import os, fnmatch, sys
import numpy as np
import matplotlib.pyplot as plt 
import pydicom
import cv2

def pltshowim(img):
    plt.imshow(img,cmap='gray')
    plt.xticks([]), plt.yticks([])
    plt.show() 


ipath = 'images'
imnames = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(ipath)
                for f in fnmatch.filter(files,'pat*'+'.dcm')]

for im in imnames:
    f = pydicom.read_file(im)  # load image
    img = f.pixel_array.astype('uint8') # convert to numpy array
    mask = np.zeros_like(img, dtype='uint8') # allocate and initialize mask image
    coords = np.loadtxt(im[0:-4]+'_inner.txt', delimiter=' ').astype('int')

    cv2.fillPoly(mask, [coords], 1)
    pltshowim(mask)
    cv2.imwrite(im[0:-4]+'_imask1.png', mask)
    cv2.imshow("CV test", img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    tmp = np.where(mask > 0.5, 255, 0).astype('uint8')

    coords2 = cv2.findContours(tmp.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    mask2 = np.zeros_like(img, dtype='uint8')
    cv2.drawContours(img, [coords2],-1,(0,0,255),1)
    cv2.fillPoly(mask2, [coords2], 1)
    pltshowim(mask2)
    cv2.imwrite(im[0:-4]+'_imask2.png', mask2)
