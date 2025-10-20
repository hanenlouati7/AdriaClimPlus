### To run: prepare_mean.py 1990 2014 
import subprocess
import sys
if len(sys.argv) != 3:
    print(f"Start and end yearin the format 'python prepare_mean.py 1990 2014'")
    sys.exit(1)

start_yr = int(sys.argv[1])
end_yr = int(sys.argv[2])

process_path_t2m = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/pp/files_t2m"
process_path_prec = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/pp/files_tp"
process_path_vn = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/pp/files_wind"
process_path_RH2 = "/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/pp/files_RH2"

print(f"Start year: {start_yr}. End year: {end_yr}")

### Ensemble Mean ###
seasons = ["winter", "spring", "summer", "autumn"]
months = ["1","2","3","4","5","6","7","8","9","10","11","12"]

print("T2M")
for i in range(0,4):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_t2m = f"{process_path_t2m}/T2_wrfout_d01_{yr}_{seasons[i-1]}.nc"
        output_file_t2m = f"{process_path_t2m}/T2_wrfout_d01_{start_yr}_{end_yr}_{seasons[i-1]}.nc"
        files.append(input_file_t2m)
    command = f"cdo ensmean {input_file_t2m} {output_file_t2m}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing t2m ensemble mean")

print("PREC")
for i in range(0,4):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_prec = f"{process_path_prec}/prec_wrfout_d01_{yr}_{seasons[i-1]}.nc"
        output_file_prec = f"{process_path_prec}/prec_wrfout_d01_{start_yr}_{end_yr}_{seasons[i-1]}.nc"
        files.append(input_file_prec)
    command = f"cdo ensmean {input_file_prec} {output_file_prec}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing prec ensemble mean")

print("RH2")
for i in range(0,4):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_RH2 = f"{process_path_RH2}/RH2_wrfout_d01_{yr}_{seasons[i-1]}.nc"
        output_file_RH2 = f"{process_path_RH2}/RH2_wrfout_d01_{start_yr}_{end_yr}_{seasons[i-1]}.nc"
        files.append(input_file_RH2)
    command = f"cdo ensmean {input_file_RH2} {output_file_RH2}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing RH2 ensemble mean")

print("vn")
for i in range(0,12):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_vn = f"{process_path_vn}/vn_wrfout_d01_{yr}_{months[i]}.nc"
        output_file_vn = f"{process_path_vn}/vn_wrfout_d01_{start_yr}_{end_yr}_{months[i]}.nc"
        files.append(input_file_vn)
    command = f"cdo ensmean {input_file_vn} {output_file_vn}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing vn ensemble mean")


