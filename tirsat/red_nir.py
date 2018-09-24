#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:31:23 2018
Initialize2
@author: cake
"""
import rasterops

date = '2015-03-29'

# Red band, NIR band
#RED = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/output/ls8/2015-03-29/clips/RedClip_2015-03-29.tif'
#NIR = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/output/ls8/2015-03-29/clips/NIRClip_2015-03-29.tif'
#outfile = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/output/ls8/2015-03-29/clips/RedNIR_2015-03-29.tif'


# Add and create new band
x = rasterops.readBand(RED)[2] + rasterops.readBand(NIR)[2]

# Save red+NIR as tif
kwargs = rasterops.getArgsFromRaster(RED)
out = rasterops.saveArrayToRaster(x, outfile, kwargs)

# Cut fjord out of raster
clipdir = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/output/ls8/2015-03-29/clips/'
fjordshp = r'/home/cake/2018/tir/projects/shapefiles/waterfjord.shp'
outfile = ''.join([clipdir, '/RedNIRWater_', date,'.tif'])
waterclip = rasterops.rasterClip(fjordshp, out, outfile)

# See whether I can replicate Schild's area by numpy