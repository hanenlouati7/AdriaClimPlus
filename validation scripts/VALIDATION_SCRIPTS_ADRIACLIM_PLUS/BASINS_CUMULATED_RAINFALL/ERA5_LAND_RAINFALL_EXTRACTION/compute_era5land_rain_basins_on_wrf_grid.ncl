;*********PLOTs**********
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"
; --------------------------------------------------------

;--Alessandro De Lorenzis
;--OPA Division
;--AdriaClim project

;-- Creation of .nc files containing ERA5 Land precipitation regridded on WRF grid so to be compared with WRF estrimations for basins

begin

;-- Set value for "wrf_inst" to read just lat and lon
  wrf_INST = "wrfout_d01_1991-01-01_12:00:00c"		; WRF-WRF_HYDRO
  path_INST = "/work/cmcc/ad07521/AdriaCLIM/valid_EOBS-ERA5_vs_WRF/ERA5_vs_WRF/WRF-Hydro/results_Exp1_hist/" ;WRF-WRF_HYDRO
  ;out_wrf = addfile ("/work/cmcc/ad07521/AdriaCLIM/valid_EOBS-ERA5_vs_WRF/ERA5_vs_WRF/WRF-Hydro/results_Exp1_hist/wrfout_d01_1991-01-01_12:00:00c","r") 
  
  year = tostring (getenv("YEAR"))

;--- Read files ERA5 Land
  ;out_era5   = addfile("/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/DATA_ERA5LAND_PRECIP/ERA5Land_precip_"+year+"_6h_all_year.nc" ,"r")
  out_era5   = addfile("/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_ERA5-Land/downloaded/ERA5-Land_"+year+".nc" ,"r")

;--- Extract ERA5 fields
  precip_era5= (out_era5->tp(:,::-1,:)) ;rainfall (mm)
;  printVarSummary (precip_era5)

;--- convert short to float
;  rain_era5_float = short2flt(precip_era5)
  rain_era5_float = tofloat(precip_era5)
;  print (rain_era5_float(1:10, 1:10, 1))

; convert the results from m in mm
  rain_era5 = rain_era5_float * 1000
;  print (rain_era5(1:10, 1:10, 1))

;--- extract lat lon  
  lat_era5 = out_era5->latitude(::-1)
  lon_era5 = out_era5->longitude(:)
  

;--- EXTRACT WRF DATA
;--- Read WRF output files "wrf_in" and "wrf_inst"
  wrfout_inst = addfile(path_INST+"/"+wrf_INST,"r")

;--Extract lat&lon from "wrf_inst"
  lat_wrf = (/wrfout_inst->XLAT(0,:,:)/)        ;lat (mass)
  lon_wrf = (/wrfout_inst->XLONG(0,:,:)/)       ;lon (mass)

;  printVarSummary (lat_wrf)

  DimLat = dimsizes(lat_wrf)
  nS_N = DimLat(0)           ;S_N dimension
;  nS_N = dimsizes(lat_wrf)           ;S_N dimension
  nW_E = DimLat(1)           ;W_E dimension
;  nW_E = dimsizes(lon_wrf)           ;W_E dimension
;    print("nS_N="+nS_N)
;    print("nW_E="+nW_E)

;--WRF (WRF_HYDRO) fields bilinearly interpolated on ERA5 Land regular grid
;if (year .eq. "1992" .or. year .eq. "1996" .or. year .eq. "2000" .or. year .eq. "2004" .or. year .eq. "2008" .or. year .eq. "2012" .or. year .eq. "2016" .or. year .eq. "2020") then
;	precip_wrf_interp = new((/366, nS_N, nW_E/), float)
;else 
;	precip_wrf_interp = new((/365, nS_N, nW_E/), float)  
;end if

;  INTERPOLATION ON ERA5LAND GRID
;  precip_wrf_interp = linint2 (lon_wrf(0,:),lat_wrf(:,0),rain_wrf, False, lon_era5,lat_era5, 0)

;  INTERPOLATION ON WRF GRID
   precip_era5_interp = linint2 (lon_era5,lat_era5,rain_era5, False, lon_wrf(0,:),lat_wrf(:,0), 0)
;  printVarSummary (precip_wrf_interp)
;  print (precip_era5_interp(0,1:10,1:10))

;-- fill the Nan with 
  guess     = 1                ; use zonal means
  is_cyclic = True             ; cyclic [global]
  nscan     = 1500             ; usually much less than this
  eps       = 1.e-2            ; variable dependent
  relc      = 0.6              ; relaxation coefficient
  opt       = 0                ; not used

  precip_era5_interp2 = precip_era5_interp 
  poisson_grid_fill (precip_era5_interp2, is_cyclic, guess, nscan, eps, relc, opt)

;-- remove any pre-existing file
 system ("rm -rf /work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/DATA_ERA5LAND_PRECIP/rain_ERA5Land_"+year+"_basins_on_wrf_grid.nc")

;-- open output netCDF file
 fout = addfile("/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/DATA_ERA5LAND_PRECIP/rain_ERA5Land_"+year+"_basins_on_wrf_grid.nc", "c")

;-- output variables directly. NCL will call appropriate functions to write the meta data associated with each variable
 if (year .eq. "2020") .or. (year .eq. "1992") .or. (year .eq. "1996") .or. (year .eq. "2000") .or. (year .eq. "2004") .or. (year .eq. "2008") .or. (year .eq. "2012") .or. (year .eq. "2016")  then
  	rain = new ((/1464, nS_N, nW_E/), "float")
 	time = new ((/1464/), "float")
  else 
	rain = new ((/1460, nS_N, nW_E/), "float")
 	time = new ((/1460/), "float")
  end if

  lat = new ((/nS_N/), "float")
  lon = new ((/nW_E/), "float")
;-- variable tp is 365 (time) x 193 (lat) x 181 (lon)  
  rain!0		= "time"		; assign named dimensions
  rain!1		= "lat"
  rain!2		= "lon"
  rain@long_name	= "Total precipitation"					; assigns attributes
  rain@units	= "mm"

  time!0	= "time"
  lat!0		= "lat"
  lon!0		= "lon"

  time@long_name= "time"
  time@units	= "days"
  lat@long_name	= "latitude"
  lat@units	= "north degrees"
  lon@long_name	= "longitude"
  lon@units	= "east degrees"

  fout->rain 	= rain
  fout->lat	= lat
  fout->lon     = lon
  fout->time	= time

;-- fill the variables with the appropriate values
  fout->rain 	= (/precip_era5_interp2/)
  fout->lat	= (/lat_wrf(:,0)/)
  fout->lon     = (/lon_wrf(0,:)/)

;-- create global attributes of the file
  fAtt 			= True						; assigns file attributes
  fAtt@title		= "NCL Simple Approach to netCDF Creation"
  fAtt@Conventions	= "None"
  fAtt@creation_date	= systemfunc("date")
  fileattdef (fout, fAtt)						; copy files attributes

end
