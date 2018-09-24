#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 18:56:30 2018

@author: cake
"""

import rasterio

file_list = ['/home/cake/2018/tir/landsat/hornsund/LC82100052018083LGN00/LC08_L1TP_210005_20180324_20180403_01_T2_B4.TIF',
             '/home/cake/2018/tir/landsat/hornsund/LC82100052018083LGN00/LC08_L1TP_210005_20180324_20180403_01_T2_B3.TIF', 
             '/home/cake/2018/tir/landsat/hornsund/LC82100052018083LGN00/LC08_L1TP_210005_20180324_20180403_01_T2_B2.TIF']

# Read metadata of first file
with rasterio.open(file_list[0]) as src0:
    meta = src0.meta

# Update meta to reflect the number of layers
meta.update(count = len(file_list))

# Read each layer and write it to stack
with rasterio.open('stack.tif', 'w', **meta) as dst:
    for id, layer in enumerate(file_list):
        with rasterio.open(layer) as src1:
            dst.write_band(id + 1, src1.read(1))