import subprocess
yr_v = ['1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', 
        '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', 
        '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', 
        '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', 
        '2020', '2021', '2022', '2023']
### SLP Average ###
def is_leap_year(year):
    return (year % 4 == 0)

for yr in yr_v:
    if int(yr) <= 2014:
        input_file = f"/data/inputs/METOCEAN/historical/model/atmos/ENEA/Med-CORDEX/historical/{yr}/SLP_{yr}.nc"
    else:
        input_file = f"/data/inputs/METOCEAN/historical/model/atmos/ENEA/Med-CORDEX/projections/SSP585/{yr}/SLP_{yr}.nc"
    if int(yr) == 2005:
         input_file = f"/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_MEDCORDEX/downloaded_processed/2005/SLP_{yr}.nc"
    if int(yr) == 2006:
         input_file = f"/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_MEDCORDEX/downloaded_processed/2006/SLP_{yr}.nc"
    output_file = f"../processed/MEDCORDEX_{yr}_SLP"

    seasons = ["winter", "spring", "summer", "autumn"]
    
    if is_leap_year(int(yr)):
        steps = [(1, 364), (365, 728), (729, 1096), (1097, 1464)]
    else:
        steps = [(1, 360), (361, 724), (725, 1092), (1093, 1460)]

    for i, (start, end) in enumerate(steps, 1):
        ### Extracting the seasonal data ###
        command = f"cdo seltimestep,{start}/{end} {input_file} {output_file}_all_{i}.nc"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

        ### Seasonal mean ###
        command = f"cdo timmean {output_file}_all_{i}.nc {output_file}_{seasons[i-1]}.nc"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

        command = f"rm -f {output_file}_all_{i}.nc"
        try:
            subprocess.run(command, shell=True, check=True)
        finally:
            print("Some files don't exist to delete")
