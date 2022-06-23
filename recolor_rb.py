# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 09:20:23 2021

@author: Julion
"""

from PIL import Image, ImageOps
from matplotlib import cm
from colour import Color
import numpy as np
import time
import os
import sys

# Prepare lists and bools
# w bool: To-Do; Should ask if values should be safed to files or not
# x bool: Checks if asked for base color
# y bool: Checks if asked for amount of files
# z bool: Checks if asked for minimum intensity value

print("Welcome to IF-Grad. A fluorescent image gradient converter.")

files = []
colors = []
w = False
x = False
y = False
z = False
histo = False

"""
Start color and end color for smooth transition into colormap
Amount of steps depend on how fast the transition has to be
Needs to be smaller than 256
Procedure to find these values:
    1. Check the color maps on 
    https://matplotlib.org/stable/tutorials/colors/colormaps.html
    2. Find the color from which you want to transition to black 
    3. Measure the point loosely and compare it to the full length of the map
    4. Measured point/full length * 256 is your colorSteps amount
    5. Cry in a corner because you've forgotten about this whole procedure in
    a week
Generally, the code is designed to take a color map, start on the right of it
and move to the left (hence the reverse at the end)
The transition in the pre-code makes a somewhat janky start from black 
possible.
"""
# Check if a file got drag and dropped
# try:
#     hold = str(sys.argv[1])
#     hold.split("\\")
#     files.append(hold[-1])
#     y = True
# except:
#     y = False

# Makes a transition from black to blue (rgb(0,0,0) to rgb(0,0,255)) and
# adds the colors to a list

blue2black = list()

for numbers in range(256):
    if numbers % 4 == 0:        
        colorAdd = Color(rgb=(0, 0, numbers/255))
        blue2black.append(colorAdd)

# Takes 64 values from the previous transition and adds the rest of the color 
# map (from right to left)
for i in range(256):
    if i >= 256-len(blue2black):    # Part for smooth transition
        rgbaTuple = list(blue2black[256-i-1].rgb)
        for k in range(3):
            rgbaTuple[k] = round(rgbaTuple[k]*255)        
    else:           # Rest from the color map cm.gist_rainbow here
        rgbaTuple = list(cm.gist_rainbow(i))
        rgbaTuple.pop(3)
        for j in range(3):
            rgbaTuple[j] = round(rgbaTuple[j]*255)
    colors.append(tuple(rgbaTuple))
colors.reverse()    # Flip it around
    
# Ask for base color
while not x:
    basis = str(input('Base color? (r/g/b/gray) '))
    if basis == 'r':
        basis = 0;
        x = True;
    elif basis == 'g':
        basis = 1;
        x = True;
    elif basis == 'b':
        basis = 2;
        x = True;
    elif basis == 'gray':
        basis = 3;
        x = True;
    else:
        print('Invalid input!')

# Ask for file names or folder
while not y:
    folFil = str(input("Do you want to add single files or folder? (s/f) "))
    if folFil == 's':
        addMore = 'y'
        while addMore == 'y':
            files.append(str(input('Enter filename: ')))
            try:
                img = Image.open(files[-1])
            except: 
                print("Filename either incorrect or file does not exist.")
                continue
            addMore = input('Add more files? (y/n) ')
        y = True
    elif folFil == 'f':
        path = str(input('Enter folder path (syntax: C:\\files\\myFolder\\): '))
        try:
            files = os.listdir(path)
        except:
            print("Path to folder either incorrect or folder doesn't exist.")
            continue
        y = True
    else:
        print('Invalid input!')

# Asking if data should be saved to files
while not w:
    answer = str(input('Do you want to save the color data to a file? (y/n) '))
    if answer == 'y':
        histo = True
        w = True
        histoData = np.array([np.arange(0,256,1),np.zeros(256)],np.int32)
    elif answer == 'n':
        histo = False
        w = True
    else:
        print("Please input a valid response.")


# Asking for starting intensity value
while not z:
    startValue = str(input("Minimum color intensity? (0-255) "))
    if startValue == '':
        startValue = 0
    elif startValue.isnumeric():
        startValue = int(startValue)
        if startValue > 255:
            print('Please input a number between 0 and 255')
            continue
    else:
        print('Please input a number between 0 and 255')
        continue
    colorAssignSteps = 255 / (255 - startValue)
    z = True
    
 
# Asign each pixel a new value from the prepared colors list, depending on 
# the intensity of a specified color
t = time.time()
if folFil == 's':
    for filename in files:
        if basis < 3:
            img = Image.open(filename)
            
            img = img.convert("RGB")
            datas = img.getdata()
            
            new_img_data = []
            for item in datas:
                # If histo flag is set, safe data to numpy array
                if histo:
                    histoData[1,item[basis]] = histoData[1,item[basis]] + 1
                # If defined starting intensity value is above 0, assign colors
                # on stretched scale (hopefully)
                if startValue > 0:
                    if item[basis] < startValue:
                        new_img_data.append(colors[0])
                    else:
                        newValue = item[basis] - startValue
                        new_img_data.append(colors[int(round(newValue * colorAssignSteps))])
                else:
                    new_img_data.append(colors[item[basis]])
        else:
            img = Image.open(filename)        
            img = img.convert("RGB")
            gray = ImageOps.grayscale(img)
            datas = gray.getdata()
            
            new_img_data = []
            for item in datas:
                # If histo flag is set, safe data to numpy array
                if histo:
                    histoData[1,item] = histoData[1,item] + 1
                if startValue > 0:
                    if item < startValue:
                        new_img_data.append(colors[0])
                    else:
                        newValue = item - startValue
                        new_img_data.append(colors[int(round(newValue * colorAssignSteps))])
                else:
                    new_img_data.append(colors[item])
        
        img.putdata(new_img_data)
        
        img.save('./Conversions/converted_'+filename,'TIFF')
        if histo:
            np.savetxt('./Conversions/data_'+filename+'.dat',histoData,delimiter='\t',fmt='%1i')
else:
    for filename in files:
        if basis < 3:
            img = Image.open(path + filename)
            
            img = img.convert("RGB")
            datas = img.getdata()
            
            new_img_data = []
            for item in datas:
                # If histo flag is set, safe data to numpy array
                if histo:
                    histoData[1,item[basis]] = histoData[1,item[basis]] + 1
                # If defined starting intensity value is above 0, assign colors
                # on stretched scale (hopefully)
                if startValue > 0:
                    if item[basis] < startValue:
                        new_img_data.append(colors[0])
                    else:
                        newValue = item[basis] - startValue
                        new_img_data.append(colors[int(round(newValue * colorAssignSteps))])
                else:
                    new_img_data.append(colors[item[basis]])
        else:
            img = Image.open(path + filename)        
            img = img.convert("RGB")
            gray = ImageOps.grayscale(img)
            datas = gray.getdata()
            
            new_img_data = []
            for item in datas:
                # If histo flag is set, safe data to numpy array
                if histo:
                    histoData[1,item] = histoData[1,item] + 1
                if startValue > 0:
                    if item < startValue:
                        new_img_data.append(colors[0])
                    else:
                        newValue = item - startValue
                        new_img_data.append(colors[int(round(newValue * colorAssignSteps))])
                else:
                    new_img_data.append(colors[item])
        
        img.putdata(new_img_data)
        
        img.save('./ConversionsFolder/converted_'+filename,'TIFF')
        if histo:
            np.savetxt('./ConversionsFolder/data_'+filename+'.dat',histoData,delimiter='\t',fmt='%1i')
elapsed = time.time()-t
print('Finished. Time taken: ' + str(elapsed) + 's')