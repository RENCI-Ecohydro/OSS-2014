# Get raw site data availability info
# 
# Input:
# sitesID csv file (just make sure the first column is site id, other columns will be ignored)
#
# Output:
# discharge_sites: sites that have daily discharge value 
# water_sample_sites: sites that have water nitrate sample value 
# data_availability_error_sites: sites that can't successfuly call getDataAvailability function

library(dataRetrieval)

# load sites 
sites <- read.table('filtered_watersheds.csv', header=TRUE, sep=',',colClasses=c("character","Date"))


# check sites availability
discharge_sites <- data.frame(siteID=c(),startDate=c(),endDate=c(),count=c())
water_sample_sites <- data.frame(siteID=c(),startDate=c(),endDate=c(),count=c())
data_availability_error_sites <- data.frame(siteID=c(),message=c())

for (i in seq(nrow(sites))){
  site_id <- site_id <- sites[i,1]
  
  result <- tryCatch({
    data_availability <- getDataAvailability(site_id)
  },warning = function(w){
    return(w)
  },error = function(e){
    return(e)
  })   
  
  if(inherits(result,"error")|inherits(result,"warning")) {    
    site_error <- data.frame(siteID=site_id, message=result$message[1])
    data_availability_error_sites <- rbind(data_availability_error_sites,site_error)
    next
  }
  
  discharge_info <- subset(data_availability, (statCd == '00003')&(parameter_cd == '00060'))
  quality_info <- subset(data_availability, parameter_cd == '00618')
  
  if (nrow(discharge_info)==1){
    site_discharge_info <- data.frame(siteID=site_id, startDate=discharge_info[['startDate']][1], 
                            endDate=discharge_info[['endDate']][1],count=discharge_info[['count']][1]) 
    discharge_sites <- rbind(discharge_sites,site_discharge_info)
  }
  
  
  if (nrow(quality_info)==1){
    site_sample_info <- data.frame(siteID=site_id, startDate=quality_info[['startDate']][1], 
                            endDate=quality_info[['endDate']][1],count=quality_info[['count']][1]) 
    water_sample_sites <- rbind(water_sample_sites,site_sample_info)
  }
  
}


# save results
save(discharge_sites,file="discharge_sites.Rdat")
save(water_sample_sites,file="water_sample_sites.Rdat")
save(data_availability_error_sites,file="data_availability_error_sites.Rdat")