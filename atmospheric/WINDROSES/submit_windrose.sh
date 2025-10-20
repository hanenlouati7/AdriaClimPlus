#!/bin/bash

#BSUB -q s_short
#BSUB -J windrose
#BSUB -n 1
#BSUB -o run.%J.out
#BSUB -e run.%J.err
#BSUB -P 0555
#BSUB -M 50GB

#NAME_EXP="WRF_WRF_HYDRO_PRE_EVAL_ERA5"
NAME_EXP="WRF_WRF_HYDRO_PRE_EVAL_IFS"
BASE_DIR="/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/REGIONI_IN_SITU_OBS/EMILIA_ROMAGNA/windrose/ADRIACLIM_PLUS_PRE_EVAL_RUNS"

cd ${BASE_DIR}

#for year in {2019..2023}; do
#for year in 2022; do

#        export year=$year
#        export NAME_EXP=${NAME_EXP}

#	python3 make_windrose_insitu_station.py		# conda env to be activated: rivers_rain

#done

export NAME_EXP=${NAME_EXP}
python3 multi_make_windrose_insitu_station.py
