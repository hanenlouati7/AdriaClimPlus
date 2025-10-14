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
from npp_tools import *
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
## Read input NEMO grid and bathymetry
print(' ')
print('Read input NEMO grid')
print(' ')
lonnm,latnm,bathynm = load_NEMO_bathy(bathyo_filename)
##################################################################
## Read input  initial condition
print('Read input atmospheric surface forcings fields - temporal loop')
print(' ')
##
yeari=sf_yeari
yeare=sf_yeare
datei = datetime.datetime(yeari, 1, 1)
datee = datetime.datetime(yeare, 12, 31)
nf=1+(datee-datei).days
year=yeari; dt=-1
for nn in range (0,nf):
    date0 = datei + datetime.timedelta(days = nn-1)
    date1 = datei + datetime.timedelta(days = nn)
    if(date1.year!=year): dt=-1; year=date1.year
    ny0=py.str_(date0.year)
    nm0=py.str_("{:0>2d}".format(date0.month))
    nd0=py.str_("{:0>2d}".format(date0.day))
    ny1=py.str_(date1.year)
    nm1=py.str_("{:0>2d}".format(date1.month))
    nd1=py.str_("{:0>2d}".format(date1.day))

    timef=[] ; mslf=[] ; u10f=[] ; v10f=[]
    t2mf=[]  ; d2mf=[] ; precipf=[] 
    swrdf=[] ; lwrdf=[]
    hh=-1
    final_sf_filename0=sf_input_folder+sf_input_filename+ny0+\
                       '-'+nm0+'-'+nd0+'_00:00:00'
    final_sf_filename1=sf_input_folder+sf_input_filename+ny1+\
                       '-'+nm1+'-'+nd1+'_00:00:00'
    os.system('rm -f wrf_in.nc')
    os.system('ln -s '+final_sf_filename1+' wrf_in.nc')
    os.system('ncl -Q WRF_diagnostic_fields_ncl.sh')
    for hour in range(0,18+1,6):
        hh=hh+1
        dt=dt+1
        nh=py.str_("{:0>2d}".format(hour))
        print('Year: '+ny1+' Month: '+nm1+' Day: '+nd1+' - '+nh+'hs')
        lonsf,latsf,time,msl,u10,v10,t2m,d2m,lsm,precip,swrd,lwrd = \
                 load_input_surface_forcings_WRF(final_sf_filename0,\
                 final_sf_filename1,'wrf_diag_out.nc',hh)
## Add time counter
        timef.append(dt*6)
## Check mask contain intermediate values
                #lsm[lsm==1]=1   # set land
                #lsm[lsm>1]=0    # set sea
## Check if the latitude is inverted
#               print(latsf.shape)
#               if(latsf[0]>latsf[1]):
#                    latsf=np.fliplr([latsf])[0]
#                    lsm=np.fliplr([lsm])[0] ; msl=np.fliplr([msl])[0]
#                    u10=np.fliplr([u10])[0] ; v10=np.fliplr([v10])[0]
#                    t2m=np.fliplr([t2m])[0] ; d2m=np.fliplr([d2m])[0]
#                    precip=np.fliplr([precip])[0]
#                    swrd=np.fliplr([swrd])[0] ; lwrd=np.fliplr([lwrd])[0]
##################################################################
## Apply the Land-sea mask (lsm variable - land=1 sea=0)
        precip[lsm==1]=np.nan ; msl[lsm==1]=np.nan 
        u10[lsm==1]=np.nan ; v10[lsm==1]=np.nan 
        t2m[lsm==1]=np.nan ; d2m[lsm==1]=np.nan
        lwrd[lsm==1]=np.nan ; swrd[lsm==1]=np.nan
##################################################################
## Seaoverland extrapolation fields
        mslf.append(sf_seaoverland(msl))     # Mean sea level pressure
        u10f.append(sf_seaoverland(u10))     # 10 metre U wind component
        v10f.append(sf_seaoverland(v10))     # 10 metre V wind component
        t2mf.append(sf_seaoverland(t2m))     # 2 metre temperature
        d2mf.append(sf_seaoverland(d2m))     # 2 metre dewpoint temperature
        precipf.append(sf_seaoverland(precip))  # Total precipitation
        swrdf.append(sf_seaoverland(swrd))   # Shortwave radiation
        #swrdf.append(swrd)
        lwrdf.append(sf_seaoverland(lwrd))   # Longwave radiation
##
    os.system('rm -f wrf_in.nc wrf_diag_out.nc')
## Convert precip from (mm/h) to (Kg/m**2 s)
## 1kg/m2/s = 86400mm/day = 3600 mm/h
    pconv=6*3600.  #to dt=6hs
## To convert hPa to Pa
    prconv=100
##
    mslf=np.asarray(mslf)*prconv 
    precipf=np.asarray(precipf)/pconv
    swrdf=np.asarray(swrdf); lwrdf=np.asarray(lwrdf)
    u10f=np.asarray(u10f)  ; v10f=np.asarray(v10f)
    t2mf=np.asarray(t2mf)  ; d2mf=np.asarray(d2mf)+273.15
##################################################################
## Write TS initial condition netcdf output file
#        print('Write Surface Forcing netcdf output file')
    sf_output_filenamef=sf_output_folder+sf_output_filename+\
                        '_y'+ny1+'m'+nm1+'d'+nd1+'.nc'
    oSFFile = write_SF_nc_output_ECMWF_WRF(lonsf, latsf, ny1, nm1, nd1, timef, mslf,\
              u10f, v10f, t2mf, d2mf, precipf, swrdf, lwrdf, sf_output_filenamef)
###
    del timef, mslf, u10f, v10f, t2mf, d2mf, precipf, swrdf, lwrdf
##################################################################
print(' ')
print('Surface Forcing to '+ny1+' created')
##################################################################
os.system('rm -f sample_forcing.nc *.exe coordinates.nc namelist_bicub namelist_bilin')
os.system('rm -f data_*.nc remap_*.nc weights_*.nc')
os.system('ln -s '+sf_output_filenamef+' sample_forcing.nc')
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
