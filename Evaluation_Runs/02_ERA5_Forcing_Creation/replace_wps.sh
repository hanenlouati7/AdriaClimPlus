#!/bin/bash
#BSUB -q s_short
#BSUB -J wps_chain
#BSUB -n 1
#BSUB -o run_%J.out
#BSUB -e run_%J.err
#BSUB -P 0566
#BSUB -M 32G

export WRK_DIR="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun"
cp /work/cmcc/vr25423/copied_from_zeus/DOMAIN_New/geo_em.d01_June_5_2023.nc /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/set_longrun/01-Sep-1989_31-Dec-2020/ungrib/geo_em.d01.nc


##Set start date vdt, and timestep kk
#vdt_ini=20210101
vdt_ini=19890901
kk=5

#loop over 2019 with 5days-runs
#for i in {1..122}
for i in {1..2508}
do

cp template_namelist_mercator_6km.wps namelist_wps_${i}

 vdt_end=`$WRK_DIR/jday ${vdt_ini} +$kk`
 yyyy_ini=`echo ${vdt_ini} | cut -c1-4`
 mm_ini=`echo ${vdt_ini} | cut -c5-6`
 dd_ini=`echo ${vdt_ini} | cut -c7-8`
 yyyy_end=`echo ${vdt_end} | cut -c1-4`
 mm_end=`echo ${vdt_end} | cut -c5-6`
 dd_end=`echo ${vdt_end} | cut -c7-8`
  sed -i "s/STARTDATE/${yyyy_ini}-${mm_ini}-${dd_ini}_00:00:00/g" namelist_wps_${i}
  sed -i "s/ENDDATE/${yyyy_end}-${mm_end}-${dd_end}_00:00:00/g" namelist_wps_${i}
vdt_ini=${vdt_end}
done
