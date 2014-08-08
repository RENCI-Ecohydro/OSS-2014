#:set fileformat=unix
#!bin/bash
#this requires the python wrapper for gdal to execute. 
/c/python33/python.exe /c/users/tony/OSS/Project/scripts/Utilities/gdal_merge.py -o $1.tif $2 -ot Byte
#1st argument is the path to python, 
#2nd is the path to gdal_merge.py library, 
#3rd is the output file name, 
#4 I typically write "*.tif" to merge all tif files within the directory
