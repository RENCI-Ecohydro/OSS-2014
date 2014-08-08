check_site_availability <- function(site_id,START_DATE,END_DATE,WATER_SAMPLE_SIZE) {
  
  site_data_availability = getDataAvailability(site_id)  
  site_daily_discharge_meta = subset(site_data_availability, (statCd == '00003')&(parameter_cd == '00060'))
  site_water_quality_meta = subset(site_data_availability, parameter_cd == '00618')
  
  # check discharge data 
  if (nrow(site_daily_discharge_meta)==1){
    daily_discharge_start <- as.Date(site_daily_discharge_meta[['startDate']][1])
    daily_discharge_end <- as.Date(site_daily_discharge_meta[['endDate']][1])
    
    if ((as.Date(START_DATE) >= daily_discharge_start)&(as.Date(END_DATE) <= daily_discharge_end)){ check_discharge <- 'discharge data available' }
    
  } else {check_discharge <- 'discharge data unavailable'}  
  
  # check quality data
  if (nrow(site_water_quality_meta)==1) {
    
    water_quality_start <- as.Date(site_water_quality_meta[['startDate']][1])
    water_quality_end <- as.Date(site_water_quality_meta[['endDate']][1])
    water_quality_size <- site_water_quality_meta[['count']][1]
    
    if ((as.Date(START_DATE) >= water_quality_start)&(as.Date(END_DATE) <= water_quality_end)
      &(water_quality_size >= WATER_SAMPLE_SIZE)){
      
      check_quality <- 'quality data available'
    } else {
      check_quality <- 'quality data unavailable'
    }    
    
  } else { 
    check_quality <- 'quality data unavailable'
  }
  
  # return check info
  #if ((check_discharge == 'discharge data available')&(check_quality == 'quality data available')){ 
  #modified script so we can disregard the 'water quality' filter @ Tony 08072014
  if ((check_discharge == 'discharge data available')){ 
	check_info = 'available site'
  } else {
    check_info = paste(check_discharge,',',check_quality)
  }
  
  return(check_info)  
  
}