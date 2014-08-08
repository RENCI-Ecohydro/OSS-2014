#shape_extract
#author: Tony Chang
#abstract: This script takes the HUC shapefiles and extracts underlying rasters for analysis
#date: 08.05.2014
#organization: OSS 2014 
#location: RENCI, Chapel Hill, NC
#written for Python 3.3

import numpy as np
from matplotlib import pyplot as plt
from osgeo import gdal, osr
from osgeo import ogr
import pandas as pd
from PIL import Image, ImageDraw
import subprocess
import geotool

#========================================================================================
#==========================Functions=====================================================
#========================================================================================

def getFeatureExtent(pnts):
	xmin = np.min(pnts[0])
	ymin = np.min(pnts[1])
	xmax = np.max(pnts[0])
	ymax = np.max(pnts[1])
	out = [xmin,ymin,xmax,ymax]
	#extent = source_layer.GetExtent() #use this to reference which tile will be used to gather data from
	#print(fextent) 
	return(out)
	
def findSource(extent,var):
	logfile = 'C://Users/tony/OSS/Git/OSS-2014-Project/Scripts/tile_extents_%s.csv' %(var) 
	log = pd.io.parsers.read_csv(logfile)
	sxmin = extent[0]
	symin = extent[1]
	sxmax = extent[2]
	symax = extent[3]
	filter_ul = log[(log[' minX']<sxmin) & (log[' maxX']>sxmin) & (log[' minY']<symin) & (log[' maxY']>symin)]
	filter_lr = log[(log[' minX']<sxmax) & (log[' maxX']>sxmax) & (log[' minY']<symax) & (log[' maxY']>symax)]
	filter_ur = log[(log[' minX']<sxmin) & (log[' maxX']>sxmin) & (log[' minY']<symax) & (log[' maxY']>symax)]
	filter_ll = log[(log[' minX']<sxmax) & (log[' maxX']>sxmax) & (log[' minY']<symin) & (log[' maxY']>symin)]
	f_ul = str(filter_ul['filename'].iloc[0])
	f_lr = str(filter_lr['filename'].iloc[0])
	f_ur = str(filter_ur['filename'].iloc[0])
	f_ll = str(filter_ll['filename'].iloc[0])
	if (f_ul == f_lr): #upper corner matches lower corner
		fname_list = np.array([f_ul])
	elif ((f_lr != f_ll) and (f_ul != f_ur)): #4 tile case
		fname_list = np.array([f_ul, f_lr, f_ur, f_ll])
	else: #2 tile case
		if (f_ul == f_ur): #left-right case
			fname_list = np.array([f_ul, f_ur])
		else: #up-down case
			fname_list = np.array([f_ul, f_ll])
	return(fname_list)
		
def forestLossByYear(year_loss, tc_values):
	#pixelsize = 30*30
	lossByYearArray = []
	nyears = 13
	min_tc = 90 #minimum amount to consider as forested
	total_tc = len(tc_values[tc_values>=min_tc])
	for i in range(1,nyears):
		losses = (tc_values[year_loss==i])
		#filter only areas where tree cover is greater than 90%
		tc_losses = losses[losses>=min_tc]
		if total_tc == 0: #in case there is no forest in watershed
			lossByYearArray.append(0)
		else:
			lossByYearArray.append(len(tc_losses)/total_tc)
	return(lossByYearArray)

def cumlForestLoss(flby):
	cuml_array = []
	for i in range(len(flby)):
		cuml_array.append(np.sum(flby[:i+1]))
	return(np.array(cuml_array))

def reformatData(data):
	fullout = []
	for i in range(len(data)):
		out = []
		out.append(data[i][0])
		for j in range(len(data[i][1])):
			out.append(data[i][1][j])
		for k in range(len(data[i][2])):
			out.append(data[i][2][k])
		fullout.append(out)
	colnames = ['huc']
	for year in range(2001,2013):
		colnames.append(str(year)+'_loss')
	for year in range(2001,2013):
		colnames.append(str(year)+'_closs')
	return(pandas.DataFrame(fullout, columns = colnames))

#========================================================================================
#========================================================================================
#========================================================================================

#to figure out
#write data out as a csv
#figure out why data failed at n=845 #divide by zero error
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
	for n in range(total_n):#total_n): #note error occurred in n=187!
		poly = source_layer.GetFeature(n) #look up record n (based on the id)
		g_id = poly.GetField("GAGE_ID")
		pnts = getPoints(poly)
		fextent = getFeatureExtent(pnts)
		var = 'lossyear' #first consider the loss year
		fname_lossyear = findSource(fextent,var) #look for the correct raster file to use
		if (len(fname_lossyear) >1):
			
			#fname_new = rasterMerge(fname_lossyear,n)
			#def rasterMerge(fname_list,n):
			#	#generate a new raster from the fname list
			#	gdalmerge_cmd ='c:\\python33\\python.exe 'c:\\users\tony\OSS\Project\scripts\Utilities\gdal_merge.py'
			#	outfile = 'C:\\Users\tony\OSS\Project\data\temp\temp_raster_%s.tif' %(str(n))
			#	subprocess([gdalmerge_cmd, fname_list[0], fname_list[1], '-o', outfile])
			#	return(outfile)
			#raster = gdal.Open(fname_new)	
			
			#for r in range(len(fname_lossyear)):
			#skip boundary watershed for now.....	
			
		#======Open up the raster...
			continue
		raster = gdal.Open(fname_lossyear[0])
		fcWKT = raster.GetProjectionRef() # get the raster wicket (the projection information)

		#======This step can be ignored since the shapefile and raster are in the same projection..
		pnts_T = transformProj(wkt, fcWKT, poly) #transforms the shape to match the raster
		mask = rasterizer(pnts, raster) #rasterize the points

		r_array = raster.ReadAsArray()
		raster_sub = subsetByMask(mask,r_array)
		mask_sub = subsetByMask(mask,mask)
		
		#now pull information for that watershed
		#find where mask equals 1 and pull information from the raster
		mask_i = np.where(mask_sub == 1)
		year_loss = raster_sub[mask_i]
		
		#now look at tree cover 2000
		var = 'treecover2000'
		fname_tcover = findSource(fextent,var)
		tc_raster = (gdal.Open(fname_tcover[0])).ReadAsArray()
		tc_sub = subsetByMask(mask,tc_raster)
		tc_values = tc_sub[mask_i]
		counts,bins = np.histogram(tc_values)
		saved = [g_id, np.sum(counts)]
		for i in counts:
			saved.append(i)
		watershed_summary.append(saved)
		#flby = forestLossByYear(year_loss,tc_values)
		#cuml_loss = cumlForestLoss(flby)
		#watershed_summary.append([g_id,flby,cuml_loss])
		print('%s'%str(n))
	#export results
	cols = ['huc', 'total_pixels']
	for i in range(0,100, 10):
		cols.append(str(i)+'-'+str(i+10))
	out = pd.DataFrame(watershed_summary, columns = cols)
	out.to_csv(path_or_buf='c://users/tony/OSS/Project/watershed_treecover3.csv', sep = ',', na_rep=-9999)
	#out = reformatData(watershed_summary)
	#out.to_csv(path_or_buf='c://users/tony/OSS/Project/watershed_summary.csv', sep = ',', na_rep=-9999)
	
