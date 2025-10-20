#!/bin/bash

for yy in {1989..2023}
do
  for mm in 01 02 03 04 05 06 07 08 09 10 11 12
  do
    cdo delname,var129 ${yy}/${mm}/ERA5_singlelevel_${yy}_${mm}.grib ${yy}/${mm}/1.nc
    cdo merge ${yy}/${mm}/1.nc ${yy}/${mm}/ERA5_prlevel_${yy}_${mm}.grib ${yy}/${mm}/ERA5_merged_${yy}_${mm}.grib
    rm ${yy}/${mm}/ERA5_prlevel_${yy}_${mm}.grib ${yy}/${mm}/ERA5_singlelevel_${yy}_${mm}.grib ${yy}/${mm}/1.nc
  done
done
