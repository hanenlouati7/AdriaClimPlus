##################################################################
## Input params to create a new NEMO inout files using NPP package
##################################################################
## New NEMO test name
tname='ADR01'
## Define if plot output and analysis
iplot=0    ## 0=noplot or 1=plot
######################################################################
## Define inputs to create NEMO Bathymetry
##
## Path to original bathymetry file
bathyi_filename = '../EMODnet_bathymetry/EMODnet_2020_MED.nc'
## Define if smooth the bathymetry
ibsmooth=0
## Define minimum depth bathymetry (if hmin==0, hmin not defined)
hmin=0
## Define if create an interpolation between bathymetries on the boundaries
interpbc=1
## if interpbc=1 define number of points used on the interpolation (interpnp must be greater than 2)
interpnp=4
## Path/name to bigger/father model bathymetry to be interpolated on the boundaries
bathyf_filename = '/work/opa/vs15521/NEMO_pre_proc/Reanalysis/MED-MFC_006_013_mask_bathy_cut.nc'
bathyf_name     = 'deptho'   # name of bathymetry variable
## Define new NEMO bathymetry grid limits
lonoi= 12.0000    ## min. longiutde (West limit)
lonoe= 20.97917   ## max. longiutde (East limit)
latoi= 39.0000    ## min. latitude  (South limit)
latoe= 45.8752    ## max. latitude  (North limit)
## Define new NEMO bathymetry grid resolution
dx=1./48       ## Zonal resolution (longiutde)
dy=1./48       ## Meridional resolution (latitude)
## Define open boundaries (=1)
## Also used in the boundary conditions
bdyS=1   ## South boundary (1=open; 0=close)
bdyN=0   ## North boundary (1=open; 0=close)
bdyW=0   ## West  boundary (1=open; 0=close)
bdyE=0   ## East  boundary (1=open; 0=close)
## Path/name to new interpolated NEMO bathymetry file
## in case the bathymetry file was created previously (with another package), 
## define the file's path to be used in the other files creation
bathyo_filename = '../NEMO_input_files/depth_ADRb.020_04.nc'
###################################################################
## Define inputs to create NEMO Initial conditions
##
## Define if create vertical discretization
## or if will use domain NEMO file 
kp = 120    ## Number of levels
vdiscr=1    ## 0 = create vertical discretization; 1 = use domain NEMO file
##
if(vdiscr==0):
## Define vertical grid params
    sh = 30     ## Define stretching parameter
    sr = 0.82   ## Surface resolution [zero to 1]
    zd = 2600.0 ## Max. depth considerate
##
if(vdiscr==1):
## Path/name to domain NEMO input file
    domain_NEMO_filename = '../NEMO_input_files/domain_cfg_04.nc'
## Path to output files folder
ic_output_folder='./ic_outputs_MFSe3r1'
## Name to new interpolated NEMO TS initial file
ic_output_filename = 'NEMO_NPP_TS_IC_ADRI2km_MFSe3r1M_v04_nomask_1990.nc'
## Define Temp. and Sal. Initial input files (CMEMS Reanalysis)
tempi_filename='/data/inputs/METOCEAN/historical/model/ocean/CMS/MedSea/CMCC/reanalysis/month/1990/19900101_m-CMCC--TEMP-MFSe3r1-MED-b20200901_re-sv01.00.nc'
sali_filename='/data/inputs/METOCEAN/historical/model/ocean/CMS/MedSea/CMCC/reanalysis/month/1990/19900101_m-CMCC--PSAL-MFSe3r1-MED-b20200901_re-sv01.00.nc'
#tempi_filename='/data/inputs/METOCEAN/historical/model/ocean/CMS/MedSea/CMCC/reanalysis/day/1990/01/19900101_d-CMCC--TEMP-MFSe3r1-MED-b20200901_re-sv01.00.nc'
#sali_filename='/data/inputs/METOCEAN/historical/model/ocean/CMS/MedSea/CMCC/reanalysis/day/1990/01/19900101_d-CMCC--PSAL-MFSe3r1-MED-b20200901_re-sv01.00.nc'
######################################################################
## Define inputs to create NEMO Boundary Conditions
bc_year=2019         # define year to create files
bc_monthini=1        # define initial month to create files
bc_monthend=1        # define final month to create files
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
######################################################################
## Define inputs to create NEMO Surface Forcing
sf_year=2019         # define year to create files
sf_monthini=1        # define initial month to create files
sf_monthend=1        # define final month to create files
## Path/name to input ERA5 files
sf_input_folder='/work/opa/vs15521/ERA5-ECMWF/'
## Prefix/Sufix of the input ERA5 files
sf_input_filename='ERA5-ECMWF_MED_'
## Path/name to output ERA5 files and interpolation weights NEMO files
sf_output_folder='./outputs_surface_forcing/'
## Prefix for output ERA5 files
sf_output_filename='ecmwf_NCAR'
##################################################################
