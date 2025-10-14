import subprocess
yr_v = ['1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020','2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2041', '2042', '2043', '2044', '2045', '2046', '2047', '2048', '2049', '2050', '2051', '2052', '2053', '2054', '2055', '2056', '2057', '2058', '2059', '2060', '2061', '2062', '2063', '2064', '2065', '2066', '2067', '2068', '2069', '2070', '2071', '2072', '2073', '2074', '2075', '2076', '2077', '2078', '2079', '2080', '2081', '2082', '2083', '2084', '2085', '2086', '2087', '2088', '2089', '2090', '2091', '2092', '2093', '2094', '2095', '2096', '2097', '2098', '2099', '2100']
### SWDOWN Average ###
def is_leap_year(year):
    return (year % 4 == 0)

for yr in yr_v:
    if int(yr) <= 2014:
        input_file = f"/data/inputs/METOCEAN/historical/model/atmos/ENEA/Med-CORDEX/historical/{yr}/SWDOWN_{yr}.nc"
    else:
        input_file = f"/data/inputs/METOCEAN/historical/model/atmos/ENEA/Med-CORDEX/projections/SSP245/{yr}/SWDOWN_{yr}.nc"
    if int(yr) == 2005:
         input_file = f"/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_MEDCORDEX/downloaded_processed/2005/SWDOWN_{yr}.nc"
    if int(yr) == 2006:
         input_file = f"/work/cmcc/vr25423/Project/AdriaClimPlus/data/data_MEDCORDEX/downloaded_processed/2006/SWDOWN_{yr}.nc"
    output_file = f"processed_SSP245/MEDCORDEX_{yr}_ssrd.nc"

    ### Yearly mean ###
    command = f"cdo timmean {input_file} {output_file}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {yr}")
