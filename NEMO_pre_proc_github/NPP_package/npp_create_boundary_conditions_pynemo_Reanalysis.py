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
#################################
datei = datetime.datetime(bc_year, bc_monthini, 1)
bc_dayend=1
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
    name1b=py.str_(dateb.year)
    name1r=py.str_(dater.year)
    name1a=py.str_(datea.year)
    name2b=py.str_("{:0>2d}".format(dateb.month))
    name2r=py.str_("{:0>2d}".format(dater.month))
    name2a=py.str_("{:0>2d}".format(datea.month))
    name3b=py.str_("{:0>2d}".format(dateb.day))
    name3r=py.str_("{:0>2d}".format(dater.day))
    name3a=py.str_("{:0>2d}".format(datea.day))

    os.system('rm -f '+bc_output_folder+'/OUT_*.nc.ini*')
    os.system('rm -f '+bc_output_folder+'/OUT_*.nc.end*')
    os.system('rm -f inputs_pynemo/namelist_daily.bdy')

    print('Year: ',name1r,' Month: ',name2r,' Day: ',name3r)

    os.system('cp '+bc_input_folder+'/'+name1b+'/'+name2b+'/'+name1b+name2b+name3b+\
    bc_input_ssh+' '+bc_output_folder+'/OUT_SSH.nc.ini')
    os.system('cp '+bc_input_folder+'/'+name1r+'/'+name2r+'/'+name1r+name2r+name3r+\
    bc_input_ssh+' '+bc_output_folder+'/OUT_SSH.nc.end1')
    os.system('cp '+bc_input_folder+'/'+name1a+'/'+name2a+'/'+name1a+name2a+name3a+\
    bc_input_ssh+' '+bc_output_folder+'/OUT_SSH.nc.end2')
    os.system('ncrcat -h '+bc_output_folder+'/OUT_SSH.nc.end1 '+bc_output_folder+\
    '/OUT_SSH.nc.end2 '+bc_output_folder+'/OUT_SSH.nc.end')
    os.system('rm -f '+bc_output_folder+'/OUT_SSH.nc.end1 '+bc_output_folder+'/OUT_SSH.nc.end2')

    os.system('cp '+bc_input_folder+'/'+name1b+'/'+name2b+'/'+name1b+name2b+name3b+\
    bc_input_temp+' '+bc_output_folder+'/OUT_T.nc.ini')
    os.system('cp '+bc_input_folder+'/'+name1r+'/'+name2r+'/'+name1r+name2r+name3r+\
    bc_input_temp+' '+bc_output_folder+'/OUT_T.nc.end1')
    os.system('cp '+bc_input_folder+'/'+name1a+'/'+name2a+'/'+name1a+name2a+name3a+\
    bc_input_temp+' '+bc_output_folder+'/OUT_T.nc.end2')
    os.system('ncrcat -h '+bc_output_folder+'/OUT_T.nc.end1 '+bc_output_folder+\
    '/OUT_T.nc.end2 '+bc_output_folder+'/OUT_T.nc.end')
    os.system('rm -f '+bc_output_folder+'/OUT_T.nc.end1 '+bc_output_folder+'/OUT_T.nc.end2')

    os.system('cp '+bc_input_folder+'/'+name1b+'/'+name2b+'/'+name1b+name2b+name3b+\
    bc_input_sal+' '+bc_output_folder+'/OUT_S.nc.ini')
    os.system('cp '+bc_input_folder+'/'+name1r+'/'+name2r+'/'+name1r+name2r+name3r+\
    bc_input_sal+' '+bc_output_folder+'/OUT_S.nc.end1')
    os.system('cp '+bc_input_folder+'/'+name1a+'/'+name2a+'/'+name1a+name2a+name3a+\
    bc_input_sal+' '+bc_output_folder+'/OUT_S.nc.end2')
    os.system('ncrcat -h '+bc_output_folder+'/OUT_S.nc.end1 '+bc_output_folder+\
    '/OUT_S.nc.end2 '+bc_output_folder+'/OUT_S.nc.end')
    os.system('rm -f '+bc_output_folder+'/OUT_S.nc.end1 '+bc_output_folder+'/OUT_S.nc.end2')

    os.system('cp '+bc_input_folder+'/'+name1b+'/'+name2b+'/'+name1b+name2b+name3b+\
    bc_input_vel+' '+bc_output_folder+'/OUT_VEL.nc.ini')
    os.system('cp '+bc_input_folder+'/'+name1r+'/'+name2r+'/'+name1r+name2r+name3r+\
    bc_input_vel+' '+bc_output_folder+'/OUT_VEL.nc.end1')
    os.system('cp '+bc_input_folder+'/'+name1a+'/'+name2a+'/'+name1a+name2a+name3a+\
    bc_input_vel+' '+bc_output_folder+'/OUT_VEL.nc.end2')
    os.system('ncrcat -h '+bc_output_folder+'/OUT_VEL.nc.end1 '+bc_output_folder+\
    '/OUT_VEL.nc.end2 '+bc_output_folder+'/OUT_VEL.nc.end')
    os.system('rm -f '+bc_output_folder+'/OUT_VEL.nc.end1 '+bc_output_folder+'/OUT_VEL.nc.end2')
## Prepare PyBDY input namelis and run PyBDY
    if (tidei==1 and nn==0):
        os.system('cp inputs_pynemo/namelist_tide_03s.bdy inputs_pynemo/namelist_daily.bdy')
    else:
        os.system('cp inputs_pynemo/namelist_03s.bdy inputs_pynemo/namelist_daily.bdy')
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
