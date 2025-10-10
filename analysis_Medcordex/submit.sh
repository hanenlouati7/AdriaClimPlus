#!/bin/bash
#BSUB -q s_medium
#BSUB -P 0566
#BSUB -n 1
#BSUB -J sea_level
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -R "rusage[mem=40G]"

source activate myconda

python3 compare_sea_level_TSsteric_anomaly_MKorig.py
