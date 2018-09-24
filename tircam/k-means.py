#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 10:24:45 2018
k-means classification of photo to obtain only the cold plume.
@author: cake
"""


from sklearn import cluster, datasets
from skimage import external, filters, io
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
import matplotlib.dates as mdates
import datetime as datetime


# make script so it is easy to run off image production and writing files
p_contour = False
p_kmeans = False
p_plume = False

# Also pick a colour map
theme = 'YlGnBu_r'

#pdir =  r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/latest2/*.tiff'
pdir =  r'/home/cake/mount/Users/admin/Documents/uni/school/aberystwyth/2018/tir/camera/backup_real/Record_*.csv'

# collect for plotting
countlst = []       # Fjord 'True' pixels in image
glacierts = []      # Glacier temperature per imaage
fjordts = []        # Fjord minimum temperature each image
percentage = []     # Percentage plume thresholding
kpercentage = []    # Pepercentage plume k-means
times = []          # Time of image (from title, see modify_filenames.py)
k_means_lo = []     # Lowest temp class each image inside fjord quare
k_lo_pixels = []    # Fjord pixels assigned kmeans


k_pixels_groups = []

# 

# iteration counter
i = 0
for fn in sorted(glob.glob(pdir)):
    
    data = pd.read_csv(fn, sep=';')
    data.drop(data.columns[len(data.columns)-1], axis=1, inplace=True)  # last column is NaN > remove
    m = data.values
    m = m.reshape((-1,1))


    name = fn.split(sep='/')
    name = name[-1]
    name = name.split(sep='.')
    name = name[0]
    name = name.split(sep='_')

    time = name[-1]
    
    name = name[1].split(sep='-')

    
    tbla = time.split(sep='-')

    
    times.append(datetime.datetime(year=int(name[0]), 
                                   month=int(name[1]), 
                                   day=int(name[2]), 
                                   hour=int(tbla[0]),
                                   minute=int(tbla[1])))
    
    
    k_means = cluster.KMeans(n_clusters=5, 
                             init='k-means++', 
                             n_init=10, 
                             max_iter=300, 
                             tol=0.0001, 
                             precompute_distances='auto', 
                             verbose=0, 
                             random_state=None, 
                             copy_x=True, n_jobs=1, algorithm='auto')
    
    k_means.fit(m) 
    
    values = k_means.cluster_centers_.squeeze()
    labels = k_means.labels_
    q = np.choose(labels, values)
    
    q.shape = data.shape
    
    if (p_kmeans):
        fig0 = plt.figure(figsize=[16,12])
        plt.imsave(''.join(['../quantitative/kmeans/', time, '-k_means.tiff']), 
                   q, 
                   cmap=theme)
        plt.close(fig0)
    
### Need to calculate the average temperature for the glacier, make sure that this temperature is
### temperature which the buoyant plume has to be proximal to (dep entrainment)
    mm = m
    mm.shape = data.shape    
    glacier_t = mm[110:150,200:300].mean()
    fjord_min_t = mm[155:-20].min()
    
    idx = ((q>fjord_min_t)*(q>glacier_t))
    
    if (p_plume):
        fig1 = plt.figure(figsize=[16,12])
        plt.imsave(''.join(['../quantitative/kmeans/', time, '-plume.tiff']), 
                   idx[155:-20][:], 
                   dpi=300, 
                   cmap=theme)    
        plt.close(fig1)
    pixelsFalse = np.size(idx[155:-20][:]) - np.count_nonzero(idx[155:-20][:])
    pixelsTrue = np.size(idx[155:-20][:]) - pixelsFalse
    
    print (i, time, q[155:-20].mean(), q[155:-20].min(), q[155:-20].max(), glacier_t, fjord_min_t, pixelsTrue)
    
### Finally, create a contour plot    
    if (p_contour):
        fig, ax1 = plt.subplots(figsize=[16,12])
        
        ax1.imshow(data, cmap='Greys_r')
        p = ax1.contour(data, [1,2,3,4,5,6,7,8,9], colors=['black'] ) #, cmap='Blues_r')
        
        ax1.clabel(p, #[0,1,2,3,4,5],  # label every second level
                  inline=1, fmt='%1.1f',
                  fontsize=25)
        
        #fig.colorbar(p, orientation='vertical', shrink=0.8)
        fig.tight_layout()
        fig.savefig(''.join(['../quantitative/contours/', time, '-contours.png']), cmap=theme)
        plt.close(fig)
        ### 
        
    ## add things to lists
    percent = np.size(idx[155:-20][:])/100
    percentage.append(pixelsTrue/percent)
    glacierts.append(glacier_t)
    fjordts.append(fjord_min_t)
    countlst.append(pixelsTrue)
    
    k_means_lo.append(q[155:-20][:].min())   # Lowest temp class each image inside fjord quare
    
    k_min_no = np.count_nonzero(q[155:-20][:] == q[155:-20][:].min())
    k_lo_pixels.append(k_min_no)         # Fjord pixels assigned kmeans minimum
    kpercentage.append(k_min_no/percent) # percentage of total
    
    ## kmeans tow lowest temperature classes
    kLoT = sorted(values)[:][0:2]
    kLoT_q = np.in1d(q, sorted(values)[:][0:2])
    k_pixels_groups.append(kLoT_q.sum())  
       
    i = i + 1
#    if i == 3:    
#        break
    
####### Create dataframe to make plotting etc easier:
out_df=pd.DataFrame({'Time':times, 
                 'Orig_GlacierT':glacierts,
                 'Orig_FjordMinT':fjordts,
                 'TthresPix':countlst, 
                 'TthresPercentagePx':percentage,
                 'KMeansLoT':k_means_lo,
                 'KMeansPix':k_lo_pixels,
                 'KMeansPercentagePx':kpercentage,
                 'KMeansPix2':k_pixels_groups,
                 'OrigFile':fn})
    
#%%

dates = mdates.date2num(times)
#matplotlib.pyplot.plot_date(dates, values)

fig,ax1 = plt.subplots(figsize=[8,6])
timeFmt = mdates.DateFormatter('%H:%M')

ax1.plot(times,countlst)
ax1.set_xlabel('Time (hh:mm)')
ax1.set_ylabel('Pixels (n)')
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(timeFmt)
plt.title('T_min_fjord > T > T_glacier')
plt.suptitle('Pixels classified as plume')

#columns = ['true', 'false']
#count = pd.DataFrame(countlst, columns=columns)   

#%%
#v
#ax1.imshow(J)
#p = ax1.contour(J, 10, cmap='Set1') #,[-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13], cmap='Blues_r')
#
#ax1.clabel(p, #[0,1,2,3,4,5],  # label every second level
#          inline=1, fmt='%1.1f', cmap='Dark2',
#          fontsize=14)
#
#fig.colorbar(p, orientation='vertical', shrink=0.8,  label='Temperature')
#fig.tight_layout()
#ax1.legend()


#%%
#Possible values are: Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, 
#CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, 
#Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, 
#PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, 
#RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, 
#Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, 
#YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, 
#autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, c
#ool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, 
#gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, 
#gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, 
#gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, 
#hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, 
#ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, 
#seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, 
#tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, viridis, viridis_r, winter, winter_r

#%% THIS CREATES IMAGE OF CSV FILE WITH RECTANGLE FOR FJORD AND FOR GLACIER AVERAGING SQUARE
import matplotlib.patches as patches
plt.imshow (data)
currentAxis = plt.gca()

rect_glacier = patches.Rectangle((200,110),110,35,linewidth=1,edgecolor='white',facecolor='none')
rect_fjord = patches.Rectangle((5,155),310,110,linewidth=1,edgecolor='lightblue',facecolor='none')
currentAxis.add_patch(rect_glacier)
currentAxis.add_patch(rect_fjord)

#%%
#
#
#out_df=pd.DataFrame({'Time':times, 
#                 'Orig_GlacierT':glacierts,
#                 'Orig_FjordMinT':fjordts,
#                 'TthresPix':countlst, 
#                 'TthresPercentagePx':percentage,
#                 'KMeansLoT':k_means_lo,
#                 'KMeansPix':k_lo_pixels,
#                 'KMeansPercentagePx':kpercentage,
#                 'OrigFile':fn})


fig = plt.figure(figsize=[16,12], dpi=300)
#ax2 = ax1.twinx()
plt.title('Amount of pixels classified as plume, methods compared', fontsize=16)
ax1=plt.subplot(311)
ax1.plot(out_df['Time'], out_df['TthresPix'], color='lightsteelblue')
ln1 = ax1.plot(out_df['Time'], 
               out_df['TthresPix'].rolling(5,center=True).mean(), 
               color='blue',
               label='Threshold \'True\'')

ax2 = plt.subplot(312)
ax2.plot(out_df['Time'], out_df['KMeansPix'], color='lightsalmon')
ln2 = ax2.plot(out_df['Time'], 
               out_df['KMeansPix'].rolling(5,center=True).mean(), 
               color='red',
               label='KMeans 1 class')


ax3 = plt.subplot(313)
ax3.plot(out_df['Time'], out_df['KMeansPix2'], color='lightgrey')
ln2 = ax3.plot(out_df['Time'], 
               out_df['KMeansPix2'].rolling(5,center=True).mean(), 
               color='cyan',
               label='KMeans 2 classes')

ax1.xaxis_date()
ax1.xaxis.set_major_formatter(timeFmt)
ax1.set_ylabel('Pixels (n)')
ax1.legend()

ax2.xaxis_date()
ax2.xaxis.set_major_formatter(timeFmt)
ax2.set_ylabel('Pixels (n)')
ax2.legend()

ax3.xaxis_date()
ax3.xaxis.set_major_formatter(timeFmt)
ax3.set_ylabel('Pixels (n)')
ax3.legend()

plt.xlabel ('Time (hh:mm)')

#axes = ln1 + ln2
#labels = [l.get_label() for l in axes]
#plt.legend(axes, labels, loc=0)

fig.savefig('/home/cake/2018/dissertation/latex/images/PlumeClassifiedPixelsNew.png')


# added these three lines
#lns = lns1+lns2+lns3
#labs = [l.get_label() for l in lns]
#ax.legend(lns, labs, loc=0)





#%% Regressions & fjord temp comparisons: quality assessment
from scipy.stats import linregress
fig = plt.figure(figsize=[16,16], dpi=300)

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

plt.rc('font', **font)

###
ax1 = plt.subplot(511)
copy_df = out_df.sort_values('TthresPix')
ax1.plot(copy_df['TthresPix'],
         copy_df['KMeansPix'],
               '.', color='lightsteelblue',)

#ax1.plot(out_df['TthresPix'].rolling(5,center=True).mean(),
#         out_df['KMeansPix'].rolling(5,center=True).mean(),
#               '.', color='red', label='rolling(5)')

ax1.set_xlabel('Threshold pixels (n)')
ax1.set_ylabel('K-Means single (n)')

slope, intercept, r_value, p_value, std_err = linregress(copy_df['TthresPix'], copy_df['KMeansPix'])
line = slope*copy_df['TthresPix']+intercept
lbl2 = ''.join(['R-value = ', str(round(r_value,2))])
ln2 = ax1.plot(copy_df['TthresPix'], line, label=lbl2, color='orange')


ax1.legend()


###
ax2 = plt.subplot(512)
ax2.plot(out_df['TthresPix'],
         out_df['KMeansPix2'],
         '.', color='lightsteelblue')

#ax2.plot(out_df['TthresPix'].rolling(5,center=True).mean(),
#         out_df['KMeansPix2'].rolling(5,center=True).mean(),
#         '.', color='blue')

ax2.set_xlabel('Threshold pixels (n)')
ax2.set_ylabel('K Means double (n)')

slope, intercept, r_value, p_value, std_err = linregress(out_df['TthresPix'], out_df['KMeansPix2'])
line = slope*out_df['TthresPix']+intercept
lbl2 = ''.join(['R-value = ', str(round(r_value,2))])
ax2.plot(out_df['TthresPix'], line, label=lbl2, color='orange')
ax2.legend()

###
ax3 = plt.subplot(513)
ax3.plot(out_df['Orig_FjordMinT'],
         out_df['KMeansLoT'],
         '.')

ax3.set_xlabel('Original thermograph fjord T ($^\circ$C)')
ax3.set_ylabel('K-means fjord T ($^\circ$C)')

slope, intercept, r_value, p_value, std_err = linregress(out_df['Orig_FjordMinT'], out_df['KMeansLoT'])
line = slope*out_df['Orig_FjordMinT']+intercept
lbl2 = ''.join(['R-value = ', str(round(r_value,2))])
ax3.plot(out_df['Orig_FjordMinT'], line, label=lbl2)

ax3.legend()

###
ax4 = plt.subplot(514)

copy_df = out_df.sort_values('Orig_GlacierT')
ax4.plot(copy_df['Orig_GlacierT'],
         copy_df['KMeansPercentagePx'], color='lightsalmon')

ln1 = ax4.plot(copy_df['Orig_GlacierT'].rolling(5,center=True).mean(),
         copy_df['KMeansPercentagePx'].rolling(5,center=True).mean(),
         color='red', label='K-means %')

ax4.plot(copy_df['Orig_GlacierT'],
         copy_df['TthresPercentagePx'], color='lightsteelblue')

ln2 = ax4.plot(copy_df['Orig_GlacierT'].rolling(5,center=True).mean(),
         copy_df['TthresPercentagePx'].rolling(5,center=True).mean(),
         color='blue', label='T threshold %')

ax4.set_xlabel('Glacier T ($^\circ$C)')
ax4.set_ylabel('\'True\' pixels (%)')

lns = ln1 + ln2
labels = [l.get_label() for l in lns]
ax4.legend(lns, labels, loc=0)
#
####
ax5 = plt.subplot(515)
copy_df = out_df.sort_values('Orig_FjordMinT')

ax5.plot(copy_df['Orig_FjordMinT'],
         copy_df['KMeansPercentagePx'], '.', color='lightsalmon')

ln1 = ax5.plot(copy_df['Orig_FjordMinT'].rolling(5,center=True).mean(),
         copy_df['KMeansPercentagePx'].rolling(5,center=True).mean(),
         color='red', label='K-means %')

ax5.plot(copy_df['Orig_FjordMinT'],
         copy_df['TthresPercentagePx'], '.', color='lightsteelblue')

ln2 = ax5.plot(copy_df['Orig_FjordMinT'].rolling(5,center=True).mean(),
         copy_df['TthresPercentagePx'].rolling(5,center=True).mean(),
         color='blue', label='T threshold %')

ax5.set_xlabel('Fjord T ($^\circ$C)')
ax5.set_ylabel('\'True\' pixels (%)')

lns = ln1 + ln2
labels = [l.get_label() for l in lns]
ax5.legend(lns, labels, loc=0)







plt.tight_layout()
fig.savefig('/home/cake/2018/dissertation/latex/images/PlumeRegression.png')




#%% Fjord min T

