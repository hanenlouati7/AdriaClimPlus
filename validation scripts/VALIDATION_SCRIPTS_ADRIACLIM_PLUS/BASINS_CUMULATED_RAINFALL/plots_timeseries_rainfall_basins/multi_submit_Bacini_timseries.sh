#!/bin/bash

#BSUB -q s_medium
#BSUB -J ERA5_23
#BSUB -n 1
#BSUB -o run.%J.out
#BSUB -e run.%J.err
#BSUB -P 0566
#BSUB -M 2GB

BASE_DIR="/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/plots_timeseries_rainfall"
NCdir="/juno/opt/spacks/0.20.0/opt/spack/linux-rhel8-icelake/intel-2021.6.0/ncl/6.6.2-p2sqoijwawszna7puyc2z26xtmms75gt/bin"
NAME_EXP="EVAL_RUN_30YEARS"

cd ${BASE_DIR}

# mkdir ${BASE_DIR}/data_plots_${NAME_EXP}
# mkdir ${BASE_DIR}/data_plots_${NAME_EXP}/all

year="1990_2020"
# i=0			# counter for selecting the right lat/lon. It starts form 0 because NCL counts from 0 and not from 1

# while read line  
# do 

# 	echo "Working on basin $line"
# 	export fig_out3="${year}"
# 	export counter=${i}
# 	export basin=$line	
# 	export year=$year	
# 	export NAME_EXP=${NAME_EXP}

# 	${NCdir}/ncl < 30years_analysis_timeseries_Bacini.ncl
	
#         i=$((i+1));

# #done < ${BASE_DIR}/List_rivers_test.txt
# done < ${BASE_DIR}/List_rivers.txt

## Script to save statistics in tables  

#for year in {2018..2020}; do
export NAME_EXP=${NAME_EXP}
export year=$year	
${NCdir}/ncl multi_create_table_variables.ncl

