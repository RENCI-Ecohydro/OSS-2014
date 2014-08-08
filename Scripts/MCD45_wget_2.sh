#!/bin/bash

## This script downloads monthly MCD45 modis landfire data from Modis-fire.umd.edu lab page
## if mac does not have wget, use http://osxdaily.com/2012/05/22/install-wget-mac-os-x/ to activate


## Define years to download MCD45 fire data

YEAR="
2000
2001
2002
2003
2004
2005
2006
2007
2008
2009
2010
2011
2012
2013
2014"

## Use wget to grab data from FTP. User and Password most be defined to access page
## User = 'user' Password = 'burnt_data'
## -nc tells wget to not grab anything that is already downloaded

for YR in $YEAR; do
BASE_URL="ftp://ba1.geog.umd.edu/Collection51/TIFF/Win03/${YR}";
	wget -nc --ftp-user=user --ftp-password=burnt_data "${BASE_URL}/*.gz";
done


## decompress .gz files using gzip
## -d to decompress -k to keep the original files

gzip -dk *.gz

## merge files by year

for YR in $YEAR; do
	gdal_merge.py -o MCD45yr_${YR}_burndate_2.img -of 'HFA' -a_nodata '-32768' -n '900' -n '9998' -n '9999' -n '10000'  MCD45monthly.A${YR}???.Win03.051.burndate.tif;
done



