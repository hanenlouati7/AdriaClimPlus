- Scripts to compare ADRIACLIM_PLUS EVALUATION RUN (30 YEARS, 1990-2020) with ERA5-Land rainfall 

There are 3 directories.

STEP 1: Compute ERA5-Land rainfall

a. Go into the 'ERA5_LAND_RAINFALL_EXTRACTION' directory;
b. Execute the bash script 'submit_ERA5_to_wrf_grid_precip.sh' to run the NCL script 'compute_era5land_rain_basins_on_wrf_grid.ncl'. This script regrids the ERA5-Land data onto the WRF grid;
c. Execute the bash script 'compute_era5land_precip.sh' to run the python script 'single_years_extraction_ERA5_cumulated_rain.py' (or '30years_extraction_ERA5_cumulated_rain.py'). These scripts calculate rainfall 
   according to ERA5-Land over the 145 defined catchments.

 STEP 2: Compute WRF-WRF-HYDRO rainfall 

 a. Go into the 'WRF_WRF_HYDRO_EVAL_RAINFALL_EXTRACTION' directory;
 b. Execute the python script 'extract_basins_rainfall_from_WRF_WRF_HYDRO_EXP.py' (or 'extract_basins_rainfall_from_WRF_WRF_HYDRO_EXP_ALL_YEARS.py'). These scripts calculate rainfall according to WRF-WRF-HYDRO; 
    over the 145 defined catchments. The script reads two files, provided in the directory.

STEP 3: Plotting

a. Go into the 'plots_timeseries_rainfall_basins' directory;
b. Execute the bash script 'multi_submit_Bacini_timseries.sh' to run the NCL scripts 'multi_create_table_variables.ncl' and '30years_analysis_timeseries_Bacini.ncl'. These scripts create files for each basin with the rainfall data 
   to be plotted and generate a table collecting all statistics for each catchment;
c. Execute the bash script 'full_execute_Bacini_timseries.sh' to execute the python script 'all_python_barchart_rain_Bacini.py'. This script generates timeseries for all catchments within the evaluated time interval.