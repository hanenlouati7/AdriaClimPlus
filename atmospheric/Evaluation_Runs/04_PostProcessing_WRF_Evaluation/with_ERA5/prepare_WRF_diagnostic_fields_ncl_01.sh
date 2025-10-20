#!/bin/bash
#BSUB -q s_long
#BSUB -J slp_td2
#BSUB -n 1
#BSUB -o run_%J.out
#BSUB -e run_%J.err
#BSUB -P 0566
#BSUB -M 32G


# Set the directory containing WRF output files
WRF_DIR="/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/WRF-WRF-Hydro/1990_2020/run/EXP/"

# Loop through all wrfout_d01_ files
for wrf_file in "$WRF_DIR"/wrfout_d01*; do
    if [ -f "$wrf_file" ]; then
        echo "Processing: $wrf_file"

        # Extract base filename without the path
        base_name=$(basename "$wrf_file")

        # Remove the extension if present (optional)
        base_name_no_ext="${base_name%%.*}"

        # Create the output file name
        out_file="${base_name_no_ext}_slp_td2.nc"

        # Generate a temp NCL script
        TEMP_NCL="temp_file.ncl"
        rm -f "$TEMP_NCL"

        cat << EOF > "$TEMP_NCL"
begin
    a = addfile("$wrf_file","r")
    slp = wrf_user_getvar(a,"slp",-1)  ; slp
    td2 = wrf_user_getvar(a,"td2",-1)  ; td2

    ; Extract lat/lon at first time index
    lat2d = a->XLAT(0,:,:)
    lon2d = a->XLONG(0,:,:)

    lat2d@units = "degrees_north"
    lon2d@units = "degrees_east"
    lat2d@standard_name = "latitude"
    lon2d@standard_name = "longitude"

    setfileoption("nc","Format","NetCDF4Classic")
    f_out = addfile("/work/cmcc/vr25423/Project/AdriaClimPlus/evaluation_run_30yrs_ERA5/pp/ERA5/files_SLP/files_all_data/${out_file}","c")

    ; Write variables
    f_out->SLP = slp
    f_out->TD2 = td2
    f_out->XLAT = lat2d
    f_out->XLONG = lon2d
end
EOF
ncl -Q "$TEMP_NCL"

        # Run the NCL script
        ncl -Q "$TEMP_NCL"

        # Clean up temp script
        rm -f "$TEMP_NCL"

fi
done
echo "Processing completed!"



