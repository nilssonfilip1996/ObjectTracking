# -*- coding: utf-8 -*-
"""
Created on Thu May 16 18:10:38 2019

Used to find max distance between points

@author: nilss
"""
import math
import matplotlib.pyplot as plt
from collections import Counter

def dist(p1, p2):
    hyp = math.sqrt((int(p1[0])-int(p2[0]))**2+
                    (int(p1[1])-int(p2[1]))**2)
    return hyp

name = 'data_5'
with open(name + ".txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

c = Counter(content)
real_coord, count = c.most_common()[0]
print("Real coordinate: " + str(real_coord)) 
real_coord = real_coord.strip('()')
p1 = real_coord.split(', ')
plt.plot(int(p1[0]),int(p1[1]), 'yo', label="actual center")
#plt.text(int(p1[0])+0.3,int(p1[1])-0.3,"actual center", fontsize=15, color='green')
plt.xlim(int(p1[0])-2, int(p1[0])+2)
plt.ylim(int(p1[1])-2, int(p1[1])+2)
plt.xlabel('pixels')
plt.ylabel('pixels')
plt.title("Deviations for " + name, y=-0.01)
list2 = list(set(content))
print(list2)

biggest = -1
big1 = p1
big2 = None

for l1 in range(len(list2)):
    index = l1
    l1 = list2[l1].strip('()')
    p2 = l1.split(', ')
    if(p1==p2):
        continue
    plt.plot(int(p2[0]),int(p2[1]), 'ro')
    temp = dist(p1, p2)
    if(temp>biggest):
        big2 = p2
        biggest = temp
    print(dist(p1, p2))
print("-----------------")
biggest = round(biggest,2)
print("Biggest diff: " + str(biggest))
b1 = (int(big1[0]), int(big2[0]))
b2 = (int(big1[1]), int(big2[1]))
plt.plot(int(big2[0]), int(big2[1]), 'ro', label="deviations")
print(b1,b2)
plt.plot(b1,b2, color='blue', label="largest deviation")
plt.text((b1[0] + b1[1])/2 +0.2,(b2[0] + b2[1])/2, "dMax=" + str(biggest) + 'p', fontsize=15, color='blue')
plt.legend()
plt.show()
plt.gca().invert_yaxis()
plt.gca().xaxis.tick_top()
plt.gca().xaxis.set_label_position('top')
plt.savefig(name + '_graph.png')

#for l1 in range(len(list2)):
#    index = l1
#    l1 = list2[l1].strip('()')
#    p1 = l1.split(', ')
#    plt.plot(int(p1[0]),int(p1[1]), 'ro')
#    for l2 in range(index+1,len(list2)):
#        l2 = list2[l2].strip('()')
#        p2 = l2.split(', ')
#        #print(p1,p2)
#        temp = dist(p1, p2)
#        if(temp>biggest):
#            big1 = p1
#            big2 = p2
#            biggest = temp
#        print(dist(p1, p2))
#print("-----------------")
#print("Biggest diff: " + str(biggest))
#b1 = (int(big1[0]), int(big2[0]))
#b2 = (int(big1[1]), int(big2[1]))
#print(b1,b2)
#plt.plot(b1,b2)
#plt.show()
        

