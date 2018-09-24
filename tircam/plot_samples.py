#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 12:39:23 2018

Point sample graphs!


@author: cake
"""

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np

#
#fig = plt.figure(dpi=300) 
#ax = plt.axes()

fn = r'notpy/point_samples.csv'
df = pd.read_csv(fn)

dfsum = df.rolling(7,center=True).mean()
dfstd= df.rolling(7,center=True).std()

#fig, axes = plt.subplots(ncols=1, figsize = (20,10))
fig = plt.figure(figsize = (20,20), dpi=300)

#ax = dfsum.plot(subplots=True, legend=True, figsize=[20,20],
#           yerr=dfstd,
#           title='Running mean (25 minute averages) of plume development sample point temperatures',
#           ylim=[1.5,5.5], 
#           fontsize=12)

plt.subplot(811)
ax0 = plt.plot (dfsum['Tidewater front'], label='tidewater front')
plt.ylim(1.5, 5.5)
plt.legend(fontsize=16, loc=0)
plt.title('Thermal time-lapse transect', fontsize=20)

plt.subplot(812)
plt.ylim(1.5, 5.5)
ax1 = plt.plot(dfsum['Plume start'], label='plume start')
plt.legend(fontsize=16, loc=0)

plt.subplot(813)
plt.ylim(1.5, 5.5)
ax2 = plt.plot(dfsum['Progression 1'], label='progression 1')
plt.legend(fontsize=16, loc=0)


plt.subplot(814)
plt.ylim(1.5, 5.5)
ax3 = plt.plot(dfsum['Progression 2'], label='progression 2')
plt.legend(fontsize=16, loc=0)


plt.subplot(815)
plt.ylim(1.5, 5.5)
ax4 = plt.plot(dfsum['Progression 3'], label='island')
plt.legend(fontsize=16, loc=0)


plt.subplot(816)
plt.ylim(1.5, 5.5)
ax5 = plt.plot(dfsum['Island 1'], label='progression 3')
plt.legend(fontsize=16, loc=0)


plt.subplot(817)
plt.ylim(1.5, 5.5)
ax6 = plt.plot(dfsum['Progression 4'], label='progression 4')
plt.legend(fontsize=16, loc=0)


plt.subplot(818)
plt.ylim(1.5, 5.5)
ax7 = plt.plot(dfsum['Progression 5'], label='progression 5')
plt.legend(fontsize=16, loc=0)


#ax.set_xlabel('test')
#ax.set_ylabel('Temperature ($\circ$C)')

#
#matplotlib.rc('legend', fontsize=10)    # legend fontsize
#matplotlib.rc('figure', titlesize=12)  # fontsize of the figure title
ax0.legend(fontsize=16)
ax1.legend(fontsize=16)
ax2.legend(fontsize=16)
ax3.legend(fontsize=16)
ax4.legend(fontsize=16)
ax5.legend(fontsize=16)
ax6.legend(fontsize=16)
ax7.legend(fontsize=16)

#plt.title.set_size(40)


#%% OVERALL IMAGE BRIGHTNESS GLOB THIS FOR EACH CSV!!!
import glob
import numpy as np 

means = pd.DataFrame(columns=['T_ave','std'])

fns = r'../../camera/backup_real/Record_2*.csv'
i=0
for filename in glob.iglob(fns, recursive=True):
    #print (filename)
    csv_data = pd.read_csv(filename, sep=';', header=0)
    #means.append([np.nanmean(csv_data), np.nanstd(csv_data)])
    means.loc[i,'T_ave'] = (np.nanmean(csv_data))
    means.loc[i,'std'] = (np.nanstd(csv_data))
    #means['std'][i] = np.nanstd(csv_data)
    i=i+1
    

fig = plt.figure() 
ax = plt.axes()

#plt.plot(means.rolling(5,center=True).mean()['T_ave'])
#plt.xlabel='test'

means.rolling(5,center=True).mean()['T_ave'].plot(figsize=[8,6], 
             yerr=means.rolling(5,center=True).std(), 
             title='Rolling mean of average temperature of each file recorded by the TIM 450',
             style='classic')

#ax.fill_between(means.index, 
#                means.rolling(5,center=True).mean()['T_ave'] + means.rolling(5,center=True).mean()['std'], 
#                means.rolling(5,center=True).mean()['T_ave'] - means.rolling(5,center=True).mean()['std'],
#                color='gray', alpha=0.2)
#ax.plot(means.rolling(5,center=True).mean()['T_ave'])
ax.set_xlabel('Image number in order (n)')
ax.set_ylabel('Average image temperature ($\circ$C)')

#%% KLIMA data for comparison
fn = r'../../extra_data/eklima_Nyalesund_hourly.csv'
df = pd.read_csv(fn, sep=',')


fig = plt.figure() 
ax = plt.axes()

#plt.plot(means.rolling(5,center=True).mean()['T_ave'])
#plt.xlabel='test'

plt.plot(df['TA'][24:32])
ax.set_xlabel('Image number in order (n)')
ax.set_ylabel('Average image temperature ($\circ$C)')

