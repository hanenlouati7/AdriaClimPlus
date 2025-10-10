### This is a python script to process the 30 year evaluation data to create timeseries of T2m, Accumulated prec, wind speed, and relative humidity to evaluate WRF output using ERA5 forcing and in-situ observations ###
### Author: Alessandro De Lorenzis ###
### Project: AdriaClim PLUS ###
### Date: 12-February-2025 ###

### Import modules ###
import pandas as pd
from datetime import datetime
import math, time, sys, os
import numpy as np
from netCDF4 import Dataset
import os
from netCDF4 import Dataset as open_ncfile
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import json
from sklearn.metrics import r2_score
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from scipy import stats
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.dates as mdates

import seaborn as sns
from scipy.stats import skew, kurtosis



######################################################################
def compute_statistics (model, obs):
    """Compute all the statistics with different datasets"""

    #BIAS
    bias = model - obs
    bias_avg = np.mean(bias)

    # RMSE
    mse = np.mean((model-obs) **2)
    rmse = np.sqrt (mse)

    #NRMSE
    nrmse = rmse/max(obs)

    #PEARSON CORRELATION
    corr = stats.pearsonr (model,obs)

    #R2 REGRESSION COEFF
    r2_coeff = r2_score (model,obs)

    #MAE
    mae = mean_absolute_error (model,obs)

    return bias_avg,rmse,nrmse,mae,r2_coeff,corr[0]
######################################################################

######################################################################
def convert_numpy(obj):
    """Converte tutti gli array e tipi NumPy in tipi Python standard."""
    if isinstance(obj, np.ndarray):  # Converti array NumPy in liste
        return obj.tolist()
    elif isinstance(obj, np.generic):  # Converti tipi NumPy scalari (es. np.float32, np.int64) in tipi Python
        return obj.item()
    elif isinstance(obj, dict):  # Ricorsione sui dizionari
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):  # Ricorsione sulle liste
        return [convert_numpy(v) for v in obj]
    return obj  # Tutto il resto rimane invariato
######################################################################

######################################################################
def compute_and_print_statistics(obs, model_wrf, model_era5land, var_name, file_name):
    """
    Calcola e stampa le statistiche tra osservazioni e i modelli WRF ed ERA5-Land.
    
    Parameters:
    obs (array): Dati osservati
    model_wrf (array): Dati simulati dal modello WRF
    model_era5land (array): Dati simulati dal modello ERA5-Land
    var_name (str): Nome della variabile (es. "Wind Speed")
    file_name (str): Nome del file di testo su cui scrivere le statistiche (default "statistics_output.txt")
    """
    
    # Maschere per escludere NaN
    mask_wrf = ~np.isnan(obs) & ~np.isnan(model_wrf)
    mask_era5land = ~np.isnan(obs) & ~np.isnan(model_era5land)
    
    # Dati senza NaN
    obs_masked_wrf = obs[mask_wrf]
    model_wrf_masked = model_wrf[mask_wrf]
    obs_masked_era5land = obs[mask_era5land]
    model_era5land_masked = model_era5land[mask_era5land]
    
    # Calcolo statistiche
    stats_wrf = compute_statistics(model_wrf_masked, obs_masked_wrf)
    stats_era5land = compute_statistics(model_era5land_masked, obs_masked_era5land)
    
    # Apriamo il file di output in modalità append
    with open(file_name, 'a') as f:
        # Scriviamo le informazioni sul file
        f.write("\n**************************\n")
        f.write(f"{var_name} (ADRIACLIM_PLUS vs OBS)\n")
        f.write("**************************\n")
        f.write(f"{var_name} OBS (avg): {np.round(np.mean(obs_masked_wrf), 2)}\n")
        f.write(f"{var_name} ADRIACLIM_PLUS (avg): {np.round(np.mean(model_wrf_masked), 2)}\n")
        f.write(f"BIAS (avg): {round(stats_wrf[0], 2)}\n")
        f.write(f"RMSE: {round(stats_wrf[1], 2)}\n")
        f.write(f"NRMSE: {round(stats_wrf[2], 2)}\n")
        f.write(f"MAE: {round(stats_wrf[3], 2)}\n")
        f.write(f"R2: {round(stats_wrf[4], 2)}\n")
        f.write(f"CORRELATION: {round(stats_wrf[5], 2)}\n")
        
        f.write("\n**************************\n")
        f.write(f"{var_name} (ERA5-LAND vs OBS)\n")
        f.write("**************************\n")
        f.write(f"{var_name} OBS (avg): {np.round(np.mean(obs_masked_era5land), 2)}\n")
        f.write(f"{var_name} ERA5-LAND (avg): {np.round(np.mean(model_era5land_masked), 2)}\n")
        f.write(f"BIAS (avg): {round(stats_era5land[0], 2)}\n")
        f.write(f"RMSE: {round(stats_era5land[1], 2)}\n")
        f.write(f"NRMSE: {round(stats_era5land[2], 2)}\n")
        f.write(f"MAE: {round(stats_era5land[3], 2)}\n")
        f.write(f"R2: {round(stats_era5land[4], 2)}\n")
        f.write(f"CORRELATION: {round(stats_era5land[5], 2)}\n")

######################################################################




######################################################################
def relative_humidity(t2m_K, d2m_K):
    """Calcola l'umidità relativa (%) dato t2m (temperatura aria in Kelvin) e d2m (temperatura punto di rugiada in Kelvin)."""
    
    # Calcolare la pressione di vapore di saturazione per t2m (aria) e d2m (punto di rugiada)
    e_t = 6.112 * np.exp(17.67 * (t2m_K - 273.15) / ((t2m_K - 273.15) + 243.5))  # Pressione di vapore di saturazione per la temperatura dell'aria (°C)
    e_td = 6.112 * np.exp(17.67 * (d2m_K - 273.15) / ((d2m_K - 273.15) + 243.5))  # Pressione di vapore di saturazione per il punto di rugiada (°C)
    
    # Calcolare l'umidità relativa
    rh = 100 * (e_td / e_t)  # Percentuale di umidità relativa
    
    return rh

######################################################################
######################################################################








##################################### INPUTS ###########################################
##### Region to be evaluated #####
region = "EMILIA_ROMAGNA"

##### Forcing #####
forcing = "ERA5"

##### Flag that defines if the accumualted precipitation of observation can be shifted towards the WRF data ###
shift_flag = 1 # 0 for not aligning observed data. 1 for aligning it.


#### FIGURES PATH ####
# path where to save the figures
out_path = "/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/ADRIACLIM_PLUS_30YEARS_EVAL_RUN_REANAL/timeseries_figures/"+region

# some variables related to years
begin_year = 2004       # year where the first obs point refers to
begin_month = 4         # month where the first obs point refers to
begin_day = 30         # day where the first obs point refers to
end_year = 2020       # year where the last obs point refers to
end_month = 12       # month where the last obs point refers to
end_day = 31       # day where the last obs point refers to

# Anni e mesi per la ricerca dei file di WRF
years = ["%04d" % x for x in np.arange(begin_year, end_year+1)]
#years = ["%04d" % x for x in np.arange(2004, 2007)]
months = ["%02d" % x for x in np.arange(1, 13)]
days = ["%02d" % x for x in range(32)]

name_station = "BOLOGNA_URBANA"

#################
### STATISTICS
# filename where to save statistics for ADOY, TIMESERIES AND BOX PLOT
filename_statistics = f"statistics_{name_station}_EVAL_RUN_30Y_vs_OBS_{begin_year}-{begin_month}-{begin_day}_{end_year}-{end_month}-{end_day}.txt"

f = open(filename_statistics, 'a')
f.write(f"#####################################\n")
f.write(f"STATION: {name_station}\n")
f.write(f"RANGE: {begin_year}_{begin_month}_{begin_day}-{end_year}_{end_month}_{end_day}\n")
f.write(f"#####################################\n")
f.close()


################################### Processing Data #####################################

#####################################################
###################### IN-SITU OBSERVATIONS ####################
#####################################################

# Definisci il nome della regione (esempio: 'EMILIA_ROMAGNA')
region = "EMILIA_ROMAGNA"

# Definisci il percorso ai dati della regione
path_to_region_insitu_data = f"/path/to/in-situ/station/data"

# Carica il dataframe dal file CSV delle stazioni
file_path = f"{path_to_region_insitu_data}"
df = pd.read_csv(file_path, delimiter="\t")  # Cambia se il separatore è diverso (ad esempio, ',' per la virgola)

# Estrai i nomi delle stazioni
station_names = df['STAZIONE'].unique()

# Crea un dizionario per memorizzare i dati per ciascuna stazione
station_data = {
    station: {
        "data": [],
        "t2m": [],
        "precipitation": [],
        "wind_speed": [],
        "humidity": [],
        "lat": None,  # Aggiungi latitudine
        "lon": None,  # Aggiungi longitudine
        "start_date": None,  # Aggiungi data di inizio
        "end_date": None  # Aggiungi data di fine
    }
    for station in station_names
}

# Aggiungi latitudine, longitudine, inizio e fine per ciascuna stazione
for _, row in df.iterrows():
    station = row['STAZIONE']
    lat = row['LAT']
    lon = row['LON']
    start_date = row['INIZIO']
    end_date = row['FINE']
    
    # Aggiungi queste informazioni al dizionario
    station_data[station]["lat"] = lat
    station_data[station]["lon"] = lon
    station_data[station]["start_date"] = start_date
    station_data[station]["end_date"] = end_date

# Per ogni stazione, cerca il file corrispondente
for station in station_names:
    # Trova il file che contiene il nome della stazione nel suo nome
    files_in_directory = os.listdir(path_to_region_insitu_data)
    matching_files = [f for f in files_in_directory if station in f]
    
    if matching_files:
        # Se esiste almeno un file che contiene il nome della stazione
        file_name = matching_files[0]  # Usa il primo file che corrisponde
        
        try:
            # Leggi il file di testo
            with open(os.path.join(path_to_region_insitu_data, file_name), "r") as file:
                # Salta l'header del file di testo
                next(file)
                
                # Leggi ogni riga nel file
                for line in file:
                    # Splitta la riga in base alla virgola e salva i dati nelle rispettive liste
                    data, t2m, precipitation, wind_speed, humidity = line.strip().split(",")
                    
                    # Aggiungi i dati nel dizionario della stazione corrispondente
                    station_data[station]["data"].append(data)
                    station_data[station]["t2m"].append(float(t2m))
                    station_data[station]["precipitation"].append(float(precipitation))
                    station_data[station]["wind_speed"].append(float(wind_speed))
                    station_data[station]["humidity"].append(float(humidity))
        except FileNotFoundError:
            print(f"File per la stazione {station} non trovato.")
    else:
        print(f"Nessun file trovato per la stazione {station}.")

# Ora il dizionario `station_data` contiene i dati separati per ciascuna stazione,
# con aggiunte le informazioni di latitudine, longitudine, data di inizio e fine.

# Stampa la struttura del dizionario per ogni stazione
for station, data in station_data.items():
    print(f"Stazione: {station}")
    print(f"  Latitudine: {data['lat']}")
    print(f"  Longitudine: {data['lon']}")
    print(f"  Data di inizio: {data['start_date']}")
    print(f"  Data di fine: {data['end_date']}")
    print(f"  Numero di dati per la stazione: {len(data['data'])}")
    print('-' * 40)  # Separatore per migliorare la leggibilità


#####################################################
###################### ERA5-Land ####################
#####################################################

# Definizione del percorso base
base_path = "/path/to/era5land/data"

# Crea un dizionario vuoto per memorizzare i risultati per ogni stazione
era5land_results = {}

# Itera su ogni stazione
for station, data in station_data.items():
    start_date_station = datetime.strptime(data['start_date'], "%Y-%m-%d")
    end_date_station = datetime.strptime(data['end_date'], "%Y-%m-%d")
    
    # Crea un dizionario per la stazione
    era5land_results[station] = {
        't2m_era5land': [],
        'precipitation_era5land': [],
        'humidity_era5land': [],
        'wind_speed_era5land': []
    }
    
    # Per ogni anno di dati, estrai i dati da Era5Land
    for anno in range(start_date_station.year, end_date_station.year + 1):
        file_nc = f"{base_path}ERA5-Land_{anno}_unpacked.nc"
        file_nc_hum = f"{base_path}new_ERA5-Land_{anno}_unpacked.nc"
        #print(file_nc)
        
        # Apri il file nc
        era5land = Dataset(file_nc, "r")
        era5land_hum = Dataset(file_nc_hum, "r")
        
        # Leggi le coordinate latitudine e longitudine di Era5Land
        era5land_lat = era5land.variables["latitude"][:]
        era5land_lon = era5land.variables["longitude"][:]
        
        # Trova gli indici più vicini alla latitudine e longitudine della stazione
        era5land_lat_ind = np.argmin(np.abs(era5land_lat - data['lat']))
        era5land_lon_ind = np.argmin(np.abs(era5land_lon - data['lon']))
        
        # Leggi le variabili per l'anno in corso
        t2m = np.array(era5land.variables["t2m"][:, era5land_lat_ind, era5land_lon_ind])  # Temperatura
        d2m = np.array(era5land_hum.variables["d2m"][:, era5land_lat_ind, era5land_lon_ind])  # 2 metre dewpoint temperature (in DEG)
        #p_surface = np.array(era5land_hum.variables["sp"][:, era5land_lat_ind, era5land_lon_ind])  # surface pressure (in Pa)
        u10 = np.array(era5land.variables["u10"][:, era5land_lat_ind, era5land_lon_ind])  # Componente u del vento
        v10 = np.array(era5land.variables["v10"][:, era5land_lat_ind, era5land_lon_ind])  # Componente v del vento
        tp = np.array(era5land.variables["tp"][:, era5land_lat_ind, era5land_lon_ind])  # Precipitazione
        
        # Calcola la velocità del vento
        vn10 = np.sqrt(u10 ** 2 + v10 ** 2)

        # calcola l'umidità relativa
        rh_era5land = relative_humidity(t2m, d2m)
        #print (t2m)
        #print (d2m)
        #print (p_surface)
        #print (rh_era5land)
        

        # Calcola il numero di giorni nell'anno (dipende se l'anno è bisestile)
        giorni_anno = 366 if anno % 4 == 0 else 365
                
        # Per ogni giorno, somma e calcola la media dei dati
        for giorno in range(giorni_anno):
            # Filtra i dati per il giorno specifico
            start_idx = giorno * 4  # Ogni giorno ha 4 intervalli di 6 ore
            end_idx = (giorno + 1) * 4
            
            # Estrai i dati di temperatura, precipitazione e velocità del vento per il giorno
            t2m_day = np.mean(t2m[start_idx:end_idx])
            vn10_day = np.mean(vn10[start_idx:end_idx])
            rh_day = np.mean(rh_era5land[start_idx:end_idx])
            tp_day = np.sum(tp[start_idx:end_idx])  # Somma le precipitazioni per il giorno
            
            # Aggiungi i dati giornalieri al dizionario della stazione
            era5land_results[station]['t2m_era5land'].append(t2m_day)
            era5land_results[station]['precipitation_era5land'].append(tp_day)
            era5land_results[station]['humidity_era5land'].append(rh_day)
            era5land_results[station]['wind_speed_era5land'].append(vn10_day)


# # Stampa la struttura del dizionario per ogni stazione
# for station, data in era5land_results.items():
#      print(f"Stazione: {station}")
#      print(f"  Numero di dati per la stazione: {len(data['t2m_era5land'])}")
#      print('-' * 40)  # Separatore per migliorare la leggibilità


#############################################
# REMOVING DATA FROM ERA5LAND DICTIONARY
#############################################

# Calcola la differenza tra le lunghezze
diff = len(era5land_results[name_station]['t2m_era5land']) - len(station_data[name_station]['t2m'])

# Rimuovi la quantità di dati dalla lista di era5land_results pari alla differenza
for station in station_names:
    era5land_results[station]['t2m_era5land'] = era5land_results[station]['t2m_era5land'][diff:]
    era5land_results[station]['humidity_era5land'] = era5land_results[station]['humidity_era5land'][diff:]
    era5land_results[station]['precipitation_era5land'] = era5land_results[station]['precipitation_era5land'][diff:]
    era5land_results[station]['wind_speed_era5land'] = era5land_results[station]['wind_speed_era5land'][diff:]

# Stampa la struttura del dizionario per ogni stazione
for station, data in era5land_results.items():
     print(f"Stazione: {station}")
     print(f"  Numero di dati per la stazione: {len(data['t2m_era5land'])}")
     print('-' * 40)  # Separatore per migliorare la leggibilità

#print (era5land_results[station]['humidity_era5land'])
#exit()

#####################################################
###################### WRF-WRFHYDRO ####################
#####################################################

# Percorso dei file WRF
wrf_file_path = "/path/to/ADRIACLIM-PLUS/data"

# Carica i file di riferimento per ottenere la griglia WRF
wrf_ref_file = open_ncfile("/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP/wrfout_d01_2019-01-01_00:00:00", "r")
lat_wrf = wrf_ref_file.variables["XLAT"][0, :, :]
lon_wrf = wrf_ref_file.variables["XLONG"][0, :, :]

# Crea una lista dei file WRF disponibili nel percorso
file_list = [f for f in os.listdir(wrf_file_path) if "wrfout" in f]

# Crea un dizionario vuoto per memorizzare i risultati per ogni stazione
wrf_results = {}

# Cicla attraverso ogni stazione e carica i dati
for station, data in station_data.items():

    # Crea un dizionario per la stazione
    wrf_results[station] = {
        't2m_wrf': [],
        'precipitation_wrf': [],
        'wind_speed_wrf': [],
        'humidity_wrf': [],
    }

    # Trova le coordinate della stazione
    st_lat = data['lat']
    st_lon = data['lon']

    #print (st_lat)
    #print (st_lon)

    # Trova l'indice della griglia WRF più vicino
    lat_ind = np.where(np.abs(lat_wrf[:,0]-st_lat) == np.min(np.abs(lat_wrf[:,0]-st_lat)))[0]
    lon_ind = np.where(np.abs(lon_wrf[0,:]-st_lon) == np.min(np.abs(lon_wrf[0,:]-st_lon)))[0]


    # Cicla su tutti gli anni per estrarre i dati
    for year in years:
        print (year)
        prec_val = []
        for month in months:
            print (month)
            for day in days[1::]:  # Partiamo dal giorno 01    #ORIG
            #for day in days:  # Partiamo dal giorno 0
                # Componi il nome del file WRF per questo giorno
                sim_file = f"wrfout_d01_{year}-{month}-{day}_00:00:00"
                #print (sim_file)

                # Verifica se il file esiste
                if sim_file in file_list:
                    wrf_file = open_ncfile(wrf_file_path + sim_file, "r")
                    
                    # Estrai le variabili necessarie
                    TH2 = np.array(wrf_file.variables["TH2"][:, lat_ind, lon_ind])
                    T2 = np.array(wrf_file.variables["T2"][:, lat_ind, lon_ind])
                    Q2 = np.array(wrf_file.variables["Q2"][:, lat_ind, lon_ind])
                    U10 = np.array(wrf_file.variables["U10"][:, lat_ind, lon_ind])
                    V10 = np.array(wrf_file.variables["V10"][:, lat_ind, lon_ind])
                    var_RAINC_start = np.array(wrf_file.variables["RAINC"][0, lat_ind, lon_ind])
                    var_RAINNC_start = np.array(wrf_file.variables["RAINNC"][0, lat_ind, lon_ind])
                    var_I_RAINC_start = np.array(wrf_file.variables["I_RAINC"][0, lat_ind, lon_ind])
                    var_I_RAINNC_start = np.array(wrf_file.variables["I_RAINNC"][0, lat_ind, lon_ind])

                    # Calcola la precipitazione e le altre variabili
                    prec_val.append (var_RAINC_start + var_RAINNC_start + (100 * var_I_RAINC_start) + (100 * var_I_RAINNC_start))
                    RH = np.mean(100 * ((100000 / ((TH2 / T2)**(1 / 0.286))) * Q2 / (Q2 * (1 - 0.622) + 0.622)) / 
                                 (611.2 * np.exp(17.67 * (T2 - 273.15) / (T2 - 29.65))))
                    VN10 = np.sqrt((U10 ** 2) + (V10 ** 2))

                    # # Aggiungi i risultati
                    # rh_sim.append(RH)
                    # t2m_sim.append(np.mean(T2))
                    # wind_sim.append(np.mean(VN10))

                    # Aggiungi i dati giornalieri al dizionario della stazione
                    wrf_results[station]['t2m_wrf'].append(np.mean(T2))
                    wrf_results[station]['wind_speed_wrf'].append(np.mean(VN10))
                    wrf_results[station]['humidity_wrf'].append(RH)

                    #print (wrf_results[station]['humidity_wrf'])

                    #exit()

        # Calcola la precipitazione giornaliera
        prec_val1 = np.array(prec_val).flatten()
        #prec = np.array(prec_val1[1::] - prec_val1[:-1])   #ORIG
        prec = np.diff(prec_val1, prepend=np.nan)       # aggiunge nan all'inizio 

        # Aggiungi i dati giornalieri al dizionario della stazione
        wrf_results[station]['precipitation_wrf'].append(prec)

        #print (wrf_results[station]['precipitation_wrf'])

#print ("PRECIP AFTER END LOOP INTO THE DIC", wrf_results[station]['precipitation_wrf'])     

# # Leggi il file JSON
# with open("wrf_results.json", "r", encoding="utf-8") as f:
#     dizionario = json.load(f)

# wrf_results = dizionario


# #############################################
# # REMOVING DATA FROM WRF DICTIONARY
# #############################################

# Calcola la differenza tra le lunghezze
diff = len(wrf_results[name_station]['t2m_wrf']) - len(station_data[name_station]['t2m'])

# Rimuovi la quantità di dati dalla lista di era5land_results pari alla differenza
for station in station_names:
    wrf_results[station]['t2m_wrf'] = wrf_results[station]['t2m_wrf'][diff:]
    #wrf_results[station]['precipitation_wrf'] = wrf_results[station]['precipitation_wrf'][diff:]
    wrf_results[station]['wind_speed_wrf'] = wrf_results[station]['wind_speed_wrf'][diff:]
    wrf_results[station]['humidity_wrf'] = wrf_results[station]['humidity_wrf'][diff:]

precip_wrf_extr = np.concatenate(wrf_results[station]['precipitation_wrf'])
print(f"Lunghezza dati concatenati: {len(precip_wrf_extr)}")

precip_wrf = precip_wrf_extr[diff:]
print(f"Lunghezza dati tagliati: {len(precip_wrf)}")


# Stampa la struttura del dizionario per ogni stazione
for station, data in wrf_results.items():
     print(f"Stazione: {station}")
     print(f"  Numero di dati per la stazione: {len(data['t2m_wrf'])}")
     print('-' * 40)  # Separatore per migliorare la leggibilità



############################################################################################################################################################
#################################
# AVERAGE DAY OF YEAR (ADOY) 
##################################

# Definisci l'intervallo di date (dal 2004 al 2020, un giorno alla volta)
date_range = pd.date_range(start=f"{begin_year}-{begin_month}-{begin_day}", end=f"{end_year}-{end_month}-{end_day}", freq="D")

# Crea un DataFrame con la colonna Data
df = pd.DataFrame({"Data": date_range})

# Popola il DataFrame con i dati osservati
# Supponiamo che tu voglia usare "station" come nome della stazione
station = name_station  # Modifica con la tua stazione specifica

# Temperature, precipitazione, vento e umidità osservati
df["T2m_OBS"] = station_data[station]["t2m"] # Temperature
df["Rain_OBS"] = station_data[station]["precipitation"]  # Precipitazione
df["Wind_OBS"] = station_data[station]["wind_speed"]  # Velocità vento
df["Hum_OBS"] = station_data[station]["humidity"]  # Umidità

# Aggiungi i dati di ERA5-Land
df["T2m_ERA5-Land"] = np.array(era5land_results[station]["t2m_era5land"]) - 273.15   # Temperature
df["Rain_ERA5-Land"] = np.array(era5land_results[station]["precipitation_era5land"])*1000  # Precipitazione
df["Wind_ERA5-Land"] = era5land_results[station]["wind_speed_era5land"]  # Velocità vento
df["Hum_ERA5-Land"] = era5land_results[station]["humidity_era5land"]  # relative humidity

# Aggiungi i dati di WRF (inclusa la precipitazione che è un np.array)
df["T2m_WRF"] = np.array(wrf_results[station]["t2m_wrf"]) - 273.15   # Temperature
df["Rain_WRF"] = precip_wrf  # Precipitazione (np.array)
df["Wind_WRF"] = wrf_results[station]["wind_speed_wrf"]  # Velocità vento
df["Hum_WRF"] = wrf_results[station]["humidity_wrf"]  # Umidità

# Visualizza le prime righe del DataFrame
print(df)

# Aggiungi una colonna per il giorno dell'anno (Day of Year)
df['DOY'] = df['Data'].dt.dayofyear

# Calcola la media per ogni giorno dell'anno per ciascuna variabile
df_doy_mean = df.groupby('DOY').agg({
    'T2m_OBS': 'mean',
    'Rain_OBS': 'mean',
    'Wind_OBS': 'mean',
    'Hum_OBS': 'mean',
    'T2m_ERA5-Land': 'mean',
    'Rain_ERA5-Land': 'mean',
    'Wind_ERA5-Land': 'mean',
    'Hum_ERA5-Land': 'mean',
    'T2m_WRF': 'mean',
    'Rain_WRF': 'mean',
    'Wind_WRF': 'mean',
    'Hum_WRF': 'mean',
}).reset_index()

# Visualizza il DataFrame con la media per ciascun giorno dell'anno
print(df_doy_mean)

# Creazione della figura con subplot
fig, axs = plt.subplots(2, 2, figsize=(20, 10))

# Titolo generale con il nome della stazione
fig.suptitle(f"Average day of year for {station}", fontsize=16, fontweight='bold')

# Mesi per l'asse X
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
month_positions = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]  # Approssimati per il DOY

# Funzione per personalizzare i subplot
def format_plot(ax, title, ylabel):
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_xticks(month_positions)
    ax.set_xticklabels(month_labels, fontsize=12)
    ax.legend()

# Temperatura
axs[0, 0].plot(df_doy_mean['DOY'], df_doy_mean['T2m_OBS'], label='Observations', color='blue')
axs[0, 0].plot(df_doy_mean['DOY'], df_doy_mean['T2m_ERA5-Land'], label='ERA5-Land', color='red')
axs[0, 0].plot(df_doy_mean['DOY'], df_doy_mean['T2m_WRF'], label='ADRIACLIM_PLUS', color='green')
format_plot(axs[0, 0], '2m Temperature (°C)', '2m Temperature (°C)')

# Precipitazione
axs[0, 1].plot(df_doy_mean['DOY'], df_doy_mean['Rain_OBS'], label='Observations', color='blue')
axs[0, 1].plot(df_doy_mean['DOY'], df_doy_mean['Rain_ERA5-Land'], label='ERA5-Land', color='red')
axs[0, 1].plot(df_doy_mean['DOY'], df_doy_mean['Rain_WRF'], label='ADRIACLIM_PLUS', color='green')
format_plot(axs[0, 1], 'Precipitation (mm)', 'Precipitation (mm)')

# Vento
axs[1, 0].plot(df_doy_mean['DOY'], df_doy_mean['Wind_OBS'], label='Observations', color='blue')
axs[1, 0].plot(df_doy_mean['DOY'], df_doy_mean['Wind_ERA5-Land'], label='ERA5-Land', color='red')
axs[1, 0].plot(df_doy_mean['DOY'], df_doy_mean['Wind_WRF'], label='ADRIACLIM_PLUS', color='green')
format_plot(axs[1, 0], 'Wind Speed (m/s)', 'Wind Speed (m/s)')

# Umidità
axs[1, 1].plot(df_doy_mean['DOY'], df_doy_mean['Hum_OBS'], label='Observations', color='blue')
axs[1, 1].plot(df_doy_mean['DOY'], df_doy_mean['Hum_ERA5-Land'], label='ERA5-Land', color='red')
axs[1, 1].plot(df_doy_mean['DOY'], df_doy_mean['Hum_WRF'], label='ADRIACLIM_PLUS', color='green')
format_plot(axs[1, 1], 'Relative Humidity (%)', 'Relative Humidity (%)')

# Migliora la disposizione
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Per non sovrapporre al titolo generale
plt.savefig(f"{station}_adoy_plot.png", bbox_inches='tight')


############################################
# COMPUTE STATISTICS FOR ADOY
############################################

########

# Esempio di utilizzo
f = open(filename_statistics, 'a')
f.write(f"#####################################\n")
f.write(f"ADOY STATISTICS\n")
f.write(f"#####################################\n")
f.close()

compute_and_print_statistics(df_doy_mean['T2m_OBS'], df_doy_mean['T2m_WRF'], df_doy_mean['T2m_ERA5-Land'], "2m Temperature (°C)", filename_statistics)
compute_and_print_statistics(df_doy_mean['Rain_OBS'], df_doy_mean['Rain_WRF'], df_doy_mean['Rain_ERA5-Land'], "Precipitation (mm)", filename_statistics)
compute_and_print_statistics(df_doy_mean['Wind_OBS'], df_doy_mean['Wind_WRF'], df_doy_mean['Wind_ERA5-Land'], "Wind Speed (m/s)", filename_statistics)
compute_and_print_statistics(df_doy_mean['Hum_OBS'], df_doy_mean['Hum_WRF'], df_doy_mean['Hum_ERA5-Land'], "Relative Humidity (%)", filename_statistics)

f = open(filename_statistics, 'a')
f.write(f"\n#####################################\n")
f.write(f"BOX PLOT STATISTICS\n")
f.write(f"#####################################\n")
f.close()


########################
# BOX PLOT
########################

# Funzione per calcolare le metriche statistiche
def calcola_metriche(dati):
    return {
        "Media": np.mean(dati),
        "Mediana": np.median(dati),
        "Deviazione Std": np.std(dati),
        "Q1": np.percentile(dati, 25),
        "Q3": np.percentile(dati, 75),
        "Min": np.min(dati),
        "Max": np.max(dati),
        "IQR": np.percentile(dati, 75) - np.percentile(dati, 25),
        "Asimmetria": skew(dati),
        "Curtosi": kurtosis(dati)
    }

# Funzione per creare le figure con tutti i box plot
def crea_boxplot_completo(df_obs, df_mod1, df_mod2, nomi_modelli, name_station,filename):
    variabili = ["2m Temperature (˚C)", "Precipitation (mm)", "Wind speed (m/s)", "Humidity (%)"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Box Plot - {name_station}", fontsize=14, fontweight='bold')
    
    palette = {"Observations": "blue", nomi_modelli[0]: "red", nomi_modelli[1]: "green"}
    metriche_originali, metriche_bias = {}, {}
    
    for ax, variabile in zip(axes.flatten(), variabili):
        dati = pd.DataFrame({
            "Observations": df_obs[variabile],
            nomi_modelli[0]: df_mod1[variabile],
            nomi_modelli[1]: df_mod2[variabile]
        })
        
        sns.boxplot(data=dati, ax=ax, palette=palette)
        ax.set_title(f"{variabile}")
        ax.set_ylabel(variabile)
        ax.grid(True, linestyle="--", alpha=0.6)

        # Imposta i limiti per la precipitazione
        if variabile == "Precipitation (mm)":
            ax.set_ylim(-2, 20)
        
        metriche_originali[variabile] = {col: calcola_metriche(dati[col].dropna()) for col in dati.columns}

        # # Stampa delle metriche a terminale
        # print(f"Metriche per {variabile}:")
        # for col, metriche in metriche_originali[variabile].items():
        #     print(f"{col}:")
        #     for metrica, valore in metriche.items():
        #         print(f"  {metrica}: {round(valore,2)}")
        # print("\n" + "-"*50 + "\n")

        with open(filename, 'a') as f:
            f.write(f"Metriche per {variabile}:\n")
            for col, metriche in metriche_originali[variabile].items():
                f.write(f"{col}:\n")
                for metrica, valore in metriche.items():
                    f.write(f"  {metrica}: {round(valore, 2)}\n")
            f.write("\n" + "-"*50 + "\n")
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f"{name_station}_BOX_PLOT_COMPLETO.png", bbox_inches='tight')
    plt.close()
    
    # Box plot dei bias
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Bias Box Plot - {name_station}", fontsize=14, fontweight='bold')

    # Aggiorna la palette per i bias
    palette_bias = {f"Bias {nomi_modelli[0]}": "red", f"Bias {nomi_modelli[1]}": "green"}
    
    for ax, variabile in zip(axes.flatten(), variabili):
        bias1 = df_mod1[variabile] - df_obs[variabile]
        bias2 = df_mod2[variabile] - df_obs[variabile]
        dati_bias = pd.DataFrame({
            f"Bias {nomi_modelli[0]}": bias1,
            f"Bias {nomi_modelli[1]}": bias2
        })
        
        sns.boxplot(data=dati_bias, ax=ax, palette=palette_bias)
        ax.set_title(f"{variabile}")
        ax.set_ylabel(f"Bias {variabile}")
        ax.grid(True, linestyle="--", alpha=0.6)

        # Imposta i limiti per la precipitazione
        if variabile == "Precipitation (mm)":
            ax.set_ylim(-20, 40)
        
        metriche_bias[variabile] = {col: calcola_metriche(dati_bias[col].dropna()) for col in dati_bias.columns}

        # # Stampa delle metriche del bias a terminale
        # print(f"Metriche Bias per {variabile}:")
        # for col, metriche in metriche_bias[variabile].items():
        #     print(f"{col}:")
        #     for metrica, valore in metriche.items():
        #         print(f"  {metrica}: {round(valore,2)}")
        # print("\n" + "-"*50 + "\n")

        with open(filename, 'a') as f:
            f.write(f"Metriche Bias per {variabile}:\n")
            for col, metriche in metriche_bias[variabile].items():
                f.write(f"{col}:\n")
                for metrica, valore in metriche.items():
                    f.write(f"  {metrica}: {round(valore, 2)}\n")
            f.write("\n" + "-"*50 + "\n")
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f"{name_station}_BOX_PLOT_BIAS.png", bbox_inches='tight')
    plt.close()
    
    return metriche_originali, metriche_bias

# Esempio di utilizzo con DataFrame ipotetici
df_obs = pd.DataFrame({
    "2m Temperature (˚C)": station_data[name_station]["t2m"],
    "Precipitation (mm)": station_data[name_station]["precipitation"],
    "Wind speed (m/s)": station_data[name_station]["wind_speed"],
    "Humidity (%)": station_data[name_station]["humidity"]
})

df_era5land = pd.DataFrame({
    "2m Temperature (˚C)": np.array(era5land_results[name_station]["t2m_era5land"])-273.15,
    "Precipitation (mm)": np.array(era5land_results[name_station]["precipitation_era5land"])*1000,
    "Wind speed (m/s)": era5land_results[name_station]["wind_speed_era5land"],
    "Humidity (%)": era5land_results[name_station]["humidity_era5land"]
})

df_wrf = pd.DataFrame({
    "2m Temperature (˚C)": np.array(wrf_results[name_station]["t2m_wrf"])-273.15,
    "Precipitation (mm)": precip_wrf,
    "Wind speed (m/s)": wrf_results[name_station]["wind_speed_wrf"],
    "Humidity (%)": wrf_results[name_station]["humidity_wrf"]
})

df_era5land.columns = df_obs.columns
df_wrf.columns = df_obs.columns

nomi_modelli = ["ERA5-Land", "ADRIACLIM_PLUS"]


# Generazione box plot completo e metriche
metriche_originali, metriche_bias = crea_boxplot_completo(df_obs, df_era5land, df_wrf, nomi_modelli, name_station, filename_statistics)



###################################################################### Plotting ############################################################################
#####################################
# PLOTTING TIMESERIES
#####################################

f = open(filename_statistics, 'a')
f.write(f"\n#####################################\n")
f.write(f"TIMESERIES STATISTICS\n")
f.write(f"#####################################\n")
f.close()


# Esempio di intervallo di date dal 2004 al 2020
start_date = datetime(begin_year, begin_month, begin_day)
#end_date = datetime(2006, 12, 31)  # for test
end_date = datetime(end_year, end_month, end_day)

# Genera una lista di date con frequenza giornaliera
dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# Estrai i primi giorni di ogni anno
#years = range(2004, 2007)  # for test
years = range(begin_year, end_year+1)
year_starts = [datetime(year, 1, 1) for year in years]

# Ottieni le posizioni dei ticks corrispondenti al primo giorno di ogni anno
tick_positions = [(date - start_date).days for date in year_starts]
tick_labels = [date.strftime("%Y") for date in year_starts]

# Aggiungi la data del primo dato plottato
first_data_label = start_date.strftime("%d-%m-%Y")
first_data_position = 0

tick_positions_with_first = [first_data_position] + tick_positions
tick_labels_with_first = [first_data_label] + tick_labels

################################
################# Plot RH ###############
###############################

for station, data in station_data.items():
    print ('**************************')
    print(f"Plotting RH for station: {station}")
    print ('**************************')

    # Crea il grafico
    fig = plt.figure(num=None, figsize=(20, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.subplots_adjust(hspace=0.6, wspace=0.1)
    plt.rc('xtick', labelsize=25)
    plt.rc('ytick', labelsize=25)

    ax = fig.add_subplot(111)

    ax.set_xlabel('Years', fontsize=25, labelpad=15)
    ax.set_ylabel('RH (%)', fontsize=25, labelpad=10)
    ax.tick_params(axis='y', colors='black', which='both', width=2)
    ax.yaxis.label.set_color('black')
    ax.set_yticks(np.arange(0, 120, 10))
    ax.set_xticks(tick_positions_with_first)
    ax.set_xticklabels(tick_labels_with_first, rotation=90)
    ax.set_xlim(0, len(dates) - 1)
    ax.set_ylim(0, 110)

    humidity_wrf = np.array(wrf_results[station]['humidity_wrf'])

    ax.plot(np.arange(0, len(dates)), station_data[station]['humidity'], linestyle='-', color='blue', linewidth=2.0)
    ax.plot(np.arange(0, len(dates)), humidity_wrf, linestyle='-', color='green', linewidth=1.0)
    ax.plot(np.arange(0, len(dates)), era5land_results[station]['humidity_era5land'], linestyle='-', color='red', linewidth=1.0)

    plt.legend(labels=['Observations', 'ADRIACLIM_PLUS','ERA5-Land'], fontsize=20, loc='upper center', bbox_to_anchor=(0.7, -0.5))
    plt.savefig(f"{station}_timeseries_RH_plot_ADOY.png", bbox_inches='tight')
    plt.clf()

    ### Statistics ###
    obs_rh = np.array(station_data[station]['humidity'])
    era5land_rh = np.array(era5land_results[station]['humidity_era5land'])

    compute_and_print_statistics(obs_rh, humidity_wrf, era5land_rh, "Relative humidity (%)", filename_statistics)

###################


################################
################# Plot T2m ###############
###############################

for station, data in station_data.items():
    print()
    print ('**************************')
    print(f"Plotting 2m TEMPERATURE for station: {station}")
    print ('**************************')

    # Crea il grafico
    fig = plt.figure(num=None, figsize=(20, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.subplots_adjust(hspace=0.6, wspace=0.1)
    plt.rc('xtick', labelsize=25)
    plt.rc('ytick', labelsize=25)

    ax = fig.add_subplot(111)

    ax.set_xlabel('Years', fontsize=25, labelpad=15)
    ax.set_ylabel('Temperature (˚C)', fontsize=25, labelpad=10)
    ax.tick_params(axis='y', colors='black', which='both', width=2)
    ax.yaxis.label.set_color('black')
    #ax.set_yticks(np.arange(-5, 35, 5))
    ax.set_xticks(tick_positions_with_first)
    ax.set_xticklabels(tick_labels_with_first, rotation=90)
    ax.set_xlim(0, len(dates) - 1)
    #ax.set_ylim(-5, 35)

    t2m_wrf = np.array(wrf_results[station]['t2m_wrf'])-273.15
    #t2m_wrf = (t2m_wrf_extr[0,120:397])-273.15
    t2m_era5land_plot = np.array(era5land_results[station]['t2m_era5land'])-273.15

    ax.plot(np.arange(0, len(dates)), station_data[station]['t2m'], linestyle='-', color='blue', linewidth=2.0)
    ax.plot(np.arange(0, len(dates)), t2m_wrf, linestyle='-', color='green', linewidth=1.0)
    ax.plot(np.arange(0, len(dates)), t2m_era5land_plot, linestyle='-', color='red', linewidth=1.0)

    plt.legend(labels=['Observations', 'ADRIACLIM_PLUS', 'ERA5-Land'], fontsize=20, loc='upper center', bbox_to_anchor=(0.7, -0.5))
    plt.savefig(f"{station}_timeseries_T2M_plot_ADOY.png", bbox_inches='tight')
    plt.clf()

    ### Statistics ###
    obs_t2m = np.array(station_data[station]['t2m'])
    era5land_t2m = np.array(era5land_results[station]['t2m_era5land'])-273.15

    compute_and_print_statistics(obs_t2m, t2m_wrf, era5land_t2m, "Temperature (˚C)", filename_statistics)

###################


################################
################# Plot Wind Speed ###############
###############################

for station, data in station_data.items():
    print()
    print ('**************************')
    print(f"Plotting Wind speed for station: {station}")
    print ('**************************')

    # Crea il grafico
    fig = plt.figure(num=None, figsize=(20, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.subplots_adjust(hspace=0.6, wspace=0.1)
    plt.rc('xtick', labelsize=25)
    plt.rc('ytick', labelsize=25)

    ax = fig.add_subplot(111)

    ax.set_xlabel('Years', fontsize=25, labelpad=15)
    ax.set_ylabel('Wind speed (m/s)', fontsize=25, labelpad=10)
    ax.tick_params(axis='y', colors='black', which='both', width=2)
    ax.yaxis.label.set_color('black')
    #ax.set_yticks(np.arange(0, 6, 1))
    ax.set_xticks(tick_positions_with_first)
    ax.set_xticklabels(tick_labels_with_first, rotation=90)
    ax.set_xlim(0, len(dates) - 1)
    #ax.set_ylim(0, 6)

    wind_speed_wrf = np.array(wrf_results[station]['wind_speed_wrf'])
    #wind_speed_wrf = wind_speed_wrf_extr[0,120:397]
    wind_speed_era5land_plot = np.array(era5land_results[station]['wind_speed_era5land'])

    #print (station_data[station]['wind_speed'])

    ax.plot(np.arange(0, len(dates)), station_data[station]['wind_speed'], linestyle='-', color='blue', linewidth=2.0)
    ax.plot(np.arange(0, len(dates)), wind_speed_wrf, linestyle='-', color='green', linewidth=1.0)
    ax.plot(np.arange(0, len(dates)), wind_speed_era5land_plot, linestyle='-', color='red', linewidth=1.0)

    plt.legend(labels=['Observations', 'ADRIACLIM_PLUS', 'ERA5-Land'], fontsize=20, loc='upper center', bbox_to_anchor=(0.7, -0.5))
    plt.savefig(f"{station}_timeseries_Wind_Speed_plot_ADOY.png", bbox_inches='tight')
    plt.clf()

    ### Statistics ###
    obs_wind_speed = np.array(station_data[station]['wind_speed'])
    era5land_wind_speed = np.array(era5land_results[station]['wind_speed_era5land'])
    
    compute_and_print_statistics(obs_wind_speed, wind_speed_wrf, era5land_wind_speed, "Wind speed (m/s)", filename_statistics)


###################



################################
################# Plot Precipitation ###############
###############################

for station, data in station_data.items():
    print()
    print ('**************************')
    print(f"Plotting Precipitation for station: {station}")
    print ('**************************')

    # Crea il grafico
    fig = plt.figure(num=None, figsize=(20, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.subplots_adjust(hspace=0.6, wspace=0.1)
    plt.rc('xtick', labelsize=25)
    plt.rc('ytick', labelsize=25)

    ax = fig.add_subplot(111)

    ax.set_xlabel('Years', fontsize=25, labelpad=15)
    ax.set_ylabel('Precipitation (mm/day)', fontsize=25, labelpad=10)
    ax.tick_params(axis='y', colors='black', which='both', width=2)
    ax.yaxis.label.set_color('black')
    #ax.set_yticks(np.arange(0, 200, 20))
    ax.set_xticks(tick_positions_with_first)
    ax.set_xticklabels(tick_labels_with_first, rotation=90)
    ax.set_xlim(0, len(dates) - 1)
    #ax.set_ylim(0, 220)

    precip_era5land_plot = np.array(era5land_results[station]['precipitation_era5land'])*1000

    precip_obs = np.array(station_data[station]['precipitation'])
   
    # computing the cumulated precipitation for wrf and era5land
    precip_wrf_cumsum = np.array(np.nancumsum(precip_wrf))

    precip_era5land_cumsum = np.cumsum(precip_era5land_plot)

    # here the part written by Veera for matching wrf output with observations when the latest are missing
    
    ### shifting observation data ###
    if shift_flag != 0:
        aa = np.where(precip_obs<0,0,precip_obs)
        #print (aa)
        precip_obs_cumsum = np.nancumsum(aa)
        #print (precip_obs_cumsum)
        switch=0
        for ii in range(0,len(precip_obs)):
        #for ii in range(0,10):
            #print ("n. dato: ", ii)
            #print ("i-esimo dato:", precip_obs[ii])
            if np.isnan(precip_obs[ii]):
                switch=1
            #print ("Switch: ", switch)
            if np.isnan(precip_obs[ii]) and switch == 1:
                #print ("Sono nel loop dopo il controllo dello switch")
                diff = precip_wrf_cumsum[ii] - precip_obs_cumsum[ii]
                #print ("Diff: ", diff)
                switch=0
                if diff > 0:
                    #print ("Prima della sostituzione con la diff: ", precip_obs_cumsum[ii:])
                    precip_obs_cumsum[ii:] = precip_obs_cumsum[ii:] + diff
                    #print ("Dopo della sostituzione con la diff: ", precip_obs_cumsum[ii:])
                    #print ("Vettore che raccoglie la cum per le obs: ", precip_obs_cumsum)
            #else:
            #    print ("Non sono nel loop in quanto non soddifo l'if")
            #    print ("Vettore che raccoglie la cum per le obs: ", precip_obs_cumsum)

        #precip_obs_masked_cumsum_updated = np.ma.masked_where(np.array(precip_obs)<0,precip_obs_cumsum)    # ORIG
        precip_obs_masked_cumsum_updated = np.where(precip_obs < 0, np.nan, precip_obs_cumsum)
        #print (precip_obs_masked_cumsum_updated)

    else:
        #precip_obs_masked_cumsum_updated = np.copy(precip_obs_masked_cumsum)   # ORIG
        #precip_obs_masked_cumsum_updated = np.ma.masked_where(np.array(precip_obs_masked)<0,precip_obs_masked_cumsum)  # ORIG
        precip_obs_masked_cumsum_updated = np.copy(precip_obs_masked_cumsum)   
        precip_obs_masked_cumsum_updated = np.where(precip_obs_masked<0, np.nan, precip_obs_masked_cumsum)
        #print (precip_obs_masked_cumsum_updated)
         
#################################

    # left y-axis: daily cumulated precipitation
    ax.plot(np.arange(0, len(dates)), precip_obs, linestyle='-', color='blue', linewidth=2.0)
    ax.plot(np.arange(0, len(dates)), precip_wrf, linestyle='-', color='green', linewidth=1.0)
    ax.plot(np.arange(0, len(dates)), precip_era5land_plot, linestyle='-', color='red', linewidth=1.0)

    ax2 = ax.twinx()
    ax2.set_ylabel("Acc. precipitation (mm)", fontsize=25,labelpad=8)
    #ax2.set_ylim(0, 40000)
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.tick_params(which='both', width=2)
    ax2.tick_params(which='major', length=7)
    ax2.tick_params(which='minor', length=4)

    ax2.plot(np.arange(0, len(dates)), precip_obs_masked_cumsum_updated, linestyle='-', color='blue', linewidth=2.0)
    ax2.plot(np.arange(0, len(dates)), precip_wrf_cumsum, linestyle='-', color='green', linewidth=2.0)
    ax2.plot(np.arange(0, len(dates)), precip_era5land_cumsum, linestyle='-', color='red', linewidth=2.0)

    #print (precip_wrf_cumsum)
    #print (precip_obs_masked_cumsum_updated)

    #print (len(precip_obs_masked_cumsum_updated))
    #print (len(precip_wrf_cumsum))

    plt.legend(labels=['Observations', 'ADRIACLIM_PLUS', 'ERA5-Land'], fontsize=20, loc='upper center', bbox_to_anchor=(0.7, -0.5))
    plt.savefig(f"{station}_timeseries_Precipitation_plot_ADOY.png", bbox_inches='tight')


    ### Statistics ###
    # TODO: ADD CUMULATED RAINFALL STATISTICS????
    

    obs_precip = np.array(station_data[station]['precipitation'])
    era5land_precip = precip_era5land_plot

    f = open(filename_statistics, 'a')
    f.write(f"\nTOTAL PRECIPITATION (OBS): {np.nansum(precip_obs)}\n")
    f.write(f"TOTAL PRECIPITATION (ADRIACLIM): {np.nansum(precip_wrf)}\n")
    f.write(f"TOTAL PRECIPITATION (ERA5-LAND): {np.nansum(precip_era5land_plot)}\n")
    f.close()

    compute_and_print_statistics(obs_precip, precip_wrf, era5land_precip, "Precipitation (mm/day)",filename_statistics)

    
    

###################
####################################################################################################################################
