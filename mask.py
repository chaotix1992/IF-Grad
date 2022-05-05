"""
Created on Fri Apr 22 14:00:00 2022

@author: Julian Happel
"""

from PIL import Image, ImageOps
from matplotlib import cm
from colour import Color
import numpy as np
import time
import os

files = []
pathCorrect = False
w = False
x = False
y = False
z = False

# Script to transform any IF picture into a desired mask
# First step is to introduce to the user

print("Welcome to mask.py!")

# Let the user input a filename
while not w:
    folFil = str(input("Do you want to add single files or a folder? (s/f) "))
    if folFil == "s":
        addMore = "y"
        while addMore == "y":
            files.append(str(input("Please input the desired filename of the file you want to create a mask of, including file extension: ")))
            # Check if file exists, if so, save it to the img variable, otherwise ask again
            try:
                img = Image.open(files[-1])
            except:
                print("Filename either incorrect or file does not exist.")
                continue
            addMore = str(input("Add more files? (y/n) "))
    elif folFil == "f":
        while not pathCorrect:
            path = str(input("Enter folder path (syntax: C:\\files\\myFolder\\): "))
            try:
                files = os.listdir(path)
            except:
                print("Folder does not exist or path is incorrect.")
                continue
            pathCorrect = True
    else:
        print("Invalid input.")
        continue
    w = True

# Let user choose the base color of the picture
while not x:
    filterColor = str(input("Please input the filter color (r, g, b): "))
    if filterColor == "r" or filterColor == "red":
        filterColor = 1
    elif filterColor == "g" or filterColor == "green":
        filterColor = 2
    elif filterColor == "b" or filterColor == "blue":
        filterColor = 3
    else:
        print("Please input a valid base color.")
        continue
    x = True

# Let user input the lower bounds of the mask

while not y:
    startValue = str(input("Minimum color intensity? (0-255) "))
    # Catch case if given no input
    if startValue == '':
        startValue = 0
    # Checks if input is actually a number
    elif startValue.isnumeric():
        startValue = int(startValue)
        # Check if number is smaller than 256
        if startValue > 255:
            print('Please input a number between 0 and 255')
            continue
    # Catch case if input isn't a number
    else:
        print('Please input a number between 0 and 255')
        continue
    y = True

# Let the user input the mask color

while not z:
    maskColor = str(input("Please input your desired mask color (red, green, blue, black): "))
    if maskColor == "red" or maskColor == "r":
        maskColor = (255, 0, 0)
        print("Thank you. Starting to work now...")
        t = time.time()
    elif maskColor == "green" or maskColor == "g":
        maskColor = (0, 255, 0)
        print("Thank you. Starting to work now...")
        t = time.time()
    elif maskColor == "blue" or maskColor == "b":
        maskColor = (0, 0, 255)
        print("Thank you. Starting to work now...")
        t = time.time()
    elif maskColor == "black":
        maskColor = (0, 0, 0)
        print("Thank you. Starting to work now...")
        t = time.time()
    else:
        print("Please input a valid color for the mask.")
        continue
    white = (255, 255, 255)
    z = True

if folFil == "s":
    for fileName in files:
        img = Image.open(fileName)

        img = img.convert("RGB")
        data = img.getdata()

        newImageData = []
        
        for entry in data:
            if entry[filterColor-1] < startValue:
                newImageData.append(white)
            else: 
                newImageData.append(maskColor)
        
        img.putdata(newImageData)
        img.save('./Masks/masked_'+fileName,'TIFF')
else:
    for fileName in files:
        img = Image.open(path + fileName)

        img = img.convert("RGB")
        data = img.getdata()

        newImageData = []
        
        for entry in data:
            if entry[filterColor-1] < startValue:
                newImageData.append(white)
            else: 
                newImageData.append(maskColor)
        
        img.putdata(newImageData)
        img.save('./MasksFolder/masked_'+fileName,'TIFF')

elapsed = time.time()-t
print("Finished in "+str(elapsed)+"s.")