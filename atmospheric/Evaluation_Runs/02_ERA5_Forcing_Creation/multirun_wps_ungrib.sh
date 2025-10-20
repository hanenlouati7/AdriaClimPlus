#!/bin/bash
#BSUB -q s_long
#BSUB -J ungrib
#BSUB -n 1
#BSUB -o ungrib_%J.out
#BSUB -e ungrib_%J.err
#BSUB -P 0566
#BSUB -M 32G

export WRK_DIR="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun"
export WPS_DIR="/users_home/cmcc/vr25423/source/WRFV4.4.1_JUNO/WPS-4.4"

R_OUT="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun/01-Sep-1989_31-Dec-2020/ungrib"

cd ${R_OUT}


#type alias "adriwrf" or load one of the conf.sh (wrf environment) below:
#source /work/opa/wrf_cmcc-dev/giorgia/conf.sh
# source /users_home/cmcc/vr25423/source/WRFV4.4.1_JUNO/WPS-4.4/conf.sh
export I_MPI_PLATFORM="skx"
export I_MPI_EXTRA_FILESYSTEM=0
export I_MPI_HYDRA_BOOTSTRAP="lsf"
export I_MPI_HYDRA_BRANCH_COUNT=$(echo $LSB_MCPU_HOSTS | grep -Eo n[0-9][0-9][0-9] | wc -l)
export I_MPI_HYDRA_COLLECTIVE_LAUNCH=1

# edit namelist.wps and change record &ungrib with 'prefix'=FILE_3d

## link the appropriate VTable
 ln -sf ${WPS_DIR}/ungrib/Variable_Tables/Vtable.ECMWF_modified Vtable  #Specific humidity is added as per Luca's file

#define start day of simulation chain and time window of chain chunk
#vdt_ini=20210201
vdt_ini=19890901
kk=5

rm *.err *.out

#for i in {1..122}
for i in {1..2508}
do
cp  /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun/namelist_wps_${i} namelist.wps

 dd=`expr \( ${i} - 1 \) \* 5`
 vdt_1=`$WRK_DIR/jday ${vdt_ini} +$dd`
 yyyy_1=`echo ${vdt_1} | cut -c1-4`
 mm_1=`echo ${vdt_1} | cut -c5-6`
 dd_1=`echo ${vdt_1} | cut -c7-8`

 vdt_5=`$WRK_DIR/jday ${vdt_ini} +$((dd +5))`
 yyyy_5=`echo ${vdt_5} | cut -c1-4`
 mm_5=`echo ${vdt_5} | cut -c5-6`
 dd_5=`echo ${vdt_5} | cut -c7-8`

## link the appropriate GRIB files
#note that the only ECMWF grib files crresponding to the simul chunk have to be linked) 
ln -sf ${WPS_DIR}/link_grib.csh link_grib.csh
./link_grib.csh /data/cmcc/vr25423/inputs/model/atmos/ECMWF/ERA5/reanalysis/1h/grib/${yyyy_1}/${mm_1}/*.grib /data/cmcc/vr25423/inputs/model/atmos/ECMWF/ERA5/reanalysis/1h/grib/${yyyy_5}/${mm_5}/*.grib

# MPI mode, intermediate FILE_3d:2019* are randomly corrupted
#time mpiexec.hydra -l ./ungrib.exe >& ungribecmwf_2019_${i}.log

#./ungrib.exe >& ungribecmwf_2019_${i}.log

ln -sf ${WPS_DIR}/ungrib/src/ungrib.exe ungrib.exe

./ungrib.exe >& ungribecmwf_${yyyy_1}_${i}.log

wait
done
