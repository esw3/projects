#!/home/cake/python3/venv/spyder/bin/python3 


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raster search, download, and clip operations.

@author: cake
"""
import os,re

import rasterio
import rasterio.mask as mask
import rasterio.fill as fill

from shapely.geometry import LinearRing, Polygon, Point, mapping
import fiona
from fiona.crs import from_epsg

import numpy as np
import pandas as pd
from subprocess import call

def rasterDownload(path, row, bands, destdir):
    'Download the bands from s3scene'
    


def polygonFromCoords(c):
    ''' Create polygon from coordinates'''
    r = LinearRing(c)
    polygon = Polygon(r)
    return polygon

def shapefileFromPolygon(polygon, name):
    ''' Create shapefile from polygon'''
    schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
        'init': {'epsg':'int'}
    }

    # Write a new Shapefile 'your_shapefile.shp', 'w',crs=from_epsg(3857) crs=from_epsg(32633), 
    with fiona.open(name, 'w', 'ESRI Shapefile', schema) as c:
        c.write({
            'geometry': mapping(polygon),
            'properties': {'id': 123},
            'init': {'epsg': 32633}
        })
    
    print ('Polygon written to ', name)
    return c

def openRasterAsArray(raster):
    'Open a aster as a numpy array'
    with rasterio.open(raster) as src:
        out_meta = src.meta.copy()  
        arr = np.array(src.read(1))
        #print(arr.shape)
    return(arr)

#def rasterClip(shapefile, raster, destdir):
def rasterClip(shapefile, raster, outfile):
    'take the raster, cut it to shapefile size'
    with fiona.open(shapefile, "r", crs=from_epsg(32633)) as shapefile:
        features = [feature["geometry"] for feature in shapefile]
        print('Opened shapefile', shapefile)
        
    with rasterio.open(raster) as src:
        print('Opening raster', src)
        
        out_image, out_transform = mask.mask(src, features, crop=True)
        out_meta = src.meta.copy()

        out_meta.update({"driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "nodata": 255})
    
    #print('raster', raster)
    #name_parts = raster.split('.')
    #print(name_parts)
    #name_parts = name_parts[0].split('/')
    
    #outfile = ''.join([destdir, '/NOOfile.tif'])
    #outfile = ''.join([destdir, name_parts[3], '_masked.tif'])
    
    with rasterio.open( outfile , "w", **out_meta) as dest:
        print('Image output: ', outfile)                        
        mk = dest.write(out_image)
        
    return(outfile)
      
def dirForData(top, data):
    directory = ''.join([top, data])
    print(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return(directory)

def rasterClipCmdln(raster, shapefile, outfile):
    # rio clip 
    # ../landsat/2015_data/LC82200032015097LGN01/LC08_L1TP_220003_20150407_20170410_01_T1_B9.TIF 
    # output.tif --bounds $(fio info my_shp2.shp --bounds)
    if not os.path.exists(outfile):
        cmd = ''.join(['/home/cake/python3/venv/spyder/bin/rio clip ', raster, ' ', outfile, ' --bounds ', '$(fio info ', shapefile, ' --bounds)'])
        call(cmd)
    else:
        print (outfile, ' exists')
    
    #call(cmd)
    #return(ret)
    
    
def readDatefromMtl(mtlfile):
    with open(mtlfile) as f:    
        lines = f.readlines()
        for l in lines:
            if re.search('DATE_ACQUIRED', l):
                d = l.split('=')[1]
                return(d.strip())

def metadata(raster, metafile):
    'Open metadata file and associated geotiff raster, output K1, K2, and RADIANCE_*'
    band = raster.split('_') 
    
    pattern = '^B' # band in string as B10, B11.
    bno = ''
    for b in band:
        if re.search(pattern, b):
            bno = b[1:]

    f = open(metafile)
    values = ['K1', 'K2']
    consts = {}
    
    for line in f:
        for val in values:
            pattern = ''.join([val,'_CONSTANT_BAND_', bno])
            if re.search(pattern, line):
                const = line.split('=')[1]
                const= const.strip()
                const=float(const)
                consts[val] = const
    
        add_str = ''.join(['RADIANCE_MULT_BAND_', bno])
        if re.search(add_str, line):
            const =  line.split('=')[1]
            const = const.strip()
            consts['mult'] = float(const)
            
        add_str = ''.join(['RADIANCE_ADD_BAND_', bno])
        if re.search(add_str, line):
            const =  line.split('=')[1]
            const = const.strip() 
            consts['add'] = float(const)
    
    f.close()
    return(consts)   

def openRasterAsArray(raster):
    'Open a aster as a numpy array'
    with rasterio.open(raster) as src:
        out_meta = src.meta.copy()  
        arr = np.array(src.read(1))
        #print(arr.shape)
    return(arr)
    
def DNToToa(inraster, metafn, outfile):
    '''Use the formula & constants from the landsat 8 manual'''
    metavalues = metadata(inraster, metafn)

    with rasterio.open(inraster) as src:
        bounds = src.bounds
        kwargs = src.meta
    
    kwargs['transform'] = rasterio.transform.guard_transform(kwargs['transform'])
    kwargs['dtype'] = 'float64'
    kwargs['nodata'] = 255
          
    dn = openRasterAsArray(inraster)
    L = (metavalues['mult'] * dn) + metavalues['add']

#    outfile = inraster.split('.')[1]
#    outfile = ''.join([outfile, '_TOA.tif'])
#    outfile = outfile.replace('/','')

    with rasterio.open(outfile, 'w', **kwargs) as dst:
        dst.write_band(1, L.astype(rasterio.float64))
    
    #self.toa = outfile
    return outfile
        

def getTemp(raster, metafn, outfile):
    '''Use the formula & constants from the landsat 8 manual'''
    metavalues = metadata(raster, metafn)

    # open raster
    with rasterio.open(raster) as src:
        out_meta = src.meta.copy()      
        arr = np.array(src.read(1))
        kwargs = src.meta
        
    kwargs['transform'] = rasterio.transform.guard_transform(kwargs['transform'])
    kwargs['dtype'] = 'int16'
    kwargs['nodata'] = 255

    # calculate
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide(metavalues['K1'],arr)
        c[c == np.inf] = 0
        c = np.nan_to_num(c)
        
    denominator = np.log(c + 1)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        temp = np.true_divide(metavalues['K2'], denominator)
        temp[temp == np.inf] = 0
        temp = np.nan_to_num(temp)
        
    temp = np.subtract(temp, 272.15) # from kelvin to celsius
    test = pd.DataFrame(data=temp)
    test.to_csv('test.csv')
    #temp = np.round(temp,3)

    temp = temp.astype(np.int16)
    
    # Repeated operation should make this a single function
#    outfile = raster.split('.')[0]
#    outfile = ''.join([outfile, '_celsius.tif'])
#    outfile = outfile.replace('/','')

    with rasterio.open(outfile, 'w', **kwargs) as dst:
        dst.write_band(1, temp.astype(rasterio.int16))

    print('Raster output: ', outfile)
    
    #self.temp = outfile
    return (temp, outfile)

def readBand(band):
    'Open the file and read the first band as an array. Return shape, metadata and band data array'
    b = rasterio.open(band)
    rb = b.read(1)
    return (b.shape, b.meta, rb)

def saveArrayToRaster(array, outfile, kwargs):
    with rasterio.open(outfile, 'w', **kwargs) as dst:
        kwargs['nodata'] = 255
        dst.write_band(1, array.astype(rasterio.uint16))      
    return(outfile)
       
def getArgsFromRaster(raster):
    with rasterio.open(raster) as src:
        #out_meta = src.meta.copy()      
        #arr = np.array(src.read(1))
        kwargs = src.meta
    return(kwargs)
    
    
    