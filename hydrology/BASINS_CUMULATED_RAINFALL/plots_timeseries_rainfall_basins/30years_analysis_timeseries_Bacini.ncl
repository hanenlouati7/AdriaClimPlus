;*********PLOTs**********
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"
;load "roms_func.ncl"
; --------------------------------------------------------

;--validation procedure set by Alessandro De Lorenzis and Giorgia Verri
;--OPA Division
;--AdriaClim project

;--Script for producing timeseries to compare WRF output with ERA5Land measurements for 145 basins

begin

; -- Env variables for naming figures
   model = "WRF-WRF_HYDRO"
   name_exp = tostring(getenv("NAME_EXP"))
   dataset = "ERA5Land"

;-- Get env variables 
  counter = tointeger(getenv("counter"))	
  year = tostring(getenv("year"))	
  basin = tostring(getenv("basin"))
  print ("Counter = "+counter)  
  print ("I'm working on "+basin+ " basin")

  fig_out3 = tostring(getenv("fig_out3"))
  figs=(/fig_out3/)

; -- Path to ERA5Land and WRF data
  ERA5Land_data = "//work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/ERA5_LAND_RAINFALL_EXTRACTION/Rainfall_1990_2020_ERA5_Land_basins_on_wrf_grid.csv"
  wrf_data = "/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/WRF_WRF_HYDRO_EVAL_30_YEARS_RAINFALL_EXTRACTION/Rainfall_1990_2020_WRF_WRF-HYDRO_EVALUATION_30_YEARS.csv"
  Rivers_coordinates = "/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/Rivers.csv"

  path_fig = "/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/plots_timeseries_rainfall/data_plots_"+name_exp+"/all"


;  Read all fields for basins: name, lat and lon
   strs1 = asciiread(Rivers_coordinates,-1,"string")     ;Read all data into strs
;   printVarSummary (strs1)

; set the delimiter of each fields in Puglia dataset
   delim     = ","
 
;-----read the 10th column: name of the basin (for check)
   basin_name = str_get_field(strs1(counter+1), 10, delim)

;-----read 5th column: lon basin 
   lon_basin = stringtofloat(str_get_field(strs1(counter+1), 5, delim))

;-----read 6th column: lat basin 
   lat_basin = stringtofloat(str_get_field(strs1(counter+1), 6, delim))
 
   print ("   ")
   print ("CHECK!!! THE BASIN CONSIDERED IS: "+basin_name)
   print ("LAT: "+lat_basin)
   print ("LON: "+lon_basin)

;----------------------
; DATA EXTRACTION
;----------------------

;------ ERA5LAND DATA

; for this dataset, the datum at 00:00 refers to the cumlated rain registered in that day
; so, to compute the data every 6h, we need to follow this table:

;dato precip ore 6: dato ore 6
;dato precip ore 12: dato ore 12 - dato ore 6
;dato precip ore 18: dato ore 18 - dato ore 12
;dato ore 00: dato ore 00 giorno successivo - dato ore 18

strs_era5 = asciiread(ERA5Land_data,-1,"string")     ;Read all data into strs

; starting from 1 and not to 0 to avoid considering the cumulated of the first day of the year
; first value is the 06:00 of 1 January of the year considered
rain_era5_basin_extr = stringtofloat(str_get_field(strs_era5(2:45292), counter+2, delim))
;print (rain_era5_basin_extr)

 
rain_era5_basin = new ((/45291/),float) 
do index=0,45284
   	rain_era5_basin(index) =   rain_era5_basin_extr(index)					        ; datum at h 06
	rain_era5_basin(index+1) = rain_era5_basin_extr(index+1) - rain_era5_basin_extr(index) 		; datum at h 12
	rain_era5_basin(index+2) = rain_era5_basin_extr(index+2) - rain_era5_basin_extr(index+1)	; datum at h 18
	rain_era5_basin(index+3) = rain_era5_basin_extr(index+3) - rain_era5_basin_extr(index+2) 	; datum at h 00
	index := index+3
end do 	 
	rain_era5_basin(45288) = rain_era5_basin_extr(45288)
	rain_era5_basin(45289) = rain_era5_basin_extr(45289) - rain_era5_basin_extr(45288) 		; datum at h 12
	rain_era5_basin(45290) = rain_era5_basin_extr(45290) - rain_era5_basin_extr(45289) 		; datum at h 12


; to avoid negative values of precip (small values)
  do cc=0,dimsizes(rain_era5_basin)-1
	if (rain_era5_basin (cc) .lt. "0" ) then
		rain_era5_basin(cc) = 0
	end if
  end do
 
; compute the increasing cumulated precip
rain_era5_cumul = new ((/45292/),float)
rain_era5_cumul(0) = rain_era5_basin(0)	; first datum equal to the rain registered at 6 am 01/01/$year 
do pp=1,45290
	rain_era5_cumul(pp) = rain_era5_basin(pp)+rain_era5_cumul(pp-1)
end do
	rain_era5_cumul(45291) = -999
	rain_era5_cumul@_FillValue=-999


; compute the cumulated rain for ERA5Land
; we sum ONLY the 00:00 slices, that contains the cumulated rain for that day
 
;printVarSummary (rain_era5_basin_extr) 
rain_era5_part = new ((/11322/),float)
ii=0
do kk=0,11321
;	print ("kk begin loop: "+kk)
	rain_era5_part (kk) = rain_era5_basin_extr(ii+3)
	ii := ii+4   
;	print ("kk end loop: "+kk)
;	print (ii)
end do

;print (rain_era5_part)
rain_era5_cumul_sum = sum (rain_era5_part)
;print ("ERA5 cumul rain: "+rain_era5_cumul) 

;  printVarSummary (rain_era5_basin)
;  print (rain_era5_basin_extr(0:10))



;-------------------------
;------ WRF DATA
;--------------------------

strs_wrf = asciiread(wrf_data,-1,"string")     ;Read all data into strs
;  ncols     = dimsizes(str_split(strs_wrf(0),","))
;  nrows     = dimsizes(strs_wrf)
;  print("This file has " + nrows + " rows and " + ncols + " columns.")

rain_wrf = stringtofloat(str_get_field(strs_wrf(1:45292), counter+2, delim))
;printVarSummary (rain_wrf)
;  print (rain_wrf(0:10))


; compute the increasing cumulated precipitation
rain_wrf_cumul = new ((/45292/),float)
do ix=0,45290
	rain_wrf_cumul(ix) = rain_wrf(ix+1)-rain_wrf(0)
end do

;  print (rain_wrf_cumul(0:10))


; for this dataset, we have, for each line, the cumulated rainfall, according to the model, starting from the $year/01/01
; in order to compute the 6h precipitation, we need to subtract the (i+1)-th line with the i-th one 
  
rain_wrf_basin = new ((/45292/),float)
do iter=0,45290
   rain_wrf_basin (iter) = rain_wrf (iter+1) - rain_wrf (iter)
end do
   
;  printVarSummary (rain_wrf_basin)
;  print (rain_wrf_basin(0:10))



;----------
; STATISTICS
;-----------

;printVarSummary (rain_era5_basin)
;printVarSummary (rain_wrf_basin)
rain_era5_basin_final = new ((/45292/),float)
rain_era5_basin_final(0:45290) = rain_era5_basin  
;rain_era5_basin_final(1463) = 9.96921e+36
rain_era5_basin_final(45291) = -999
rain_era5_basin_final@_FillValue = -999

; BIAS (WRF-OBSERVATIONS)
  rain_bias = rain_wrf_basin-rain_era5_basin_final
;  print (rain_bias)

; RMSE 
  rain_rmse = dim_rmsd (rain_wrf_basin, rain_era5_basin_final)

; NRMSE ( = RMSE/max of observations)
  rain_norm_rmse = rain_rmse/max(rain_era5_basin_final)

; CV RMSE (= RMSE/sigma (model))
  rain_cv_rmse = rain_rmse/stddev(rain_wrf_basin)

; CORR
  rain_corr = escorc (rain_wrf_basin, rain_era5_basin_final)

;---- Print statistical indices
   
   print ("         ")
   print ("YEAR: "+year)
   print ("WRF WRF HYDRO : "+name_exp)
   print ("Rain WRF cumulated = "+sum(rain_wrf_basin))
   print ("Rain ERA5Land Basin cumulated = "+rain_era5_cumul_sum)
   print ("Rain BIAS cumulated = "+(sum(rain_wrf_basin)-rain_era5_cumul_sum))
   print ("         ")
   print ("Rain WRF 6h = "+avg(rain_wrf_basin))
   print ("Rain Basin 6h = "+avg(rain_era5_basin_final))
   print ("BIAS 6h = "+avg(rain_bias))
   print ("RMSE = "+rain_rmse)
   print ("NORM RMSE = "+rain_norm_rmse)
   print ("CV RMSE = "+rain_cv_rmse)
   print ("CORR = "+rain_corr)
   print ("         ")


;--- save statistics for each basin in an external file to be used in the "create_table.ncl" script to create the table
  namefile_stat = path_fig+"/"+model+"_"+name_exp+"_vs_"+dataset+"_rain_ave_"+year+".txt"
  write_table (namefile_stat,"a", [/basin_name, sum(rain_wrf_basin), rain_era5_cumul_sum, (sum(rain_wrf_basin)-rain_era5_cumul_sum), \
				   avg(rain_wrf_basin), avg(rain_era5_basin_final), avg(rain_bias), rain_rmse, rain_norm_rmse, rain_cv_rmse, rain_corr/],\
				   "%s %f %f %f %f %f %f %f %f %f %f")

;--- save variables in an external files for the plots in python
  rain_wrf_6h_table = new ((/45291/),float)
  rain_era5_6h_table = new ((/45291/),float)
  rain_wrf_cumul_table = new ((/45291/),float)
  rain_era5_cumul_table = new ((/45291/),float)
  rain_wrf_6h_table = rain_wrf_basin(0:45290)
  rain_era5_6h_table = rain_era5_basin_final(0:45290)
  rain_wrf_cumul_table = rain_wrf_cumul(0:45290)
  rain_era5_cumul_table = rain_era5_cumul(0:45290)

  namefile_plot = basin+"_"+model+"_"+name_exp+"_vs_"+dataset+"_rain_"+year+".txt"
  write_table (namefile_plot,"a", [/rain_wrf_6h_table, rain_era5_6h_table, rain_wrf_cumul_table, rain_era5_cumul_table/]," %.4f %.4f %.4f %.4f")
  out_dir="/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/plots_timeseries_rainfall/data_plots_"+name_exp+"/all"
  system("mv "+namefile_plot+" "+out_dir)


end
