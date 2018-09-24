#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 20:52:15 2018

Temp from waterclip

@author: cake
"""


import glob

import geopandas as gpd 

import rasterops


tldir = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/output/'
fnmatch = ''.join([tldir, 'l8/*/clips/WaterClip_*.tif']) 

for fn in glob.iglob(fnmatch, recursive=True):
    band = rasterops.readBand(fn)
    
    
#%%   
# read shapefile into geopandas    
gdf = gpd.read_file(fn)
    


#%%
from osgeo import ogr

#vlayer = iface.activeLayer()

#provider = vlayer.dataProvider()

#path = provider.dataSourceUri()

#tmp = path.split("|")

#path_to_shp_data = tmp[0]
shp = r'../shapefiles/waterfjord.shp'

driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(shp, 1)
layer = dataSource.GetLayer()

new_field = ogr.FieldDefn("Area", ogr.OFTReal)
new_field.SetWidth(32)
new_field.SetPrecision(2) #added line to set precision
#layer.CreateField(new_field)


feature = layer.GetFeature(0)
geom = feature.GetGeometryRef()
area = geom.GetArea() 
print (area/1000000)
feature.SetField("Area", area)
layer.SetFeature(feature)



#dataSource = None 


    