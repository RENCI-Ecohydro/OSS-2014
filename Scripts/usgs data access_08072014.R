## R code to get the water quantity and quality data from USGS 
#
# User Input: 
# WATER_SAMPLE_SIZE, YEARS_BEFORE_DISTURBANCE, YEARS_AFTER_DISTURBANCE (set this in this code file see below)
# site_disturbance_data.csv (put this file in the same folder with this code)
#
# Output:
# available_sites.Rdat, unavailable_sites.Rdat
# site_meta.Rdat
# daily_discharge.Rdat, water_quality.Rdat
# 
# Utility r code: checkSite.r (just put this file in the same folder with this code )

#install dataRetrieval
#install.packages("dataRetrieval", 
#repos=c("http://usgs-r.github.com","http://cran.us.r-project.org"),
#dependencies=TRUE,
#type="both")
# load library

library(dataRetrieval)
source('checkSite_08072014.r')


# User Input:
WATER_SAMPLE_SIZE <- 10
YEARS_BEFORE_DISTURBANCE <- 2
YEARS_AFTER_DISTURBANCE <- 1

# read sitesID  
sites <- read.table('site_disturbance_data.csv', header=TRUE, sep=',',colClasses=c("character"))

# set the data frames to store the downloaded data
available_sites <- data.frame(siteID=c())
unavailable_sites <- data.frame(siteID=c(),info=c())
daily_discharge <- data.frame()
water_quality <- data.frame()
site_meta <- data.frame()
daily_discharge_quantiles <- data.frame()
error_sites <- data.frame()

# check data availability
for (i in seq(nrow(sites))){
  site_id <- sites[i,1]
  dis_date <- as.Date(sites[i,2])
  START_DATE <- as.POSIXlt(dis_date)
  START_DATE$year <- (START_DATE$year-YEARS_BEFORE_DISTURBANCE) 
  START_DATE <- as.Date(START_DATE)
  END_DATE <- as.POSIXlt(dis_date)
  END_DATE$year <- (END_DATE$year+YEARS_AFTER_DISTURBANCE) 
  END_DATE <- as.Date(END_DATE)
  
  check_info <- check_site_availability(site_id,START_DATE,END_DATE,WATER_SAMPLE_SIZE)
  if ( check_info == 'available site') {
    new_site <- data.frame(siteID=site_id,startDate=START_DATE,endDate=END_DATE,disDate=dis_date)
    available_sites  <- rbind(available_sites,new_site)   
       
  } else {
    new_site <- data.frame(siteID=site_id,info=check_info,startDate=START_DATE,endDate=END_DATE,disDate=dis_date)
    unavailable_sites <- rbind(unavailable_sites,new_site)
  }
}
save(available_sites,file="available_sites.Rdat")
save(unavailable_sites, file='unavailable_sites.Rdat')


## The following 3 sections can be run separately
# download site meta info and write to .Rdat file
for (i in seq(nrow(available_sites))){
  site_id <- available_sites[i,1]
  site_info <- getSiteFileData(as.character(site_id)) 
  site_meta <- rbind(site_meta,site_info)  
} 
save(site_meta,file="site_meta.Rdat")

# download discharge daily mean discharge and write to .Rdat file
for (i in seq(nrow(available_sites))){  
  site_id <- as.character(available_sites[i,1])
  START_DATE <- as.character(available_sites[i,2])
  END_DATE <- as.character(available_sites[i,3])
  try_site <- tryCatch(
		getDVData(site_id,'00060',START_DATE,END_DATE,convert=TRUE),# if convert=True unit will be cms
		error=function(e)
			{message(paste("site does not seem to exist:", site_id))
			# Choose a return value in case of error
			return(e)})
  if(inherits(try_site, "error")) 	
	{
	error_sites<- rbind(error_sites, site_id)
	next
	}	# if there is an error in try site, skip
  site_discharge <- getDVData(site_id,'00060',START_DATE,END_DATE,convert=TRUE)# if convert=True unit will be cms 
  siteID <- data.frame(siteID=rep(site_id,nrow(site_discharge)))
  daily_discharge <- rbind(daily_discharge,cbind(siteID,site_discharge)) 
  message(paste("Processed site:", site_id))}
save(daily_discharge,file="daily_discharge.Rdat")

#commented out water quality extraction due to time constraint @Tony 08072014
# download quality data and write to .Rdat file
#for (i in seq(nrow(available_sites))){  
#  site_id <- as.character(available_sites[i,1])
#  START_DATE <- as.character(available_sites[i,2])
#  END_DATE <- as.character(available_sites[i,3])
#  site_water_quality <- getSampleData(site_id,"00618",START_DATE,END_DATE)
#  siteID <- data.frame(siteID=rep(site_id,nrow(site_water_quality)))
#  water_quality <- rbind(water_quality,cbind(siteID,site_water_quality))
#}
#save(water_quality,file="water_quality.Rdat")





