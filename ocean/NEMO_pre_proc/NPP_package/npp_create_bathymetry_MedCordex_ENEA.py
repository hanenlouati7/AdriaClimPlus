##################################################################
##################################################################
# Nemo PreProcessing (NPP) package
# npp_create_bathymetry.py
#
# Vladimir Santos da Costa - CMCC
# vladimir.santosdacosta@cmcc.it
#
# Lecce, IT, 02/02/2022
##################################################################
##################################################################
from npp_tools import *
from npp_inputparams import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.offsetbox import AnchoredText
##################################################################
## Read input bathymetry
print(' ')
print('Read input bathymetry')
print(' ')
lonco,latco,longo,latgo,dxo,dyo,zco,zgo,dzco,dzgo,ffo,masko,bathyo = \
        load_input_MedCordex_bathy(bathyi_filename)
##################################################################
print('Re-write MedCordex bathymetry on NEMO input format')
print(' ')
oFile = create_write_nc_bathy_output(lonco, latco, bathyo, bathyo_filename)
##################################################################
print('Write mesh_hgr.nc')
print(' ')
oFile_mh = write_nc_mesh_hgr(lonco,latco,longo,latgo,dxo,dyo,zco,ffo,meshho_filename)
##################################################################
print('Write mesh_zgr.nc')
print(' ')
oFile_mz = write_nc_mesh_zgr(longo,latgo,dxo,dyo,zco,zgo,dzco,dzgo,ffo,bathyo,meshzo_filename)
##################################################################
print('Write mask.nc')
print(' ')
oFile_mk = write_nc_mask(longo,latgo,zco,masko,masko_filename)
##################################################################
