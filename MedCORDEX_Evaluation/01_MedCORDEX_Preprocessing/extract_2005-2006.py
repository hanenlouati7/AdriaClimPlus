import subprocess
import os

def extract_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

yr_v = ['2005', '2006']
target_files = ["V10_earth_2005.nc","U10_earth_2005.nc","T2_2005.nc","SLP_2005.nc","RH2_2005.nc","PSFC_2005.nc","CLDT_2005.nc","CLDT_2005.nc","LWUPB_2005.nc","RAINC_2005.nc","RAINNC_2005.nc","SWDOWN_2005.nc","V10_earth_2006.nc","U10_earth_2006.nc","T2_2006.nc","SLP_2006.nc","RH2_2006.nc","PSFC_2006.nc","CLDT_2006.nc","CLDT_2006.nc","LWUPB_2006.nc","RAINC_2006.nc","RAINNC_2006.nc","SWDOWN_2006.nc"]
for yr in yr_v:
    directory_path = f"/data/inputs/METOCEAN/historical/model/atmos/ENEA/Med-CORDEX/historical/{yr}"
    file_paths = extract_files(directory_path)
    
    out_path = f"/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_MEDCORDEX/downloaded_processed/{yr}"
    os.makedirs(out_path, exist_ok=True)
    
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        if filename in target_files:
            output_file = os.path.join(out_path, f"{filename}")
            
            command = f"cdo seltimestep,1/2920/2 {file_path} {output_file}"
            try:
                subprocess.run(command, shell=True, check=True)
                print(f"Processed: {file_path} -> {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {file_path}: {e}")
