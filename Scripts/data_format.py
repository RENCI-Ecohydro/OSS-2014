import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

filename = "C://Users/tony/OSS/Git/OSS-2014-Project/data/watershed_lossyear_full.csv"
rawdata = pd.io.parsers.read_csv(filename)

keys = ['0','huc']
for j in range(2):
	for i in range(2000,2013):
		if j ==0:
			keys.append(str(i)+'_loss')
		if j ==1:
			keys.append(str(i)+'_closs')

to_key = ['id','huc']
for j in range(2):
	for i in range(2000,2013):
		if j ==0:
			to_key.append(str(i))
		if j ==1:
			to_key.append(str(i)+'_c')

new = {keys[x]: to_key[x]  for x in range(len(keys))}
			
d_renamed = rawdata.rename(columns=new)
list(d_renamed.columns.values)
d_filtered = d_renamed.iloc[:,1:-12]
datap = pd.melt(d_filtered,id_vars='huc', var_name='Year', value_name='% loss')
datap['Year']  = pd.to_datetime(datap['Year'])
datas= datap.sort(['huc','Year'])
d_cumsum = datas.groupby(by=['huc','Year']).sum().groupby(level=[0]).cumsum()

#generate np.array for each huc
huc = np.zeros((len(datas)/12,12))
count = 0
for i in range(0,len(datas)-12,12):
	huc[count] = datas['% loss'][i:i+12]
	count +=1

#figure out what cutoff point to use for determining break year
fy = []
z = []
filter_list = np.arange(0,1,0.01)
for filter in filter_list:
	a,b =np.where(huc>=filter)
	fhuc = np.where(huc<filter,0,huc)
	ind = np.unique(a) #explore how many unique disturbance sites occurs 
	z.append(len(a)-len(ind))
	#for i in ind:
		 #plt.plot(np.arange(2001,2013), fhuc[i])
	fy.append(len(ind))
fy = np.array(fy)

filter= 0.23
a,b =np.where(huc>=filter)
fhuc = np.where(huc<filter,0,huc)
ind = np.unique(a) #explore how many unique disturbance sites occurs 

for i in ind:
	 plt.plot(np.arange(2001,2013), fhuc[i])

#get the hucs back
disturb = ind*12
disturbed_hucs = []
ds =[]
for d in range(len(disturb)):
	d_array = datas[disturb[d]:disturb[d]+12]
	ds.append(d_array)
	year_disturb = d_array[d_array['% loss']>filter]['Year'].iloc[0] #first major disturbance?
	d_amount = d_array[d_array['% loss']>filter]['% loss'].iloc[0]
	d_huc = datas[disturb[d]:disturb[d]+12]['huc'].iloc[0]
	str_huc = str(int(d_huc))
	if (len(str_huc) <8):
		str_huc = '0' + str_huc
	disturbed_hucs.append([str_huc,year_disturb.strftime('%Y-%m-%d'), round(d_amount,2)])
	
out = pd.DataFrame(disturbed_hucs, columns = ['siteID', 'disDate', 'pLoss' ])
out.to_csv(path_or_buf='c://users/tony/OSS/Git/OSS-2014-Project/data/filtered_watersheds.csv', sep = ',', na_rep=-9999, index = False)

	
