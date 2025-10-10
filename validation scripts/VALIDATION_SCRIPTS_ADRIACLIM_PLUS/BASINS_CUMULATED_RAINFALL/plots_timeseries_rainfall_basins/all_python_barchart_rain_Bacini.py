import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import csv
import os
#import matplotlib
#matplotlib.use('tkagg')

year = os.environ["year"]
basin = os.environ["basin"]
name_exp = os.environ["NAME_EXP"]

#print (year)
#print (basin)
#print (name_exp)

data_dir_wrf='/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/plots_timeseries_rainfall/data_plots_EVAL_RUN_30YEARS/all'
filename_wrf = data_dir_wrf+'/'+basin+'_WRF-WRF_HYDRO_EVAL_RUN_30YEARS_vs_ERA5Land_rain_'+year+'.txt'

#print(filename)

f_wrf=open(filename_wrf,"r")
temp_wrf=f_wrf.read().splitlines()

rain_wrf_6h_extr=[] 
rain_wrf_cumul_extr=[]

rain_era5land_6h_extr=[]
rain_era5land_cumul_extr=[]

for x in temp_wrf:
    rain_wrf_6h_extr.append(x.split(' ')[1])
f_wrf.close()
for x in temp_wrf:
    rain_era5land_6h_extr.append(x.split(' ')[2])
f_wrf.close()

for x in temp_wrf:
    rain_wrf_cumul_extr.append(x.split(' ')[3])
f_wrf.close()
for x in temp_wrf:
    rain_era5land_cumul_extr.append(x.split(' ')[4])
f_wrf.close()

rain_wrf_6h = pd.to_numeric(rain_wrf_6h_extr)
rain_era5land_6h = pd.to_numeric(rain_era5land_6h_extr)

rain_wrf_cumul = pd.to_numeric(rain_wrf_cumul_extr)
rain_era5land_cumul = pd.to_numeric(rain_era5land_cumul_extr)

nrow=rain_wrf_6h.shape[0]
days = np.linspace (1,nrow,nrow)
#d={'days':days, 'rain_wrf_era5_6h':rain_wrf_era5_6h, 'rain_wrf_ifs_6h':rain_wrf_ifs_6h, 'rain_era5land_6h':rain_era5land_6h, 'rain_wrf_era5_cumul':rain_wrf_era5_cumul, 'rain_wrf_ifs_cumul':rain_wrf_ifs_cumul, 'rain_era5land_cumul':rain_era5land_cumul}

d={'days':days, 'rain_wrf_6h':rain_wrf_6h, 'rain_era5land_6h':rain_era5land_6h, 'rain_wrf_cumul':rain_wrf_cumul, 'rain_era5land_cumul':rain_era5land_cumul}

df = pd.DataFrame (data=d)
#print (df)


# plot
#ax = df.plot(y='Cumulated(mm/6h)', color='magenta', ls='-.', figsize=(10, 6), ylabel='Rainfall ($)')
fig, ax1 = plt.subplots() 

ax1.set_xlabel('Years') 
ax1.set_ylabel('Total precipitation (mm/6h)') 
ax1.plot(df['days'].values, df['rain_wrf_6h'].values, color = 'blue', label='ADRIACLIM_PLUS')  
ax1.plot(df['days'].values, df['rain_era5land_6h'].values, color = 'black', label='ERA5LAND, '+year) 
ax1.tick_params(axis ='y') 
plt.legend(loc="upper left")

# Definizione del range di anni
anni = np.arange(1990, 2022, 2)  # Da 1990 a 2020, step di 2 anni
punti = (anni - 1990) * 1460  # Calcola le posizioni corrispondenti

# Imposta i tick sull'asse x
plt.xticks(punti, [f'{anno}' for anno in anni], fontsize=10, rotation=90)

if basin == 'PoPontelagoscuro':
    plt.title('Po, WRF_WRF-HYDRO EVAL RUN vs ERA5LAND, '+year)
else:
    plt.title(basin+', WRF_WRF-HYDRO EVAL RUN vs ERA5LAND, '+year)
 
# Adding Twin Axes
ax2 = ax1.twinx() 
  
ax2.set_ylabel('Total precipitation over the period (mm)') 
ax2.plot(df['days'].values, df['rain_wrf_cumul'].values, color = 'blue') 
ax2.plot(df['days'].values, df['rain_era5land_cumul'].values, color = 'black')  
ax2.tick_params(axis ='y') 

#plt.show()

plt_dir='/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/plots_timeseries_rainfall/figures_'+name_exp

if basin == 'PoPontelagoscuro':
    figname='Po_Rainfall_timeseries_WRF_WRF-HYDRO_'+name_exp+'.png'
else:
    figname=basin+'_Rainfall_timeseries_WRF_WRF-HYDRO_'+name_exp+'.png'

plt.savefig(plt_dir+'/'+figname, dpi=300,bbox_inches='tight')
