#web download of data
#author: Tony Chang
#abstract: This is a short script to automate the  download the Hansen et al #2013 Forest Cover Change dataset from Google Earth Engine url. 
#date: 07.23.2014
#organization: OSS 2014 
#location: RENCI, Chapel Hill, NC
#written for Python 3.3

import urllib
import numpy as np
from matplotlib import pyplot as plt

import gdal 
from gdalconst import *
import osr
import os

def get_url(var, ulc): #need to specify the variable and the upper left corner 
	workspace = 'http://commondatastorage.googleapis.com/earthenginepartners-hansen/GFC2013/Hansen_GFC2013_'
	filename = "%s_%s.tif" %(var,ulc)
	url = "%s%s" %(workspace,filename)
	return(url,filename)

def gen_ulc(lat,lon):
	if (lon<100):
		slon = '0'+ str(lon)
	else:
		slon = str(lon)
	slat = str(lat)
	out = "%sN_%sW" %(slat,slon)
	return(out)

if __name__ == "__main__":
	variable_names = np.array(['treecover2000','loss', 'gain', 'lossyear', 'datamask', 'first', 'last']) #finished these variables 07.23.14
	localworkspace = 'C://Users/tony/OSS/Project/data/Hansen/' #change this workspace to your specific drive that you desire
	latlist = np.arange(30,60,10) #minor changes to make...modified 07.23.14
	lonlist = np.arange(70,140,10)
	for var in variable_names:
		for lat in latlist:
			for lon in lonlist:
				ulc = gen_ulc(lat,lon)
				f_url,fname = get_url(var,ulc)
				print('Opening %s\n' %f_url) #if using Python 2.7 comment out this line,  or remove the '()' parentheses with "" quotes
				local_file = "%s%s/%s" %(localworkspace,var,fname)
				try:
					os.stat(localworkspace+var) #check if the directory exists
				except:
					os.mkdir(localworkspace+var) #if not create directory
				response = urllib.request.urlretrieve(f_url,local_file)
				print('Completed copying %s\n' %f_url)

# to do:
# generate a log file to note how much has been downloaded and how much is left
# to download...
'''
#check
test = gdal.Open(local_file).ReadAsArray()
plt.imshow(test) 
plt.colorbar()
plt.show()
'''