import pandas as pd
from datetime import datetime

def calcola_media_giornaliera(file_input, file_output):
    # Definisci il formato della data
    data_format = "%Y-%m-%d %H:%M:%S"  # Modifica questo formato in base al formato delle tue date
    
    # Funzione per convertire le date
    def parse_dates(x):
        # Rimuovi la virgola alla fine e prova a convertire la data
        x = str(x).strip(',')  # Rimuove la virgola finale se presente
        return datetime.strptime(x, data_format)
    
    # Legge il file di input, usando la virgola come separatore e il formato definito per le date
    df = pd.read_csv(file_input, header=None, sep=',', parse_dates=[1], 
                     names=["col1", "data", "id_bacino", "col4", "col5", "discharge", "col7", "col8"])
    
    # Gestisci la colonna delle date separatamente
    df['data'] = pd.to_datetime(df['data'], errors='coerce', format=data_format)
    
    # Conversione della colonna discharge in numerico, gestendo errori
    df["discharge"] = pd.to_numeric(df["discharge"], errors="coerce")
    
    # Rimuove righe con valori NaN in discharge o data
    df = df.dropna(subset=["discharge", "data"])
    
    # Verifica il numero di righe per giorno
    counts = df.groupby(df['data'].dt.date)['data'].count()
    giorni_errati = counts[counts != 145].index.tolist()
    if giorni_errati:
        print(f"Attenzione! I seguenti giorni hanno un numero errato di valori: {giorni_errati}")
    
    # Calcola la media giornaliera per ogni ID bacino
    df['data'] = df['data'].dt.date  # Mantiene solo la parte di data senza ora
    media_giornaliera = df.groupby(["data", "id_bacino"])["discharge"].mean().reset_index()
    
    # Salva l'output in un file CSV
    media_giornaliera.to_csv(file_output, index=False, header=False)
    
    print(f"Media giornaliera calcolata e salvata in {file_output}")

# Esempio di utilizzo
calcola_media_giornaliera("REF_ADRIACLIM_PLUS_EVAL_RUN_30_YEARS_1990_2020.txt", "output.csv")
