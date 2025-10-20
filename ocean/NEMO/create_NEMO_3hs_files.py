#################################      
import numpy as np
import pylab as py
##import netCDF4
import datetime
import os
import os.path
#################################
ifolder='/work/cmcc/resm-dev/vladimir/FLAME/EXPS/EvalRUN_03s/output_NEMO/'
ofolder='/work/cmcc/resm-dev/vladimir/FLAME/EXPS/EvalRUN_03s/ERDAP/output_ERDAP_3h/'
year=1990
df=365+120
#################################
##os.system('source /users_home/cmcc/resm-dev/bin/netcdf_environment.sh') 
datei = datetime.datetime(year, 1, 1)
#datei = datetime.datetime(year, 11, 14)
for nn in range (0,df, 60): #30):
    pp=nn+59 #29
    date1 = datei + datetime.timedelta(days = nn)
    name11=py.str_(date1.year)
    name12=py.str_("{:0>2d}".format(date1.month))
    name13=py.str_("{:0>2d}".format(date1.day))
    name14=py.str_("{:0>2d}".format(date1.hour))
    print('Date ini.: '+name13+'/'+name12+'/'+name11)
    date2 = datei + datetime.timedelta(days = pp)
    name21=py.str_(date2.year)
    name22=py.str_("{:0>2d}".format(date2.month))
    name23=py.str_("{:0>2d}".format(date2.day))
    if os.path.exists(ifolder+'FLAME_MED24_3h_'+\
                      name11+name12+name13+'_'+\
                      name21+name22+name23+'_grid_T.nc'):
        os.system('cdo splitsel,1 '+ifolder+'FLAME_MED24_3h_'+\
                  name11+name12+name13+'_'+name21+name22+name23+
                  '_grid_T.nc outT')
        for tt in range(0,60*8): #30):
            datef = date1 + datetime.timedelta(days = tt/8)
            namef1=py.str_(datef.year)
            namef2=py.str_("{:0>2d}".format(datef.month))
            namef3=py.str_("{:0>2d}".format(datef.day))
            namef4=py.str_("{:0>2d}".format(datef.hour))

            os.system('ncks -v nav_lon,nav_lat,time_counter,'+\
                  'votemper,vosaline,sossheig,wspd outT000'+\
                  py.str_("{:0>3d}".format(tt+1))+\
                  '.nc midT1.nc')
            os.system('ncks -C -O -x -v nav_lon,nav_lat'+\
                  ' midT1.nc midT.nc')

            os.system('ncrename -O -d x,lon -d y,lat midT.nc')

            os.system('ncks -A -v lon lonlatT.nc midT.nc')
            os.system('ncks -A -v lat lonlatT.nc midT.nc')

            os.system('nccopy -7 -d 5 midT.nc midTf1.nc')

            os.system('./change_netcdf_attributes_3h.sh '+\
                      namef1+' '+namef2+' '+namef3+' '+namef4)

            os.system('rm -f midT1.nc midT.nc midTf1.nc')

        os.system('rm -f outT*')

    else:
        print('File not found')
        exit()
