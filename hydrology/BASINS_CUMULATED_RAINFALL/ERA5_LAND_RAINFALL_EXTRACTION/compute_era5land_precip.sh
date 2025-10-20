#!/bin/bash

#BSUB -q s_long
#BSUB -J era5land
#BSUB -n 1
#BSUB -o run.%J.out
#BSUB -e run.%J.err
#BSUB -P 0555
#BSUB -M 100GB

BASE_DIR="/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/ERA5_LAND_RAINFALL_EXTRACTION"

cd ${BASE_DIR}

#python3 30years_extraction_ERA5_cumulated_rain.py
python3 single_years_extraction_ERA5_cumulated_rain.py
