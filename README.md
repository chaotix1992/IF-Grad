# Fluorescent image gradient converter
The purpose of this repository is to take an immunofluorescent picture and convert the intensity of the color to a pre-defined spectrum.

## Prerequisites
The Python script has been written in Python 3.8.6. The files `recolor_rb.py` and `histo.py` require the following Python modules for execution:
- [Pillow](https://github.com/python-pillow/Pillow)
- [matplotlib](https://github.com/matplotlib/matplotlib)
- [colour](https://github.com/vaab/colour)

## How to use `recolor_rb.py`
Navigate to the folder you saved the file in. Open the terminal in this folder (Windows: Right-click -> Open Terminal here, sometimes also referred to as PowerShell). Type "python recolor_rb.py". The script will now ask you for the base color of your picture, that you want to measure the intensity of. Type "r" for red, "g" for green, "b" for blue or "gray" for gray and confirm with Enter. The script will then ask you if you want to convert a single file or an entire folder. Type "s" for a single fil or "f" for folder and confirm with Enter. Now enter the file name. You will be prompted to add more files (type "y") or convert (type "n"). The script should now create a new folder, called Conversions and store the converted file there.
