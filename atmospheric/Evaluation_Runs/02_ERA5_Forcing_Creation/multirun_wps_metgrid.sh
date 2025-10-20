#!/bin/bash
#BSUB -q s_long
#BSUB -J metgrid
#BSUB -n 1
#BSUB -o metgrid_%J.out
#BSUB -e metgrid_%J.err
#BSUB -P 0566
#BSUB -M 32G

export WRK_DIR="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun"
export WPS_DIR="/users_home/cmcc/vr25423/source/WRFV4.4.1_JUNO/WPS-4.4"

R_OUT="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun/01-Sep-1989_31-Dec-2020/ungrib"
cd ${R_OUT}

#type alias "adriwrf" or load wrf environment below:
#source /work/opa/wrf_cmcc-dev/giorgia/conf.sh

export I_MPI_PLATFORM="skx"
export I_MPI_EXTRA_FILESYSTEM=0
export I_MPI_HYDRA_BOOTSTRAP="lsf"
export I_MPI_HYDRA_BRANCH_COUNT=$(echo $LSB_MCPU_HOSTS | grep -Eo n[0-9][0-9][0-9] | wc -l)
export I_MPI_HYDRA_COLLECTIVE_LAUNCH=1

ln -sf  ${WPS_DIR}/metgrid/METGRID.TBL METGRID.TBL #This is the same METGRID.TBL used by luca as in /work/opa/wrf_cmcc-dev/giorgia/TestLuca/WPS/2018_2022/run_SH

#use the proper ungrib files under ${R_OUT} directory

#for i in {1..2}
for i in {1..2508}
do

rm metgrid.log*
cp ${WRK_DIR}/namelist_wps_${i} namelist.wps

###change namelist record: &metgrid
#time mpiexec.hydra -l ./metgrid.exe >& metgrid.log
ln -sf ${WPS_DIR}/metgrid/src/metgrid.exe metgrid.exe

./metgrid.exe >& metgrid.log
wait

done

