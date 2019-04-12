# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:28:00 2019

@author: nilss
"""

import math

def isInBoundary(coord1, coord2, r): 
  
    x1 = math.pow((coord2[0]-coord1[0]), 2) 
    y1 = math.pow((coord2[1]-coord1[1]), 2) 
    hyp = math.sqrt(x1 + y1) # distance between the centre and given point 
    return (hyp<r)