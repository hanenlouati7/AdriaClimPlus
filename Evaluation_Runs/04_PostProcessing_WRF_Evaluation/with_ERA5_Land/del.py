import subprocess
import xarray as xr
import os
from glob import glob
yr_v = ['2000']
mn_v = ['01','02','03','04','05','06','07','08','09','10','11','12']
dt_v = [str(i).zfill(2) for i in range(1, 32)]
wrfout_path = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP"
era5land_path = "/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_ERA5-Land/processed"
process_path = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/pp/files_tp"
### Precipitation ###
def is_leap_year(year):
    year = int(year)
    return (year % 4 == 0)

for yr in yr_v:

    ### Merging ###
    file_pattern = os.path.join(process_path, f"del_remapped_prec_wrfout_d01_{yr}-*-*_00:00:00")
    files = sorted(glob(file_pattern))
    output_file = f"{process_path}/del_remapped_prec_wrfout_d01_{yr}.nc"
    command = f"cdo mergetime {' '.join(files)} {output_file}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")

    ### preparing prec ###
    input_file = f"{process_path}/del_remapped_prec_wrfout_d01_{yr}.nc"
    output_file = f"{process_path}/del_processed_remapped_prec_wrfout_d01_{yr}.nc"
    command = f"cdo expr,'prec=RAINC+RAINNC+(100*I_RAINC)+(100*I_RAINNC)' {input_file} {output_file}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")

    ### Preparing seasonal Prec ###
    seasons = ["winter", "spring", "summer", "autumn"]
    if is_leap_year(int(yr)):
        steps = [(1, 364), (365, 728), (729, 1096), (1097, 1464)]
    else:
        steps = [(1, 360), (361, 724), (725, 1092), (1093, 1460)]

    for i, (start, end) in enumerate(steps, 1):
        input_file = f"{process_path}/del_processed_remapped_prec_wrfout_d01_{yr}.nc"
        output_file = f"{process_path}/prec_wrfout_d01_{yr}_{seasons[i-1]}.nc"
        ### Extracting the seasonal data ###
        command = f"cdo seltimestep,{start}/{end} {input_file} {output_file}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

    command = f"rm -f {process_path}/del_*"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")
