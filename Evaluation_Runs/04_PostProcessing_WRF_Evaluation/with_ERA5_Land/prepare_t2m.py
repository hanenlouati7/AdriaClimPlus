import subprocess
import xarray as xr
import os
from glob import glob
yr_v = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
mn_v = ['01','02','03','04','05','06','07','08','09','10','11','12']
dt_v = [str(i).zfill(2) for i in range(1, 32)]
wrfout_path = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP"
era5land_path = "/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_ERA5-Land/processed"
process_path = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/pp/files_t2m"
### T2m Average ###
def is_leap_year(year):
    year = int(year)
    return (year % 4 == 0)

for yr in yr_v:
    for mn in mn_v:
        if mn == '02':
            days_in_month = 29 if is_leap_year(yr) else 28
        elif mn in ['04', '06', '09', '11']:
            days_in_month = 30
        else:
            days_in_month = 31
        dt_v = [str(i).zfill(2) for i in range(1, days_in_month + 1)]
        for dt in dt_v:
            ### Extracting T2m ###
            input_file = f"{wrfout_path}/wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            output_file = f"{process_path}/del_T2_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            command = f"cdo selvar,T2 {input_file} {output_file}"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while processing {yr}: {e}")

            ### Remapping ###
            input_file = f"{process_path}/del_T2_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            remap_ref_file = f"{era5land_path}/ERA5-Land_1990_unpacked.nc"
            remapped_output_file = f"{process_path}/del_remapped_T2_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            command = f"cdo -remapnn,{remap_ref_file} {input_file} {remapped_output_file}"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while processing {yr}: {e}")

    ### Merging ###
    file_pattern = os.path.join(process_path, f"del_remapped_T2_wrfout_d01_{yr}-*-*_00:00:00")
    files = sorted(glob(file_pattern))
    output_file = f"{process_path}/del_remapped_T2_wrfout_d01_{yr}.nc"
    command = f"cdo mergetime {' '.join(files)} {output_file}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")

    ### Preparing seasonal T2m ###
    seasons = ["winter", "spring", "summer", "autumn"]
    if is_leap_year(int(yr)):
        steps = [(1, 364), (365, 728), (729, 1096), (1097, 1464)]
    else:
        steps = [(1, 360), (361, 724), (725, 1092), (1093, 1460)]

    for i, (start, end) in enumerate(steps, 1):
        input_file = f"{process_path}/del_remapped_T2_wrfout_d01_{yr}.nc"
        output_file = f"{process_path}/del_remapped_T2_wrfout_d01_{yr}"
        ### Extracting the seasonal data ###
        command = f"cdo seltimestep,{start}/{end} {input_file} {output_file}_all_{i}.nc"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")


        input_file = f"{process_path}/del_remapped_T2_wrfout_d01_{yr}_all_{i}.nc"
        output_file = f"{process_path}/T2_wrfout_d01_{yr}"
        ### Seasonal mean ###
        command = f"cdo timmean {input_file} {output_file}_{seasons[i-1]}.nc"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")
    command = f"rm -f {process_path}/del_*"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")

