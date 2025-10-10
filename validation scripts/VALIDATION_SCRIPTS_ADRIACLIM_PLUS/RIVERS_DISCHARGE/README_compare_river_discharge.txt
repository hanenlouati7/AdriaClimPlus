- Script to compare ADRIACLIM_PLUS EVALUATION RUN (30 YEARS, 1990-2020) with river discharge observations

- How to execute the script:

Run the python script 'Evaluator_discharge_DELO.py'

- Variables and datasets considered 

The script compares the following outputs:

a. ADRIACLIM_PLUS EVALUATION RUN; 
b. EFAS dataset; 
c. in-situ observations (where available);

The hydrological variable processed is river discharge. 

- Type of plot generated

The script produces river discharge timeseries for 12 of the 145 catchments where observations are available: Po, Livenza, Brenta, Piave, Isonzo, Ofanto, Tagliamento, Neretva, Adige, Foglia, Potenza, Tronto.

- Statistics computed

The script computes the following statistics:

a. KGE (Kling-Gupta Efficency);
b. NSE (Nash-Sutcliffe Efficiency);
c. ratio of volumes (in %, representing how much volume is modeled compared to the observation);

All computed statistics are saved in an external .txt file.

- Files/information needed to execute the script

To run the script, the following information must be modified within the script:

a. path to the ADRIACLIM-PLUS output (to be created using the provided script: 'compute_daily_mean_WRF-WRF_HYDRO_exps.py');
b. path to the EFAS dataset (provided in the folder for the range 1991-2020: 'Portate_Efas_Daily_1991_2020.csv');
c. path to IN-SITU observation dataset (provided in the folder for the range 1990-2023: 'discharge_obs_range_1990_2023_ADRIACLIM_PLUS.csv').
