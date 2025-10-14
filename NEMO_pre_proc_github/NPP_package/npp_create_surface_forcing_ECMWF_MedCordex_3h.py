##################################################################
##################################################################
# Nemo PreProcessing (NPP) package
# npp_create_surface_forcing.py
#
# Vladimir Santos da Costa - CMCC
# vladimir.santosdacosta@cmcc.it
#
# Lecce, IT, 12/05/2022
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
for year in range(yeari,yeare+1):
    ny=py.str_(year)
    dt=-2
    for month in range(sf_monthini,sf_monthend+1):
        nm=py.str_("{:0>2d}".format(month))
        daye=31
        if(month==2): daye=28
        if(month==2 and year % 4 == 0): daye=29
        if(month==4 or month==6 or month==9 or month==11): daye=30
        for day in range(1,daye+1):
            nd=py.str_("{:0>2d}".format(day))
            timef=[] ; mslf=[] ; tccf=[] ; u10f=[] ; v10f=[]
            t2mf=[]  ; d2mf=[] ; precipf=[] 
            swrdf=[] ; lwrdf=[]
            for hour in range(0,18+1,6):
                dt=dt+2
                nh=py.str_("{:0>2d}".format(hour))
                print('Year: '+ny+' Month: '+nm+' Day: '+nd+' - '+nh+'hs')
                final_sf_filename1=sf_input_folder+ny+'/'+sf_input_filename1+ny+'.nc'
                final_sf_filename2=sf_input_folder+ny+'/'+sf_input_filename2+ny+'.nc'
                final_sf_filename3=sf_input_folder+ny+'/'+sf_input_filename3+ny+'.nc'
                final_sf_filename4=sf_input_folder+ny+'/'+sf_input_filename4+ny+'.nc'
                final_sf_filename5=sf_input_folder+ny+'/'+sf_input_filename5+ny+'.nc'
                final_sf_filename6=sf_input_folder+ny+'/'+sf_input_filename6+ny+'.nc'
                final_sf_filename7=sf_input_folder+ny+'/'+sf_input_filename7+ny+'.nc'
                final_sf_filename8=sf_input_folder+ny+'/'+sf_input_filename8+ny+'.nc'
                final_sf_filename9=sf_input_folder+ny+'/'+sf_input_filename9+ny+'.nc'
                final_sf_filename10=sf_input_folder+ny+'/'+sf_input_filename10+ny+'.nc'
                final_sf_filename11=sf_input_folder+ny+'/'+sf_input_filename11
                lonsf,latsf,time,msl,tcc,u10,v10,t2m,d2m,lsm,precip,swrd,lwrd = \
                load_input_surface_forcings_ECMWF_MedCordex(final_sf_filename1,\
                final_sf_filename2,final_sf_filename3,final_sf_filename4,\
                final_sf_filename5,final_sf_filename6,final_sf_filename7,\
                final_sf_filename8,final_sf_filename9,final_sf_filename10,\
                final_sf_filename11,dt) 
## Add time counter
                timef.append(dt*3)
## Check mask contain intermediate values
                lsm[lsm>0.5]=1   # set land
                lsm[lsm<0.5]=0   # set sea
## Check if the latitude is inverted
#               print(latsf.shape)
#               if(latsf[0]>latsf[1]):
#                   latsf=np.fliplr([latsf])[0]
#                   lsm=np.fliplr([lsm])[0] ; msl=np.fliplr([msl])[0]
#                   tcc=np.fliplr([tcc])[0]
#                   u10=np.fliplr([u10])[0] ; v10=np.fliplr([v10])[0]
#                   t2m=np.fliplr([t2m])[0] ; d2m=np.fliplr([d2m])[0]
#                   precip=np.fliplr([precip])[0]
#                   swrd=np.fliplr([swrd])[0] ; lwrd=np.fliplr([lwrd])[0]
##################################################################
## Apply the Land-sea mask (lsm variable - land=1 sea=0)
                msl[lsm==1]=np.nan ; tcc[lsm==1]=np.nan
                precip[lsm==1]=np.nan
                u10[lsm==1]=np.nan ; v10[lsm==1]=np.nan 
                t2m[lsm==1]=np.nan ; d2m[lsm==1]=np.nan
            #swrd[lsm==1]=np.nan  
                lwrd[lsm==1]=np.nan
##################################################################
## Seaoverland extrapolation fields
                mslf.append(sf_seaoverland(msl))     # Mean sea level pressure
                tccf.append(sf_seaoverland(tcc))
                u10f.append(sf_seaoverland(u10))     # 10 metre U wind component
                v10f.append(sf_seaoverland(v10))     # 10 metre V wind component
                t2mf.append(sf_seaoverland(t2m))     # 2 metre temperature
                d2mf.append(sf_seaoverland(d2m))     # 2 metre dewpoint temperature
                precipf.append(sf_seaoverland(precip))  # Total precipitation
                #swrdf.append(sf_seaoverland(swrd))   # Shortwave radiation
                swrdf.append(swrd)
                lwrdf.append(sf_seaoverland(lwrd))   # Longwave radiation
## To convert hPa to Pa
            prconv=100
## To adjust long-wave to Reanalysis level [value in W/m2]
            lwconv=75.0  #1990 
## Convert precip from (mm/h) to (Kg/m**2 s)
## 1kg/m2/s = 86400mm/day = 3600 mm/h
            pconv=6*3600.  #to dt=6hs
##
            mslf=np.asarray(mslf)*prconv ; tccf=np.asarray(tccf)
            precipf=np.asarray(precipf)/pconv
            swrdf=np.asarray(swrdf); lwrdf=np.asarray(lwrdf)+lwconv
            u10f=np.asarray(u10f)  ; v10f=np.asarray(v10f)
            t2mf=np.asarray(t2mf)  ; d2mf=np.asarray(d2mf)
##################################################################
## Write TS initial condition netcdf output file
#        print('Write Surface Forcing netcdf output file')
            sf_output_filenamef=sf_output_folder+sf_output_filename+\
                                '_y'+ny+'m'+nm+'d'+nd+'.nc'
            oSFFile = write_SF_nc_output_ECMWF(lonsf, latsf, ny, nm, nd, timef, mslf,\
                      tccf, u10f, v10f, t2mf, d2mf, precipf, swrdf, lwrdf, sf_output_filenamef)
###
            del timef, mslf, tccf, u10f, v10f, t2mf, d2mf, precipf, swrdf, lwrdf
##################################################################
print(' ')
print('Surface Forcing to '+ny+' created')
##################################################################
#os.system('rm -f sample_forcing.nc *.exe coordinates.nc namelist_bicub namelist_bilin')
#os.system('rm -f data_*.nc remap_*.nc weights_*.nc')
#os.system('ln -s '+sf_output_filenamef+' sample_forcing.nc')
#os.system('ln -s inputs_surface_forcing/*.exe .')
#os.system('ln -s inputs_surface_forcing/coordinates.nc .')
#os.system('ln -s inputs_surface_forcing/namelist_bicub .')
#os.system('ln -s inputs_surface_forcing/namelist_bilin .')

#os.system('./scripgrid.exe << EOF  \n namelist_bicub \n EOF')

#os.system('./scrip.exe << EOF      \n namelist_bicub \n EOF')

#os.system('./scripshape.exe << EOF \n namelist_bicub \n EOF')

#os.system('./scripgrid.exe << EOF  \n namelist_bilin \n EOF')

#os.system('./scrip.exe << EOF      \n namelist_bilin \n EOF')

#os.system('./scripshape.exe << EOF \n namelist_bilin \n EOF')

#os.system('mv data_*.nc '+sf_output_folder)
#os.system('mv remap_*.nc '+sf_output_folder)
#os.system('mv weights_*.nc '+sf_output_folder)

#print(' ')
#print('Surface Forcing weights created')
##################################################################
