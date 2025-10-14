### Script to calculate windroses ###
#Follow this procedure to update the insitu data
#In this path /work/cmcc/vr25423/Project/AdriaClimPlus/data/insitu/REGIONI_IN_SITU_OBS/LOCALI, grep only the required station data.
# The raw station data is in the following location: /work/cmcc/vr25423/Project/AdriaClimPlus/data/insitu/REGIONI_IN_SITU_OBS/raw_data/DATA_STATIONS_EMILIA_ROMAGNA_1989_2017_REF_03_12_2024
# Use this script to update the data with missing values=-99999 from 1990 to 2020 in /users_home/cmcc/vr25423/scripts/WRF_Evaluation/missing_data.ipynb
############################################
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from windrose import plot_windrose
import matplotlib.cm as cm
import os
#from metpy.calc import wind_direction
#import geopy.distance
#from shapely.geometry import Point, MultiPoint
#from shapely.ops import nearest_points
############################################

# PYTHON ENV to be activated: rivers_rain

name_exp = "PARMA_CAMPUS"



base_path_insitu = '/work/cmcc/vr25423/Project/AdriaClimPlus/data/insitu/REGIONI_IN_SITU_OBS/LOCALI'
base_path_wrf = '/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/pp'
path_list_stations = base_path_insitu+"/station_PARMA_CAMPUS_LOCALI.txt"

town_name=np.loadtxt(path_list_stations, usecols=0, dtype='str')
lat_town=np.loadtxt(path_list_stations, usecols=2, dtype='float')
lon_town=np.loadtxt(path_list_stations, usecols=3, dtype='float')
freq_town=np.loadtxt(path_list_stations, usecols=4, dtype='str')

print (town_name)
print (lat_town)
print (lon_town)
print (freq_town)

print ('Working on station ', town_name)
print ('LATITUDE station: ', lat_town)
print ('LONGITUDE station: ', lon_town)
print ('Frequency for this station: ', freq_town)


# preparing vectors that will contain obs data 
wind_dir_station = []
wind_module_station = []


#-- import the files with obs wind speed/direction data 
path_wind_dir_station = base_path_insitu+"/WIND_DIR_HOURLY_PARMA_CAMPUS_1987_1999_Filled.txt"
path_wind_module_station = base_path_insitu+"/WIND_VEL_HOURLY_PARMA_CAMPUS_1987_1999_Filled.txt"

wind_dir_station = np.loadtxt(path_wind_dir_station, usecols=0, dtype='float')
wind_module_station = np.loadtxt(path_wind_module_station, usecols=0, dtype='float')

wind_dir_station [wind_dir_station == -99999.00] = np.nan
wind_module_station [wind_module_station == -99999.00] = np.nan

np.set_printoptions(threshold=np.inf)

print ('Number of data available: ', np.count_nonzero(~np.isnan(wind_dir_station)))
print ('')
    
# select just the data for which we have WRF+WRFHYDRO values (00:00, 06:00, 12:00, 18:00) 
data_station_direction = []
data_station_module = []
if (freq_town == '30min'):
    print ('This station has values every 30 mins')
    for counter in range (0,len(wind_dir_station), 12):
        data_station_direction.append (wind_dir_station[counter])
        data_station_module.append (wind_module_station[counter])
elif (freq_town == '1h'):
    print ('This station has values every 1 hour')
    for counter in range (0,len(wind_dir_station), 6):
        data_station_direction.append (wind_dir_station[counter])
        data_station_module.append (wind_module_station[counter])
elif (freq_town == '15min'):
    print ('This station has values every 15 mins')
    for counter in range (0,len(wind_dir_station), 24):
        data_station_direction.append (wind_dir_station[counter])
        data_station_module.append (wind_module_station[counter])


# UPLOADING WRF+WRF_HYDRO AND ERA5LAND DATA
path_wrf_wrfhydro = base_path_wrf+'/wind.nc'
path_era5land = base_path+'/DATA_WIND_HOURLY_ERA5LAND/ERA5-LAND_2019_2023_hourly_wind_data.nc'   

#-- read the file
ds_wrf = nc.Dataset(path_wrf_wrfhydro, 'r')
ds_era5land = nc.Dataset(path_era5land, 'r')
#print (ds_wrf)

#-- read the variables from the files
lat_wrf_extr = ds_wrf.variables['XLAT'] [:,:]
lon_wrf_extr = ds_wrf.variables['XLONG'] [:,:]
lat_wrf_1D = ds_wrf.variables['XLAT'] [:,0]
lon_wrf_1D = ds_wrf.variables['XLONG'] [0,:]
wind_speed_wrf_extr = ds_wrf.variables['vn'] [:,:,:]
wind_direction_wrf_extr = ds_wrf.variables['vdir'] [:,:,:]

lat_era5land_part = ds_era5land.variables['latitude'] [::-1]
lon_era5land_part = ds_era5land.variables['longitude'] [:]
#    u10_era5land_extr = ds_era5land.variables['u10'] [:,:,:]
#    v10_era5land_extr = ds_era5land.variables['v10'] [:,:,:]
wind_speed_era5land_extr = ds_era5land.variables['VN'] [:,::-1,:]
wind_direction_era5land_extr = ds_era5land.variables['uv10'] [:,::-1,:]

lon_era5land_extr,lat_era5land_extr = np.meshgrid (lon_era5land_part,lat_era5land_part)

#print (lat_era5land)
#print (lon_era5land)

# find nearest point in WRF and ERA5land array
lat_wrf = lat_wrf_extr.flatten()
lon_wrf = lon_wrf_extr.flatten()

lat_era5land = lat_era5land_extr.flatten()
lon_era5land = lon_era5land_extr.flatten()

distances_wrf = (lat_wrf-lat_town)**2 + (lon_wrf-lon_town)**2
distances_era5land = (lat_era5land-lat_town)**2 + (lon_era5land-lon_town)**2

idx_wrf = np.argmin (distances_wrf)
idx_era5land = np.argmin (distances_era5land)
#print (idx_wrf)

print ('Latitude for WRF: ', lat_wrf[idx_wrf]) 
print ('Longitude for WRF: ', lon_wrf[idx_wrf]) 
print ('Latitude for ERA5-LAND: ', lat_era5land[idx_era5land]) 
print ('Longitude for ERA5-LAND: ', lon_era5land[idx_era5land]) 

index_lat_wrf = np.array (np.where (lat_wrf_1D == lat_wrf[idx_wrf]))
index_lon_wrf = np.array (np.where (lon_wrf_1D == lon_wrf[idx_wrf]))

index_lat_era5land = np.array (np.where (lat_era5land_part == lat_era5land[idx_era5land]))
index_lon_era5land = np.array (np.where (lon_era5land_part == lon_era5land[idx_era5land]))

# extract wind speed module and components for WRF and ERA5-LAND
wind_module_wrf_at_station = wind_speed_wrf_extr[:,index_lat_wrf,index_lon_wrf].ravel()
wind_direction_wrf_at_station = wind_direction_wrf_extr[:,index_lat_wrf,index_lon_wrf].ravel()



wind_module_era5land_at_station = wind_speed_era5land_extr[:,index_lat_era5land,index_lon_era5land].ravel()
wind_direction_era5land_at_station = wind_direction_era5land_extr[:,index_lat_era5land,index_lon_era5land].ravel()

print("data_station_direction ", len(data_station_direction))

ax = WindroseAxes.from_ax()
ax.bar (data_station_direction, data_station_module, normed=True, opening=0.8, nsector=22, bins=np.arange(0,10,2), cmap=cm.jet, edgecolor="white")
ax.set_legend()

r = np.arange(0, 16, 2)
ax.set_yticks(r)
rrr = []
for el in r:
    rrr.append("{NUM}%".format(NUM=el))
ax.set_yticklabels(rrr)
plt.title(town_name+', IN-SITU OBSERVATIONS, 1987-1999 ')
plt.savefig(town_name+'_STATION_2019_2023_WINDROSE',dpi=300,bbox_inches='tight')

ax1 = WindroseAxes.from_ax()
ax1.bar (wind_direction_wrf_at_station, wind_module_wrf_at_station, normed=True, opening=0.8, nsector=22, bins=np.arange(0,10,2), cmap=cm.jet, edgecolor="white")
ax1.set_legend()

r = np.arange(0, 16, 2)
ax1.set_yticks(r)
rrr = []
for el in r:
    rrr.append("{NUM}%".format(NUM=el))
ax1.set_yticklabels(rrr)

##ax1.set_yticks(np.arange(0, 20, step=2))
##ax1.set_yticklabels(np.arange(0, 20, step=2))
##ax.set_xticklabels([u'0\N{DEGREE SIGN}', u'45\N{DEGREE SIGN}', u'90\N{DEGREE SIGN}', u'135\N{DEGREE SIGN}',\
##            u'180\N{DEGREE SIGN}',u'225\N{DEGREE SIGN}',u'270\N{DEGREE SIGN}',u'315\N{DEGREE SIGN}'])
##ax.set_xticklabels(['90˚', '45˚', '0˚', '315˚' , '270˚', '225˚','180˚', '135˚'],fontsize=14)
plt.title(town_name+' ,'+name_exp+', 1987-1999')
plt.savefig(town_name+'_'+name_exp+'_1987-1999_WINDROSE',dpi=300,bbox_inches='tight')


ax2 = WindroseAxes.from_ax()
ax2.bar (wind_direction_era5land_at_station, wind_module_era5land_at_station, normed=True, opening=0.8, nsector=22, bins=np.arange(0,10,2), cmap=cm.jet, edgecolor="white")
ax2.set_legend()

r = np.arange(0, 16, 2)
ax2.set_yticks(r)
rrr = []
for el in r:
    rrr.append("{NUM}%".format(NUM=el))
ax2.set_yticklabels(rrr)

##ax1.set_yticks(np.arange(0, 20, step=2))
##ax1.set_yticklabels(np.arange(0, 20, step=2))
##ax.set_xticklabels([u'0\N{DEGREE SIGN}', u'45\N{DEGREE SIGN}', u'90\N{DEGREE SIGN}', u'135\N{DEGREE SIGN}',\
##            u'180\N{DEGREE SIGN}',u'225\N{DEGREE SIGN}',u'270\N{DEGREE SIGN}',u'315\N{DEGREE SIGN}'])
##ax.set_xticklabels(['90˚', '45˚', '0˚', '315˚' , '270˚', '225˚','180˚', '135˚'],fontsize=14)
plt.title(town_name+', ERA5-LAND, 1987-1999')
plt.savefig(town_name+'_ERA5_LAND_1987-1999_WINDROSE',dpi=300,bbox_inches='tight')
