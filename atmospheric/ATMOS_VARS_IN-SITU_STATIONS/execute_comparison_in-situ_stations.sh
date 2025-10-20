#!/bin/bash
#BSUB -q s_medium
#BSUB -J Venezia
#BSUB -n 1
#BSUB -o run.%J.out
#BSUB -e run.%J.err
#BSUB -P 0555
#BSUB -M 100GB 

python plot_timeseries_adoy_box_plot_prec_t2m_wind_speed_hum_DELO.py