##################################################################
##################################################################
# Nemo PreProcessing (NPP) package
# npp_create_boundary_conditions_pynemo.py
#
# Vladimir Santos da Costa - CMCC
# vladimir.santosdacosta@cmcc.it
#
# Lecce, IT, 16/06/2023
##################################################################
##################################################################
from npp_tools import *
from npp_inputparams import *
import pylab as py
import datetime
import os
from netCDF4 import num2date
import sys
#################################
for bc_year in range(bc_yearini,bc_yearend+1):
    ifileT = bc_input_folder+\
            'THETA_'+py.str_(bc_year)+'_Daily_regrid.nc'
    ifileS = bc_input_folder+\
            'SALT_'+py.str_(bc_year)+'_Daily_regrid.nc'
    ifileU = bc_input_folder+\
            'UVEL_'+py.str_(bc_year)+'_Daily_regrid.nc'
    ifileV = bc_input_folder+\
            'VVEL_'+py.str_(bc_year)+'_Daily_regrid.nc'
    ifileE = bc_input_folder+\
            'ELEVATION_'+py.str_(bc_year)+'_Daily_regrid.nc'
######
    ifileTb = bc_input_folder+\
            'THETA_'+py.str_(bc_year-1)+'_Daily_regrid.nc'
    ifileSb = bc_input_folder+\
            'SALT_'+py.str_(bc_year-1)+'_Daily_regrid.nc'
    ifileUb = bc_input_folder+\
            'UVEL_'+py.str_(bc_year-1)+'_Daily_regrid.nc'
    ifileVb = bc_input_folder+\
            'VVEL_'+py.str_(bc_year-1)+'_Daily_regrid.nc'
    ifileEb = bc_input_folder+\
            'ELEVATION_'+py.str_(bc_year-1)+'_Daily_regrid.nc'
######
    ifileTa = bc_input_folder+\
            'THETA_'+py.str_(bc_year+1)+'_Daily_regrid.nc'
    ifileSa = bc_input_folder+\
            'SALT_'+py.str_(bc_year+1)+'_Daily_regrid.nc'
    ifileUa = bc_input_folder+\
            'UVEL_'+py.str_(bc_year+1)+'_Daily_regrid.nc'
    ifileVa = bc_input_folder+\
            'VVEL_'+py.str_(bc_year+1)+'_Daily_regrid.nc'
    ifileEa = bc_input_folder+\
            'ELEVATION_'+py.str_(bc_year+1)+'_Daily_regrid.nc'
######
    nct  = Dataset(ifileS)
    time = nct.variables['time']
    dtime= num2date(time[:],time.units)
######
    datei = datetime.datetime(bc_year, bc_monthini, 1)

    bc_dayend=31
    if(bc_monthend==2): bc_dayend=28
    if(bc_year%4==0 and bc_monthend==2): bc_dayend=29
    if(bc_monthend==4 or bc_monthend==6 or bc_monthend==9 or bc_monthend==11): bc_dayend=30
    datee = datetime.datetime(bc_year, bc_monthend, bc_dayend)
#########
    nnend=datee-datei
    for nn in range(0,nnend.days+1):
        dateb = datei + datetime.timedelta(days = nn-1)
        dater = datei + datetime.timedelta(days = nn)
        datea = datei + datetime.timedelta(days = nn+1)
        if(dateb.year < bc_year): dateb = dater
        if(datea.year > bc_year): datea = dater
        name1r=py.str_(dater.year)
        name2r=py.str_("{:0>2d}".format(dater.month))
        name3r=py.str_("{:0>2d}".format(dater.day))
        for tt in range(0,len(time)):
            if(dtime[tt]==dateb): ttb=tt+1
            if(dtime[tt]==dater): ttr=tt+1
            if(dtime[tt]==datea): tta=tt+1
        os.system('rm -f '+bc_output_folder+'/OUT_*.nc.ini*')
        os.system('rm -f '+bc_output_folder+'/OUT_*.nc.end*')
        os.system('rm -f inputs_pynemo/namelist_daily.bdy')

        print(' ')
        print('Year: ',name1r,' Month: ',name2r,' Day: ',name3r)

        if(dateb.month==1 and dateb.day==1):
            ttb=365
            if(dateb.year-1%4==0): ttb=366
            if(dateb.year-1==1980): ttb=152
            print('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileEb+' '+bc_output_folder+'/OUT_SSH.nc.ini')
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileEb+' '+bc_output_folder+'/OUT_SSH.nc.ini > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileE+' '+bc_output_folder+'/OUT_SSH.nc.ini > \
                      /dev/null 2>&1')
#############
        os.system('cdo -w seltimestep,'+py.str_(ttr)+'/'+py.str_(ttr)+\
                  ' '+ifileE+' '+bc_output_folder+'/OUT_SSH.nc.end1 > \
                  /dev/null 2>&1')
        if(datea.month==12 and datea.day==31):
            tta=1
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileEa+' '+bc_output_folder+'/OUT_SSH.nc.end2 > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileE+' '+bc_output_folder+'/OUT_SSH.nc.end2 > \
                      /dev/null 2>&1')
        os.system('ncrcat -h '+bc_output_folder+'/OUT_SSH.nc.end1 '+\
                  bc_output_folder+'/OUT_SSH.nc.end2 '+bc_output_folder+\
                  '/OUT_SSH.nc.end')
        os.system('rm -f '+bc_output_folder+'/OUT_SSH.nc.end1 '+\
                  bc_output_folder+'/OUT_SSH.nc.end2')

        if(dateb.month==1 and dateb.day==1):
            ttb=365
            if(dateb.year-1%4==0): ttb=366
            if(dateb.year-1==1980): ttb=152
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileTb+' '+' '+bc_output_folder+'/OUT_T.nc.ini > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileT+' '+' '+bc_output_folder+'/OUT_T.nc.ini > \
                      /dev/null 2>&1')
        os.system('cdo -w seltimestep,'+py.str_(ttr)+'/'+py.str_(ttr)+\
                  ' '+ifileT+' '+' '+bc_output_folder+'/OUT_T.nc.end1 > \
                  /dev/null 2>&1')
        if(datea.month==12 and datea.day==31):
            tta=1
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileTa+' '+' '+bc_output_folder+'/OUT_T.nc.end2 > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileT+' '+' '+bc_output_folder+'/OUT_T.nc.end2 > \
                      /dev/null 2>&1')
        os.system('ncrcat -h '+bc_output_folder+'/OUT_T.nc.end1 '+\
                  bc_output_folder+'/OUT_T.nc.end2 '+bc_output_folder+\
                  '/OUT_T.nc.end')
        os.system('rm -f '+bc_output_folder+'/OUT_T.nc.end1 '+\
                  bc_output_folder+'/OUT_T.nc.end2')

        if(dateb.month==1 and dateb.day==1):
            ttb=365
            if(dateb.year-1%4==0): ttb=366
            if(dateb.year-1==1980): ttb=152
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileSb+' '+' '+bc_output_folder+'/OUT_S.nc.ini > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileS+' '+' '+bc_output_folder+'/OUT_S.nc.ini > \
                      /dev/null 2>&1')
        os.system('cdo -w seltimestep,'+py.str_(ttr)+'/'+py.str_(ttr)+\
                  ' '+ifileS+' '+' '+bc_output_folder+'/OUT_S.nc.end1 > \
                  /dev/null 2>&1')
        if(datea.month==12 and datea.day==31):
            tta=1
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileSa+' '+' '+bc_output_folder+'/OUT_S.nc.end2 > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileS+' '+' '+bc_output_folder+'/OUT_S.nc.end2 > \
                      /dev/null 2>&1')
        os.system('ncrcat -h '+bc_output_folder+'/OUT_S.nc.end1 '+\
                  bc_output_folder+'/OUT_S.nc.end2 '+bc_output_folder+\
                  '/OUT_S.nc.end')
        os.system('rm -f '+bc_output_folder+'/OUT_S.nc.end1 '+\
                  bc_output_folder+'/OUT_S.nc.end2')

        if(dateb.month==1 and dateb.day==1):
            ttb=365
            if(dateb.year-1%4==0): ttb=366
            if(dateb.year-1==1980): ttb=152
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileUb+' '+' '+bc_output_folder+'/OUT_VELU.nc.ini > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileU+' '+' '+bc_output_folder+'/OUT_VELU.nc.ini > \
                      /dev/null 2>&1')
        os.system('cdo -w seltimestep,'+py.str_(ttr)+'/'+py.str_(ttr)+\
                  ' '+ifileU+' '+' '+bc_output_folder+'/OUT_VELU.nc.end1 > \
                  /dev/null 2>&1')
        if(datea.month==12 and datea.day==31):
            tta=1
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileUa+' '+' '+bc_output_folder+'/OUT_VELU.nc.end2 > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileU+' '+' '+bc_output_folder+'/OUT_VELU.nc.end2 > \
                      /dev/null 2>&1')
        os.system('ncrcat -h '+bc_output_folder+'/OUT_VELU.nc.end1 '+\
                  bc_output_folder+'/OUT_VELU.nc.end2 '+bc_output_folder+\
                  '/OUT_VELU.nc.end')
        os.system('rm -f '+bc_output_folder+'/OUT_VELU.nc.end1 '+\
                  bc_output_folder+'/OUT_VELU.nc.end2')

        if(dateb.month==1 and dateb.day==1):
            ttb=365
            if(dateb.year-1%4==0): ttb=366
            if(dateb.year-1==1980): ttb=152
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileVb+' '+' '+bc_output_folder+'/OUT_VELV.nc.ini > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(ttb)+'/'+py.str_(ttb)+\
                      ' '+ifileV+' '+' '+bc_output_folder+'/OUT_VELV.nc.ini > \
                      /dev/null 2>&1')
        os.system('cdo -w seltimestep,'+py.str_(ttr)+'/'+py.str_(ttr)+\
                  ' '+ifileV+' '+' '+bc_output_folder+'/OUT_VELV.nc.end1 > \
                  /dev/null 2>&1')
        if(datea.month==12 and datea.day==31):
            tta=1
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileVa+' '+' '+bc_output_folder+'/OUT_VELV.nc.end2 > \
                      /dev/null 2>&1')
        else:
            os.system('cdo -w seltimestep,'+py.str_(tta)+'/'+py.str_(tta)+\
                      ' '+ifileV+' '+' '+bc_output_folder+'/OUT_VELV.nc.end2 > \
                      /dev/null 2>&1')
        os.system('ncrcat -h '+bc_output_folder+'/OUT_VELV.nc.end1 '+\
                  bc_output_folder+'/OUT_VELV.nc.end2 '+bc_output_folder+\
                  '/OUT_VELV.nc.end')
        os.system('rm -f '+bc_output_folder+'/OUT_VELV.nc.end1 '+\
                  bc_output_folder+'/OUT_VELV.nc.end2')
## Prepare PyBDY input namelis and run PyBDY
        if (tidei==1 and nn==0):
            os.system('cp inputs_pynemo/namelist_MedCordex_tide.bdy inputs_pynemo/namelist_daily.bdy')
        else:
            os.system('cp inputs_pynemo/namelist_MedCordex.bdy inputs_pynemo/namelist_daily.bdy')
        os.system('sed -i "s/iyear/'+name1r+'/g" inputs_pynemo/namelist_daily.bdy')
        os.system('sed -i "s/imonth/'+name2r+'/g" inputs_pynemo/namelist_daily.bdy')
        os.system('pybdy -s inputs_pynemo/namelist_daily.bdy')
         
## Change name of outpus files: monthly names to daily names
        os.system('mv '+bc_output_folder+'/'+bc_output_file+'_bdyT_y'+name1r+'m'+name2r+\
        '.nc '+bc_output_folder+'/'+bc_output_file+'_bdyT_y'+name1r+'m'+name2r+'d'+name3r+'.nc')
        os.system('mv '+bc_output_folder+'/'+bc_output_file+'_bdyU_y'+name1r+'m'+name2r+\
        '.nc '+bc_output_folder+'/'+bc_output_file+'_bdyU_y'+name1r+'m'+name2r+'d'+name3r+'.nc')
        os.system('mv '+bc_output_folder+'/'+bc_output_file+'_bdyV_y'+name1r+'m'+name2r+\
        '.nc '+bc_output_folder+'/'+bc_output_file+'_bdyV_y'+name1r+'m'+name2r+'d'+name3r+'.nc')
## Remove input PyBDY files fron bc_output folder
        os.system('rm -f '+bc_output_folder+'/OUT_*.nc.ini*')
        os.system('rm -f '+bc_output_folder+'/OUT_*.nc.end*')
## Subset output variables along to 1 boundary point
        if(spBDY==1):
            dout1=Dataset(bc_output_folder+'/'+bc_output_file+'_bdyT_y'+name1r+'m'+name2r+'d'+name3r+'.nc','r+')
            lgT=len(dout1.variables['nbrdta'][:][dout1.variables['nbrdta'][:]==1])-1
            lgU=lgT-1 ; lgV=lgT
            dout1.close()
            os.system('ncks -O -d xbT,0,'+py.str_(lgT)+' -d xbU,0,'+py.str_(lgU)+' -d xbV,0,'+\
            py.str_(lgV)+' '+bc_output_folder+'/coordinates.bdy.nc '+bc_output_folder+\
            '/coordinates.bdy.nc')
            os.system('ncks -O -d xb,0,'+py.str_(lgT)+' '+bc_output_folder+'/'+bc_output_file+\
            '_bdyT_y'+name1r+'m'+name2r+'d'+name3r+'.nc '+bc_output_folder+'/'+bc_output_file+\
            '_bdyT_y'+name1r+'m'+name2r+'d'+name3r+'.nc')
            os.system('ncks -O -d xb,0,'+py.str_(lgU)+' '+bc_output_folder+'/'+bc_output_file+\
            '_bdyU_y'+name1r+'m'+name2r+'d'+name3r+'.nc '+bc_output_folder+'/'+bc_output_file+\
            '_bdyU_y'+name1r+'m'+name2r+'d'+name3r+'.nc')
            os.system('ncks -O -d xb,0,'+py.str_(lgV)+' '+bc_output_folder+'/'+bc_output_file+\
            '_bdyV_y'+name1r+'m'+name2r+'d'+name3r+'.nc '+bc_output_folder+'/'+bc_output_file+\
            '_bdyV_y'+name1r+'m'+name2r+'d'+name3r+'.nc')
#########################################################
