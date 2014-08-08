#tile preprocessing
#author: Tony Chang
#abstract: This is a short script to automate a log file that describes the extent of each tile for referencing in later extraction of data with shapefiles
#date: 08.05.2014
#organization: OSS 2014 
#location: RENCI, Chapel Hill, NC
#written for Python 3.3

import numpy as np
from matplotlib import pyplot as plt
import gdal
import csv

def genExtent(gt,size):
	minx = gt[0]
	miny = gt[3]+gt[5]*size[1]
	maxx = gt[0]+gt[1]*size[0]
	maxy = gt[3]
	return([minx,miny,maxx,maxy])

def formatData(data):
	return([data[0],data[3][0],data[3][1],data[3][2],data[3][3],data[1][1],
			data[2][0],data[2][1]])
			
def writeCSV(data,outname):
	myfile = open(outname, 'w', newline='')
	wr = csv.writer(myfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	wr.writerows(header)
	for i in range(len(data)):
		wr.writerow(formatData(data[i]))
	myfile.close()
	return()

if __name__ == "__main__":
	localworkspace = 'C://Users/tony/OSS/Project/data/Hansen/' #change this workspace to your specific drive that you desire
	latlist = np.arange(30,60,10) 
	lonlist = np.arange(70,140,10)
	var = 'loss' # use the loss data as a reference
	data = []
	
	for lat in latlist:
		for lon in lonlist:
			if lon<100:
				strlon = '0' + str(lon)
			else:
				strlon = str(lon)
			strlat = str(lat)
			local_file = "%s%s/%s_%sN_%sW.tif" %(localworkspace,var,var,strlat,strlon)
			print(local_file)
			temp = gdal.Open(local_file)
			gt = temp.GetGeoTransform()
			size = np.shape(temp.ReadAsArray())
			extent = genExtent(gt, size)
			data.append([local_file,gt,size, extent])
	writeCSV(data,'tile_extents.csv')