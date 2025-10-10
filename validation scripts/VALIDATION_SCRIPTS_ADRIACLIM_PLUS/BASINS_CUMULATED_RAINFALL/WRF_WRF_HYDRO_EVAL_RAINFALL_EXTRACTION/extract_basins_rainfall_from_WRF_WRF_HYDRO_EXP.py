import numpy as np
import pandas as pd
#import sys
from netCDF4 import Dataset
from datetime import datetime
from datetime import timedelta

path_river = "/work/cmcc/ad07521/AdriaCLIM/Bacini/Rivers.csv"

mask_path = "/work/cmcc/ad07521/AdriaCLIM/Bacini/Masc_basin.asc"		#mask based on WRF grid
#mask_path = "/work/opa/ad07521/AdriaCLIM/Bacini/Era5_Mask.asc"		#mask based on Era5Land grid 

#mask = np.genfromtxt(mask_path, delimiter = " ", dtype = int, skip_header=5)
mask = np.genfromtxt(mask_path, delimiter = " ", dtype = int)

rivername = pd.read_csv(path_river)

count = np.bincount(mask.flat)
print(rivername.head())

nameP = rivername['River']

for year_sim in range (1990,2021):

	date_init = datetime(year = year_sim, month = 1, day = 1, hour = 0)		#for comparison with WRF stand-alone exp (2019)

	if year_sim == 2023:
		date_end = datetime(year = year_sim, month = 12, day = 31, hour = 18)
	else:
		date_end = datetime(year = year_sim+1, month = 1, day = 1, hour = 18)

	data = []

	dateindexP = pd.date_range(date_init, end = date_end, freq = "6h")
	#dateindexP = pd.date_range(date_init, end = date_end, freq = "24h")
	print(dateindexP)

	while date_init <= date_end:
	
		# for WRF estimations
		#dato = Dataset("/work/opa/vr25423/Project/AdriaClimPlus/preevaluation_run_5yrs_ERA5_EXP52/WRF-WRF-Hydro/2018_2023/run/EXP/wrfout/wrfout_d01_"+date_init.strftime("%Y-%m-%d")+"_00:00:00", 'r')
		dato = Dataset("/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP/wrfout_d01_"+date_init.strftime("%Y-%m-%d")+"_00:00:00", 'r')

		for i in range(0,4):
			pioggia = -9999*np.ones((402, 288))

			pioggia = dato.variables['RAINNC'][i][:][:]
			pioggia = pioggia + dato.variables['RAINC'][i][:][:]
			pioggia = pioggia + 100*dato.variables['I_RAINC'][i][:][:]
			pioggia = pioggia + 100*dato.variables['I_RAINNC'][i][:][:]
			pioggia_ok = np.flip(pioggia,0)
			#print(len(pioggia_ok))
			#print(len(mask))
			tot_rain = np.bincount(mask.flatten(), weights=pioggia_ok.flatten())
			avg_rain = tot_rain/count
			avg_rain2 = avg_rain[1:]
			data.append(avg_rain2)

		print(date_init)
		dato.close()
	
		date_init = date_init+timedelta(hours = 24)
		#date_init = date_init+timedelta(hours = 6)
	
	
	df = pd.DataFrame(data, columns = nameP)
	df = df.set_index(dateindexP)
	df.index.name = 'Datetime'
	print(df)
	
	df.to_csv(path_or_buf = "./Rainfall_"+str(year_sim)+"_WRF_WRF-HYDRO_EVAL_RUN_30years_6h.csv", index = True)
