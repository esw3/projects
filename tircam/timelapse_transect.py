#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 22:28:12 2018

Identifying pixels in a transect


@author: cake
"""

from matplotlib import pyplot as plt
from matplotlib import patches as patches
import glob 
import pandas as pd
import numpy as np
# single data csv open

# list of (x,y) coordinates
# THIS CREATES IMAGE OF CSV FILE WITH RECTANGLE FOR FJORD AND FOR GLACIER AVERAGING SQUARE


x = [340, 325, 300, 275, 250, 225, 200, 175, 135,  95,  55,   5]
y = [175, 200, 210, 220, 230, 240, 245, 250, 250, 250, 250, 250]

# 1 make sure create image of points to be looked at
#plt.imshow (data)
#currentAxis = plt.gca()
#
#for a,b in lst:
#    currentAxis.annotate('X', xy=(a,b) )
#    
# Get the values from each csv for each x,y coordinate
path = r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/backup_real/*.csv'

test = []
for fn in sorted(glob.iglob(path, recursive=True)):
    data = pd.read_csv(fn, sep=';')
    lst = zip(x,y)
    
    lst2 = []
    for a,b in lst:
        #print(data.iloc[b][a])
        c = data.iloc[b][a]
        lst2.append(c)
        
    test.append(lst2)

# 1 make sure create image of points to be looked at
plt.imshow (data)
currentAxis = plt.gca()
lst = zip(x,y)
for a,b in lst:
    print(a,b)
    currentAxis.annotate('X', xy=(a,b) )

#%% Plot in a row
q = np.transpose(test)
n = 0
plot = 100
plt.figure(dpi=300, figsize=[20,13])

for l in q:
    #if n > 3:
    plt.subplot(len(q),1,n+1)
    #p.add_subplot(1,1,n)
    plt.plot(q[n][40:])
    plt.ylim([-1,7])
    plt.grid()    
    n = n + 1
plt.tight_layout()

    
