# Fluorescent image gradient converter
The purpose of this repository is to take an immunofluorescent picture and convert the intensity of the color to a pre-defined spectrum.

<img src="https://github.com/chaotix1992/IF-Grad/blob/main/GDp.png" width="300" height="300"> <img src="https://github.com/chaotix1992/IF-Grad/blob/main/converted_GDp.png" width="300" height="300"> <img src="https://github.com/chaotix1992/IF-Grad/blob/main/masked_GDp.png" width="300" height="300">

## Prerequisites
The Python script has been written in Python 3.8.6. The files `recolor_rb.py` and `mask.py` require the following Python modules for execution:
- [Pillow](https://github.com/python-pillow/Pillow)
- [matplotlib](https://github.com/matplotlib/matplotlib)
- [colour](https://github.com/vaab/colour)

## How to use `recolor_rb.py`
Before using `recolor_rb.py`, please make sure to have a folder called "Conversions" and "ConversionsFolder" in the same directory as `recolor_rb.py`.
Navigate to the folder you saved the file in. Open the terminal in this folder (Windows: Right-click -> Open Terminal here, sometimes also referred to as PowerShell). Type "python recolor_rb.py". The script will now ask you a series of questions for your preferences.

## How to use `mask.py`
Before using `mask.py`, please make sure to have a folder called "Masks" and "MasksFolder" in the same directory as `mask.py`. Navigate to the folder you saved the file in. Open the terminal in this folder (Windows: Right-click -> Open Terminal here, sometimes also referred to as PowerShell). Type "python mask.py". The script will now ask you a series of questions for your preferences.
