# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:14:18 2019

@author: nilss
"""

import datetime


s1 = '17:03:09.86'
s2 = '17:03:09.54'

d1 = datetime.datetime.strptime(s1, '%H:%M:%S:%ms')
d2 = datetime.datetime.strptime(s2, '%H:%M:%S')

print(d1-d2)