#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 21:31:40 2018

Plots

@author: cake
"""
import glob
import pandas as pd
import numpy as np
from matplotlib import dates
from matplotlib import pyplot as plt



#fn = r'../quantitative/lines/Line1.csv'
#fn = r'../quantitative/lines/kongsfjorden_line.csv'
#fn = r'../quantitative/lines/kongsfjorden_line2.csv'
fn = r'../quantitative/lines/hornbreen.csv'

running_average = 20

df = pd.read_csv(fn, header=0)

fig = plt.subplots(figsize=[8,6], dpi=300)


#timeFmt = mdates.DateFormatter('%H:%M')

#ax1.plot(df['datetime'][673120:673420],
#         df['svluwobs:svluw2:ctd_181:temperature [°C]'][673120:673420].rolling(25,center=True).mean(),
#         color='g', label='Temperature')

ax1 = plt.subplot(211)

#title = ''.join(['(', str(running_average), ' point running average)'])
title = 'Hornbreen/Hamburgerbreen 06/07/2015'
plt.title(title)
#plt.suptitle('Profile of Red+NIR and Temperature ')

ax1.plot(         df['redNIR'],
         color='lightsalmon', label='red+NIR')

ln1 = ax1.plot(         df['redNIR'].rolling(running_average,center=True).mean(),
         color='r', label='red+NIR')

ax2 = ax1.twinx()

ax2.plot(         df['temp'],
         color='palegreen', label='Band10 T')
ln2 = ax2.plot(         df['temp'], #.rolling(running_average,center=True).mean(),
         color='g', label='B10 T')

#ax3 = plt.subplot(212)
#ax3.plot(df['redNIR'].rolling(running_average,center=True).mean(), df['temp'], '.')
#ax3.set_yscale('log')

ax1.set_xlabel('Digital points sampled (n)')
ax1.set_ylabel('DN')
ax2.set_ylabel('Temperature ($^\circ$)')


lines = ln1 + ln2
labs = [l.get_label() for l in lines]
ax1.legend(lines, labs, loc='center right')

#lines, labels = ax1.get_legend_handles_labels()
#lines2, labels2 = ax2.get_legend_handles_labels()
#ax2.legend(lines + lines2, labels + labels2, loc='lower left', bbox_to_anchor=(1.2, 0.5))

#ax2.set_ylabel('Salinity (PSU)')
#ax1.xaxis.set_major_formatter(timeFmt)

plt.tight_layout()

