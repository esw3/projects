#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 22:12:24 2018.rolling(25,center=True).mean(

@author: cake
"""

#%% AWI temperature data for comparison
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import datetime 
import matplotlib.dates as mdates
import seaborn as sns

fn = r'../../extra_data/awi/data2_TS.csv'
df = pd.read_csv(fn, sep=',', parse_dates=['datetime'])

fig,ax1 = plt.subplots(figsize=[8,6])
#plt.figure(figsize=[8,6]) 
#ax = plt.axes()

#ax2=ax1.twinx()

#plt.plot(means.rolling(5,center=True).mean()['T_ave'])
#plt.xlabel='test'
timeFmt = mdates.DateFormatter('%H:%M')

ax1.plot(df['datetime'][673120:673420],
         df['svluwobs:svluw2:ctd_181:temperature [°C]'][673120:673420]),
         color='g', label='Temperature')

ax2.plot(df['datetime'][673120:673420],
         df['svluwobs:svluw2:ctd_181:salinity [PSU]'][673120:673420].rolling(25,center=True).mean(),
         color='r', label='Salinity')

ax1.set_xlabel('Time (hh:mm)')
ax1.set_ylabel('Temperature ($\circ$C)')
#ax2.set_ylabel('Salinity (PSU)')
ax1.xaxis.set_major_formatter(timeFmt)
plt.title('(25 minute running average)')
plt.suptitle('Water temperature in Ny-Alesund (AWIPEV)')
#ax1.legend()
#ax2.legend()

#%% tidal data for comparison

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import datetime 
import matplotlib.dates as mdates
import seaborn as sns

fn = r'../../extra_data/tide_from_kartverket_no_2.csv'

df = pd.read_csv(fn, sep=',', parse_dates=[0], header=0) 

timeFmt = mdates.DateFormatter('%H:%M')
fig,ax1 = plt.subplots(figsize=[8,6])

ax1.plot(df['datetime'][24:31],
         df['tide1'][24:31],
         color='g', label='height1 (cm)')

ax1.plot(df['datetime'][24:31],
         df['tide2'][24:31],
         color='r', label='height2 (cm)')

ax1.set_xlabel('Time (hh:mm)')
ax1.set_ylabel('Tide height (cm)')
#ax2.set_ylabel('Salinity (PSU)')
ax1.xaxis.set_major_formatter(timeFmt)
plt.title('Tide height projection (astronomical) for Ny-Alesund (Kartverket)')
#plt.suptitle('Water temperature in Ny-Alesund (AWIPEV)')
plt.legend()

#%%
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import datetime 
import matplotlib.dates as mdates
import seaborn as sns

fn = r'../../extra_data/tide_from_kartverket_no_2.csv'

df = pd.read_csv(fn, sep=',', parse_dates=[0], header=0) 

timeFmt = mdates.DateFormatter('%d-%m')
fig,ax1 = plt.subplots(figsize=[8,6])

ax1.plot(df['datetime'],
         df['tide1'],
         color='g', label='height1 (cm)')

ax1.plot(df['datetime'],
         df['tide2'],
         color='r', label='height2 (cm)')



ax1.set_xlabel('Days (day-month)')
ax1.set_ylabel('Tide height (cm)')
#ax2.set_ylabel('Salinity (PSU)')
ax1.xaxis.set_major_formatter(timeFmt)
plt.title('Tide height projection for Ny-Alesund (Kartverket)')
#plt.suptitle('Water temperature in Ny-Alesund (AWIPEV)')
plt.legend()


#%% CLOUDS


#%% INSOLATION 
