#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 11:25:10 2018


Modify times from appropriate start time, since the computer datetime was wrong. 


@author: cake
"""

#%% Copy files to new date-time from start date.

import os

start_Y = 2018
start_M = 8
start_D= 17
start_H = 23
start_m = 30
start_S= 0

min_interval = 5 #minutes
other_interval = 1 # hours, days, etc
max_time = 59 # seconds, minutes, etc

# format: Record_ 2018-08-16 _15-59-46.csv
fns = r'../../camera/working_2018-03-09/Record_*.csv'
i=0

for filename in sorted(glob.iglob(fns, recursive=True)):
    lst = filename.split('/')
    part1, part2, part3 = lst[-1].split('_')
    if i == 0:
 #       start_date = ''.join([str(start_Y), '-', start_M, '-', start_D])
 #       start_time = ''.join([start_H, '-', start_H, '-', start_S ])
        #last = ''.join([part1, '_', start_date, '_', start_time, '.csv'])
        m = start_m
        h = start_H
        d = start_D       
        #print (last)
    else:
        if m < 55:    
            m = m + 5
                
        elif h < 23:
            m = 0
            h = h + 1
            
        else:
            m = 0
            h = 0
            d = d + 1
            
    m1 = m
    h1 = h
    if m1 < 10:
        m1 = ''.join([str(0),str(m)])
    if h1 < 10:
        h1 = ''.join([str(0),str(h)])
    
    start_date = ''.join([str(start_Y), '-', str(start_M), '-', str(d)])
    start_time = ''.join([str(h1), '-', str(m1) ])             
    newfn =  (''.join(['../../camera/backup_real/', 'Record_', start_date, '_', start_time, '.csv']))
    os.rename(filename, newfn)
    print(filename, newfn)
    i = i + 1
    
print ('### END ###')
    