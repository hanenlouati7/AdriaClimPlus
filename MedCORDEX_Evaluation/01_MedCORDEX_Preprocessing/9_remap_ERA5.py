### remap MEDCORDEX data over the ERA5 grid since MEDCORDEX data is finer than ERA5
#ERA5 --> 0.1 deg
#ERA 5 - Land --> 0.25 deg
#MEDCORDEX --> lat: 0.00014 deg to 0.03197 deg;   lon: 0.1 deg
# move all data except *remap*.nc to processed/ #
import subprocess
import sys
yr_v = ['1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989',
        '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999',
        '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
        '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
        '2020', '2021', '2022', '2023']

start_yr1 = 1985
end_yr1 = 2014 
start_yr2 = 2015
end_yr2 = 2023

seasons = ["winter", "spring", "summer", "autumn"]
months = ["1","2","3","4","5","6","7","8","9","10","11","12"]

### T2m Remap ###
#Each year
for yr in yr_v:
    for i in range(len(seasons)):
        input_file_era5land_t2m = f"../../data_ERA5/processed/ERA5_{yr}_t2m_{seasons[i]}.nc"
        input_file_medcordex_t2m = f"../processed/MEDCORDEX_{yr}_t2m_{seasons[i]}.nc"
        output_file_medcordex_t2m = f"../processed/MEDCORDEX_{yr}_t2m_remap_{seasons[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_t2m} {input_file_medcordex_t2m} {output_file_medcordex_t2m}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

#Ensemble
steps = [(start_yr1, end_yr1), (start_yr2, end_yr2)]
for start_yr, end_yr in steps:
    for i in range(len(seasons)):
        input_file_era5land_t2m = f"../../data_ERA5/processed/ERA5_{start_yr}_{end_yr}_t2m_{seasons[i]}.nc"
        input_file_medcordex_t2m = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_t2m_{seasons[i]}.nc"
        output_file_medcordex_t2m = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_t2m_remap_{seasons[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_t2m} {input_file_medcordex_t2m} {output_file_medcordex_t2m}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")



### Prec Remap ###
#Each year
for yr in yr_v:
    for i in range(len(seasons)):
        input_file_era5land_tp = f"../../data_ERA5/processed/ERA5_{yr}_tp_{seasons[i]}.nc"
        input_file_medcordex_tp = f"../processed/MEDCORDEX_{yr}_tp_{seasons[i]}.nc"
        output_file_medcordex_tp = f"../processed/MEDCORDEX_{yr}_tp_remap_{seasons[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_tp} {input_file_medcordex_tp} {output_file_medcordex_tp}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

#Ensemble
steps = [(start_yr1, end_yr1), (start_yr2, end_yr2)]
for start_yr, end_yr in steps:
    for i in range(len(seasons)):
        input_file_era5land_tp = f"../../data_ERA5/processed/ERA5_{start_yr}_{end_yr}_tp_{seasons[i]}.nc"
        input_file_medcordex_tp = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_tp_{seasons[i]}.nc"
        output_file_medcordex_tp = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_tp_remap_{seasons[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_tp} {input_file_medcordex_tp} {output_file_medcordex_tp}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")



### Vn Remap ###
#Each year
for yr in yr_v:
    for i in range(0,12):
        input_file_era5land_vn = f"../../data_ERA5/processed/ERA5_{yr}_vn_{months[i]}.nc"
        input_file_medcordex_vn = f"../processed/MEDCORDEX_{yr}_vn_{months[i]}.nc"
        output_file_medcordex_vn = f"../processed/MEDCORDEX_{yr}_vn_remap_{months[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_vn} {input_file_medcordex_vn} {output_file_medcordex_vn}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

#Ensemble
steps = [(start_yr1, end_yr1), (start_yr2, end_yr2)]
for start_yr, end_yr in steps:
    for i in range(0,12):
        input_file_era5land_vn = f"../../data_ERA5/processed/ERA5_{start_yr}_{end_yr}_vn_{months[i]}.nc"
        input_file_medcordex_vn = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_vn_{months[i]}.nc"
        output_file_medcordex_vn = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_vn_remap_{months[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_vn} {input_file_medcordex_vn} {output_file_medcordex_vn}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

### PSFC Remap ###
#Each year
for yr in yr_v:
    for i in range(len(seasons)):
        input_file_era5land_PSFC = f"../../data_ERA5/processed/ERA5_{yr}_PSFC_{seasons[i]}.nc"
        input_file_medcordex_PSFC = f"../processed/MEDCORDEX_{yr}_PSFC_{seasons[i]}.nc"
        output_file_medcordex_PSFC = f"../processed/MEDCORDEX_{yr}_PSFC_remap_{seasons[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_PSFC} {input_file_medcordex_PSFC} {output_file_medcordex_PSFC}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

#Ensemble
steps = [(start_yr1, end_yr1), (start_yr2, end_yr2)]
for start_yr, end_yr in steps:
    for i in range(len(seasons)):
        input_file_era5land_PSFC = f"../../data_ERA5/processed/ERA5_{start_yr}_{end_yr}_PSFC_{seasons[i]}.nc"
        input_file_medcordex_PSFC = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_PSFC_{seasons[i]}.nc"
        output_file_medcordex_PSFC = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_PSFC_remap_{seasons[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_PSFC} {input_file_medcordex_PSFC} {output_file_medcordex_PSFC}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")


### SLP Remap ###
#Each year
for yr in yr_v:
    for i in range(len(seasons)):
        input_file_era5land_SLP = f"../../data_ERA5/processed/ERA5_{yr}_MSLP_{seasons[i]}.nc"
        input_file_medcordex_SLP = f"../processed/MEDCORDEX_{yr}_SLP_{seasons[i]}.nc"
        output_file_medcordex_SLP = f"../processed/MEDCORDEX_{yr}_SLP_remap_{seasons[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_SLP} {input_file_medcordex_SLP} {output_file_medcordex_SLP}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

#Ensemble
steps = [(start_yr1, end_yr1), (start_yr2, end_yr2)]
for start_yr, end_yr in steps:
    for i in range(len(seasons)):
        input_file_era5land_SLP = f"../../data_ERA5/processed/ERA5_{start_yr}_{end_yr}_MSLP_{seasons[i]}.nc"
        input_file_medcordex_SLP = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_SLP_{seasons[i]}.nc"
        output_file_medcordex_SLP = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_SLP_remap_{seasons[i]}.nc"
        command = f"cdo -remapnn,{input_file_era5land_SLP} {input_file_medcordex_SLP} {output_file_medcordex_SLP}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

