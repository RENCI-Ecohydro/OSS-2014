import numpy as np
from matplotlib import pyplot as plt
from osgeo import gdal, osr
from osgeo import ogr
import pandas as pd
import geotool as geo
#========================================================================================
#==========================Functions=====================================================
#========================================================================================

def extractPRISMhead():
	workspace = "C://Users/tony/OSS/Project/data/PRISM/"
	year = 1982
	filenum = 1
	PRISMExtent = [-125.02083333333, 24.0625, -66.47916757, 49.9375]
	minx = AOA[0] 
	miny = AOA[1]
	maxx = AOA[2]
	maxy = AOA[3]
	filename = '%s/us_%s_%s.%s' %(workspace,var,var,year,month)
	
	readfile = open(filename, 'r')
	a = readfile.readline()
	temp = a.split()
	ncols = int(temp[1])        #Define number of columns
	a = readfile.readline()
	temp = a.split()
	nrows = int(temp[1])        #Define number of rows
	a = readfile.readline()
	temp = a.split()
	xllcorner = float(temp[1])  #Define xll corner
	a = readfile.readline()
	temp = a.split()
	yllcorner = float(temp[1])  #Define yll corner
	a = readfile.readline()
	temp = a.split()
	cellsize  = float(temp[1])  #Define cellsize
	a = readfile.readline()
	temp = a.split()
	NODATA_value  = temp[1]     #Define NoData value
	readfile.close()

	yulcorner = PRISMExtent[1]+(cellsize*nrows)

	xstart = int((AOA[0] - PRISMExtent[0])/cellsize)    #first x-extent index
	xend = xstart + int((AOA[2]-AOA[0])/cellsize)       #end x-extent index

	ystart = int((yulcorner - AOA[3])/cellsize)         #first y-extent index
	yend = ystart + int((AOA[3]-AOA[1])/cellsize)       # end of y-extent index

def extractPRISM(var, AOA):
	#extracts the prism data as a numpy array
	# variable of interest (tmax, tmin, ppt, tdmean)
	workspace = "C://Users/tony/OSS/Project/data/PRISM/"
	year = str(1982)
	month = '01'
	filename = '%s/%s/us_%s_%s.%s' %(workspace,var,var,year,month)
	readfile =  open(filename,'r')
	nhead = 6                   #First 6 lines of the header to be removed
	ncols = 1405
	nrows = 621
	cellsize = 0.04166667
	PRISMExtent = [-125.02083333333, 24.0625, -66.47916757, 49.9375]
	yulcorner = PRISMExtent[3]
	xstart = int((AOA[0] - PRISMExtent[0])/cellsize)    #first x-extent index
	xend = xstart + int((AOA[2]-AOA[0])/cellsize)       #end x-extent index
	ystart = int((yulcorner - AOA[3])/cellsize)         #first y-extent index
	yend = ystart + int((AOA[3]-AOA[1])/cellsize)       # end of y-extent index
	
	addmatrix = []
	for z in range(nhead):      #Strip out header
		a = readfile.readline()
	for y_pos in range(0, nrows+1):
		line = readfile.readline()
		datarow = line.split()
		if (y_pos >= ystart and y_pos <= yend):
		   newrow = datarow[xstart:(xend+1)]
		   addmatrix.append(newrow)
	newcols = len(addmatrix[0]) #define new column length
	newrows = len(addmatrix)    #define new row length
	newyulcorner = yulcorner - (ystart*cellsize)
	newxllcorner = PRISMExtent[0] + (xstart*cellsize)
	addmatrix = np.array(addmatrix).astype(np.float) #changes addmatrix list into array for statistical analysis
	return(addmatrix)

	
#===================================================
if __name__ == "__main__":
	shapeworkspace = 'C://Users/tony/OSS/Project/data/Basin_ref-2014-08-05/Basin_ref/'
	shapefile = 'CONUS_base_ref.shp' #using the huc8 for test file
	sname = '%s%s' %(shapeworkspace,shapefile)
	orig_data_source = ogr.Open(sname)
	source_ds = ogr.GetDriverByName("Memory").CopyDataSource(orig_data_source, "")
	source_layer = source_ds.GetLayer(0)
	source_srs = source_layer.GetSpatialRef()
	wkt = source_srs.ExportToWkt() #this is the full definition of the projection as a string
	total_n = source_layer.GetFeatureCount()
	watershed_summary = []
	for n in range(1):
		poly = source_layer.GetFeature(n) #look up record n (based on the id)
		g_id = poly.GetField("GAGE_ID")
		pnts = getPoints(poly)
		fextent = getFeatureExtent(pnts)
		var = 'ppt'
		pdata = extractPRISM(var, fextent)