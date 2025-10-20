#!/bin/bash
#=======================================================================
yy=$1
mm=$2
dd=$3
hh=$4
#=========
ncatted -O -a title,global,o,c,"AdriaClimPlus / NEMO / EvalRUN / ocean T grid variables" midTf1.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
ncatted -O -a adriaclimplus_dataset,global,c,c,"model" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc 
ncatted -O -a adriaclimplus_model,global,c,c,"NEMO" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
ncatted -O -a adriaclimplus_scale,global,c,c,"Adriatic" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
ncatted -O -a adriaclimplus_timeperiod,global,c,c,"3h" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
ncatted -O -a name,global,o,c,"NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
ncatted -O -a summary,global,o,c,"AdriaClimPlus / NEMO / EvalRUN / ocean T grid variables" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
ncatted -O -a institution,global,o,c,"Euro-Mediterranean Center on Climate Change (CMCC)" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
ncatted -O -a infoUrl,global,o,c,"https://cmcc.it" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
ncatted -O -a history,global,o,c,"" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
ncatted -O -a history_of_appended_files,global,o,c,"" NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc
mv NEMO_ADR_3h_${yy}${mm}${dd}${hh}_grid_T.nc output_ERDAP_3h/${yy}/${mm}/
#=======================================================================
