!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
!! NEMO/OPA  : namelist for BDY generation tool
!!            
!!             User inputs for generating open boundary conditions
!!             employed by the BDY module in NEMO. Boundary data
!!             can be set up for v3.2 NEMO and above.
!!            
!!             More info here.....
!!            
!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

!------------------------------------------------------------------------------
!   vertical coordinate
!------------------------------------------------------------------------------
   ln_zco      = .false.   !  z-coordinate - full    steps   (T/F)  
   ln_zps      = .true.    !  z-coordinate - partial steps   (T/F)
   ln_sco      = .false.   !  s- or hybrid z-s-coordinate    (T/F)
   rn_hmin     =   5       !  min depth of the ocean (>0) or 
                           !  min number of ocean level (<0)

!------------------------------------------------------------------------------
!   s-coordinate or hybrid z-s-coordinate
!------------------------------------------------------------------------------
   rn_sbot_min =   10.     !  minimum depth of s-bottom surface (>0) (m)
   rn_sbot_max = 7000.     !  maximum depth of s-bottom surface 
                           !  (= ocean depth) (>0) (m)
   ln_s_sigma  = .false.   !  hybrid s-sigma coordinates
   rn_hc       =  150.0    !  critical depth with s-sigma

!------------------------------------------------------------------------------
!  grid information 
!------------------------------------------------------------------------------
   sn_src_hgr = '/work/cmcc/vs15521/NEMO_pre_proc/MedCordex_ENEA/MedCordex_ENEA_mesh_hgr.nc'
   sn_src_zgr = '/work/cmcc/vs15521/NEMO_pre_proc/MedCordex_ENEA/MedCordex_ENEA_mesh_zgr.nc'
   sn_dst_hgr = '/work/cmcc/vs15521/NEMO_pre_proc/NEMO_input_files/mesh_hgr_03s.nc'
   sn_dst_zgr = '/work/cmcc/vs15521/NEMO_pre_proc/NEMO_input_files/mesh_zgr_03s.nc'
   sn_src_msk = '/work/cmcc/vs15521/NEMO_pre_proc/MedCordex_ENEA/MedCordex_ENEA_mask.nc'
   sn_bathy   = '/work/cmcc/vs15521/NEMO_pre_proc/NEMO_input_files/depth_ADRb.020_03s_notime.nc'

!------------------------------------------------------------------------------
!  I/O 
!------------------------------------------------------------------------------
   sn_src_dir = '/work/cmcc/vs15521/NEMO_pre_proc/NPP_package/inputs_pynemo/src_data_MedCordex.ncml'
   sn_dst_dir = '/work/cmcc/vs15521/NEMO_pre_proc/NPP_package/bc_outputs_MedCordex_ENEA'
   sn_fn      = 'ADR_MedCordex_ENEA_historical'             ! prefix for output files
   nn_fv      = -1e20                 !  set fill value for output files
   nn_src_time_adj = 0                ! src time adjustment
   sn_dst_metainfo = 'Benchmark Data'

!------------------------------------------------------------------------------
!  unstructured open boundaries                         
!------------------------------------------------------------------------------
    ln_coords_file = .true.               !  =T : produce bdy coordinates files
    cn_coords_file = 'coordinates.bdy.nc' !  name of bdy coordinates files 
                                          !  (if ln_coords_file=.TRUE.)
    ln_mask_file   = .false.              !  =T : read mask from file
    cn_mask_file   = 'mask.nc'            !  name of mask file 
                                          !  (if ln_mask_file=.TRUE.)
    ln_dyn2d       = .true.              !  boundary conditions for 
                                          !  barotropic fields
    ln_dyn3d       = .true.              !  boundary conditions for 
                                          !  baroclinic velocities
    ln_tra         = .true.               !  boundary conditions for T and S
    ln_ice         = .false.              !  ice boundary condition   
    nn_rimwidth    = 3                   !  width of the relaxation zone

!------------------------------------------------------------------------------
!  unstructured open boundaries tidal parameters                        
!------------------------------------------------------------------------------
    ln_tide        = .false.               !  =T : produce bdy tidal conditions
    sn_tide_model  = 'TPXO7p2'            !  Name of tidal model (FES2014|TPXO7p2)
    clname(1)      = 'M2'                 !  constituent name
    clname(2)      = 'S2'
    clname(3)      = 'N2'
    clname(4)      = 'K2'
    clname(5)      = 'K1'
    clname(6)      = 'O1'
    clname(7)      = 'P1'
    ln_trans       = .true.               !  interpolate transport rather than
                                          !  velocities
!------------------------------------------------------------------------------
!  Time information
!------------------------------------------------------------------------------
    nn_year_000     = 1981        !  year start
    nn_year_end     = 1981        !  year end
    nn_month_000    = 12          !  month start (default = 1 is years>1)
    nn_month_end    = 12          !  month end (default = 12 is years>1)
    sn_dst_calendar = 'gregorian' !  output calendar format
    nn_base_year    = 1900        !  base year for time counter
	! location of TPXO data
    sn_tide_grid   = '/work/cmcc/vs15521/NEMO_pre_proc/OTPS_highres/OTPSnc/DATA_MED/gridMed.nc'
    sn_tide_h      = '/work/cmcc/vs15521/NEMO_pre_proc/OTPS_highres/OTPSnc/DATA_MED/hf.Med2011.nc'
    sn_tide_u      = '/work/cmcc/vs15521/NEMO_pre_proc/OTPS_highres/OTPSnc/DATA_MED/uv.Med2011.nc'
!	sn_tide_grid   = '/work/cmcc/vs15521/FLAME/TPXO9.1/grid_tpxo9.nc'
!	sn_tide_h      = '/work/cmcc/vs15521/FLAME/TPXO9.1/h_tpxo9.v1.nc'
!	sn_tide_u      = '/work/cmcc/vs15521/FLAME/TPXO9.1/u_tpxo9.v1.nc'
	! location of FES2014 data
!	sn_tide_fes      = '/Users/mgunduz/PyNEMO/inputs/FES2014/'

	
!------------------------------------------------------------------------------
!  Additional parameters
!------------------------------------------------------------------------------
    nn_wei  = 1                   !  smoothing filter weights 
    rn_r0   = 0.041666666         !  decorrelation distance use in gauss
                                  !  smoothing onto dst points. Need to 
                                  !  make this a funct. of dlon
    sn_history  = 'Benchmarking test case'
                                  !  history for netcdf file
    ln_nemo3p4  = .true.          !  else presume v3.2 or v3.3
    nn_alpha    = 0               !  Euler rotation angle
    nn_beta     = 0               !  Euler rotation angle
    nn_gamma    = 0               !  Euler rotation angle
	rn_mask_max_depth = 100.0     !  Maximum depth to be ignored for the mask
	rn_mask_shelfbreak_dist = 20000.0 !  Distance from the shelf break
