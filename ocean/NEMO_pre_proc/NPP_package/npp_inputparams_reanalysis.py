##################################################################
## Input params to create a new NEMO inout files using NPP package
##################################################################
## New NEMO test name
tname='AdriaClimPlus'
## Defines if plot output and analysis
iplot=0    ## 0=noplot or 1=plot
######################################################################
## Defines inputs to create NEMO Bathymetry
##
## Path to original bathymetry file
bathyi_filename = '../NEMO_input_files/EMODnet_2020_MED.nc'
#bathyi_filename = '../EMODnet_bathymetry/all_adriatic_Murat.nc'
## Defines if smooth the bathymetry (1=true; 0=false)
ibsmooth=0
## Defines minimum depth bathymetry (if hmin==0, hmin not defined)
hmin=0
## Defines if create an interpolation between bathymetries on the boundaries (1=true; 0=false)
interpbc=1
## if interpbc=1, define number of points used on the interpolation (interpnp must be greater than 2)
interpnp=4
## if interpbc=1, define path/name to bigger/father model bathymetry to be interpolated on the boundaries
bathyf_filename = '/work/opa/vs15521/NEMO_pre_proc/Reanalysis/MED-MFC_006_013_mask_bathy_cut.nc'
bathyf_name     = 'deptho'   # name of bathymetry variable
## Defines new NEMO bathymetry grid limits
lonoi= 12.0000    ## min. longitude (West limit)
lonoe= 20.97917   ## max. longitude (East limit)
latoi= 39.0000    ## min. latitude  (South limit)
latoe= 45.8752    ## max. latitude  (North limit)
## Defines new NEMO bathymetry grid resolution
dx=1./48       ## Zonal resolution (longitude)
dy=1./48       ## Meridional resolution (latitude)
## Defines open boundaries (=1)
## Also used in the boundary conditions
bdyS=1   ## South boundary (1=open; 0=close)
bdyN=0   ## North boundary (1=open; 0=close)
bdyW=0   ## West  boundary (1=open; 0=close)
bdyE=0   ## East  boundary (1=open; 0=close)
## Path/name to new interpolated NEMO bathymetry file
## in case the bathymetry file was created previously (with another package), 
## define the file's path to be used in the other files creation
#bathyo_filename = '../NEMO_input_files/bathymetry_npp_nosmooth.nc'
#bathyo_filename = '../NEMO_input_files/depth_ADRb.020_03s_notime.nc'
bathyo_filename = '../NEMO_input_files/depth_ADRb.020_03s.nc'
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
    domain_NEMO_filename = '../NEMO_input_files/domain_cfg_03s.nc'
## Path to output files folder
ic_output_folder='./ic_outputs_MedCordex'
## Name to new interpolated NEMO TS initial file
ic_output_filename = 'IC_MedCordex_19800801.nc'
## Defines Temp. and Sal. Initial input files (CMEMS Reanalysis)
tempi_filename='/data/inputs/METOCEAN/historical/model/ocean/ENEA/Med-CORDEX/historical/1980/THETA_1980_Daily.nc'
sali_filename='/data/inputs/METOCEAN/historical/model/ocean/ENEA/Med-CORDEX/historical/1980/SALT_1980_Daily.nc'
######################################################################
######################################################################
## Define inputs to create NEMO Boundary Conditions
bc_year=2019         # define year to create files
bc_monthini=1        # define initial month to create files
bc_monthend=1        # define final month to create files
## Path/name to input daily files folder
bc_input_folder='/data/inputs/METOCEAN/historical/model/ocean/CMS/MedSea/CMCC/reanalysis/day'
## Prefix/Sufix to complete the input files names
bc_input_ssh ='_d-CMCC--ASLV-MFSe3r1-MED-b20200901_re-sv01.00.nc'
bc_input_temp='_d-CMCC--TEMP-MFSe3r1-MED-b20200901_re-sv01.00.nc'
bc_input_sal ='_d-CMCC--PSAL-MFSe3r1-MED-b20200901_re-sv01.00.nc'
bc_input_vel ='_d-CMCC--RFVL-MFSe3r1-MED-b20200901_re-sv01.00.nc'
## Path/name to output files folder
bc_output_folder='./bc_outputs_reanalysis'
## Prefix for output files
bc_output_file='ADR_Reanalysis'
## Defines if BC only for 1 point (1=true; 0=false)
spBDY=1
## Defines to create tidal input files (1=true; 0=false)
tidei=1
######################################################################
## Defines inputs to create NEMO Surface Forcing
sf_year=1981         # define year to create files
sf_monthini=1        # define initial month to create files
sf_monthend=1        # define final month to create files
## Path/name to input ERA5 files
sf_input_folder='/work/opa/vs15521/FLAME/ERA5-ECMWF/hourly/'
## Path and name to input ERA5 mask file
#sf_mask_filename='/work/opa/vs15521/ERA5-ECMWF/ERA5_land_sea_mask_global.nc'
## Prefix/Sufix of the input ERA5 files
sf_input_filename='ERA5_ECMWF_'
## Path/name to output ERA5 files and interpolation weights NEMO files
sf_output_folder='./outputs_surface_forcing/'
## Prefix for output ERA5 files
sf_output_filename='ecmwf'
##################################################################
