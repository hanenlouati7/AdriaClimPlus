from netCDF4 import Dataset
import numpy as np

Dato = Dataset("/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/wrfinput_d01", "a")
Dato2 = Dataset("/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WPS/DOMAIN/geo_em.d01_18Nov2024.nc", "r")





for i in range (0, 402):
    for j in range (0, 288):
        Dato.variables['REFKDT_2D_LSM'][0,i,j] = Dato2.variables['REFKDT_2D_LSM'][0][i][j]
        Dato.variables['SLOPE_2D_LSM'][0,i,j] = Dato2.variables['SLOPE_2D_LSM'][0][i][j]
Dato.close()
Dato2.close()
