#Author: Tony Chang and John Lovette
#Date: July 31 2014
#Title: fire_preprocess.py
#Abstract: Takes monthly burn date data, denoted by julian date
# and aggregate into a single year
#Dependency: python 2.7+; gdal, osr, gdalconst, numpy

import numpy as np
from matplotlib import pyplot as plt
import gdal as gdal
from gdalconst import *
import osr


#====================================
#====================================
#====================================
def getFireData(name):
	monthly_fire = gdal.Open(filename)
	return(monthly_fire.ReadAsArray())

def correctData(data):
	return(np.where(data>=900,data*-1,data))

def reclassAnom(data):
	temparray = data
	original = [-10000,-9999,-9998,-900] # 900 snow/aerosol, 9998 inland water, 9999 sea/ocean,
											# 10000 not enough data for inversion through period
	to = [-4,-3,-2,-1]
	for i in range(len(original)):
		temparray = np.where(temparray==original[i],to[i],temparray)
	return(temparray)
	
def compressFireData(annual_fire):
	#some sorting routine to combine 12 months of fire data
	cum_fire = correctData(annual_fire[0])
	for i in range(1,len(annual_fire)):
		next_fire = correctData(annual_fire[i])
		cum_fire = np.where(next_fire>cum_fire,next_fire,cum_fire)
	return(cum_fire)#some merged data)

def getHeader():
	#function to retrieve the header data from the fire data layers
	ref_file = "/Users/jplovette/Desktop/MCD45/MCD45monthly.A2001335.Win03.051.burndate.tif" 
	dataset = gdal.Open(ref_file)
	ncols = dataset.RasterXSize
	nrows = dataset.RasterYSize
	bands = dataset.RasterCount
	driver = "GTIFF"
	geotransform = dataset.GetGeoTransform()
	header = [geotransform, driver, bands, ncols, nrows]
	return(header)
	
def writeFireTiff(annual_fire, workspace, year):
	#write the merged data into GTIFF format
	h = getHeader()
	fileformat = h[1]
	geotransform = h[0]
	nbands = h[2]
	nrows = h[-1]
	ncols = h[-2]
	outarray = reclassAnom(annual_fire)
	writename = workspace +'/MCD45yearly'+ str(year)+'.tif'
	ds = gdal.GetDriverByName(fileformat)
	srs = osr.SpatialReference()
	outDs = ds.Create(writename,ncols,nrows,nbands,gdal.GDT_Int32) 
	outDs.SetGeoTransform(geotransform)
	srs.SetWellKnownGeogCS("WGS84") #make sure this georeference is correct
	outDs.SetProjection(srs.ExportToWkt())
	outBand = outDs.GetRasterBand(nbands)
	outBand.SetNoDataValue(-32768)  #np.nan but only for float
	outBand.WriteArray(outarray,0,0)
	outDs = None
	print(writename + " filebuilt!\n")
	return()	

def findJulianDate(year):
	#given a year, return the julian dates for the start of each month
	leap_years = np.array([2000,2004,2008,2012])
	julian_day_array = []
	if (len(np.where(year == leap_years)[0]))==0: #find if is a leap year
		month_days = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
	else:
		month_days = np.array([31,29,31,30,31,30,31,31,30,31,30,31])
	for i in range(len(month_days)):
		julian_day_array.append(np.sum(month_days[:i])+1)
	return np.array(julian_day_array)

def threeDigitString(day):
	if len(str(day))==1:
		out = '00'+str(day)
	elif len(str(day))==2:
		out = '0'+str(day)
	else:
		out = str(day)
	return(out)


#====================================
#====================================
#====================================

if __name__=='__main__':
	workspace = "/Users/jplovette/Desktop/MCD45"
	first_year = 2000
	last_year = 2014
	year_array = np.arange(first_year,last_year+1)
	month_array = np.arange(1,13)
	
	fire_array = []

	for year in year_array:
		annual_fire = []
		jd_array = findJulianDate(year)
		for day in jd_array:
			#MCD45monthly.A2006091.Win03.051.burndate.tif 
			strday = threeDigitString(day)
			filename = workspace+ '/MCD45monthly.A'+str(year)+strday+'.Win03.051.burndate.tif'
			#print('opening ' + filename + '\n')
			try:
				monthly_fire = getFireData(filename)
				annual_fire.append(monthly_fire) #fire array created
			except AttributeError:
				#print(filename + "doen't exist! skipping it \n")
				continue
		merged_fire_data = compressFireData(annual_fire) #function to compress fire data
		writeFireTiff(merged_fire_data,workspace,year)
		fire_array.append(merged_fire_data) #store the compiled fire array


	
	


