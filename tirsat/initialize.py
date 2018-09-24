#!/home/cake/python3/venv/spyder/bin/python3 


'''#!/usr/bin/env python3'''
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:43:28 2018

Run initializer

@author: cake
"""

import rasterops, shapeops
import glob


# INPUTS
#n = 0

# --> subs = landsat dir, output dir, s3hapefile square, shapefile water outline

#subs = ('hornsund', 'hornsund', 'hornsund_square', 'hornsund_fjord2')
#subs = ('tunabreen', 'tunabreen','tuna_square', 'tuna_fjord')
#subs = ('hornsund', 'akseloya', 'akseloya_square', 'akseloya_fjord')
#subs = ('allunder10', 'ls8', 'clipshape', 'waterfjord')
#subs = ('allunder10', 'comfortless', 'comfortless_square', 'comfortless_fjord')
#subs = ('allunder10', 'kongsfjorden', 'kongs_square', 'kongsfjorden_fjord')
#subs = ('hornsund', 'hansbreen', 'hansbreen_square', 'hansbreen_fjord')
#subs = ('hornsund', 'samarinbreen', 'samarin_square', 'samarin_fjord')
#subs = ('tunabreen', 'nordenskioldbreen','nordenskiold_square', 'nordenskiold_fjord')
#subs=('18-08-2018', 'camday', 'clipshape', 'waterfjord_outline')
#subs = ('18-08-2018', 'kongsfjorden', 'kongs_square', 'kongsfjorden_fjord')
#subs = ('allunder10', 'kongs_whole', 'kongsfjorden_whole', 'kongsfjorden_fjord')
subs = ('hornsund', 'hornsund_whole', 'hornsund_whole', 'hornsund_whole')

#srcs = ['hornsund', '2015_data', 'schild', 'tunabreen', 'allunder10', 'allunder10','akseloya']
#dsts = ['hornsund', '2015_data', '', 'tunabreen', 'ls8', 'kongsfjorden,','akseloya']

# SOURCE  
srcdir = r'/home/cake/2018/tir/landsat/'
fnmatch = ''.join([srcdir, subs[0], '/*/*B10*TIF']) 
print (fnmatch)

#fnmatch = r'/home/cake/2018/tir/landsat/2015_data/*/*B10*TIF'
#fnmatch = r'/home/cake/2018/tir/landsat/schild/*/*B10*TIF'
#fnmatch = r'/home/cake/2018/tir/landsat/allunder10/*/*B10*TIF'
#fnmatch = r'/home/cake/2018/tir/landsat/tunabreen/*/*B10*TIF'
#fnmatch = r'/home/cake/2018/tir/landsat/hornsund/*/*B10*TIF'

for filename in glob.iglob(fnmatch, recursive=True):
    B10 = filename
    mtlfile = filename.replace('B10.TIF', 'MTL.txt')
    B1 = filename.replace('B10', 'B1')
    NIR = filename.replace('B10', 'B5')
    RED = filename.replace('B10', 'B4')
    CLOUD = filename.replace('B10', 'B9')
      
    print(filename)
    # 1. make subdir for dir
    #tl = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/output/ls8/'
    #tl = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/output/tunabreen/'
    #tl = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/output/akseloya/'
 
    
    # DEST 
    dstdir = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/output/'
    tl  = ''.join([dstdir, subs[1],'/'])  
    #print (tl)
    
    # SHAPES
    shfdir = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/projects/shapefiles/'
    areashp = ''.join([shfdir, subs[2], '.shp'])      # square
    fjordshp = ''.join([shfdir, subs[3], '.shp'])     # fjord
    
    #print (areashp)

    #--1.1 run for each directory, find all mtl files
    date = rasterops.readDatefromMtl(mtlfile)
    
    #-- create the directory
    dirmake = rasterops.dirForData(tl, date)
    
    #-- subdirectories for shapefiles, clipped rasters, etc
    shapedir = rasterops.dirForData(dirmake, '/shapes')
    clipdir = rasterops.dirForData(dirmake, '/clips')
    
    #-- Clip the plain band 10 to polygon
    #areashp = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/python/shapefiles/fjord/clipshape.shp'
    #areashp = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/projects/shapefiles/tuna_square.shp'
    #areashp = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/projects/shapefiles/akseloya_square.shp'
        # 1. B10 clip
    outfile = ''.join([clipdir, '/OrigClip_', date,'.tif'])
    clip = rasterops.rasterClip(areashp, B10, outfile)
        # 1. B1 clip
    outfile = ''.join([clipdir, '/B1Clip_', date,'.tif'])
    B1fn = rasterops.rasterClip(areashp, B1, outfile)    
        # 1. B4 clip
    outfile = ''.join([clipdir, '/RedClip_', date,'.tif'])
    B4fn = rasterops.rasterClip(areashp, RED, outfile)    
        # 1. B5 clip
    outfile = ''.join([clipdir, '/NIRClip_', date,'.tif'])
    B5fn = rasterops.rasterClip(areashp, NIR, outfile)    
    
    #-- Convert the clipped band to TOA, then to Temperature
    outfile = ''.join([clipdir, '/ClipTOA_', date,'.tif'])
    toa = rasterops.DNToToa(clip, mtlfile, outfile)
    
    outfile = ''.join([clipdir, '/ClipTemp_', date,'.tif'])
    arr, temp = rasterops.getTemp(toa, mtlfile, outfile)
    
    #-- Mask the fjord based on shapefile, set everything else to -255 [??]
    #fjordshp = r'/home/cake/2018/tir/projects/shapefiles/waterfjord.shp'
    #fjordshp = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/projects/shapefiles/tuna_fjord.shp'
    
    #fjordshp = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/projects/shapefiles/akseloya_fjord.shp'
    outfile = ''.join([clipdir, '/WaterClip_', date,'.tif'])  
    waterclip = rasterops.rasterClip (fjordshp, temp, outfile)
    
    #-- Create the Red+NIR Plume band
    x = rasterops.readBand(RED)[2] + rasterops.readBand(NIR)[2]
    kwargs = rasterops.getArgsFromRaster(RED)
    outfile = ''.join([clipdir, '/BigRedNIR_', date,'.tif']) 
    RedNIR = rasterops.saveArrayToRaster(x, outfile, kwargs)
    
    # Cut the area out of the Red+NIR Plume band
    # Cut fjord out of Red+NIR Plume band
    outfile = ''.join([clipdir, '/RedNIRClip_', date,'.tif'])
    RedNIRclip = rasterops.rasterClip(areashp, RedNIR, outfile)    

    # Cut fjord out of Red+NIR Plume band
    outfile = ''.join([clipdir, '/RedNIRWater_', date,'.tif'])
    RedNIRclip = rasterops.rasterClip(fjordshp, RedNIR, outfile)

    #-- Need the cirrus band to make sure that it's a plume
    outfile = ''.join([clipdir, '/CirrusClip_', date,'.tif'])
    RedNIRclip = rasterops.rasterClip(areashp, CLOUD, outfile)       
