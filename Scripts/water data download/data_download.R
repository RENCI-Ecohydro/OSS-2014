# Download discharge and water sample data
# 
# Input:
# discharge_sites.Rdat, water_sample_sites.Rdat (These two files are obtained by runing data_availability_info.R)
# start_date, end_date, water sample_size (see code below)
#
# Output:
# For discharge:     
#     good_discharge_sites: sites that satisfy the start and end date criteria and can actually download the discharge data
#     daily_discharge: daily dishcharge data for sites from good_discharge_sites
#     discharge_download_error_sites: sites that satisfy the criteria but has download error
# For water sample:
#     good_water_sample_sites: sites that satisfy the start and end date and water sample size criteria and can actually download the water sampel data
#     water_sample: water sample data for sites from good_discharge_sites
#     water_sample_download_error_sites: sites that satisfy the criteria but has download error



library(dataRetrieval)
load('discharge_sites.Rdat')
load('water_sample_sites.Rdat')

## set the criteria
start_date <- '2000-01-01'
end_date <- '2012-12-31'
water_sample_size <- 1 


## Check and Download the discharge data  
discharge_sites_subset <- subset(discharge_sites, (startDate <= as.Date(start_date))&(endDate >= as.Date(end_date)))
good_discharge_sites <- as.character(discharge_sites_subset[['siteID']])
discharge_download_error_sites <- data.frame(siteID=c(),message=c())
daily_discharge <- data.frame()

# Download the discharge data
for (i in seq(length(good_discharge_sites))){
  site_id <- good_discharge_sites[i]
  result <- tryCatch({
    site_discharge <- getDVData(site_id,'00060',start_date,end_date,convert=TRUE)# if convert=True unit will be cms
  },warning = function(w){
    return(w)
  },error = function(e){
    return(e)
  }) 
  
  if(inherits(result,"error")|inherits(result,"warning")) {    
    site_error <- data.frame(siteID=site_id, message=result$message[1])
    discharge_download_error_sites <- rbind(discharge_download_error_sites,site_error)
    next
  }
  
  siteID <- data.frame(siteID=rep(site_id,nrow(site_discharge)))
  daily_discharge <- rbind(daily_discharge,cbind(siteID,site_discharge))   
}

save(daily_discharge,file="daily_discharge.Rdat")
good_discharge_sites <- unique(as.character(daily_discharge[['siteID']]))
save(good_discharge_sites,file='good_discharge_sites.Rdat')
save(discharge_download_error_sites,file='discharge_download_error_sites.Rdat')


  
## Check and Download the water sample data
water_sample_sites_subset <- subset(water_sample_sites, (startDate <= as.Date(start_date))&(endDate >= as.Date(end_date))&(count>=water_sample_size))
good_water_sample_sites <- as.character(water_sample_sites_subset[['siteID']])
water_sample_download_error_sites <- data.frame(siteID=c(),message=c())
water_sample<- data.frame()  

# Download the water sample data
for (i in seq(length(good_water_sample_sites))){
  site_id <- good_water_sample_sites[i]
  result <- tryCatch({
    site_water_quality <- getSampleData(site_id,"00618",start_date,end_date)
  },warning = function(w){
    return(w)
  },error = function(e){
    return(e)
  }) 
  
  if(inherits(result,"error")|inherits(result,"warning")) {    
    site_error <- data.frame(siteID=site_id, message=result$message[1])
    water_sample_download_error_sites <- rbind(water_sample_download_error_sites,site_error)
    next
  }
  
  siteID <- data.frame(siteID=rep(site_id,nrow(site_water_quality)))
  water_sample <- rbind(water_sample,cbind(siteID,site_water_quality)) 
}

save(water_sample,file="water_sample.Rdat")
good_water_sample_sites <- unique(as.character(water_sample[['siteID']]))
save(good_water_sample_sites,file='good_water_sample_sites.Rdat')
save(water_sample_download_error_sites,file='water_sample_download_error_sites.Rdat')


  





  
  