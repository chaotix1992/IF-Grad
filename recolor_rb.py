# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 09:20:23 2021

@author: Julion
"""

from PIL import Image, ImageOps
from matplotlib import cm
from colour import Color
import os

# Prepare lists and bool
files = []
colors = []
x = False
y = False
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


black = Color("#000000")
deepblue1 = Color("#000033")
deepblue2 = Color("#000034")
darkerblue1 = Color("#000084")
darkerblue2 = Color("#000085")
darkblue1 = Color("#0000AB")
darkblue2 = Color("#0000AC")
blue = Color("#0001FF")
colorSteps = 16
black2deep = list(black.range_to(deepblue1,colorSteps))
deep2darker = list(deepblue2.range_to(darkerblue1,colorSteps))
darker2dark = list(darkerblue2.range_to(darkblue1,colorSteps))
dark2blue = list(darkblue2.range_to(blue,colorSteps))
blue2black = black2deep + deep2darker + darker2dark + dark2blue


# Takes 64 values from the previous transition and adds the rest of the color 
# map (from right to left)
for i in range(256):
    if i >= 256-4*colorSteps:    # Part for smooth transition
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
            addMore = input('Add more files? (y/n) ')
        y = True
    elif folFil == 'f':
        path = str(input('Enter folder path (syntax: C:\\files\\myFolder\\): '))
        files = os.listdir(path)
        y = True
    else:
        print('Invalid input!')

# Asign each pixel a new value from the prepared colors list, depending on 
# the intensity of a specified color
if folFil == 's':
    for filename in files:
        if basis < 3:
            img = Image.open(filename)
            
            img = img.convert("RGB")
            datas = img.getdata()
            
            new_img_data = []
            for item in datas:
                new_img_data.append(colors[item[basis]])
        else:
            img = Image.open(filename)        
            img = img.convert("RGB")
            gray = ImageOps.grayscale(img)
            datas = gray.getdata()
            
            new_img_data = []
            for item in datas:
                new_img_data.append(colors[item])
        
        img.putdata(new_img_data)
        
        img.save('./Conversions/converted_'+filename,'TIFF')
else:
    for filename in files:
        if basis < 3:
            img = Image.open(path + filename)
            
            img = img.convert("RGB")
            datas = img.getdata()
            
            new_img_data = []
            for item in datas:
                new_img_data.append(colors[item[basis]])
        else:
            img = Image.open(path + filename)        
            img = img.convert("RGB")
            gray = ImageOps.grayscale(img)
            datas = gray.getdata()
            
            new_img_data = []
            for item in datas:
                new_img_data.append(colors[item])
        
        img.putdata(new_img_data)
        
        img.save('./Conversions/converted_'+filename,'TIFF')