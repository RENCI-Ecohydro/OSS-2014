"""
Author: Tony Chang
Date: July 29 2014
Abstract: Opens the USGS gauge station shapefile and 
then queries the database and writes the results in csv
Depends: numpy, osgeo
"""
from osgeo import ogr
import osgeo
import numpy as np

if __name__ == "__main__":
	workspace = "C:\\Users\\tony\\OSS\\Project\\data\\Streamgauges\\Shape\\"
	gauge_filename = "USGS_Streamgages-NHD_Locations.shp"
	fname = "%s%s" %(workspace, gauge_filename)

	driver = ogr.GetDriverByName("ESRI Shapefile")
	dataSource = driver.Open(fname, 0)
	gauge = dataSource.GetLayer()

	filter_condition = "DAYN >= 20030930" 
	#find stations who has a last station report date of sep-30 2003
	gauge.SetAttributeFilter(filter_condition)

	siteno = []
	for feature in gauge:
		siteno.append(feature.GetField("SITE_NO"))

	siteno = np.array(siteno)
	#write the output
	outputName = 'filter_gages_siteno.csv'
	ofile = "%s%s" %(workspace, outputName)
	np.savetxt(ofile, siteno, fmt = '%s8', delimiter=',')
