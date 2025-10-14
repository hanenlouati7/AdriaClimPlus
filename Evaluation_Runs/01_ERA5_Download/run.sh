#!/bin/bash
#BSUB -q s_long
#BSUB -J ERA5_download
#BSUB -n 1
#BSUB -o ERA5_download_%J.out
#BSUB -e ERA5_download_%J.err
#BSUB -P 0566
#BSUB -M 32G


/users_home/cmcc/vr25423/.conda/envs/PYTHON_VR_3.9/bin/python /data/cmcc/vr25423/inputs/model/atmos/ECMWF/ERA5/reanalysis/1h/grib/ERA5_download_script.py >&log_run&


