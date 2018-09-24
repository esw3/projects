# -*- coding: utf-8 -*-
"""
This module is intended to cut shapes out of the original data to distinguish 
between the fjord and the land/glacier surfaces. 

@author: esw3@aber.ac.uk
"""

import numpy as np
import rasterio
import fiona, json
from shapely.geometry.polygon import LinearRing, Polygon
from shapely.geometry import mapping
from fiona.crs import from_epsg
from pyproj import Proj, transform

def differenceIndex(band1, band2, outfile):
    'Get difference index between two bands'
    b1 = rasterio.open(band1)
    rb1 = b1.read(1) 
    b2 = rasterio.open(band2)
    rb2 = b2.read(1)
    
    dif_idx = np.zeros(b1.shape, dtype=rasterio.float32)

    upper = rb1 - rb2
    lower = rb1 + rb2

    # calculate including division by 0
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide(upper,lower)
        c[c == np.inf] = 0
        dif_idx = np.nan_to_num(c)

    kwargs = b1.meta
    kwargs.update(
        dtype=rasterio.float32,
        count=1,
        compress='lzw')

    with rasterio.open(outfile, 'w', **kwargs) as dst:
        dst.write_band(1, dif_idx.astype(rasterio.float32))
        
    return(dif_idx)
    
def getMaskfromArray(a, lo, hi):
    'generates an array of the same size as the input array with 1 where cell between hi and lo'
    mask = (a<lo)|(a>hi)
    a1 = a.copy()
    a1[mask] = 0
    a1[~mask] = 1    
    return (a1)

def writeRasterFromArray(infile, a, outfile):
    'given the shape of an existing raster, write an array to a new raster'
    b1 = rasterio.open(infile)

    # use rasterio.default_gtiff_profile() instead of infile!
    
    kwargs = b1.meta
    kwargs.update(
        dtype=rasterio.uint8,
        count=1,
        compress='lzw')

    with rasterio.open(outfile, 'w', **kwargs) as dst:
        dst.write_band(1, a.astype(rasterio.uint8))
        

def shpFromBounds(inshp, outshp):
    with fiona.open(inshp, 'r', 'ESRI Shapefile') as c:
        bounds = c.bounds
    
    tps = [(bounds[0], bounds[1]), 
           (bounds[2], bounds[1]),
           (bounds[2], bounds[3]),
           (bounds[0], bounds[3])]
       
    if bounds[0] < 500:
        tps[0] = convLatLon(tps[0])
        tps[1] = convLatLon(tps[1])
        tps[2] = convLatLon(tps[2])
        tps[3] = convLatLon(tps[3])
    else:
        print('No conversion required')

    ring = Polygon(tps)

    schema = {
            'geometry': 'Polygon',
            'properties': {'id': 'int'},
            'init': {'epsg:32633'}
            }
    
    with fiona.open(outshp, 'w', 'ESRI Shapefile', schema, crs=from_epsg(32633)) as d:
        ## If there are multiple geometries, put the "for" loop here
        d.write({
                'geometry': mapping(ring),
                'properties': {'id': 123},
                'init': {'epsg:32633'}
                })
    return(outshp) 
        
def convLatLon(coords):
    'convert from latitude longitude to UTM x,y'
    p = Proj(proj='utm', zone=33, ellps='WGS84')
    x,y = p(coords[0], coords[1])
    return(x,y)
    
