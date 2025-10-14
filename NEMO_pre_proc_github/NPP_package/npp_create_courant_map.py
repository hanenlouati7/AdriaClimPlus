##################################################################
##################################################################
# Nemo PreProcessing (NPP) package
# npp_create_initial_condition.py
#
# Vladimir Santos da Costa - CMCC
# vladimir.santosdacosta@cmcc.it
#
# Lecce, IT, 06/02/2022
##################################################################
##################################################################
from npp_tools import *
from npp_inputparams import *
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from matplotlib.offsetbox import AnchoredText
import netCDF4 
##################################################################
## Read lon and lat from bathymetry file
print(' ')
print('Read lon and lat from bathymetry file')
print(' ')
nb=netCDF4.Dataset('../NEMO_input_files/depth_ADRb.020_03s.nc')
lon=np.squeeze(nb.variables['nav_lon'])
lat=np.squeeze(nb.variables['nav_lat'])
bathy=np.squeeze(nb.variables['Bathymetry'])
nb.close()
##################################################################
## Read dx and dy from domain_cfg file
print('Read dx and dy from domain_cfg file')
print(' ')
nc=netCDF4.Dataset('../NEMO_input_files/domain_cfg_03s.nc')
dx=np.squeeze(nc.variables['e1t'])
dy=np.squeeze(nc.variables['e2t'])
nc.close()
##################################################################
## Calculate barotropic Courant
g=9.81   # Gravity aceleration [m/s**2] 
C=np.sqrt(bathy*g)
cx=1/dx
cy=1/dy
courant=(cx+cy)/(C**2)
print('Max. Courant number: ',np.min(courant))
##################################################################
## Plot seaoverland temp. extrapolated
print('Plot Bathymetry and Courant number')
print(' ')
plt.figure()
plt.pcolor(lon,lat,courant)
plt.title('Barotropic courant number')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.colorbar()
# Save the figure to file
plt.savefig('./FIGURES/COURANT_NUMBER.png',dpi=150)
plt.close()
##################################################################
