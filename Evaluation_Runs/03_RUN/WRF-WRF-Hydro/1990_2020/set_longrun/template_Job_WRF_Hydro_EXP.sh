#!/bin/bash
#BSUB -q p_long
#BSUB -J Ev_HNUM
#BSUB -n 576
#BSUB -x
#BSUB -o run_PrEv_%J.out
#BSUB -e run_PrEv_%J.err
#BSUB -P 0566
#BSUB -M 200G
#BSUB -app flame

source /users_home/cmcc/vr25423/source/WRFV4.4.1_JUNO/WRFV4.4.1_sp_dist/conf.sh

WRK_DIR="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/set_longrun"


cd PATHOUT

#type alias "adriwrf" or load wrf environment below:
#source /work/cmcc/wrf_cmcc-dev/giorgia/conf.sh
export I_MPI_PLATFORM="skx"
export I_MPI_EXTRA_FILESYSTEM=0
export I_MPI_HYDRA_BOOTSTRAP="lsf"
export I_MPI_HYDRA_BRANCH_COUNT=$(echo $LSB_MCPU_HOSTS | grep -Eo n[0-9][0-9][0-9] | wc -l)
export I_MPI_HYDRA_COLLECTIVE_LAUNCH=1

FILE=./wrfrst_d01_STARTYEAR-STARTMONTH-STARTDAY_00:00:00
if [ -f "$FILE" ]; then
    echo "$FILE exists."


rm wrfbdy_d01

#symbolic link to metgrid interpolated fields
#ln -sf /work/cmcc/wrf_cmcc-dev/giorgia/TestLuca/WPS/2018_2022/run_NewDomain/metgrid/met_em* .

#5giu2023: metgrid with LAI resolution 30 arcsec
#ln -sf /work/cmcc/wrf_cmcc-dev/giorgia/Test_ALE/WPS/run_five/metgrid/met_em* .

rm -f met_em*

#6lug2023: like 5giu2023 but with specific humidity
ln -sf /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun/01-Sep-1989_31-Dec-2020/metgrid/met_em.d01.STARTYEAR-STARTMONTH* .
ln -sf /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun/01-Sep-1989_31-Dec-2020/metgrid/met_em.d01.STARTYEAR-NEXTMONTH* .
ln -sf /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun/01-Sep-1989_31-Dec-2020/metgrid/met_em.d01.ENDYEAR-ENDMONTH* .
#26sep2023: old soiltype, with specific humidity, LAI and GREENFRACTION from MODIS
#ln -sf /work/cmcc/wrf_cmcc-dev/giorgia/Test_ALE/WPS/run_SH_old_static_fields/metgrid/met_em* .

rm rsl.*
rm wrfbdy*
rm wrflowinp*

cp ${WRK_DIR}/NAMELIST namelist.input
cp ${WRK_DIR}/HYDRONAME hydro.namelist

ulimit -s unlimited
time mpiexec.hydra -l ./real.exe >& real.log
wait

if [[ NEXTJOB == 2 ]]; then
  /juno/opt/anaconda/3-2022.10/bin/python /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/set_longrun/wrfinput_update.py >& log_wrfinput.log
  wait
  echo "wrfinput updated"
fi

wait
time mpiexec.hydra -l ./wrf.exe >& wrf.log
wait

# NEW: remove previous restart file, move and compress  wrf and wrfhydro output  files
mv wrfout*00 EXPERIMENT/
mv wrfxtrm*00 EXPERIMENT/
mv 20*GRID1 EXPERIMENT/
mv 20*DOMAIN1 EXPERIMENT/



mv wrfout_d01_* EXPERIMENT/

mv wrfxtrm_d01_* EXPERIMENT/




#mv frxst_pts_out.txt EXPERIMENT/frxst_pts_out_NUM.txt

bsub -app flame < ${WRK_DIR}/Job_WRF_Hydro_EXP_NEXTJOB.sh
fi

echo "Job completed at: `date`"
