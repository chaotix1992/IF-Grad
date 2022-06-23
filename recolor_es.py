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

print("Bienvenido a IF-Grad. Un conversor de gradiente para imagen de inmunofluorescencia.")

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
    basis = str(input('¿Color de base? (r = rojo/g = verde/b = azul/gray = gris) '))
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
        print('Entrada inválida')

# Ask for file names or folder
while not y:
    folFil = str(input("¿Quiere añadir archivos de forma individual o una carpeta? (s = archivo, f = carpeta) "))
    if folFil == 's':
        addMore = 'y'
        while addMore == 'y':
            files.append(str(input('Introduzca el nombre del archivo: ')))
            try:
                img = Image.open(files[-1])
            except: 
                print("Nombre de archivo incorrecto o el archivo no existe.")
                continue
            addMore = input('¿Añadir más archivos? (y = sí, n = no) ')
        y = True
    elif folFil == 'f':
        path = str(input('Introduzca la dirección de la ubicación de la carpeta (syntax: C:\\files\\myFolder\\): '))
        try:
            files = os.listdir(path)
        except:
            print("Ruta a la carpeta incorrecta o la carpeta indicada no existe.")
            continue
        y = True
    else:
        print('Entrada inválida')

# Asking if data should be saved to files
while not w:
    answer = str(input('¿Quiere guardar los datos de los valores de la imagen? (y = sí/n = no) '))
    if answer == 'y':
        histo = True
        w = True
        histoData = np.array([np.arange(0,256,1),np.zeros(256)],np.int32)
    elif answer == 'n':
        histo = False
        w = True
    else:
        print("Por favor, introduzca una respuesta válida.")


# Asking for starting intensity value
while not z:
    startValue = str(input("¿Cuál es el valor mínimo de la escala de intensidad? (0-255) "))
    if startValue == '':
        startValue = 0
    elif startValue.isnumeric():
        startValue = int(startValue)
        if startValue > 255:
            print('Por favor, introduzca un número entre 0 y 255')
            continue
    else:
        print('Por favor, introduzca un número entre 0 y 255')
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
print('Fin. Tiempo: ' + str(elapsed) + 's')