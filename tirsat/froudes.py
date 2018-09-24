#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 14:36:21 2018


Froude number hahaha
@author: cake
"""

import seawater 
import math


# list of initial velocities 

velocities = [0.1, 0.5, 1, 2, 4, 8]  #ms^-1
d = 250     # diameter 250m
g = 9.81    # ac'n grav ms^-2
rho_plume =  seawater.dens(0,2,0)     # assume T, S of fresh water
rho_ambient =  seawater.dens(34,6,0)  # assume T, S of sea water 

denominator = math.sqrt(g * ( (rho_ambient - rho_plume )/rho_plume) * d)

froudenos = []
for u in velocities:
    fr = u / denominator
    froudenos.append(fr)
    
print (froudenos)


