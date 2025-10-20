#!/bin/bash
#BSUB -q s_long
#BSUB -J hydro_chain
#BSUB -n 1
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -P 0684
#BSUB -R "rusage[mem=20MB]"

repo="/work/cmcc/gv29119/AdriaClim/nemo/runoff_wrf2nemo/AdriaClimPlus"

for i in {1..145}
do
    for yy in {1989..2021}
    do
    year=",${yy}-"
    for range in "EvalRun"; do
    #for range in {"hist","proj"}; do

    string="00:00,"
    string="${string}${i}"
    if [[ $i -lt 10 ]]
    then
    #create string2 by addding white spaces
    string2="$(echo "$string" | sed 's/,/,           /g')"; #echo "$string2" #11 white spaces
    elif [[ $i -lt 100 ]]
    then
    string2="$(echo "$string" | sed 's/,/,          /g')"; #echo "$string2" #10 white spaces
    else
    string2="$(echo "$string" | sed 's/,/,         /g')"; #echo "$string2" #9 white spaces
    fi

    #search strings ${year} and {string2} on the same line and put into splitted txt files
    grep "${year}" ${repo}/frxst_pts_out_${range}.txt | grep "${string2}" > ${repo}/erddap_EvalRun/runoff_${range}_${i}_${yy}.txt
    wait
    done
    done

done

##--prints the names of the matching empty files to the terminal and delete them
#find temp*txt -size  0 -print -delete
