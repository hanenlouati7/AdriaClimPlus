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
loni,lati,bathyi = load_input_EMODnet_bathy(lonoi,lonoe,latoi,latoe,bathyi_filename)
bathyiv = load_input_EMODnet_venice_bathy(loni,lati,bathyi,bathyiv_filename)
##################################################################
## Interpolate bathymetry to new region
print('Interpolate bathymetry to new domain')
print(' ')
lono,lato,bathyo,mask = interp_bathy(loni,lati,bathyiv,lonoi,lonoe,dx,latoi,latoe,dy)
##################################################################
## Remove isolated sea point
print('Remove isolated sea points')
print(' ')
bathyo = remove_isolated_point(bathyo)
##################################################################
## Smooth the Bathymetry
if(ibsmooth==1):
    print('Smoothing the Bathymetry')
    print(' ')
    bathyo = smoothgrid(bathyo)
##################################################################
## Boundary interpolation to father grid bathymetry
if(interpbc==1):
    print('Boundary bathymetry interpolation to the bigger boundary conditions bathymetry')
    print(' ')
    lonf,latf,bathyfi = load_input_father_bathy(bathyf_filename,bathyf_name)
    lonf,latf,bathyf = load_input_father_bathy(bathyf_filename,bathyf_name)
    M=len(np.squeeze(bathyo[:,0]))-1
    L=len(np.squeeze(bathyo[0,:]))-1
    bathyf[bathyf==np.min(bathyf)]=0
    Fbdy=griddata((lonf.flatten(),latf.flatten()),bathyf.flatten(),(lono,lato),method='linear')
    Fbdy[Fbdy>1.e10]=0
    for i in range(0,interpnp+2):
        if(i==0): aa=1.0; bb=0.0
        if(i>=1 and i<=interpnp): np=interpnp/1.0; nn=i-1.0; aa=(np-nn)/np; bb=nn/np
        if(i==interpnp+1): aa=0.0; bb=1.0
        if(bdyS==1):
            #bathyo[i,:]=aa*Fbdy[0,:]+bb*bathyo[interpnp+1,:]
            bathyo[i,:]=Fbdy[i,:]
        if(bdyN==1):
            #bathyo[M-i,:]=aa*Fbdy[M,:]+bb*bathyo[M-interpnp,:]
            bathyo[M-i,:]=Fbdy[M-i,:]
        if(bdyW==1):
            #bathyo[:,i]=aa*Fbdy[:,0]+bb*bathyo[:,interpnp+1]
            bathyo[:,i]=Fbdy[:,i]
        if(bdyE==1):
            #bathyo[:,L-i]=aa*Fbdy[:,L]+bb*bathyo[:,L-interpnp]
            bathyo[:,L-i]=Fbdy[:,L-i]
        del aa, bb
##################################################################
## Edit mask 
editfig = input('Do you want to edit the mask (y or n)?')
mask[bathyo>0]=1.0
nn=0
while (editfig.lower() == "y".lower()):
    nn=nn+1
    plt.figure(figsize=(12, 12))
    plt.pcolor(mask, shading='flat', vmin=0, vmax=1)
    plt.contour(mask, [0.5], colors='w', linewidths=2)
    plt.show(block=False)
    if(nn==1):
        editfig = input("Do you want to start editing the mask (y or n - zoom in on the region of interest before answering the question)?")
    if(nn>1):
        editfig = input("Do you want to continue editing the mask (y or n - zoom in on the region of interest before answering the question)?")
    if (editfig.lower() == "y".lower()):
        gg = plt.ginput(n=2, timeout=0, show_clicks=True)
        p1 = gg[0] ; p2 = gg[1]
        y1=int(min(p1[1],p2[1])) ; y2=int(max(p1[1],p2[1]))
        x1=int(min(p1[0],p2[0])) ; x2=int(max(p1[0],p2[0]))
        mask[y1:y2,x1:x2]=0.0
        bathyo[y1:y2,x1:x2]=0.0
    #plt.show(block=False)
    plt.pause(1)
    plt.close()
##################################################################
## Apply minimum depth bathymetry
##if(hmin>0):
bathyo[bathyo<hmin]=hmin
##
#minln=lono[0,0] ; maxln=lono[0,-1]
#minlt=lato[0,0] ; maxlt=lato[-1,0]

#for i in range(0, len(lonf[0,:])):
#    if(lonf[0,i]<=minln): ln1=i
#    if(lonf[0,i]<=maxln): ln2=i
#for i in range(0, len(latf[:,0])):
#    if(latf[i,0]<=minlt): lt1=i
#    if(latf[i,0]<=maxlt): lt2=i
#ln1=ln1+1 ; lt1=lt1+1

#bathy_ft=griddata((lono.flatten(),lato.flatten()),bathyo.flatten(),(lonf[lt1-1:lt2-1,ln1-1:ln2-1],latf[lt1-1:lt2-1,ln1-1:ln2-1]),method='linear')

#bathyf[lt1-1:lt2-1,ln1-1:ln2-1]=bathy_ft
##################################################################
### zero bathymetry gradient along the 3 last points on open boundaries
##print('Zero bathymetry gradient along open boundaries')
##bathyo = zero_bathy_gradient(bdyS,bdyN,bdyW,bdyE,bathyo)
##################################################################
## Create and write interpolated bathymetry netcdf output file
print(' ')
print('Create and write new domain bathymetry netcdf output file')
print(' ')
oFile1 = create_write_nc_bathy_output_agrif(lono, lato, bathyo, mask, bathyo_filename)
#oFile2 = create_write_nc_bathy_output(lonf, latf, bathyf, bathyf_filename_new)
##################################################################
## Plot original and interpolated bathymetries
if(iplot==1):
    print('Plot original and new domain bathymetries')
    print(' ')

    cmap = plt.cm.jet  # define the colormap
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    # force the first color entry to be grey
    cmaplist[0] = (.5, .5, .5, 1.0)
    # create the new map
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

    fig,axs = plt.subplots(1, 2, figsize=(10,6))
    fig.suptitle('NEMO BATHYMETRY - Created by NPP package',fontsize=14,fontweight='bold')
    for ax in axs.flat:
        ax.set_xlabel('Longitude',fontsize=12,fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12,fontweight='bold')

    aa=axs[0].pcolor(loni,lati,bathyiv,cmap=cmap, vmin=0, vmax=2000)
    anchored_text1 = AnchoredText('Original Bathy', loc=1)
    axs[0].add_artist(anchored_text1)

    aa=axs[1].pcolor(lono,lato,bathyo,cmap=cmap, vmin=0, vmax=np.max(bathyo))#2000)
    anchored_text1 = AnchoredText('Interpolated Bathy', loc=1)
    axs[1].add_artist(anchored_text1)

    fig.subplots_adjust(right=0.875)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
    fig.colorbar(aa, cax=cbar_ax)
    cbar_ax.set_title('m')
    cbar_ax.tick_params(labelsize=12)

    # Save the figure to file
    plt.savefig('./FIGURES/NEMO_Bathymetry_'+tname+'.png',dpi=150)

    plt.show()
##################################################################
