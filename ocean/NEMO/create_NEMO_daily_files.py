#################################      
import numpy as np
import pylab as py
##import netCDF4
import datetime
import os
import os.path
#################################
ifolder='/work/cmcc/resm-dev/vladimir/FLAME/EXPS/EvalRUN_03s/output_NEMO/'
ofolder='/work/cmcc/resm-dev/vladimir/FLAME/EXPS/EvalRUN_03s/ERDAP/output_ERDAP/'
year=2023
df=365
#################################
os.system('source /users_home/cmcc/resm-dev/bin/netcdf_environment.sh') 
#datei = datetime.datetime(year, 1, 1)
datei = datetime.datetime(year, 11, 4)
for nn in range (0,df, 60): #30):
    pp=nn+59 #29
    date1 = datei + datetime.timedelta(days = nn)
    name11=py.str_(date1.year)
    name12=py.str_("{:0>2d}".format(date1.month))
    name13=py.str_("{:0>2d}".format(date1.day))
    print('Date ini.: '+name13+'/'+name12+'/'+name11)
    date2 = datei + datetime.timedelta(days = pp)
    name21=py.str_(date2.year)
    name22=py.str_("{:0>2d}".format(date2.month))
    name23=py.str_("{:0>2d}".format(date2.day))
    if os.path.exists(ifolder+'FLAME_MED24_1d_'+\
                      name11+name12+name13+'_'+\
                      name21+name22+name23+'_grid_T.nc'):
        os.system('cdo splitsel,1 '+ifolder+'FLAME_MED24_1d_'+\
                  name11+name12+name13+'_'+name21+name22+name23+
                  '_grid_T.nc outT')
        os.system('cdo splitsel,1 '+ifolder+'FLAME_MED24_1d_'+\
                  name11+name12+name13+'_'+name21+name22+name23+
                  '_grid_V.nc outV')
        os.system('cdo splitsel,1 '+ifolder+'FLAME_MED24_1d_'+\
                  name11+name12+name13+'_'+name21+name22+name23+
                  '_grid_U.nc outU')
        for tt in range(0,60): #30):
            datef = date1 + datetime.timedelta(days = tt)
            namef1=py.str_(datef.year)
            namef2=py.str_("{:0>2d}".format(datef.month))
            namef3=py.str_("{:0>2d}".format(datef.day))

            os.system('ncks -v nav_lon,nav_lat,deptht,time_counter,'+\
                  'thetao,so,zos outT0000'+py.str_("{:0>2d}".format(tt+1))+\
                  '.nc midT1.nc')
            os.system('ncks -C -O -x -v nav_lon,nav_lat,deptht_bnds,'+\
                  'time_counter_bnds midT1.nc midT.nc')
            os.system('ncks -v nav_lon,nav_lat,depthu,time_counter,'+\
                  'vozocrtx outU0000'+py.str_("{:0>2d}".format(tt+1))+\
                  '.nc midU1.nc')
            os.system('ncks -C -O -x -v nav_lon,nav_lat,depthu_bnds,'+\
                  'time_counter_bnds midU1.nc midU.nc')
            os.system('ncks -v nav_lon,nav_lat,depthv,time_counter,'+\
                  'vomecrty outV0000'+py.str_("{:0>2d}".format(tt+1))+\
                  '.nc midV1.nc')
            os.system('ncks -C -O -x -v nav_lon,nav_lat,depthv_bnds,'+\
                  'time_counter_bnds midV1.nc midV.nc')

            os.system('ncrename -O -d x,lon -d y,lat midT.nc')
            os.system('ncrename -O -d x,lon -d y,lat midU.nc')
            os.system('ncrename -O -d x,lon -d y,lat midV.nc')

            os.system('ncks -A -v lon lonlatT.nc midT.nc')
            os.system('ncks -A -v lat lonlatT.nc midT.nc')
            os.system('ncks -A -v lon lonlatU.nc midU.nc')
            os.system('ncks -A -v lat lonlatU.nc midU.nc')
            os.system('ncks -A -v lon lonlatV.nc midV.nc')
            os.system('ncks -A -v lat lonlatV.nc midV.nc')

            os.system('cdo chname,deptht,depth midT.nc midTf.nc')
            os.system('cdo chname,depthu,depth midU.nc midUf.nc')
            os.system('cdo chname,depthv,depth midV.nc midVf.nc')

            os.system('nccopy -7 -d 5 midTf.nc midTf1.nc')
            os.system('nccopy -7 -d 5 midUf.nc midUf1.nc')
            os.system('nccopy -7 -d 5 midVf.nc midVf1.nc')

            os.system('./change_netcdf_attributes_daily.sh '+\
                      namef1+' '+namef2+' '+namef3)

            os.system('rm -f midT1.nc midU1.nc midV1.nc midT.nc '+\
                      'midU.nc midV.nc midTf.nc midUf.nc midVf.nc '+\
                      'midTf1.nc midUf1.nc midVf1.nc')

        os.system('rm -f outT* outU* outV*')

    else:
        print('File not found')
        exit()
