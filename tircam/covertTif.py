#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 10:19:32 2018

@author: cake
"""

from __future__ import print_function
import os, sys
from PIL import Image
import glob
from sklearn import cluster
#
#
#for infile in sys.argv[1:]:
#    f, e = os.path.splitext(infile)
#    outfile = f + ".tif"
#    if infile != outfile:
#        try:
#            Image.open(infile).save(outfile)
#        except IOError:
#            print("cannot convert", infile)
#            
#k_means = cluster.KMeans(n_clusters=5, 
#                 init='k-means++', 
#                 n_init=10, 
#                 max_iter=300, 
#                 tol=0.0001, 
#                 precompute_distances='auto', 
#                 verbose=0, 
#                 random_state=None, 
#                 copy_x=True, n_jobs=1, algorithm='auto')
##def csvToTif(infile):

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import tifffile as tiff
from skimage import io
#io.use_plugin('freeimage')

#outpath = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/latest2/'
outpath = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/16092018-01/'
path = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/backup_real/*.csv'

for fn in sorted(glob.iglob(path, recursive=True)):

    #fn = '../../camera/real/Record_2018-08-16_16-49-46.csv'
    #out = './out.tif'
    lst = fn.split('/')
    file = lst[-1].split('.')[0]
    out = ''.join([outpath, file, '.tiff'])
    bla = ''.join([outpath, file, 'que.tiff'])
    pngout = ''.join([outpath, file, '.png'])
    
    data2 = pd.read_csv(fn, header=0, sep=';')
    data2.drop(data2.columns[len(data2.columns)-1], axis=1, inplace=True)  # last column is NaN > remove
    
    io.imsave(out, data2.values)    
    print(out)
#    break
    