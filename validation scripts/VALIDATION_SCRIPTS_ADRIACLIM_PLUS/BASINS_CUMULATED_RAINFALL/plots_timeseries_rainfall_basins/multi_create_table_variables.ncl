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

;--Saving statistics in Table

begin

; -- Env variables for naming figures
  model = "WRF-WRF_HYDRO"
  name_exp = tostring(getenv("NAME_EXP")) 
  year = tostring(getenv("year"))
  dataset = "ERA5Land"

;-- Path to the .txt file containing data  
 path_data = "/work/cmcc/ad07521/FLAME/WRF_WRF_HYDRO_validation/BACINI/ADRIACLIM_PLUS_EVAL_RUN_VALID/plots_timeseries_rainfall/data_plots_"+name_exp+"/all/"+model+"_"+name_exp+"_vs_"+dataset+"_rain_ave_1990_2020.txt"   

; open the .txt file with data 
 basins_list = asciiread(path_data,-1,"string")
 
; set the delimiter of each fields in Puglia dataset
 delim     = " "

 basins = str_get_field(basins_list, 1, delim) 		                            ; col. 1, name basins
 wrf_rain_cumulated = stringtofloat(str_get_field(basins_list, 2, delim))           ; col. 2, wrf cumulated
 era5_rain_cumulated = stringtofloat(str_get_field(basins_list, 3, delim))          ; col. 3, era5 cumulated
 bias_cumulated = stringtofloat(str_get_field(basins_list, 4, delim))               ; col. 4, bias cumulated
 wrf_rain_daily = stringtofloat(str_get_field(basins_list, 5, delim))               ; col. 5, wrf daily
 era5_rain_daily = stringtofloat(str_get_field(basins_list, 6, delim))              ; col. 6, era5 daily
 bias_daily = stringtofloat(str_get_field(basins_list, 7, delim))                   ; col. 7, bias daily
 rmse_rain = stringtofloat(str_get_field(basins_list, 8, delim))                    ; col. 8, rmse
 norm_rmse_rain = stringtofloat(str_get_field(basins_list, 9, delim))               ; col. 9, norm rmse
 cv_rmse_rain = stringtofloat(str_get_field(basins_list, 10, delim))                ; col.10, cv rmse
 corr_rain = stringtofloat(str_get_field(basins_list, 11, delim))                   ; col.11, corr
 
; FORMAT THE DATA IN MATRICES SO TO HAVE ONLY TWO NUMBERS AFTER COMMA
 
 tab_basins = basins
 tab_wrf_cumulated = sprintf("%.0f", wrf_rain_cumulated)
 tab_era5_cumulated = sprintf("%.0f", era5_rain_cumulated)
 tab_bias_cumulated = sprintf("%.0f", bias_cumulated)
 tab_wrf_daily = sprintf("%.2f", wrf_rain_daily)
 tab_era5_daily = sprintf("%.2f", era5_rain_daily)
 tab_bias_daily = sprintf("%.2f", bias_daily)
 tab_rmse = sprintf("%.2f", rmse_rain)
 tab_norm_rmse= sprintf("%.2f", norm_rmse_rain)
 tab_cv_rmse = sprintf("%.2f", cv_rmse_rain)
 tab_corr = sprintf("%.2f", corr_rain)

; CREATE TABLE FOR RAIN

; Header
;  ncr1  = (/1,1/)               ; 1 row, 1 column
;  x1    = (/0.005,0.335/)       ; Start and end X
;  y1    = (/0.900,0.995/)       ; Start and end Y
;  text1 = number_experiment+" "+variable_1

; Sub header
  ncr2  = (/2,11/)               ; 2 rows, 8 columns
  x2    = (/0,0.995/)           ; Start and end X
  y2    = (/0.900,0.995/)       ; Start and end Y
  text2 = (/ (/name_exp+", "+year,"WRF_HYDRO CUMUL.","ERA5LAND CUMUL.","BIAS CUMUL.","WRF_HYDRO 6h","ERA5LAND 6h","BIAS 6h","RMSE","NRMSE",\ 
	     "CV RMSE", "CORR"/),(/"BASIN", "mm/year", "mm/year", "mm/year", "mm/6h","mm/6h", "mm/6h", "mm/6h", "", "", ""/) /)

; Main table body

  ncr3  = (/145,11/) ; number of stations, 8 columns
  x3    = (/0,0.995/)       ; Start and end X
  y3    = (/0,0.900/)       ; Start and end Y

; create the text matrix

  text3_matrix_rain = new ((/145, 11/),string)

; fill the matrix 
  text3_matrix_rain (:,0) = basins
  text3_matrix_rain (:,1) = tostring(tab_wrf_cumulated)
  text3_matrix_rain (:,2) = tostring(tab_era5_cumulated)
  text3_matrix_rain (:,3) = tostring(tab_bias_cumulated)
  text3_matrix_rain (:,4) = tostring(tab_wrf_daily)
  text3_matrix_rain (:,5) = tostring(tab_era5_daily)
  text3_matrix_rain (:,6) = tostring(tab_bias_daily)
  text3_matrix_rain (:,7) = tostring(tab_rmse)
  text3_matrix_rain (:,8) = tostring(tab_norm_rmse)
  text3_matrix_rain (:,9) = tostring(tab_cv_rmse)
  text3_matrix_rain (:,10) = tostring(tab_corr)  
  
;  printVarSummary(text3_matrix)

  text3_rain = (/ text3_matrix_rain /)

  namefile2 = "Table_"+year+"_Basins_"+model+"_"+name_exp+"_vs_"+dataset
  wks = gsn_open_wks("png",namefile2)  ; send graphics to ps file

;
; Main header.
;
;  res1               = True
;  res1@txFontHeightF = 0.03
;  res1@gsFillColor   = "CornFlowerBlue"

;  gsn_table(wks,ncr1,x1,y1,text1,res1)

;
; Sub header
;
  res2               = True
  res2@txFontHeightF = 0.007
  res2@gsFillColor   = "CornFlowerBlue"

  gsn_table(wks,ncr2,x2,y2,text2,res2)

;
; Main body of table.
;
  res3 = True             ; Set up resource list

;  res3@gsnDebug = True     ; Useful to print NDC row,col values used.

  res3@txFontHeightF = 0.005
;  res3@gsFillColor = (/ (/"gray","transparent","transparent", "transparent","transparent","transparent","transparent","transparent"/) /)

  gsn_table (wks,ncr3,x3,y3,text3_rain,res3)

  frame(wks)      ; Advance the frame. 

end


