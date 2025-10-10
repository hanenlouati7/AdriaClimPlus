- Script to compare ADRIACLIM_PLUS EVALUATION RUN (30 YEARS, 1990-2020) with Atmospheric in-situ station data

- How to execute the script:

Run the bash script 'execute_comparison_in-situ_stations.sh'

- Variables and datasets considered 

The script 'plot_timeseries_adoy_box_plot_prec_t2m_wind_speed_hum_DELO.py' allows for the comparison of the following outputs:

a. ADRIACLIM_PLUS EVALUATION RUN; 
b. ERA5-LAND dataset; 
c. in-situ observations (where available);

The atmospheric variables processed are:

a. total precipitation (in mm);
b. relative humidity at 2m (%);
c. wind speed (in m/s);
d. air temperature at 2m (in ˚C);

- Types of plots generated

The script produces the following plots:

1. daily mean timeseries for the 4 variables mentioned above covering the overlapping time interval among the 3 datasets;
2. average day-of-year timeseries (ADOY);
3. box plot to evaluate the data distribution;
4. box plot to evaluate the bias with respect the avaiable in-situ observations for the 2 models.

- Statistics computed

For the timeseries listed above (types 1,2), and for all 4 variables (where available), the script computes:

a. bias with respect in-situ observations;
b. RMSE (Root Mean Square Error);
c. NRMSE (Normalized RMSE);
d. MAE (Mean Absolute Error;
e. R2 (Coefficient of Determination);
f. CORRELATION (Pearson correlation).

For box-plots (types 3,4), the script computes:

a. average;
b. median (Q2 or 50th percentile);
c. Standard deviation;
d. Lower Quartile (Q1 or 25th percentile);
e. Upper Quartile (Q3 or 75th percentile)
f. Whiskers lower limit: Q1 - 1.5*IQR;
g. Whiskers upper limit: Q3 + 1.5*IQR;
h. Interquartile Range (IQR);
i. Skewness;
j. Kurtosis.

All computed statistics are saved in an external .txt file.

- Files/information needed to execute the script

To run the script, the following information must be modified inside the script:

a. path to the ADRIACLIM_PLUS output;
b. path to the ERA5-LAND dataset;
c. path to IN-SITU observation datasets (evaluated regions: Emilia Romagna, Veneto, Friuli Venezia Giulia, Marche, Puglia, Croatia);
d. start date of in-situ observations;
e. end date of in-situ observations;
f. name of the in-situ station to be evaluated.