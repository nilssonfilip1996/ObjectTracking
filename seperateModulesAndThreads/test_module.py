# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 11:29:11 2019

@author: nilss
"""
import dictdiffer  

if __name__ == '__main__':
    d1 = {}
    d1['1'] = "100,200"
    d1['2'] = "300,400"
    d1['3'] = "50,50"
    #print(type(d1))
    
    d2 = {}
    d2['1'] = "100,300"
    d2['4'] = "50,100"
    
    print(d1)
    print(d2)
    print()
    print("Diff in keys: " + str((d2.keys()^d1.keys())))
    print()
    for diff in list(dictdiffer.diff(d1, d2)):         
        print(diff)