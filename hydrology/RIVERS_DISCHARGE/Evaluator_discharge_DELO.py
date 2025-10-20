### This is a python script to compare river discharge from AdriaClimPLUS output with EFAS dataset and observations ###
### Author: Alessandro De Lorenzis ###
### Project: AdriaClim PLUS ###
### Date: 12-February-2025 ###

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import hydroeval as he
import numpy as np
import matplotlib
import matplotlib.dates as mdates
import csv

base_dir_figure="/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/DISCHARGE/make_plots/figures"
base_dir ="/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/DISCHARGE/make_plots"

# upload file with observations
df_obs = pd.read_csv("discharge_obs_range_1990_2023_ADRIACLIM_PLUS.csv", sep=";")
# Converti la colonna 'Datetime' con il formato corretto
df_obs["Datetime"] = pd.to_datetime(df_obs["Datetime"], format="%d/%m/%y %H:%M", errors="coerce")
df_obs.set_index("Datetime", inplace=True)

# upload file with Efas predictions
df_Efas = pd.read_csv("Portate_Efas_Daily_1991_2020.csv")
df_Efas["Datetime"] = pd.to_datetime(df_Efas["Datetime"],format='%Y-%m-%d',errors="coerce")
df_Efas.set_index ("Datetime", inplace=True)
#df_Efas = df_Efas.set_index(df_Efas['Datetime'])
#df_Efas.index.name = 'Datetime'
#print (df_Efas)

#upload the file with WRF-WRF-HYDRO data
# the file is organized as DATE, ID BACINO, DAILY_MEAN
df_pred = pd.read_csv(base_dir+"/DAILY_MEAN_DISCHARGE_ADRIACLIM_PLUS_EVAL_RUN_30_YEARS_1990_2020.txt", sep=",", header=None, names=["Data", "ID_Bacino", "Discharge"])
df_pred = df_pred.set_index(df_pred['Data'])
df_pred.index.name = 'Datetime'
#print (df_pred)
#print (df_pred['Data'])

# Modifichiamo il dataframe dell'output di WRF-WRFHYDRO in modo che abbia lo stesso aspetto degli altri due,
# ossia con prima colonna data e colonne successive quelle dei fiumi con relativi discharge

# Carica il file con ID Bacino e Nome Fiume
fiumi_df = pd.read_csv("Rivers_name_ID_bacini_WRF_WRFHYDRO.txt", sep=r"\s+", header=None, names=["ID_Bacino", "Nome_Fiume"])
#print (fiumi_df)

# Unisci i due DataFrame in base all'ID Bacino
# Ora il DataFrame ha le colonne: Datetime, ID_Bacino, Discharge, Nome_Fiume
df_pred_new = pd.merge(df_pred, fiumi_df, on="ID_Bacino")

# Crea il DataFrame finale con la data e una colonna per ogni fiume
final_df_pred = df_pred_new.pivot_table(index="Data", columns="Nome_Fiume", values="Discharge", aggfunc="mean")

# Ripristina l'ordine originale delle colonne (in base all'ordine nel file 'file_fiumi.csv')
column_order = fiumi_df['Nome_Fiume'].tolist()
final_df_pred = final_df_pred[column_order]

#print(final_df_pred.columns)

# Mostra il DataFrame finale
final_df_pred.index.name = 'Datetime'
final_df_pred.index = pd.to_datetime(final_df_pred.index, format='%Y-%m-%d')

#print (final_df_pred.index)
#print (final_df_pred.columns)

#####################################
# EXTRACTION OF THE COMMON DATES
#####################################

# since EFAS dataset is available starting from 1991-01-01, we will extract from the 3 dataframes just the data starting from this data and till 2020-12-31

# Definizione delle date di inizio e fine
start_date_slice = "1991-01-02"
end_date_slice = "2020-12-31"

# Filtra le righe comprese tra data_inizio e data_fine
df_obs_sliced = df_obs[(df_obs.index >= start_date_slice) & (df_obs.index <= end_date_slice)]
#df_obs_sliced = df_obs[(df_obs["Datetime"] >= start_date_slice) & (df_obs["Datetime"] <= end_date_slice)]
#df_efas_sliced = df_Efas[(df_Efas["Datetime"] >= start_date_slice) & (df_Efas["Datetime"] <= end_date_slice)]
df_efas_sliced = df_Efas[(df_Efas.index >= start_date_slice) & (df_Efas.index <= end_date_slice)]
df_pred_sliced = final_df_pred[(final_df_pred.index >= start_date_slice) & (final_df_pred.index <= end_date_slice)]



#####################################
# EXTRACTION OF THE FIRST AVAILABLE OBS DATUM
#####################################

# Inizializza una lista vuota per memorizzare i risultati
results = []

# Itera sulle colonne (eccetto la prima, che è la data)
for column in df_obs_sliced.columns:
    # Trova il primo e l'ultimo valore non NaN
    first_valid_index = df_obs_sliced[column].first_valid_index()
    last_valid_index = df_obs_sliced[column].last_valid_index()
    
    # Ottieni le date corrispondenti
    start_date = first_valid_index if first_valid_index is not None else None
    end_date = last_valid_index if last_valid_index is not None else None
    
    # Aggiungi i risultati alla lista
    results.append([column, start_date, end_date])

# Crea un DataFrame con i risultati
df_start_end = pd.DataFrame(results, columns=["Nome_Fiume", "Data_Inizio_Obs", "Data_Fine_Obs"])

# Visualizza il DataFrame risultante
#print(df_start_end)
#print (df_start_end["Nome_Fiume"])


################################
# PLOTS AND COMPUTING STATISTICS
################################

#colormap = matplotlib.colormaps['rainbow'].resampled(5)

nse = []
kge = []
ratVol = []
nse_efas = []
kge_efas = []
ratVol_efas = []

for bacino in df_start_end["Nome_Fiume"]:
	print(bacino)
	#print(df_obs_sliced[str(bacino)])
	#print(df_Efas[str(bacino)])
		
	plt.rcParams["figure.figsize"] = (20,10)
	
	nseRaw =[]
	kgeRaw =[]
	ratioRaw =[]
	nseRaw_efas =[]
	kgeRaw_efas =[]
	ratioRaw_efas =[]

	#for exp in range(6,11):
	plt.plot(df_efas_sliced[bacino], color='blue', label="Efas", linewidth=1.5)
	plt.plot(df_pred_sliced[bacino], color='red', label="ADRIACLIM PLUS", linewidth=1.5)
	plt.plot(df_obs_sliced[bacino], color = 'black', label ="Observed", linewidth=1.5)

	plt.rcParams.update({'font.size': 20})

	# Imposta la dimensione dei numeri sugli assi
	plt.xticks(fontsize=20)
	plt.yticks(fontsize=20)
	plt.legend(fontsize=20)
	plt.ylabel('Discharge [m³/s]', fontsize=20)
	plt.xlabel ('Years', fontsize=20)
	# beautify the x-labels
	plt.xticks(rotation=45)
		
	#merge tra i dati di WRF_WRF-HYDRO e quelli delle osservazioni	
	Po = pd.merge(df_pred_sliced[bacino], df_obs_sliced[bacino], left_index=True, right_index=True, how='inner')
	Po_efas = pd.merge(df_efas_sliced[bacino], df_obs_sliced[bacino], left_index=True, right_index=True, how='inner')
	#esclude i NaN
	Po2 = Po.dropna()
	Po2_efas = Po_efas.dropna()
	#Nash-Sutcliffe Efficiency (NSE)
	nseH = he.evaluator(he.nse, Po2[bacino+'_x'].values, Po2[bacino+'_y'].values)
	nseH_efas = he.evaluator(he.nse, Po2_efas[bacino+'_x'].values, Po2_efas[bacino+'_y'].values)
	#Kling-Gupta Efficiency (KGE)
	kgeH = he.evaluator(he.kge, Po2[bacino+'_x'].values, Po2[bacino+'_y'].values)
	kgeH_efas = he.evaluator(he.kge, Po2_efas[bacino+'_x'].values, Po2_efas[bacino+'_y'].values)
	#Bias percentuale tra previsione e osservazione
	ratioH = (Po2[bacino+'_x'].mean() - Po2[bacino+'_y'].mean())/Po2[bacino+'_y'].mean()*100
	ratioH_efas = (Po2_efas[bacino+'_x'].mean() - Po2_efas[bacino+'_y'].mean())/Po2_efas[bacino+'_y'].mean()*100
		
	nseRaw.append(nseH[0])
	kgeRaw.append(kgeH[0,0])
	ratioRaw.append(ratioH)
	nseRaw_efas.append(nseH_efas[0])
	kgeRaw_efas.append(kgeH_efas[0,0])
	ratioRaw_efas.append(ratioH_efas)
			
	nse.append(nseRaw)
	kge.append(kgeRaw)
	ratVol.append(ratioRaw)		
	nse_efas.append(nseRaw_efas)
	kge_efas.append(kgeRaw_efas)
	ratVol_efas.append(ratioRaw_efas)

	start_date = df_start_end.loc[df_start_end["Nome_Fiume"] == bacino, "Data_Inizio_Obs"].values
	end_date = df_start_end.loc[df_start_end["Nome_Fiume"] == bacino, "Data_Fine_Obs"].values

	#print (start_date)
	#print (end_date)
	
	#df_efas_sliced.info()
	#df_efas_sliced['Datetime'] = pd.to_datetime(df_efas_sliced['Datetime'])
	
	# Converti datetime64[ns] in una lista di oggetti datetime
	#dates = pd.to_datetime(df_efas_sliced[bacino])
	#print (dates)
	
	if bacino == 'PoPontelagoscuro':
		plt.title(f'Po, {start_date[0].astype("datetime64[D]")} - {end_date[-1].astype("datetime64[D]")}')
	elif bacino == 'ZitomislicNeretvaStation':
		plt.title(f'Neretva, {start_date[0].astype("datetime64[D]")} - {end_date[-1].astype("datetime64[D]")}')
	else:
		plt.title(f'{bacino}, {start_date[0].astype("datetime64[D]")} - {end_date[-1].astype("datetime64[D]")}')



	# Impostiamo l'asse X con solo il 1° gennaio di ogni anno
	plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # Localizzatore per ogni anno
	# Impostiamo il formatter per visualizzare la data nel formato desiderato
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Mostra solo l'anno

	plt.xlim(left=pd.to_datetime(start_date),right=pd.to_datetime(end_date))

	plt.legend()

	if bacino == 'PoPontelagoscuro':
		plt.savefig(base_dir_figure+'/Po.png')
	elif bacino == 'ZitomislicNeretvaStation':
		plt.savefig(base_dir_figure+'/Neretva.png')
	else:
		plt.savefig(base_dir_figure+'/'+bacino+'.png')
	
	plt.clf()
	

#print(kge)


# Creiamo una lista di righe
header = ["Nome_Fiume", "Start_date", "End_date", "NSE-ADRIACLIM", "NSE-EFAS", 
          "KGE-ADRIACLIM", "KGE-EFAS", "ratVol-ADRIACLIM", "ratVol-EFAS"]

# Troviamo la larghezza massima di ogni colonna per un migliore allineamento
col_widths = [max(len(h), 20) for h in header]  # Nome fiume almeno 20 caratteri

rows = []
for i, nome_fiume in enumerate(df_start_end['Nome_Fiume']):
    nse_value = float(nse[i]) if isinstance(nse[i], (int, float)) else nse[i][0]
    kge_value = float(kge[i]) if isinstance(kge[i], (int, float)) else kge[i][0]
    ratVol_value = float(ratVol[i]) if isinstance(ratVol[i], (int, float)) else ratVol[i][0]

    nse_value_efas = float(nse_efas[i]) if isinstance(nse_efas[i], (int, float)) else nse_efas[i][0]
    kge_value_efas = float(kge_efas[i]) if isinstance(kge_efas[i], (int, float)) else kge_efas[i][0]
    ratVol_value_efas = float(ratVol_efas[i]) if isinstance(ratVol_efas[i], (int, float)) else ratVol_efas[i][0]

    row = [
        nome_fiume.ljust(col_widths[0]),  
        str(df_start_end.loc[df_start_end["Nome_Fiume"] == nome_fiume, "Data_Inizio_Obs"].iloc[0].date()).rjust(col_widths[1]),  
        str(df_start_end.loc[df_start_end["Nome_Fiume"] == nome_fiume, "Data_Fine_Obs"].iloc[0].date()).rjust(col_widths[2]),  
        f"{nse_value:.4f}".rjust(col_widths[3]),  
        f"{nse_value_efas:.4f}".rjust(col_widths[4]),  
        f"{kge_value:.4f}".rjust(col_widths[5]),  
        f"{kge_value_efas:.4f}".rjust(col_widths[6]),  
        f"{ratVol_value:.4f}".rjust(col_widths[7]),  
        f"{ratVol_value_efas:.4f}".rjust(col_widths[8])
    ]
    
    rows.append(row)

# Scrittura in file con formato tabellare
output_file = base_dir_figure + "/STATS_NSE_KGE_RatVol_ADRIACLIM_PLUS_EVAL_RUN_1990_2020.txt"

with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow([h.ljust(col_widths[i]) for i, h in enumerate(header)])  # Scrive l'intestazione allineata
    writer.writerows(rows)  # Scrive i dati allineati

print(f"File salvato correttamente: {output_file}")
