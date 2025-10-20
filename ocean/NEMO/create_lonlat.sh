#!/bin/bash

echo " Start Re-write Ocean AdriaClim NEMO model "

#ncks -v lon,lat /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_T.nc lonlatT.nc
#ncks -v lon,lat /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_U.nc lonlatU.nc
#ncks -v lon,lat /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_V.nc lonlatV.nc
#ncks -v lon,lat /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_W.nc lonlatW.nc

#############
### CREATING NEW LON AND LAT TO REPLACE ON THE FILES
## To T files
ncks -v nav_lon /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_T.nc lonT1.nc
ncks -v nav_lat /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_T.nc latT1.nc

ncwa -a y lonT1.nc lonT2.nc
ncwa -a x latT1.nc latT2.nc

ncrename -O -d x,lon lonT2.nc
ncrename -O -d y,lat latT2.nc

cdo chname,nav_lon,lon lonT2.nc lonT.nc
cdo chname,nav_lat,lat latT2.nc latT.nc

rm -f latT1.nc lonT1.nc latT2.nc lonT2.nc

## To U files
ncks -v nav_lon /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_U.nc lonU1.nc
ncks -v nav_lat /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_U.nc latU1.nc

ncwa -a y lonU1.nc lonU2.nc
ncwa -a x latU1.nc latU2.nc

ncrename -O -d x,lon lonU2.nc
ncrename -O -d y,lat latU2.nc

cdo chname,nav_lon,lon lonU2.nc lonU.nc
cdo chname,nav_lat,lat latU2.nc latU.nc

rm -f latU1.nc lonU1.nc latU2.nc lonU2.nc

## To V files
ncks -v nav_lon /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_V.nc lonV1.nc
ncks -v nav_lat /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_V.nc latV1.nc

ncwa -a y lonV1.nc lonV2.nc
ncwa -a x latV1.nc latV2.nc

ncrename -O -d x,lon lonV2.nc
ncrename -O -d y,lat latV2.nc

cdo chname,nav_lon,lon lonV2.nc lonV.nc
cdo chname,nav_lat,lat latV2.nc latV.nc

rm -f latV1.nc lonV1.nc latV2.nc lonV2.nc

## To W files
ncks -v nav_lon /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_W.nc lonW1.nc
ncks -v nav_lat /data/products/ERDDAP/projects/AdriaClim/NEMO/historical/day/1992/01/ADRIACLIM2_1d_19920101_grid_W.nc latW1.nc

ncwa -a y lonW1.nc lonW2.nc
ncwa -a x latW1.nc latW2.nc

ncrename -O -d x,lon lonW2.nc
ncrename -O -d y,lat latW2.nc

cdo chname,nav_lon,lon lonW2.nc lonW.nc
cdo chname,nav_lat,lat latW2.nc latW.nc

rm -f latW1.nc lonW1.nc latW2.nc lonW2.nc
##############
