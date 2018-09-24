#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 10:50:00 2018
Calc insolation/solar angle clearsky-radiation
@author: cake
"""
from pysolar.solar import *
import datetime
import pytz

#date = datetime.datetime.now()
#print(get_altitude(42.206, -71.382, date))

altitude = []
azimuths = []
clear_sky_rad = []

#lon = 
lat = 87.73724
#lon = 43.9669097265537	 #
lon = 12.067060 #googlemap longitude
#lat = 87.986966 #googlemap latitude

#start_date = datetime.datetime(2018, 8, 18, 00, 00, 0, 000000, tzinfo=datetime.timezone.utc)


for d in times:
    local = pytz.timezone ("Europe/Oslo")
    #naive = datetime.datetime.strptime ("2001-2-3 10:11:12", "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(d, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)

    altitude_deg = get_altitude(lat, lon, utc_dt)
    az = get_azimuth(lat, lon, utc_dt)
    rads = radiation.get_radiation_direct(utc_dt, altitude_deg)
    
    print (d, altitude_deg, az, rads)
    
    altitude.append(altitude_deg)
    azimuths.append(az)
    clear_sky_rad.append(rads)

#latitude_deg = 42.206 # positive in the northern hemisphere
#longitude_deg = -71.382 # negative reckoning west from prime meridian in Greenwich, England
#date = datetime.datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=datetime.timezone.utc)
#altitude_deg = get_altitude(latitude_deg, longitude_deg, date)
#radiation.get_radiation_direct(date, altitude_deg)



# get transmission angle: snells law
import math
n1 = 1.000293 # air
n2 = 1.330    # water
trans_angles = []

for alt in altitude:
    coo = math.degrees(math.asin(n1/n2 * math.sin(math.radians(90-alt))))
    if coo < 0:
        coo = abs(coo)
    trans_angles.append(coo)
    
# get dielectric-dielectric reflectivity from Fresnel eq
angles = zip(altitude,trans_angles)
out = []
for a1,a2 in angles:
    a1 = math.radians(a1)
    a2 = math.radians(a2)
    out.append(90-math.degrees(abs((n1*math.cos(a1)-n2*math.cos(a2)) / (n1*math.cos(a1)+n2*math.cos(a2)))))

print (out)
    