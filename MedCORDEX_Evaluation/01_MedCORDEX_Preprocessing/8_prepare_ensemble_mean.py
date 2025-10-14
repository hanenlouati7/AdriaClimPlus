### To run: 7_prepare_ensemble_mean.py 1980 2014 
import subprocess
import sys
if len(sys.argv) != 3:
    print(f"Start and end yearin the format 'python 5_prepare_ensemble_mean.py 2019 2023'")
    sys.exit(1)

start_yr = int(sys.argv[1])
end_yr = int(sys.argv[2])

print(f"Start year: {start_yr}. End year: {end_yr}")

def is_leap_year(year):
    return (year % 4 == 0)

### Ensemble Mean ###
seasons = ["winter", "spring", "summer", "autumn"]
months = ["1","2","3","4","5","6","7","8","9","10","11","12"]

print("T2M")
for i in range(0,4):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_t2m = f"../processed/MEDCORDEX_{yr}_t2m_{seasons[i]}.nc"
        output_file_t2m = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_t2m_{seasons[i]}.nc"
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
        input_file_tp = f"../processed/MEDCORDEX_{yr}_tp_{seasons[i]}.nc"
        output_file_tp = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_tp_{seasons[i]}.nc"
        if is_leap_year(int(yr)):
            del_file_tp = f"../processed/del_MEDCORDEX_{yr}_tp_{seasons[i]}.nc"
            command = f"cdo del29feb {input_file_tp} {del_file_tp}"
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while processing tp ensemble mean")
            files.append(del_file_tp)
        else:
            files.append(input_file_tp)
    command = f"cdo ensmean {input_file_tp} {output_file_tp}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing tp ensemble mean")

    command = "rm ../processed/del_*"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing tp ensemble mean")

print("Vn")
for i in range(0,12):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_vn = f"../processed/MEDCORDEX_{yr}_vn_{months[i]}.nc"
        output_file_vn = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_vn_{months[i]}.nc"
        files.append(input_file_vn)
    command = f"cdo ensmean {input_file_vn} {output_file_vn}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing vn ensemble mean")

print("LWsurfup")
for i in range(0,4):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_stru = f"../processed/MEDCORDEX_{yr}_stru_{seasons[i]}.nc"
        output_file_stru = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_stru_{seasons[i]}.nc"
        files.append(input_file_stru)
    command = f"cdo ensmean {input_file_stru} {output_file_stru}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing stru ensemble mean")

print("SWsurfdown")
for i in range(0,4):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_ssrd = f"../processed/MEDCORDEX_{yr}_ssrd_{seasons[i]}.nc"
        output_file_ssrd = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_ssrd_{seasons[i]}.nc"
        files.append(input_file_ssrd)
    command = f"cdo ensmean {input_file_ssrd} {output_file_ssrd}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing ssrd ensemble mean")

print("PSFC")
for i in range(0,4):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_PSFC = f"../processed/MEDCORDEX_{yr}_PSFC_{seasons[i]}.nc"
        output_file_PSFC = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_PSFC_{seasons[i]}.nc"
        files.append(input_file_PSFC)
    command = f"cdo ensmean {input_file_PSFC} {output_file_PSFC}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing PSFC ensemble mean")

print("SLP")
for i in range(0,4):
    files = []
    for yr in range(start_yr,end_yr+1):
        input_file_SLP = f"../processed/MEDCORDEX_{yr}_SLP_{seasons[i]}.nc"
        output_file_SLP = f"../processed/MEDCORDEX_{start_yr}_{end_yr}_SLP_{seasons[i]}.nc"
        files.append(input_file_SLP)
    command = f"cdo ensmean {input_file_SLP} {output_file_SLP}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing SLP ensemble mean")

