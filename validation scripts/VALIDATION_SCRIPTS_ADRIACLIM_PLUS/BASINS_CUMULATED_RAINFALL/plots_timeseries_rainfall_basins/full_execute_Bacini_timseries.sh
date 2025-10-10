#!/bin/bash

#BSUB -q s_medium
#BSUB -J rain_all
#BSUB -n 1
#BSUB -o run.%J.out
#BSUB -e run.%J.err
#BSUB -P 0566
#BSUB -M 2GB

BASE_DIR="/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/plots_timeseries_rainfall"
NAME_EXP="EVAL_RUN_30YEARS_1990-2020"

#mkdir ${BASE_DIR}/figures_${NAME_EXP}

cd ${BASE_DIR}
 
i=0			# counter for selecting the right lat/lon. It starts form 0 because NCL counts from 0 and not from 1

year="1990_2020"

while read line  
do 
		
	echo "Working on basin $line"
	export fig_out3="${year}"
	export counter=${i}
	export basin=$line	
	export year=$year	
	export NAME_EXP=${NAME_EXP}

	python3 all_python_barchart_rain_Bacini.py
	
        i=$((i+1));

	done < ${BASE_DIR}/List_rivers.txt
# 	done < ${BASE_DIR}/List_rivers_test.txt

