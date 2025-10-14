import subprocess
yr_v = ['1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', 
        '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', 
        '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', 
        '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', 
        '2020', '2021', '2022', '2023']
### Wind Average ###
def is_leap_year(year):
    return (year % 4 == 0)

for yr in yr_v:
    if int(yr) <= 2014:
        input_file1 = f"/data/inputs/METOCEAN/historical/model/atmos/ENEA/Med-CORDEX/historical/{yr}/U10_earth_{yr}.nc"
        input_file2 = f"/data/inputs/METOCEAN/historical/model/atmos/ENEA/Med-CORDEX/historical/{yr}/V10_earth_{yr}.nc"
    else:
        input_file1 = f"/data/inputs/METOCEAN/historical/model/atmos/ENEA/Med-CORDEX/projections/SSP585/{yr}/U10_earth_{yr}.nc"
        input_file2 = f"/data/inputs/METOCEAN/historical/model/atmos/ENEA/Med-CORDEX/projections/SSP585/{yr}/V10_earth_{yr}.nc"

    if int(yr) == 2005:
         input_file1 = f"/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_MEDCORDEX/downloaded_processed/2005/U10_earth_{yr}.nc"
         input_file2 = f"/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_MEDCORDEX/downloaded_processed/2005/V10_earth_{yr}.nc"
    if int(yr) == 2006:
         input_file1 = f"/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_MEDCORDEX/downloaded_processed/2006/U10_earth_{yr}.nc"
         input_file2 = f"/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_MEDCORDEX/downloaded_processed/2006/V10_earth_{yr}.nc"

    output_file = f"../processed/vn_MEDCORDEX_{yr}_merged"
    command = f'cdo -O merge {input_file1} {input_file2} {output_file}'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")

    input_file = f"../processed/vn_MEDCORDEX_{yr}_merged"
    output_file = f"../processed/vn_MEDCORDEX_{yr}_vn"
    command = f'cdo expr,"vn=sqrt(U10_earth*U10_earth + V10_earth*V10_earth)" {input_file} {output_file}'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")

    output_file1 = f"../processed/vn_MEDCORDEX_{yr}_merged_vn"
    command = f'cdo -O merge {input_file} {output_file} {output_file1}'
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}: {e}")

    input_file = f"../processed/vn_MEDCORDEX_{yr}_merged_vn"
    output_file = f"../processed/MEDCORDEX_{yr}_vn"

    if is_leap_year(int(yr)):
        steps = [(1, 124), (125, 240), (241, 364), (365, 484), (485, 608), (609, 728), (729, 852), (853, 976), (977, 1096), (1097, 1220), (1221, 1340), (1341, 1464)]
    else:
        steps = [(1, 124), (125, 236), (237, 360), (361, 480), (481, 604), (605, 724), (725, 848), (849, 972), (973, 1092), (1093, 1216), (1217, 1336), (1337, 1460)]

    for i, (start, end) in enumerate(steps, 1):
        ### Extracting the seasonal data ###
        command = f"cdo seltimestep,{start}/{end} {input_file} {input_file}_{i}.nc"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

        ### Extracting the seasonal data ###
        command = f"cdo timmean {input_file}_{i}.nc {output_file}_{i}.nc"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while processing {yr} for part {i}: {e}")

    command = f"rm -f ../processed/vn_*"
    try:
        subprocess.run(command, shell=True, check=True)
    finally:
        print("Some files don't exist to delete")

