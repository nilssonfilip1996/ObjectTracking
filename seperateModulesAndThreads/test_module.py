# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 11:29:11 2019

@author: nilss
"""  
import math
from collections import Counter

def checkDictEquality(od, nd):
    for k in nd.keys():
        if(k in od.keys()):
            if(not isInBoundary(od[k], nd[k], 50)):
                return False
        else:
            return False
    return True
                
def isInBoundary(coord1, coord2, r): 
  
    x1 = math.pow((coord2[0]-coord1[0]), 2) 
    y1 = math.pow((coord2[1]-coord1[1]), 2) 
    hyp = math.sqrt(x1 + y1) # distance between the centre and given point 
    #print(hyp)
    return (hyp<r)

if __name__ == '__main__':
#    d1 = {}
#    d1['1'] = (100,200)
#    #d1['2'] = (300,400)
#    d1['3'] = (50,50)
#    #print(type(d1))
#    
#    d2 = {}
#    d2['1'] = (100,202)
#    d2['3'] = (50,100)
#    
#    print(d1)
#    print(d2)
#    print(checkDictEquality(d1, d2))
#    print("Diff in keys: " + str((d2.keys()^d1.keys())))
#    print()
#    for diff in list(dictdiffer.diff(d1, d2)):         
#        print(diff)
    
#    l1 = [(1,3), (3,5)]
#    l2 = [(1,2), (3,5)]
#    value = [x//2 for x in l1[0]]
#    print(value)
    
    d1 = {"1": (100,300), "2": (300, 400), "3": (50,50)}
    d2 = {"1": (101,300),"3": (50,51)}
    d3 = {"1": (100,300), "2": (300, 400), "3": (50,50)}
    d4 = {"1": (101,300), "2": (300, 400), "3": (50,50)}
    d5 = {"1": (100,300), "3": (50,50)}
    
    d_list = [d1,d2,d3,d4,d5]
    
    full_d = {}
    for d in d_list:
        for d_key in d:
            if(not  d_key in full_d):
                full_d[d_key] = []
            full_d[d_key].append(d[d_key])
            
    print(full_d)
            
    for d_key in full_d:
        c = Counter(full_d[d_key])
        value = str(c.most_common()[0][0])
        print("Key " + d_key +" has most frequent value: " + value)
            