#!/bin/sh
#BSUB -P 0419 
#BSUB -n 1
#BSUB -q s_long
#BSUB -J wrfout
#BSUB -R "rusage[mem=2G]"
#BSUB -o wrfout.out
#BSUB -e wrfout.err

echo " Start Re-write WRF model to CF "
#############
if [ -f "lon_WRF.nc" ]; then
echo "lon_WRF.nc exists."
else
ncks -v XLONG /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP/wrfout_d01_1990-01-01_00:00:00 lon_WRF.nc
ncrename -O -v XLONG,lon lon_WRF.nc
ncwa -a Time,south_north lon_WRF.nc lon_WRF1.nc
ncrename -d west_east,lon lon_WRF1.nc lon_WRF2.nc
ncks -A -v lon lon_WRF1.nc lon_WRF2.nc
rm -f lon_WRF.nc lon_WRF1.nc
mv lon_WRF2.nc lon_WRF.nc
fi
if [ -f "lat_WRF.nc" ]; then
echo "lat_WRF.nc exists."
else
ncks -v XLAT /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP/wrfout_d01_1990-01-01_00:00:00 lat_WRF.nc
ncrename -O -v XLAT,lat lat_WRF.nc
ncwa -a Time,west_east lat_WRF.nc lat_WRF1.nc 
ncrename -d south_north,lat lat_WRF1.nc lat_WRF2.nc
ncks -A -v lat lat_WRF1.nc lat_WRF2.nc
rm -f lat_WRF.nc lat_WRF1.nc 
mv lat_WRF2.nc lat_WRF.nc 
fi
#############
for counter1 in {1990..1994}; do

if [ -d "WRF_$counter1" ]; then
echo "WRF_$counter1 does exist."
else
mkdir WRF_$counter1
fi

for counter2 in {1..12}; do

for counter3 in {1..31}; do
###########	
if [ -e /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP/wrfout_d01_$counter1-$(printf "%02d" $counter2)-$(printf "%02d" $counter3)_00:00:00 ]; then

echo "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP/wrfout_d01_"$counter1"-"$(printf "%02d" $counter2)"-"$(printf "%02d" $counter3)"_00:00:00"

echo "Year: "$counter1" month: "$(printf "%02d" $counter2)" day: "$(printf "%02d" $counter3)
############
if [ -e WRF_IN.nc ]; then
rm -f WRF_IN.nc
fi
ln -s /work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP/wrfout_d01_$counter1-$(printf "%02d" $counter2)-$(printf "%02d" $counter3)_00:00:00 WRF_IN.nc
export YEAR=$counter1
export MONTH=$(printf "%02d" $counter2)
export DAY=$(printf "%02d" $counter3)
ncl 'file_in="WRF_IN.nc"' 'file_out="WRF_OUT.nc"' wrfout_to_cf_final.ncl
######
ncks -C -O -x -v lon,lat WRF_OUT.nc WRF_OUT1.nc
wait
ncrename -O -d west_east,lon -d south_north,lat WRF_OUT1.nc
wait
ncks -A -v lon lon_WRF.nc WRF_OUT1.nc
wait
ncks -A -v lat lat_WRF.nc WRF_OUT1.nc
wait
######
nccopy -7 -d 5 WRF_OUT1.nc WRF_$counter1/wrfpost_$counter1$(printf "%02d" $counter2)$(printf "%02d" $counter3).nc
rm -f WRF_IN.nc WRF_OUT.nc WRF_OUT1.nc
############
fi
############
done
done
done
#############
echo " Done "

