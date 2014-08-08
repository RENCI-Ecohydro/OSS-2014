#geotool
#author: Tony Chang
#abstract: This script is a set of commonly used tools for extracting raster data to shapes
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

def getFeatureExtent(pnts):
	xmin = np.min(pnts[0])
	ymin = np.min(pnts[1])
	xmax = np.max(pnts[0])
	ymax = np.max(pnts[1])
	out = [xmin,ymin,xmax,ymax]
	#extent = source_layer.GetExtent() #use this to reference which tile will be used to gather data from
	#print(fextent) 
	return(out)
	
def getPoints(poly):
	poly.DumpReadable()
	# dump the data, just to check the first time we look at it
	geom = poly.GetGeometryRef()
	pts = geom.GetGeometryRef(0)
	points = []
	for p in range(pts.GetPointCount()):
		points.append((pts.GetX(p), pts.GetY(p))) #this picks up all the vertices for the n-th feature
	pnts = np.array(points).transpose() #make it a column array
	#print(points[:10]) #print the first ten points to check
	return(pnts)

def worldToPixel(geoMatrix, x, y):
	"""
	Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
	the pixel location of a geospatial coordinate
	"""
	ulX = geoMatrix[0]
	ulY = geoMatrix[3]
	xDist = geoMatrix[1]
	yDist = geoMatrix[5]
	rtnX = geoMatrix[2]
	rtnY = geoMatrix[4]
	pixel = np.round((x - ulX) / xDist).astype(np.int)
	line = np.round((ulY - y) / xDist).astype(np.int)
	return (pixel, line)

def imageToArray(i):
# This function will convert the rasterized clipper shapefile
# to a mask for use within GDAL.
    """
    Converts a Python Imaging Library array to a
    numpy array.
    """
    a=np.fromstring(i.tostring(),'b')
    a.shape=i.im.size[1], i.im.size[0]
    return(a)

def transformProj(swkt, rwkt, poly):
	oSRS = osr.SpatialReference ()
	oSRSop = osr.SpatialReference()
	oSRSop.ImportFromWkt(rwkt)
	# wkt from above, is the wicket from the shapefile
	oSRS.ImportFromWkt(swkt)
	# now make sure we have the shapefile geom
	geom = poly.GetGeometryRef()
	pts = geom.GetGeometryRef(0)
	# pts is the polygon of interest
	pts.AssignSpatialReference(oSRS)
	# so transform it to the MODIS geometry
	pts.TransformTo(oSRSop)
	# extract and plot the transformed data
	points = []
	for p in range(pts.GetPointCount()):
		points.append((pts.GetX(p), pts.GetY(p)))
	pnts = np.array(points).transpose()
	return(pnts)

def rasterizer(pnts,raster):
	geo_t = raster.GetGeoTransform()
	pixel, line = worldToPixel(geo_t,pnts[0],pnts[1])
	rasterPoly = Image.new("L", (raster.RasterXSize, raster.RasterYSize),1)
	rasterize = ImageDraw.Draw(rasterPoly)
	listdata = [(pixel[i],line[i]) for i in range(len(pixel))]
	rasterize.polygon(listdata,0)
	mask = 1 - imageToArray(rasterPoly)
	return(mask)

def subsetByMask(mask, fullset):
	#subset the raster 
	#cut the raster to a smaller extent to perform mask analysis...
	aoa_region = np.where(mask == 1)
	minxi = np.min(aoa_region[0])
	minyi = np.min(aoa_region[1])
	maxxi = np.max(aoa_region[0])
	maxyi = np.max(aoa_region[1])
	return(fullset[minxi:maxxi,minyi:maxyi])