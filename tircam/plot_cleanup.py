#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 21:38:18 2018

@author: cake
"""


import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

fn = r'point_samples.csv'
df = pd.read_csv(fn)

dfsum = df.rolling(7,center=True).mean()
dfstd= df.rolling(7,center=True).std()

fig,ax = plt.subplots(figsize=[6,8])
ax.plot(df)
ax.plot(dfsum)
#ax.error(dfsum, dfstd)


#fig = plt.figure() 
#ax = plt.axes()
#ax.set_xlabel('test')
#ax.set_ylabel('Temperature ($\circ$C)')
#
#dfsum.plot(subplots=True, legend=True, figsize=[12,12],
#           yerr=dfstd,
#           title='Running mean (25 minute averages) of plume development sample point temperatures',
#           ylim=[1.5,5.5])
#
#ax.set_xlabel('test')
#ax.set_ylabel('Temperature ($\circ$C)')




#plt.figure(figsize=[8,6]) 
#ax = plt.axes()

#ax2=ax1.twinx()

#plt.plot(means.rolling(5,center=True).mean()['T_ave'])
#plt.xlabel='test'
#timeFmt = mdates.DateFormatter('%H:%M')
#
#ax1.plot(df['datetime'][673120:673420],
#         df['svluwobs:svluw2:ctd_181:temperature [°C]'][673120:673420].rolling(25,center=True).mean(),
#         color='g', label='Temperature')
#
#ax2.plot(df['datetime'][673120:673420],
#         df['svluwobs:svluw2:ctd_181:salinity [PSU]'][673120:673420].rolling(25,center=True).mean(),
#         color='r', label='Salinity')


#ax1.set_xlabel('Time (hh:mm)')
#ax1.set_ylabel('Temperature ($\circ$C)')
##ax2.set_ylabel('Salinity (PSU)')
#ax1.xaxis.set_major_formatter(timeFmt)
#plt.title('(25 minute running average)')
#plt.suptitle('Water temperature in Ny-Alesund (AWIPEV)')