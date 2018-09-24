#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 13:48:24 2018

@author: cake
"""

import openpiv.tools
import openpiv.process
import openpiv.scaling
import openpiv.validation
import openpiv.filters

import numpy as np
#from PIL import Image
from skimage import io, exposure, img_as_uint, img_as_float


# Run this for each 
source_dir = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/16092018-01/'
result_dir = '/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/piv/'


fn1 = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/16092018-01/Record_2018-8-18_04-20.tiff'
fn2 = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/16092018-01/Record_2018-8-18_04-30.tiff'

# need a mask to lock out islands,glaciers,sky,etc. 
# Create mask from manually created masking file (gimp)
msk = r'mask3.png'
ma = io.imread(msk)
ma2 = (ma<255)
ma3 = np.invert(ma2)

im1 = io.imread(fn1)
im1 = exposure.rescale_intensity(im1, out_range='float')
test1 = img_as_uint(im1)
test1[ma3] = 0
test1=test1.astype(np.int32)

im2= io.imread(fn2)
im2 = exposure.rescale_intensity(im2, out_range='float')
test2 = img_as_uint(im2)
test2[ma3] = 0
test2=test2.astype(np.int32)

# read file 1
frame_a  = openpiv.tools.imread( fn1 )
frame_a = frame_a.astype(np.int32)
frame_a[ma3] = 0

# read file 2 
frame_b  = openpiv.tools.imread( fn2 )
frame_b = frame_b.astype(np.int32)
frame_b[ma3] = 0

wsize = 28
overl = 12

# copied this directly from the tutorial:
u, v, sig2noise = openpiv.process.extended_search_area_piv(test1, 
                                                           test2, 
                                                           window_size=wsize, 
                                                           overlap=overl, 
                                                           dt=0.05, 
                                                           search_area_size=128, 
                                                           sig2noise_method='peak2mean' )
#u, v, sig2noise = openpiv.process.extended_search_area_piv( frame_a, 
#                                                           frame_b, 
#                                                           window_size=24, 
#                                                           overlap=6, 
#                                                           dt=0.05, 
#                                                           search_area_size=64, 
#                                                           sig2noise_method='peak2mean' )

x, y = openpiv.process.get_coordinates( image_size=frame_a.shape, window_size=wsize, overlap=overl )

u, v, mask = openpiv.validation.sig2noise_val( u, v, sig2noise, threshold = 1.5 )

u, v = openpiv.filters.replace_outliers( u, v, method='localmean', max_iter=20, kernel_size=3)

x, y, u, v = openpiv.scaling.uniform(x, y, u, v, scaling_factor = 96.52 )

openpiv.tools.save(x, y, u, v, mask, 'exp1_001.txt' )

#plt.imshow(mask)
plt.quiver(x, y, u, v)
#plt.imshow(u)
