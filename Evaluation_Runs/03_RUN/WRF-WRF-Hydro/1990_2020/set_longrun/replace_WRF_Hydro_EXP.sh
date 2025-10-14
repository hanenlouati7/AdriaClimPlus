#!/bin/bash
#BSUB -q s_short
#BSUB -J wrf_chain
#BSUB -n 1
#BSUB -o run_%J.out
#BSUB -e run_%J.err
#BSUB -P 0566
#BSUB -M 32G

export WRK_DIR="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/set_longrun"
MAIN_DIR="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/set_longrun"
PATH_OUT="\/work\/cmcc\/vr25423\/Project\/AdriaClimPlus\/evaluation_run_30yrs_ERA5\/WRF-WRF-Hydro\/1990_2020\/run"
PATH_OUTPUT="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run"

##Set start date vdt, and timestep kk
vdt_ini=19890901
kk=30
##Set exp name
name='EXP'
mkdir $PATH_OUTPUT/$name

##loop over Sep2018-Dec2023
for i in {1..382}
do

cp template_namelist_input namelist_input_${i}
cp template_hydro_namelist hydro_namelist_${i}
cp template_Job_WRF_Hydro_EXP.sh Job_WRF_Hydro_EXP_${i}.sh 

 
vdt_end=`$MAIN_DIR/jday ${vdt_ini} +$kk`
 
yyyy_ini=`echo ${vdt_ini} | cut -c1-4`
  mm_ini=`echo ${vdt_ini} | cut -c5-6`
  dd_ini=`echo ${vdt_ini} | cut -c7-8`

yyyy_end=`echo ${vdt_end} | cut -c1-4`
  mm_end=`echo ${vdt_end} | cut -c5-6`
  dd_end=`echo ${vdt_end} | cut -c7-8`

vdt_rst=`$MAIN_DIR/jday ${vdt_ini} -7`
yyyy_rst=`echo ${vdt_rst} | cut -c1-4`
  mm_rst=`echo ${vdt_rst} | cut -c5-6`
  dd_rst=`echo ${vdt_rst} | cut -c7-8`

sed -i "s/STARTYEAR/${yyyy_ini}/g" namelist_input_${i}
sed -i "s/STARTMONTH/${mm_ini}/g" namelist_input_${i}
sed -i "s/STARTDAY/${dd_ini}/g" namelist_input_${i}
sed -i "s/ENDYEAR/${yyyy_end}/g" namelist_input_${i}
sed -i "s/ENDMONTH/${mm_end}/g" namelist_input_${i}
sed -i "s/ENDDAY/${dd_end}/g" namelist_input_${i}
if [ $i -gt 1 ]
then
sed -i "s/RESTARTTF/true/g" namelist_input_${i}
else
sed -i "s/RESTARTTF/false/g" namelist_input_${i}
fi

sed -i "s/STARTYEAR/${yyyy_ini}/g" hydro_namelist_${i}
sed -i "s/STARTMONTH/${mm_ini}/g" hydro_namelist_${i}
sed -i "s/STARTDAY/${dd_ini}/g" hydro_namelist_${i}

vdt_ini=${vdt_end}
next=`expr ${i} \+ 1`
sed -i "s/NAMELIST/namelist_input_${i}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/HYDRONAME/hydro_namelist_${i}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/EXPERIMENT/$name/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/NUM/${i}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/NEXTJOB/$next/g" Job_WRF_Hydro_EXP_${i}.sh
#NEW
next_month=$(( (mm_ini % 12) + 1 ))
sed -i "s/NEXTMONTH/${next_month}/g" Job_WRF_Hydro_EXP_${i}.sh

sed -i "s/YYYYRST/${yyyy_rst}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/MMRST/${mm_rst}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/DDRST/${dd_rst}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/STARTYEAR/${yyyy_ini}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/STARTMONTH/${mm_ini}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/STARTDAY/${dd_ini}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/ENDYEAR/${yyyy_end}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/ENDMONTH/${mm_end}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/ENDDAY/${dd_end}/g" Job_WRF_Hydro_EXP_${i}.sh
sed -i "s/PATHOUT/${PATH_OUT}/g" Job_WRF_Hydro_EXP_${i}.sh
#end NEW

done

sed -i "s/GW_RESTART = 1/GW_RESTART = 0/g" hydro_namelist_1
sed -i "s/RESTART_FILE/! RESTART_FILE/g" hydro_namelist_1
sed -i "s/#WRFINPUTUNO/rm wrfinput*/g" Job_WRF_Hydro_EXP_1.sh
sed -i "s/#WRFINPUTDUE/cp \/work\/cmcc\/vr25423\/Project\/AdriaClimPlus\/evaluation_run_30yrs_ERA5\/WPS\/DOMAIN\/wrfinput_d01 \./g" Job_WRF_Hydro_EXP_1.sh

