#!/bin/bash

#BSUB -q s_medium
#BSUB -J valid
#BSUB -n 1
#BSUB -o run.%J.out
#BSUB -e run.%J.err
#BSUB -P 0555
#BSUB -M 10GB

BASE_DIR="/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI"
NCdir="/juno/opt/spacks/0.20.0/opt/spack/linux-rhel8-icelake/intel-2021.6.0/ncl/6.6.2-p2sqoijwawszna7puyc2z26xtmms75gt/bin"

cd ${BASE_DIR}

for year in {2021..2023}; do
#for year in 2021; do
 
         export YEAR="$year"

	 ${NCdir}/ncl compute_era5land_rain_basins_on_wrf_grid.ncl
	
done
