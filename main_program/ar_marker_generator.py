# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 13:20:20 2019

@author: nilss

Follow this guide in order to use dependancies: https://pypi.org/project/ar-markers/
"""
from ar_markers import HammingMarker
from PIL import Image
from numpy.random import randint

if __name__ == '__main__':

        for x in range(1, 31):          #Creating x amount of markers.
            #markerId = randint(100)     #Marker value is randomized
            marker = HammingMarker(x)    #created marker pattern
            img = Image.fromarray(marker.generate_image())  #npArray->img
            img = img.convert("L")                          #Dunno what this is, had to do it
            img.save(str(x) + '.png')                #Save file. Same path as this file.
            #img.show()         #Alternative. Used to display the image