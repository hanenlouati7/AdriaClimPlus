#!/bin/bash
bc_input_folder="/data/inputs/METOCEAN/historical/model/ocean/ENEA/Med-CORDEX/historical/"
####
for bc_year in {1981..1982}; do

cdo setgrid,mygrid ${bc_input_folder}${bc_year}/THETA_${bc_year}_Daily.nc a.nc
nccopy -7 -d 5 a.nc THETA_${bc_year}_Daily_regrid.nc
rm -f a.nc

cdo setgrid,mygrid ${bc_input_folder}${bc_year}/SALT_${bc_year}_Daily.nc a.nc
nccopy -7 -d 5 a.nc SALT_${bc_year}_Daily_regrid.nc
rm -f a.nc

cdo setgrid,mygrid ${bc_input_folder}${bc_year}/UVEL_${bc_year}_Daily.nc a.nc
nccopy -7 -d 5 a.nc UVEL_${bc_year}_Daily_regrid.nc
rm -f a.nc

cdo setgrid,mygrid ${bc_input_folder}${bc_year}/VVEL_${bc_year}_Daily.nc a.nc
nccopy -7 -d 5 a.nc VVEL_${bc_year}_Daily_regrid.nc
rm -f a.nc

cdo setgrid,mygrid ${bc_input_folder}${bc_year}/ELEVATION_${bc_year}_Daily.nc a.nc
nccopy -7 -d 5 a.nc ELEVATION_${bc_year}_Daily_regrid.nc
rm -f a.nc

done
########################################################
