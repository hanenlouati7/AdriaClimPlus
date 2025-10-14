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
##################################################################                         
## Read input NEMO grid and bathymetry
print(' ')
print('Read input NEMO grid and bathymetry')
print(' ')
lonnm,latnm,bathynm = load_NEMO_bathy(bathyo_filename)
##################################################################
## Read input Temp. and Sal. initial condition
print('Read input Temp. and Sal. initial condition')
print(' ')
lonts,latts,zts,tempi,sali = load_input_initial_TS(tempi_filename,sali_filename)
##################################################################
## Plot original temp. input 
if(iplot==1):
    print('Plot original temp. input')
    print(' ')
    fig,axs = plt.subplots(1, 2, figsize=(10,6))
    fig.suptitle('ORIGINAL INPUT TEMP. - Created by NPP package',fontsize=14,fontweight='bold')
    for ax in axs.flat:
        ax.set_xlabel('Longitude',fontsize=12,fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12,fontweight='bold')

    aa=axs[0].pcolor(lonts,latts,np.squeeze(tempi[0,:,:]), vmin=13, vmax=18)
    anchored_text1 = AnchoredText('Original Temp. surface', loc=1)
    axs[0].add_artist(anchored_text1)

    aa=axs[1].pcolor(lonts,latts,np.squeeze(tempi[len(zts)-1,:,:]), vmin=13, vmax=18)
    anchored_text1 = AnchoredText('Original Temp. bottom', loc=1)
    axs[1].add_artist(anchored_text1)

    fig.subplots_adjust(right=0.875)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
    fig.colorbar(aa, cax=cbar_ax)
    cbar_ax.set_title('degC')
    cbar_ax.tick_params(labelsize=12)
    # Save the figure to file
    plt.savefig('./FIGURES/TEMP_input_original.png',dpi=150)
    plt.close()
##################################################################
## Temp. and Sal. seaoverland extrapolation
print('Check input files limits')
print(' ')
if(np.min(lonts)>np.min(lonnm)):
    print('**Min. TS input file longitude > min. longitude NEMO new gridi - EXTRAPOLATION DONE!!')
    print(' ')
    lonts[lonts==np.min(lonts)]=np.min(lonnm)
if(np.max(lonts)<np.max(lonnm)):
    print('**Max. TS input file longitude < max. longitude NEMO new grid - EXTRAPOLATION DONE!!')
    print(' ')
    lonts[lonts==np.max(lonts)]=np.max(lonnm)
if(np.min(latts)>np.min(latnm)):
    print('**Min. TS input file latitude > min.latitude NEMO new grid - EXTRAPOLATION DONE!!')
    print(' ')
    latts[latts==np.min(latts)]=np.min(latnm)
if(np.max(latts)<np.max(latnm)):
    print('**Max. TS input file latitude < max. latitude NEMO new grid - EXTRAPOLATION DONE!!')
    print(' ')
    latts[latts==np.max(latts)]=np.max(latnm)

print('Temperature seaoverland extrapolation')
print(' ')
tempif = ts_seaoverland(tempi)
print('Salinity seaoverland extrapolation')
print(' ')
salif  = ts_seaoverland(sali)
##################################################################
## Plot seaoverland temp. extrapolated
if(iplot==1):
    print('Plot seaoverland temp. extrapolated')
    print(' ')
    fig,axs = plt.subplots(1, 2, figsize=(10,6))
    fig.suptitle('SEAOVERLAND TEMP. - Created by NPP package',fontsize=14,fontweight='bold')
    for ax in axs.flat:
        ax.set_xlabel('Longitude',fontsize=12,fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12,fontweight='bold')

    aa=axs[0].pcolor(lonts,latts,np.squeeze(tempif[0,:,:]), vmin=13, vmax=18)
    anchored_text1 = AnchoredText('Seaoverland Temp. surface', loc=1)
    axs[0].add_artist(anchored_text1)

    aa=axs[1].pcolor(lonts,latts,np.squeeze(tempif[len(zts)-1,:,:]), vmin=13, vmax=18)
    anchored_text1 = AnchoredText('Seaoverlan Temp. bottom', loc=1)
    axs[1].add_artist(anchored_text1)

    fig.subplots_adjust(right=0.875)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
    fig.colorbar(aa, cax=cbar_ax)
    cbar_ax.set_title('degC')
    cbar_ax.tick_params(labelsize=12)
    # Save the figure to file
    plt.savefig('./FIGURES/TEMP_input_seaoverland_'+tname+'.png',dpi=150)
    plt.close()
##################################################################
## Horizontal interpolation TEMP. and SAL. to NEMO grid
print('Horizontal interpolation TEMP. to NEMO grid')
print(' ')
tempnm = hinterp_to_NEMO(lonts,latts,zts,tempi,lonnm,latnm)
print('Horizontal interpolation SAL. to NEMO grid')
print(' ')
salnm = hinterp_to_NEMO(lonts,latts,zts,sali,lonnm,latnm)
#################################################################
## Create NEMO vertical discretization
print('Create NEMO vertical discretization')
print(' ')
if(vdiscr==0):
## Create vertical discretization
    gdepw = vertical_NEMO_grid(kp,sh,sr,zd)
if(vdiscr==1):
## Read input NEMO vertical discretization
    gdepw = load_NEMO_vertical(domain_NEMO_filename)
## Plot vertical grid resolution
if(iplot==1):
    print('Plot vertical grid resolution')
    print(' ')
    plt.plot(range(0,kp),-gdepw,'g-*')
    plt.xlabel("Levels")
    plt.ylabel("Depth (m)")
    plt.title('VERTIVAL LEVELS Discretization - depth max. '+py.str_(np.max(bathynm))+' m')
    # Save the figure to file
    plt.savefig('./FIGURES/VERTICAL_discretization_'+tname+'.png',dpi=150)
    plt.close()
##################################################################
## Vertical interpolation TEMP. and SAL. to NEMO grid
print('Vertical interpolation TEMP. to NEMO grid')
print(' ')
tempnmf = vinterp_to_NEMO(tempnm,zts,gdepw)
tempnmf[np.isnan(tempnmf)]=0
print('Vertical interpolation SAL. to NEMO grid')
print(' ')
salnmf = vinterp_to_NEMO(salnm,zts,gdepw)
salnmf[np.isnan(salnmf)]=0
##################################################################
## Plot vertical grid resolution
if(iplot==1):
    tempit=np.squeeze(tempi[:,284,570])
    tempnmft=np.squeeze(tempnmf[:,145,276])
    salit=np.squeeze(sali[:,284,570])
    salnmft=np.squeeze(salnmf[:,145,276])
    for i in range (0,len(gdepw)):
        if(gdepw[i]>=bathynm[145,276]): tempnmft[i]=np.nan ; salnmft[i]=np.nan
    for i in range (0,len(zts)):
        if(zts[i]>=bathynm[145,276]): tempit[i]=np.nan ; salit[i]=np.nan

    print('Plot temperature profile compare')
    print(' ')
    plt.plot(tempit,-zts,'k',label='CMEMS-Reanalysis')
    plt.plot(tempnmft,-gdepw,'r',label='NEMO')
    plt.xlabel("Temperature [degC]")
    plt.ylabel("Depth [m]")
    plt.title('Temperature profile comparison, after vertical interpolation'+\
    py.str_(np.squeeze(bathynm[145,276])))
    plt.legend()
    plt.grid()
    # Save the figure to file
    plt.savefig('./FIGURES/TEMPERATURE_PROFILE_comparison_'+tname+'.png',dpi=150)
    plt.close()
##
    print('Plot salinity profile compare')
    print(' ')
    plt.plot(salit,-zts,'k',label='CMEMS-Reanalysis')
    plt.plot(salnmft,-gdepw,'r',label='NEMO')
    plt.xlabel("Salinity [PSU]")
    plt.ylabel("Depth [m]")
    plt.title('Salinity profile comparison, after vertical interpolation'+\
    py.str_(np.squeeze(int(bathynm[145,276]))))
    plt.legend()
    plt.grid()
    # Save the figure to file
    plt.savefig('./FIGURES/SALINITY_PROFILE_comparison_'+tname+'.png',dpi=150)
    plt.close()
##################################################################
## Checking unstable profiles of potential density
print('Checking unstable profiles of potential density')
print(' ')
[tempnmfl,salnmfl] = check_pdens_profile(lonnm,latnm,gdepw,tempnmf,salnmf)
##################################################################
## Write TS initial condition netcdf output file
print('Write Temp. initial condition netcdf output file')
oTSFile = write_TS_IC_nc_output(lonnm, latnm, gdepw, tempnmfl, salnmfl, ic_output_folder, ic_output_filename)
##################################################################
##################################################################
