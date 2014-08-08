'''
Author: Tony Chang
Title: Forest cover change preanalysis
Dependencies: Python
Date: July 29 2014
Abstract: 
1. Creates a histogram of the years of forest cover loss
2. Creates a time series of % forest cover loss over time 
3. Sub-divides this regionally by HUC-2 distinctions

'''

import numpy as np
from matplotlib import pyplot as plt
import gdal

'''
class FC_Tiles:
	def __init__(self, varname):
		self.varname
		self.dataArray #This is the deck of data arrays for each band
	def fillArray():
		latlist = np.arange(30,60,10)
		lonlist = np.arange(70,140,10)
		workspace = "C:\\Users\\tony\\OSS\\Project\\data\\Hansen\\"
		vname = "%s\\%s\\%s_%sN_%sW.tif" %(workspace,varname,varname,str(lat),str(lon))
'''	
#---------------------------------------------------------------
workspace = "C:\\Users\\tony\\OSS\\Project\\data\\Hansen\\"
varname = "lossyear"
icount = np.arange(1,13)
c = np.zeros(13)
c_by_tile = []
#mosaic = 'lossyear\\lossyear_mosaic.tif'
latlist = np.arange(30,60,10)
lonlist = np.arange(70,140,10)
for lat in latlist:
	for lon in lonlist:
		temp = np.zeros(13)
		strlat = str(lat)
		if lon<100:
			strlon = '0'+str(lon)
		else:
			strlon = str(lon)
		fname = "%s\\%s\\%s_%sN_%sW.tif" %(workspace,varname,varname,strlat,strlon)
		tile = (gdal.Open(fname)).ReadAsArray()
		for i in icount:
			temp[i] += len(np.where(tile==i)[0])
			c[i] += temp[i]
		gdal.Close(fname)
		c_by_tile.append(temp[i])
mosaic = 'lossyear\\lossyear_040N_110W.tif'
fname = '%s%s' %(workspace, mosaic)

ly = (gdal.Open(fname)).ReadAsArray()

filtered_ly = ly[np.where(ly!=0)]

plt.bar(icount-1, c)

plt.hist(filtered_ly, bins = 12)

#---------------------------------------------------------------
#now find the total loss by forest cover percentage
loss = 'loss\\loss_mosaic.tif'
lname = '%s%s' %(workspace, loss)

lmask = (gdal.Open(lname)).ReadAsArray()

#over lay the lossmask over the forestcover2000 mosaic
fc = 'forestcover2000\\forestcover2000.tif'
