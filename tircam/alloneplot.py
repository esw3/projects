#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 09:52:24 2018

Get all plots as one plot?

@author: cake
"""

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import datetime 
import matplotlib.dates as mdates
import seaborn as sns

awi_fn = r'../../extra_data/awi/data2_TS.csv'
awi_ts = pd.read_csv(awi_fn, sep=',', parse_dates=['datetime'])

ekl_fn = r'../../extra_data/eklima_Nyalesund_hourly.csv'
ekl_T = pd.read_csv(ekl_fn, sep=',')

ka_fn = r'../../extra_data/tide_from_kartverket_no_2.csv'
tide = pd.read_csv(ka_fn, sep=',', parse_dates=[0], header=0) 


timeFmt = mdates.DateFormatter('%H:%M')


#fig,ax1 = plt.subplots(figsize=[8,6])


plt.figure(1, figsize=[16,12], dpi=300)

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)

############## Plume size
ax0 = plt.subplot(511)

#dates = mdates.date2num(times[6:-1])
#ax0.plot(times[6:-1],countlst[6:-1])


#ax0.plot(copy_df['TthresPix'] ,'.', label='threshold')
ax0.xaxis.set_major_formatter(timeFmt)

ax0.plot(copy_df['Time'][6:-1], copy_df['TthresPix'][6:-1], '.', label='threshold')
ax0.plot(copy_df['Time'][6:-1], copy_df['KMeansPix'][6:-1] ,'.', label='k-means 1')
ax0.plot(copy_df['Time'][6:-1], copy_df['KMeansPix2'][6:-1] ,'.', label='k-means 2')
plt.legend()


############## Air temperature
axx = plt.subplot(512)
axx.plot(tide['datetime'][1:8], ekl_T['TA'][24:31])

############## T&S AWI
ax11 = plt.subplot(513)
ax12 = ax11.twinx()
lns1 = ax11.plot(awi_ts['datetime'][673148:673388],
          awi_ts['svluwobs:svluw2:ctd_181:temperature [°C]'][673148:673388].rolling(25,center=True).mean(),
          color='g', label='Temperature')

lns2 = ax12.plot(awi_ts['datetime'][673148:673388],
          awi_ts['svluwobs:svluw2:ctd_181:salinity [PSU]'][673148:673388].rolling(25,center=True).mean(),
          color='r', label='Salinity')

#combine legends
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax12.legend(lns, labs, loc=0)

############## TIDE Kartverket
ax2 = plt.subplot(514)
ax2.plot(tide['datetime'][1:8],
         tide['tide1'][1:8],
         color='g', label='height1 (cm)')

ax2.plot(tide['datetime'][1:8],
     tide['tide2'][1:8],
     color='r', label='height2 (cm)')
ax2.legend()

############ Clear sky radiation
ax3 = plt.subplot(515)
ax3.plot(times[6:-1], clear_sky_rad[6:-1])


#--- xformatting
#ax11.set_xlim(xmin=awi_ts['datetime'][673148])


#--- labeling
ax2.set_xlabel('Time (hh:mm)')
ax0.set_ylabel('Plume (pixels)')
axx.set_ylabel('Air T')
ax11.set_ylabel('Water T')
ax12.set_ylabel('Salinity')
ax2.set_ylabel('Tide height (cm)')
ax3.set_ylabel('Clear sky rad (Wm$^{-2}$)')


##ax2.set_ylabel('Salinity (PSU)')

ax0.xaxis.set_major_formatter(timeFmt)
axx.xaxis.set_major_formatter(timeFmt)
ax11.xaxis.set_major_formatter(timeFmt)
ax12.xaxis.set_major_formatter(timeFmt)
ax2.xaxis.set_major_formatter(timeFmt)
ax3.xaxis.set_major_formatter(timeFmt)

#plt.title('Tide height projection (astronomical) for Ny-Alesund (Kartverket)')
#plt.suptitle('Water temperature in Ny-Alesund (AWIPEV)')
#plt.legend()
