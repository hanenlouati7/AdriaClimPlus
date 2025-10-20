import numpy as np
import pandas as pd
from netCDF4 import Dataset
from datetime import datetime
from datetime import timedelta

def is_leap_year(year):
    # Se l'anno è divisibile per 4, ma non per 100, o se è divisibile per 400
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False

path_river = "/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/Rivers.csv"
mask_path = "/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/Masc_basin.asc"

np.set_printoptions(threshold=np.inf)

#genfromtxt: load data from a text file, with missing values handled as specified
#	     dtype: data type of the resulting array 
#	     delimiter: the string used to separate values
# la maschera è fatta da 0 e da numeri, da 1 a 145, dove ogni numero è associato ad un bacino
# nel file csv che diamo in pasto, c'è la colonna ID che è il numero della maschera -1
# quindi ad esempio il Pò che nella maschera è 112, nel file csv ha ID 111
#mask = np.genfromtxt(mask_path, delimiter = " ", dtype = int, skip_header=5)
mask = np.genfromtxt(mask_path, delimiter = " ", dtype = int)

# passare file .nc con pioggia ERA5 con grigliato WRF
dato_fake = Dataset("/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/DATA_ERA5LAND_PRECIP/DELO_ERA5LAND_FILES_2019_2023/rain_ERA5Land_2019-2023_basins_on_wrf_grid.nc", 'r')
pioggia_fake = dato_fake.variables['rain'][0][:][:]

mask_ok = np.where(pioggia_fake < 100000000, mask, 0)
#print (mask_ok)

#read_csv: read a comma-separated values (csv) file 
rivername = pd.read_csv(path_river)

#bincount: count number of occurrences of each value in array of non-negative ints
#          flat: a 1-D iterator over the array. It allows iterating over the array as if it were a 1-D array, either in a for-loop or by calling
#	         its next method 
count = np.bincount(mask_ok.flat)

# head: returns the first n rows for the object based on position

#in this way, the field between single quote mark is considered and saved in the specified variable
nameP = rivername['River']

for year_sim in range (2020,2021):

    #datetime: a module to specify the start and stop date of the interval to be considered
    date_init = datetime(year = year_sim, month = 1, day = 1, hour = 0)
    date_end = datetime(year = year_sim, month = 12, day =31, hour = 18)

    data = []

    #date_range: returns the range of equally spaced time points such that they all satisfy start <[=] x <[=] end, with the specified frequency
    dateindexP = pd.date_range(date_init, end = date_end, freq = "6h")
    #print(dateindexP)

    if is_leap_year(year_sim):
        upper_lim = 1464
    else: 
        upper_lim = 1460

    for i in range(0,upper_lim):

        dato = Dataset("/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/DATA_ERA5LAND_PRECIP/rain_ERA5Land_"+str(year_sim)+"_basins_on_wrf_grid.nc", 'r')

        #print ('Slice of time: ' +str(i))	
	# ones: return a new array of given shape and type, filled with ones 
        pioggia = -9999*np.ones((402, 288))

        pioggia = dato.variables['rain'][i][:][:]
	#print(len(pioggia))
	
	#flip: reverse the order of elements in an array along the given axis
        pioggia_ok = np.flip(pioggia,0)
        #print(pioggia_ok)

        # Sostituire NaN con 0
        mask_ok_cleaned = np.nan_to_num(mask_ok, nan=0)  # Imposta i NaN a 0
        pioggia_ok_cleaned = np.nan_to_num(pioggia_ok, nan=0)  # Imposta i NaN a 0

        # Rimuovere eventuali valori negativi, se necessario
        mask_ok_cleaned = np.clip(mask_ok_cleaned, 0, None)  # Imposta i valori negativi a 0

        # Usare np.bincount con i pesi
        tot_rain = np.bincount(mask_ok_cleaned.flatten(), weights=pioggia_ok_cleaned.flatten())

	#flatten: return a copy of the array collapsed into one dimension
	#weights: if weights is specified, the input array is weighted by it 
	#	  i.e. if a value n is found at position 1, out[n] +=weight[i] instead of out[n] +=1
        #tot_rain = np.bincount(mask_ok.flatten(), weights=pioggia_ok.flatten())

        avg_rain = tot_rain/count
        # escludiamo lo 0
        avg_rain2 = avg_rain[1:]
	#append: takes a single item as an input parameter and adds that to the end of the list
        data.append(avg_rain2)

        dato.close()

    #DataFrame: two-dimensional, size-mutable, potentially heterogeneous tabular data
    #	    columns: column labels to use for resulting frame when data does not have them	   	
    df = pd.DataFrame(data, columns = nameP)
    #set_index: set the DataFrame index using existing columns
    df = df.set_index(dateindexP)
    df.index.name = 'Datetime'
    #print(df)
	
    df.to_csv(path_or_buf = "./Rainfall_"+str(year_sim)+"_ERA5_Land_basins_on_wrf_grid.csv", index = True)
