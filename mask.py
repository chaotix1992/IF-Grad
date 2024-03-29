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
            buffer = str(input("Please input the desired filename of the file you want to create a mask of, including file extension: "))
            # Check if file exists, if so, save it to the img variable, otherwise ask again
            try:
                img = Image.open(buffer)
            except:
                print("Filename either incorrect or file does not exist.")
                continue
            files.append(buffer)
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

print("Thank you. Starting to work now...")
t = time.time()
white = (255, 255, 255)
maskColor = (0, 0, 0)

if folFil == "s":
    for fileName in files:
        img = Image.open(fileName)

        img = img.convert("RGB")
        data = img.getdata()

        newImageData = []
        totalPixels = 0
        positivePixels = 0
        for entry in data:
            totalPixels += 1
            if entry[filterColor-1] <= startValue:
                newImageData.append(white)
            else: 
                newImageData.append(maskColor)
                positivePixels += 1
        
        img.putdata(newImageData)
        img.save('./Masks/masked_'+fileName,'TIFF')
        positivePercentage = positivePixels / totalPixels * 100
        print(f"Finished masking {fileName}. Total Pixels: {totalPixels}; Positive Pixels: {positivePixels}; Percentage: {positivePercentage:.2f}%\n")
else:
    for fileName in files:
        img = Image.open(path + fileName)

        img = img.convert("RGB")
        data = img.getdata()

        newImageData = []
        
        totalPixels = 0
        positivePixels = 0
        for entry in data:
            totalPixels += 1
            if entry[filterColor-1] <= startValue:
                newImageData.append(white)
            else: 
                newImageData.append(maskColor)
                positivePixels += 1
        
        img.putdata(newImageData)
        img.save('./MasksFolder/masked_'+fileName,'TIFF')
        
        positivePercentage = positivePixels / totalPixels * 100
        print(f"Finished masking {fileName}. Total Pixels: {totalPixels}; Positive Pixels: {positivePixels}; Percentage: {positivePercentage:.2f}%\n")

elapsed = time.time()-t
print("Finished in "+str(elapsed)+"s.")
