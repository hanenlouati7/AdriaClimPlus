#!/bin/bash
#BSUB -q s_long
#BSUB -J ERA5
#BSUB -n 1
#BSUB -o ERA5_singlelev_%J.out
#BSUB -e ERA5_singlelev_%J.err
#BSUB -P 0566
#BSUB -M 32G


/juno/opt/anaconda/3-2022.10/bin/python prepare_WRF_diagnostic_fields_ncl_02.py
