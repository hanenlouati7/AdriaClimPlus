
## Input params to create a new NEMO inout files using NPP package
##################################################################
## New NEMO test name
tname='ADR01_agrif'
## Defines if plot output and analysis
iplot=0    ## 0=noplot or 1=plot
######################################################################
## Defines inputs to create NEMO Bathymetry
##
## Define if bathymetry is for agrif configuration
agrif=1
## Path to original bathymetry file
bathyi_filename = '/work/opa/vs15521/NEMO_pre_proc/NEMO_input_files/EMODnet_2020_MED.nc'
#bathyi_filename = '../EMODnet_bathymetry/all_adriatic_Murat.nc'
## Defines if smooth the bathymetry (1=true; 0=false)
ibsmooth=0
## Defines minimum depth bathymetry (if hmin==0, hmin not defined)
hmin=0
## Defines if create an interpolation between bathymetries on the boundaries (1=true; 0=false)
interpbc=1
## if interpbc=1, define number of points used on the interpolation (interpnp must be greater than 2)
interpnp=6
## if interpbc=1, define path/name to bigger/father model bathymetry to be interpolated on the boundaries
bathyf_filename = '/work/opa/vs15521/NEMO_pre_proc/NEMO_input_files/depth_ADRb.020_03s_notime.nc'
bathyf_name     = 'Bathymetry'   # name of bathymetry variable
## Defines new NEMO bathymetry grid limits
lonoi= 11.99999905 ## 12.03385    ## min. longitude (West limit)
lonoe= 13.89583302 ## 13.94020    ## max. longitude (East limit)
latoi= 42.93750000 ## 42.95052    ## min. latitude  (South limit)
latoe= 45.81260000 ## 45.86198    ## max. latitude  (North limit)
## Defines new NEMO bathymetry grid resolution
dx=1./(48*4)       ## Zonal resolution (longitude)
dy=1./(48*4)       ## Meridional resolution (latitude)
## Defines open boundaries (=1)
## Also used in the boundary conditions
bdyS=1   ## South boundary (1=open; 0=close)
bdyN=0   ## North boundary (1=open; 0=close)
bdyW=0   ## West  boundary (1=open; 0=close)
bdyE=1   ## East  boundary (1=open; 0=close)
## Path/name to new interpolated NEMO bathymetry file
## in case the bathymetry file was created previously (with another package), 
## define the file's path to be used in the other files creation
bathyo_filename = '../NEMO_input_files/depth_ADRb.020_03s_agrif_new4.nc'
if(agrif==1):
    bathyf_filename_new = '../NEMO_input_files/depth_ADRb.020_03s_father_agrif_new4.nc'
###################################################################
## Defines inputs to create NEMO Initial conditions
##
## Defines if create vertical discretization
## or if will use domain NEMO file 
kp = 120    ## Number of levels
vdiscr=1    ## 0 = create vertical discretization; 1 = use domain NEMO file
##
if(vdiscr==0):
## Defines vertical grid params
    sh = 30     ## Defines stretching parameter
    sr = 0.82   ## Surface resolution [zero to 1]
    zd = 2600.0 ## Max. depth considerate
##
if(vdiscr==1):
## Path/name to domain NEMO input file
    domain_NEMO_filename = '../NEMO_input_files/domain_cfg_agrif_new4.nc'
    ##domain_NEMO_filename = '../NEMO_input_files/domain_cfg_father_agrif_new4.nc'
## Path to output files folder
ic_output_folder='./ic_outputs_pynemo'
## Name to new interpolated NEMO TS initial file
ic_output_filename = '1_TS_initial_cond_Reanalysis_nomask_2010_agrif_new4.nc'
## Defines Temp. and Sal. Initial input files (CMEMS Reanalysis)
tempi_filename='/data/inputs/metocean/historical/model/ocean/CMCC/CMEMS/reanalysis/day/2010/01/20100101_d-CMCC--TEMP-MFSe3r1-MED-b20200901_re-sv01.00.nc'
sali_filename='/data/inputs/metocean/historical/model/ocean/CMCC/CMEMS/reanalysis/day/2010/01/20100101_d-CMCC--PSAL-MFSe3r1-MED-b20200901_re-sv01.00.nc'
######################################################################
## Defines inputs to create NEMO Boundary Conditions
bc_year=2010         # define year to create files
bc_monthini=1        # define initial month to create files
bc_monthend=12       # define final month to create files
## Path/name to input daily files folder
bc_input_folder='/data/inputs/metocean/historical/model/ocean/CMCC/CMEMS/reanalysis/day'
## Prefix/Sufix to complete the input files names
bc_input_ssh ='_d-CMCC--ASLV-MFSe3r1-MED-b20200901_re-sv01.00.nc'
bc_input_temp='_d-CMCC--TEMP-MFSe3r1-MED-b20200901_re-sv01.00.nc'
bc_input_sal ='_d-CMCC--PSAL-MFSe3r1-MED-b20200901_re-sv01.00.nc'
bc_input_vel ='_d-CMCC--RFVL-MFSe3r1-MED-b20200901_re-sv01.00.nc'
## Path/name to output files folder
bc_output_folder='./bc_outputs_pynemo'
## Prefix for output files
bc_output_file='ADR_Reanalysis'
## Defines if BC only for 1 point (1=true; 0=false)
spBDY=1
## Defines to create tidal input files (1=true; 0=false)
tidei=1
######################################################################
## Defines inputs to create NEMO Surface Forcing
sf_year=2010        # define year to create files
sf_monthini=2        # define initial month to create files
sf_monthend=12        # define final month to create files
## Path/name to input ERA5 files
sf_input_folder='/work/opa/mg01720/force/'
## Path and name to input ERA5 mask file
#sf_mask_filename='/work/opa/vs15521/ERA5-ECMWF/ERA5_land_sea_mask_global.nc'
## Prefix/Sufix of the input ERA5 files
sf_input_filename='ERA5_ECMWF_'
## Path/name to output ERA5 files and interpolation weights NEMO files
sf_output_folder='./1_outputs_surface_forcing/'
## Prefix for output ERA5 files
sf_output_filename='1_ecmwf'
##################################################################
