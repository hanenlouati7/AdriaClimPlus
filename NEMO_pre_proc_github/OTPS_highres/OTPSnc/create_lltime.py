from datetime import datetime,timedelta
import numpy as np
import sys


data 	= np.zeros((1,2))

data[0,0]=  41.3589
data[0,1]=  16.1972

lons	= data[:,1]
lats	= data[:,0]

npoints	= len(lons)

# generate time sequence

date0	= datetime(2019,1,1,0)
delta	= timedelta(seconds=3600)

time	= [date0 + i*delta for i in range(24*365)]

for tt in time:
	for ll in range(npoints):
		print lats[ll],lons[ll],tt.strftime('%Y %-m %-d %-H %-M %-S') 
