##################################################################
##################################################################
# Nemo PreProcessing (NPP) package
# npp_create_surface_forcing_ECMWF_WRF.py
#
# Vladimir Santos da Costa - CMCC
# vladimir.santosdacosta@cmcc.it
#
# Lecce, IT, 03/03/2025
##################################################################
##################################################################
from npp_inputparams import *
import matplotlib.pyplot as plt
import numpy as np
import pylab as py
import math
from matplotlib.offsetbox import AnchoredText
import sys
import os
import matplotlib
matplotlib.use('Agg')
##################################################################                              
os.system('rm -f sample_forcing.nc *.exe coordinates.nc namelist_bicub namelist_bilin')
os.system('rm -f data_*.nc remap_*.nc weights_*.nc')
os.system('ln -s '+sf_output_folder+'WRF_y1981m12d31.nc sample_forcing.nc')
os.system('ln -s inputs_surface_forcing/*.exe .')
os.system('ln -s inputs_surface_forcing/coordinates.nc .')
os.system('ln -s inputs_surface_forcing/namelist_bicub .')
os.system('ln -s inputs_surface_forcing/namelist_bilin .')

os.system('./scripgrid.exe << EOF  \n namelist_bicub \n EOF')

os.system('./scrip.exe << EOF      \n namelist_bicub \n EOF')

os.system('./scripshape.exe << EOF \n namelist_bicub \n EOF')

os.system('./scripgrid.exe << EOF  \n namelist_bilin \n EOF')

os.system('./scrip.exe << EOF      \n namelist_bilin \n EOF')

os.system('./scripshape.exe << EOF \n namelist_bilin \n EOF')

os.system('mv data_*.nc '+sf_output_folder)
os.system('mv remap_*.nc '+sf_output_folder)
os.system('mv weights_*.nc '+sf_output_folder)

print(' ')
print('Surface Forcing weights created')
##################################################################
