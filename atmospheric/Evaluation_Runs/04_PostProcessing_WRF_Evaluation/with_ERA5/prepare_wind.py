import subprocess
import xarray as xr
import os
from glob import glob
yr_v = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
mn_v = ['01','02','03','04','05','06','07','08','09','10','11','12']
dt_v = [str(i).zfill(2) for i in range(1, 32)]
wrfout_path = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP"
era5_path = "/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_ERA5/processed"
process_path = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/pp/ERA5/files_wind"
### Wind monthly Average ###
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
            ### Extracting U10 and V10 ###
            input_file = f"{wrfout_path}/wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            output_file = f"{process_path}/del_wind_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            command = f"cdo selvar,U10,V10 {input_file} {output_file}"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while processing {yr}: {e}")
            ### Calculating Vn ###
            input_file = f"{process_path}/del_wind_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            output_file = f"{process_path}/del_vn_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            command = f'cdo expr,"vn=sqrt(U10*U10 + V10*V10)" {input_file} {output_file}'
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while processing {yr}: {e}")
            ### Merge ###
            input_file1 = f"{process_path}/del_wind_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            input_file = f"{process_path}/del_vn_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            output_file = f"{process_path}/del_merged_vn_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            command = f"cdo merge {input_file1} {input_file} {output_file}"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while processing {yr}: {e}")
            ### Remapping ###
            input_file = f"{process_path}/del_merged_vn_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            remap_ref_file = f"{era5_path}/ERA5_1990_unpacked.nc"
            remapped_output_file = f"{process_path}/del_remapped_vn_wrfout_d01_{yr}-{mn}-{dt}_00:00:00"
            command = f"cdo -remapnn,{remap_ref_file} {input_file} {remapped_output_file}"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while processing {yr}: {e}")

    ### Merging ###
    file_pattern = os.path.join(process_path, f"del_remapped_vn_wrfout_d01_{yr}-*-*_00:00:00")
    files = sorted(glob(file_pattern))
    output_file = f"{process_path}/del_remapped_vn_wrfout_d01_{yr}.nc"
    command = f"cdo mergetime {' '.join(files)} {output_file}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")

    ### Preparing seasonal T2m ###
    if is_leap_year(int(yr)):
        steps = [(1, 124), (125, 240), (241, 364), (365, 484), (485, 608), (609, 728), (729, 852), (853, 976), (977, 1096), (1097, 1220), (1221, 1340), (1341, 1464)]
    else:
        steps = [(1, 124), (125, 236), (237, 360), (361, 480), (481, 604), (605, 724), (725, 848), (849, 972), (973, 1092), (1093, 1216), (1217, 1336), (1337, 1460)]

    for i, (start, end) in enumerate(steps, 1):
        input_file = f"{process_path}/del_remapped_vn_wrfout_d01_{yr}.nc"
        output_file = f"{process_path}/del_remapped_vn_wrfout_d01_{yr}"
        ### Extracting the seasonal data ###
        command = f"cdo seltimestep,{start}/{end} {input_file} {output_file}_all_{i}.nc"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

        input_file = f"{process_path}/del_remapped_vn_wrfout_d01_{yr}_all_{i}.nc"
        output_file = f"{process_path}/vn_wrfout_d01_{yr}"
        ### Monthly mean ###
        command = f"cdo timmean {input_file} {output_file}_{i}.nc"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")
    command = f"rm -f {process_path}/del_*"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")

