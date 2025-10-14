import numpy as np #scientific module
from netCDF4 import Dataset #class of netcdf4 module for Creating/Opening/Closing a netCDF file
from scipy.interpolate import griddata #interpolation module
from scipy.interpolate import NearestNDInterpolator
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
import seawater as sw
import datetime     #standard library supplying classes for manipulating dates and times
import math

def load_input_EMODnet_bathy(lonoi,lonoe,latoi,latoe,pathi):
    jp=1
    nc = Dataset(pathi)
    lon = np.squeeze(nc.variables['lon'][:])
    #lon = np.squeeze(nc.variables['XAX'][:])
    a1=np.where(lon <= lonoi)
    a2=np.where(lon <= lonoe)
    loni=lon[len(a1[0])-jp:len(a2[0])+jp:jp]
    lat = np.squeeze(nc.variables['lat'][:])
    #lat = np.squeeze(nc.variables['YAX'][:])-0.0005
    b1=np.where(lat <= latoi)
    b2=np.where(lat <= latoe)
    lati=lat[len(b1[0])-jp:len(b2[0])+jp:jp]
    #loni, lati = np.meshgrid(lon1, lat1)
    bathyi = np.squeeze(nc.variables['elevation'][len(b1[0])-jp:len(b2[0])+jp:jp,len(a1[0])-jp:len(a2[0])+jp:jp])
    #bathyi = np.squeeze(nc.variables['DEPTH_NEW'][len(b1[0])-jp:len(b2[0])+jp:jp,len(a1[0])-jp:len(a2[0])+jp:jp])
    mask=np.zeros([len(lati),len(loni)]) ; mask[np.isfinite(bathyi)==True]=1
    bathyi[np.isnan(bathyi)] = 0
    bathyi[mask==0] = 0
    bathyi=-bathyi
    nc.close()

    return (loni,lati,bathyi)

def load_input_MedCordex_bathy(pathi):
    nc = Dataset(pathi)
    lonci = np.squeeze(nc.variables['XC'][:])
    latci = np.squeeze(nc.variables['YC'][:])
    longi = np.squeeze(nc.variables['XG'][:])
    latgi = np.squeeze(nc.variables['YG'][:])
    dxi   = np.squeeze(nc.variables['dxF'][:])
    dyi   = np.squeeze(nc.variables['dyF'][:])
    zci   = -1*np.squeeze(nc.variables['RC'][:])
    zgi   = -1*np.squeeze(nc.variables['RF'][:])
    dzci  = np.squeeze(nc.variables['drF'][:])
    dzgi  = np.squeeze(nc.variables['drC'][:])
    ffi   = np.squeeze(nc.variables['fCori'][:])
    maski = np.squeeze(nc.variables['HFacC'][:])
    bathyi= np.squeeze(nc.variables['Depth'][:])
    nc.close()

    return (lonci,latci,longi,latgi,dxi,dyi,zci,zgi,dzci,dzgi,ffi,maski,bathyi)

def load_NEMO_vertical(domain_NEMO_filename):
    nc = Dataset(domain_NEMO_filename)
    gdepw = np.squeeze(nc.variables['gdepw_1d'][:])
    nc.close()

    return (gdepw)

def load_input_father_bathy(bathyf_filename,bathyf_name):
    nc = Dataset(bathyf_filename)
#    lonf1 = np.squeeze(nc.variables['nav_lon'][60,:])
#    latf1 = np.squeeze(nc.variables['nav_lat'][:,170])
    lonf1 = np.squeeze(nc.variables['longitude'][:])
    latf1 = np.squeeze(nc.variables['latitude'][:])
    bathyf = np.squeeze(nc.variables[bathyf_name])
    lonf=np.zeros([len(latf1),len(lonf1)])
    for i in range(0,len(latf1)): lonf[i,:]=lonf1
    latf=np.zeros([len(latf1),len(lonf1)])
    for i in range(0,len(lonf1)): latf[:,i]=latf1
    return (lonf,latf,bathyf)

def load_input_initial_TS_MedCordex(tempi_filename,sali_filename):
    nc1 = Dataset(tempi_filename)
    lonts = np.squeeze(nc1.variables['lon'][:])
    latts = np.squeeze(nc1.variables['lat'][:])
    #lonts,latts = np.meshgrid(lonts1,latts1)
    zts   = np.squeeze(nc1.variables['lev'][:])
    zts   = -zts
    zts[0] = 0
    tempi = np.squeeze(nc1.variables['THETA'][1,:,:,:])
    tempi[tempi==0]=np.nan
    nc1.close()
    nc2 = Dataset(sali_filename)
    sali = np.squeeze(nc2.variables['SALT'][1,:,:,:])
    sali[sali==0]=np.nan
    nc2.close()
    return (lonts,latts,zts,tempi,sali)

def load_input_initial_TS(tempi_filename,sali_filename):
    nc1 = Dataset(tempi_filename)
    lonts = np.squeeze(nc1.variables['lon'][:])
    latts = np.squeeze(nc1.variables['lat'][:])
    zts   = np.squeeze(nc1.variables['depth'][:])
    zts[0] = 0
    tempi = np.squeeze(nc1.variables['thetao'][:])
    mask=np.zeros([len(zts),len(latts),len(lonts)])
    mask[np.isreal(tempi)]=1
    tempi[mask==0]=np.nan
    nc1.close()
    nc2 = Dataset(sali_filename)
    sali = np.squeeze(nc2.variables['so'][:])
    sali[mask==0]=np.nan
    nc2.close()
#    nc1 = Dataset(tempi_filename)
#    lonts = np.squeeze(nc1.variables['nav_lon'][:])
#    latts = np.squeeze(nc1.variables['nav_lat'][:])
##    zts   = np.squeeze(nc1.variables['deptht'][:])
##    zts[0] = 0
#    tempi = np.squeeze(nc1.variables['votemper'][0,:,:,:])
#    nc1.close()
#    nc2 = Dataset(sali_filename)
#    sali = np.squeeze(nc2.variables['vosaline'][0,:,:,:])
#    tempi[sali==0]=np.nan
#    sali[sali==0]=np.nan
#    nc2.close()
#    nc3 = Dataset('../MedCordex/NEMOMED8_deptht.nc')
#    zts   = np.squeeze(nc3.variables['deptht'][:])
#    zts[0] = 0
#    nc3.close()

    return (lonts,latts,zts,tempi,sali)

def load_input_surface_forcings_MFS(final_sf_filename,dt):
    nc = Dataset(final_sf_filename)
    lonsf = np.squeeze(nc.variables['longitude'][:])
    latsf = np.squeeze(nc.variables['latitude'][:])
    time  = np.squeeze(nc.variables['time'][dt])
    msl   = np.squeeze(nc.variables['msl'][dt,:,:])
    tcc   = np.squeeze(nc.variables['tcc'][dt,:,:])
    #tcc   = tcc*100 #Total cloud cover in percentage
    u10   = np.squeeze(nc.variables['u10'][dt,:,:])
    v10   = np.squeeze(nc.variables['v10'][dt,:,:])
    t2m   = np.squeeze(nc.variables['t2m'][dt,:,:])
    d2m   = np.squeeze(nc.variables['d2m'][dt,:,:])
    #precip= np.squeeze(nc.variables['mtpr'][dt,:,:])
    precip= np.squeeze(nc.variables['tp'][dt,:,:])
    lsm   = np.squeeze(nc.variables['lsm'][0,:,:])
    nc.close()

    return (lonsf,latsf,time,msl,tcc,u10,v10,t2m,d2m,lsm,precip)

def load_input_surface_forcings_ECMWF(final_sf_filename,dt):
    nc = Dataset(final_sf_filename)
    lonsf = np.squeeze(nc.variables['longitude'][:])
    latsf = np.squeeze(nc.variables['latitude'][:])
    time  = np.squeeze(nc.variables['time'][dt])
    msl   = np.squeeze(nc.variables['msl'][dt,:,:])
    tcc   = np.squeeze(nc.variables['tcc'][dt,:,:])
    u10   = np.squeeze(nc.variables['u10'][dt,:,:])
    v10   = np.squeeze(nc.variables['v10'][dt,:,:])
    t2m   = np.squeeze(nc.variables['t2m'][dt,:,:])
    d2m   = np.squeeze(nc.variables['d2m'][dt,:,:])
    precip= np.squeeze(nc.variables['tp'][dt,:,:])
    swrd  = np.squeeze(nc.variables['ssrd'][dt,:,:])
    lwrd  = np.squeeze(nc.variables['strd'][dt,:,:])
    lsm   = np.squeeze(nc.variables['lsm'][0,:,:])
    nc.close()

    return (lonsf,latsf,time,msl,tcc,u10,v10,t2m,d2m,lsm,precip,swrd,lwrd)

def load_input_surface_forcings_WRF(final_sf_filename0,final_sf_filename1,wrf_diag,hh):
    nc0 = Dataset(final_sf_filename0)
    nc1 = Dataset(final_sf_filename1)
    lonsf = np.squeeze(nc1.variables['XLONG'][0,:,:])
    latsf = np.squeeze(nc1.variables['XLAT'][0,:,:])
    time  = np.squeeze(nc1.variables['Times'][hh])
    u10   = np.squeeze(nc1.variables['U10'][hh,:,:])
    v10   = np.squeeze(nc1.variables['V10'][hh,:,:])
    t2m   = np.squeeze(nc1.variables['T2'][hh,:,:])
    if(hh==0):
        precip0= np.squeeze(nc0.variables['RAINC'][-1,:,:])+\
                 np.squeeze(nc0.variables['RAINNC'][-1,:,:])+\
                 100*np.squeeze(nc0.variables['I_RAINC'][-1,:,:])+\
                 100*np.squeeze(nc0.variables['I_RAINNC'][-1,:,:])
        precip1= np.squeeze(nc1.variables['RAINC'][hh,:,:])+\
                 np.squeeze(nc1.variables['RAINNC'][hh,:,:])+\
                 100*np.squeeze(nc1.variables['I_RAINC'][hh,:,:])+\
                 100*np.squeeze(nc1.variables['I_RAINNC'][hh,:,:])
    else:
        precip0= np.squeeze(nc1.variables['RAINC'][hh-1,:,:])+\
                 np.squeeze(nc1.variables['RAINNC'][hh-1,:,:])+\
                 100*np.squeeze(nc1.variables['I_RAINC'][hh-1,:,:])+\
                 100*np.squeeze(nc1.variables['I_RAINNC'][hh-1,:,:])
        precip1= np.squeeze(nc1.variables['RAINC'][hh,:,:])+\
                 np.squeeze(nc1.variables['RAINNC'][hh,:,:])+\
                 100*np.squeeze(nc1.variables['I_RAINC'][hh,:,:])+\
                 100*np.squeeze(nc1.variables['I_RAINNC'][hh,:,:])
    precip = precip1 - precip0
    swrd  = np.squeeze(nc1.variables['SWDNB'][hh,:,:])-\
            np.squeeze(nc1.variables['SWUPB'][hh,:,:])
    #swrd  = np.squeeze(nc1.variables['SWDNB'][hh,:,:])
    #lwrd  = np.squeeze(nc1.variables['LWDNB'][hh,:,:])-\
    #        np.squeeze(nc1.variables['LWUPB'][hh,:,:])
    lwrd  = np.squeeze(nc1.variables['LWDNB'][hh,:,:])
    lsm   = np.squeeze(nc1.variables['XLAND'][0,:,:])
    nc0.close()
    nc1.close()
    nc2 = Dataset(wrf_diag)
    msl   = np.squeeze(nc2.variables['SLP'][hh,:,:])
    d2m   = np.squeeze(nc2.variables['TD2'][hh,:,:])
    nc2.close()

    return (lonsf,latsf,time,msl,u10,v10,t2m,d2m,lsm,precip,swrd,lwrd)

def load_input_surface_forcings_ECMWF_MedCordex(final_sf_filename1,\
          final_sf_filename2,final_sf_filename3,final_sf_filename4,\
          final_sf_filename5,final_sf_filename6,final_sf_filename7,\
          final_sf_filename8,final_sf_filename9,final_sf_filename10,\
          final_sf_filename11,dt):
    nc1 = Dataset(final_sf_filename1) ; nc2 = Dataset(final_sf_filename2)
    nc3 = Dataset(final_sf_filename3) ; nc4 = Dataset(final_sf_filename4)
    nc5 = Dataset(final_sf_filename5) ; nc6 = Dataset(final_sf_filename6)
    nc7 = Dataset(final_sf_filename7) ; nc8 = Dataset(final_sf_filename8)
    nc9 = Dataset(final_sf_filename9) ; nc10= Dataset(final_sf_filename10)
    nc11= Dataset(final_sf_filename11)
    lonsf = np.squeeze(nc1.variables['lon'][:])
    latsf = np.squeeze(nc1.variables['lat'][:])
    time  = np.squeeze(nc1.variables['time'][dt])
    msl   = np.squeeze(nc1.variables['SLP'][dt,:,:])
    tcc   = np.squeeze(nc2.variables['CLDT'][dt,:,:])
    u10   = np.squeeze(nc3.variables['U10_earth'][dt,:,:])
    v10   = np.squeeze(nc4.variables['V10_earth'][dt,:,:])
    t2m   = np.squeeze(nc5.variables['T2'][dt,:,:])
    rh2m  = np.squeeze(nc6.variables['RH2'][dt,:,:])
    #d2m   = rh2m
    #H     = (np.log10(rh2m)-2)/0.4343 + (17.62*t2m)/(243.12+t2m)
    H     = np.log(rh2m/100) + (17.62*(t2m-273.15))/(243.12+(t2m-273.15))
    d2m   = (243.12*H/(17.62-H))+273.15 # this is the dew point in Kelvin [Magnus formula]
    precip= np.squeeze(nc7.variables['RAINC'][dt,:,:])+\
            np.squeeze(nc8.variables['RAINNC'][dt,:,:])
    swrd  = np.squeeze(nc9.variables['SWDOWN'][dt,:,:])
    lwrd  = np.squeeze(nc10.variables['LWUPB'][dt,:,:])
    lsm   = np.squeeze(nc11.variables['LANDMASK'][0,:,:])
    nc1.close() ; nc2.close() ; nc3.close() ; nc4.close()
    nc5.close() ; nc6.close() ; nc7.close() ; nc8.close()
    nc9.close() ; nc10.close() ; nc11.close() 

    return (lonsf,latsf,time,msl,tcc,u10,v10,t2m,d2m,lsm,precip,swrd,lwrd)

def load_input_mask_ECMWF(sf_mask_filename):
    nc = Dataset(sf_mask_filename)
    lonsf = np.squeeze(nc.variables['longitude'][:])
    latsf = np.squeeze(nc.variables['latitude'][:])
    lsm   = np.squeeze(nc.variables['lsm'][0,:,:])
    nc.close()

    return (lonsf,latsf,lsm)

#def load_input_surface_forcings_ECMWF(final_sf_filename,var_name,dt):
#    nc = Dataset(final_sf_filename)
#    var= np.squeeze(nc.variables[var_name][dt,:,:])
#    nc.close()
#
#    return (var)

def load_input_surface_forcings_NCAR(final_sf_filename,dt):
    nc = Dataset(final_sf_filename)
    lonsf = np.squeeze(nc.variables['longitude'][:])
    latsf = np.squeeze(nc.variables['latitude'][:])
    msl   = np.squeeze(nc.variables['msl'][dt,:,:])
#    tcc   = np.squeeze(nc.variables['tcc'][dt,:,:])
    u10   = np.squeeze(nc.variables['u10'][dt,:,:])
    v10   = np.squeeze(nc.variables['v10'][dt,:,:])
    t2m   = np.squeeze(nc.variables['t2m'][dt,:,:])
    d2m   = np.squeeze(nc.variables['d2m'][dt,:,:])
    precip= np.squeeze(nc.variables['mtpr'][dt,:,:])
    shw   = np.squeeze(nc.variables['msdwswrf'][dt,:,:])
    lgw   = np.squeeze(nc.variables['msdwlwrf'][dt,:,:])
    lsm   = np.squeeze(nc.variables['lsm'][dt,:,:])
    nc.close()

    return (lonsf,latsf,msl,u10,v10,t2m,d2m,lsm,precip,shw,lgw)

def load_NEMO_bathy(bathyo_filename):
    nc = Dataset(bathyo_filename)
    lonnm = np.squeeze(nc.variables['nav_lon'][:])
    latnm = np.squeeze(nc.variables['nav_lat'][:])
    bathynm = np.squeeze(nc.variables['Bathymetry'][:])
    nc.close()

    return (lonnm,latnm,bathynm)

def load_NEMO_bathy_agrif(bathyo_filename):
    nc = Dataset(bathyo_filename)
    lonnm = np.squeeze(nc.variables['nav_lon'][:])
    latnm = np.squeeze(nc.variables['nav_lat'][:])
    bathynm = np.squeeze(nc.variables['bathy_metry'][:])
    nc.close()

    return (lonnm,latnm,bathynm)

def interp_bathy(loni,lati,bathyi,lonoi,lonoe,dx,latoi,latoe,dy):
    lonof = np.arange(lonoi, lonoe, dx)
    latof = np.arange(latoi, latoe, dy)
    lono, lato = np.meshgrid(lonof, latof)
#    bathyo = griddata((loni.flatten(),lati.flatten()),bathyi.flatten(),(lono,lato),method='linear')
    f = interp2d(loni, lati, bathyi)
    bathyo = f(lonof, latof)

    return (lono,lato,bathyo)

def smoothgrid(h):
    coef=h
    for i in range(0,1): #8):
        coef=hann_window(coef)             # coef is a smoothed bathy
    coef=0.125*(coef/np.max(coef))         # rescale the smoothed bathy
    h=hanning_smoother_coef2d(h,coef)      # smooth with avariable coef

    return(h)

def hann_window(coef):
    yend=len(coef[:,0])-1
    xend=len(coef[0,:])-1
    OneFours=1.0/4.0
    OneEights=1.0/8.0
    OneSixteens=1.0/16.0
    coef[1:yend-1,1:xend-1]=OneFours*coef[1:yend-1,1:xend-1]+\
                       OneEights*(coef[0:yend-2,1:xend-1]+coef[2:yend  ,1:xend-1]+\
                                  coef[1:yend-1,0:xend-2]+coef[1:yend-1,2:xend  ])+\
                     OneSixteens*(coef[0:yend-2,0:xend-2]+coef[2:yend  ,2:xend  ]+\
                                  coef[0:yend-2,2:xend  ]+coef[2:yend  ,0:xend-2])
    coef[0,:]=coef[1,:]
    coef[yend,:]=coef[yend-1,:]
    coef[:,0]=coef[:,1]
    coef[:,xend]=coef[:,xend-1]
    del xend, yend

    return(coef)

def hanning_smoother_coef2d(h,coef):
    M=len(h[:,0])-1
    L=len(h[0,:])-1
    Mm=M-1
    Mmm=M-2
    Lm=L-1
    Lmm=L-2
    h[1:Mm,1:Lm]=coef[1:Mm,1:Lm]*(h[0:Mmm,1:Lm]+h[2:M,1:Lm]+\
                                  h[1:Mm,0:Lmm]+h[1:Mm,2:L])\
                 +(1-4*coef[1:Mm,1:Lm])*h[1:Mm,1:Lm]
    h[0,:]=h[1,:]
    h[M,:]=h[Mm,:]
    h[:,0]=h[:,1]
    h[:,L]=h[:,Lm]

    return(h)

def hinterp_to_NEMO(lonts,latts,zts,tsi,lonnm,latnm):
    lontso, lattso = np.meshgrid(lonts, latts)
    tsnm=np.zeros([len(latnm[:,0]),len(lonnm[0,:]),len(zts)])
    for zz in range (0,len(zts)):
        tsi1=np.squeeze(tsi[zz,:,:])
        tsnm[:,:,zz]=griddata((lontso.flatten(),lattso.flatten()),tsi1.flatten(),(lonnm,latnm),method='linear')
        #f = interp2d(lonts, latts, tsi1)
        #tsnm[:,:,zz]=f(lonnm, latnm)
        #del f, tsi1

    return (tsnm)

def hinterp_MedCordex_to_NEMO(lonts,latts,zts,tsi,lonnm,latnm):
    tsnm=np.zeros([len(latnm[:,0]),len(lonnm[0,:]),len(zts)])
    for zz in range (0,len(zts)):
        tsi1=np.squeeze(tsi[zz,:,:])
        tsnm[:,:,zz]=griddata((lonts.flatten(),latts.flatten()),tsi1.flatten(),(lonnm,latnm),method='linear')
        #f = interp2d(lonts, latts, tsi1)
        #tsnm[:,:,zz]=f(lonnm, latnm)
        #del f, tsi1

    return (tsnm)

def vinterp_to_NEMO(tsnm,zts,gdepw):
    tsnmf=np.zeros([len(gdepw),len(tsnm[:,0,0]),len(tsnm[0,:,0])])
    tsnmf[tsnmf==0]=np.nan
    gdepw2=np.zeros([len(gdepw)])
    for k in range(0,len(gdepw)):
        gdepw2[k]=gdepw[k]
    for i in range (0, len(tsnm[:,0,0])):
        for j in range (0, len(tsnm[0,:,0])):
            fint = interp1d(np.squeeze(zts), np.squeeze(np.squeeze(tsnm[i,j,:])), kind='cubic')
            tsnmf[:,i,j] = fint(gdepw2)
            del fint

    return (tsnmf)

def vertical_NEMO_grid(kp,sh,sr,zd):
    tol  = 0.00001
    low  = 1.00001
    high = 80
    while((high-low)>2*tol):
        mid = (high+low)/2
        fl  = fun5(low,kp,sh,sr,zd)
        fm  = fun5(mid,kp,sh,sr,zd)
        prod= fl*fm
        if prod>0:
            low = mid
        else:
            high= mid

    h4 = (high+low)/2
    print(h4)
    h2 = (sr-zd/(kp-1))/(np.tanh((1-h4)/sh)-sh/(kp-1)*(np.log(np.cosh((kp-h4)/sh))-np.log(np.cosh((1-h4)/sh))))
    h1 = sr-h2*np.tanh((1-h4)/sh)
    h0 = -h1-h2*sh*np.log(np.cosh((1-h4)/sh))

    gdepw = np.zeros([kp])
    for zz in range (1,kp):
        gdepw[zz-1] = h0 + h1*zz + h2*sh*np.log(np.cosh((zz-h4)/sh))

    gdepw[0]=0
    gdepw[kp-1]=zd
    print(len(gdepw))
    return (gdepw)

def fun5(x,kp,sh,sr,zd):
    h2 = (sr-zd/(kp-1))/(np.tanh((1-x)/sh)-sh/(kp-1)*(np.log(np.cosh((kp-x)/sh))-np.log(np.cosh((1-x)/sh))))
    h1 = sr-h2*np.tanh((1-x)/sh)
    h0 = -h1-h2*sh*np.log(np.cosh((1-x)/sh))

    y = h0 + h1*kp + h2*sh*np.log(np.cosh((kp-x)/sh))+zd

    return (y)

def remove_isolated_point(bathyo):
    for ii in range (1,len(bathyo)-1):
        for jj in range (1,len(bathyo[0])-1):
            summa=bathyo[ii-1,jj] + bathyo[ii+1,jj] +\
                  bathyo[ii,jj-1] + bathyo[ii,jj+1]
            if summa==0.0:
                bathyo[ii,jj]=0.0

    return (bathyo)

def zero_bathy_gradient(bdyS,bdyN,bdyW,bdyE,bathyo):
    xl=len(bathyo[0])
    yl=len(bathyo)
    if (bdyS==1):
        bathyo[1,:]=bathyo[0,:]
        bathyo[2,:]=bathyo[0,:]
    if (bdyN==1):
        bathyo[yl-3,:]=bathyo[yl-1,:]
        bathyo[yl-2,:]=bathyo[yl-1,:]
    if (bdyW==1):
        bathyo[:,1]=bathyo[:,0]
        bathyo[:,2]=bathyo[:,0]
    if (bdyE==1):
        bathyo[:,xl-3]=bathyo[:,xl-1]
        bathyo[:,xl-2]=bathyo[:,xl-1]

    return (bathyo)

def ts_seaoverland(tsi):
    for zz in range (0,len(np.squeeze(tsi[:,0,0]))):
        tt1=np.squeeze(tsi[zz,:,:])
        mask = np.where(~np.isnan(tt1))
        if(len(mask[0])>0):
            interp = NearestNDInterpolator(np.transpose(mask), tt1[mask])
            tt1 = interp(*np.indices(tt1.shape))
            del interp
            tsi[zz,:,:]=tt1
            del mask,tt1
        else:
            tsi[zz,:,:]=tsi[zz-1,:,:]

    return (tsi)

def sf_seaoverland(sfi):
    mask = np.where(~np.isnan(sfi))
    if(len(mask[0])>0):
        interp = NearestNDInterpolator(np.transpose(mask), sfi[mask])
        sfi = interp(*np.indices(sfi.shape))
        del interp
    del mask

    return (sfi)

def extrapolation_3d(tsin):
    for i in range(0,len(tsin[:,0,0])):
        tsi=np.squeeze(tsin[i,:,:])
        mask = np.where(~np.isnan(tsi))
        if(len(mask[0])>0):
            interp = NearestNDInterpolator(np.transpose(mask), tsi[mask])
            tsi = interp(*np.indices(tsi.shape))
            del interp
        tsin[i,:,:]=tsi
        del mask, tsi
    return (tsin)

def create_write_nc_bathy_output(lono, lato, bathyo, patho):
    oFile = Dataset(patho, 'w')

    # write attributes
    oFile.title = ('NEMO Bathymetry')
    oFile.description = 'Created with NPP package'
    oFile.institution = 'Euro-Mediterranean Centre for Climate Change - CMCC'
    oFile.creation_date = datetime.datetime.today().strftime('%Y/%m/%d %H:%M')

    # create dimensions
    oFile.createDimension('x', len(lono[0]))
    oFile.createDimension('y', len(lato))
    oFile.createDimension('time_counter', 1)

    # create variables
    nav_lon = oFile.createVariable('nav_lon', float, ('y', 'x'))
    nav_lon.setncattr('units', 'degrees_east')
    nav_lon.setncattr('long_name', 'Longitude')

    nav_lat = oFile.createVariable('nav_lat', float, ('y', 'x'))
    nav_lat.setncattr('units', 'degrees_north')
    nav_lat.setncattr('long_name', 'Latitude')

    Bathymetry = oFile.createVariable('Bathymetry', float, ('time_counter', 'y', 'x'))
    Bathymetry.setncattr('units','meters')
    Bathymetry.setncattr('long_name', 'Bathymetry')

    # write output variables
    nav_lon[:] = np.array(lono).astype(float)
    nav_lat[:] = np.array(lato).astype(float)
    Bathymetry[:] = np.array(bathyo).astype(float)

    # close output file
    oFile.close()

    return (oFile)

def write_nc_mesh_hgr(lonco,latco,longo,latgo,dxo,dyo,zo,ffo,meshho):
    oFile = Dataset(meshho, 'w')

    # create dimensions
    oFile.createDimension('x', len(lonco[0]))
    oFile.createDimension('y', len(latco))
    oFile.createDimension('z', len(zo))
    oFile.createDimension('t', 1)

    # create variables
    e1f = oFile.createVariable('e1f', float, ('t', 'y', 'x'))
    e1t = oFile.createVariable('e1t', float, ('t', 'y', 'x'))
    e1u = oFile.createVariable('e1u', float, ('t', 'y', 'x'))
    e1v = oFile.createVariable('e1v', float, ('t', 'y', 'x'))

    e2f = oFile.createVariable('e2f', float, ('t', 'y', 'x'))
    e2t = oFile.createVariable('e2t', float, ('t', 'y', 'x'))
    e2u = oFile.createVariable('e2u', float, ('t', 'y', 'x'))
    e2v = oFile.createVariable('e2v', float, ('t', 'y', 'x'))

    ff = oFile.createVariable('ff', float, ('t', 'y', 'x'))

    glamf = oFile.createVariable('glamf', float, ('t', 'y', 'x'))
    glamt = oFile.createVariable('glamt', float, ('t', 'y', 'x'))
    glamu = oFile.createVariable('glamu', float, ('t', 'y', 'x'))
    glamv = oFile.createVariable('glamv', float, ('t', 'y', 'x'))

    gphif = oFile.createVariable('gphif', float, ('t', 'y', 'x'))
    gphit = oFile.createVariable('gphit', float, ('t', 'y', 'x'))
    gphiu = oFile.createVariable('gphiu', float, ('t', 'y', 'x'))
    gphiv = oFile.createVariable('gphiv', float, ('t', 'y', 'x'))

    nav_lat = oFile.createVariable('nav_lat', float, ('y', 'x'))
    nav_lon = oFile.createVariable('nav_lon', float, ('y', 'x'))
    nav_lev = oFile.createVariable('nav_lev', float, ('z'))

    time_counter = oFile.createVariable('time_counter', float, ('t'))

    # write output variables
    e1f[:] = np.array(dxo).astype(float)
    e1t[:] = np.array(dxo).astype(float)
    e1u[:] = np.array(dxo).astype(float)
    e1v[:] = np.array(dxo).astype(float)
    e2f[:] = np.array(dyo).astype(float)
    e2t[:] = np.array(dyo).astype(float)
    e2u[:] = np.array(dyo).astype(float)
    e2v[:] = np.array(dyo).astype(float)
    ff[:]  = np.array(ffo).astype(float)
    glamf[:] = np.array(lonco).astype(float)
    glamt[:] = np.array(longo[0:-1,0:-1]).astype(float)
    glamu[:] = np.array(lonco).astype(float)
    glamv[:] = np.array(longo[0:-1,0:-1]).astype(float)
    gphif[:] = np.array(latco).astype(float)
    gphit[:] = np.array(latgo[0:-1,0:-1]).astype(float)
    gphiu[:] = np.array(latgo[0:-1,0:-1]).astype(float)
    gphiv[:] = np.array(latco).astype(float)
    nav_lon[:] = np.array(longo[0:-1,0:-1]).astype(float)
    nav_lat[:] = np.array(latgo[0:-1,0:-1]).astype(float)
    nav_lev[:] = np.array(zo).astype(float)
    time_counter = 0

    # close output file
    oFile.close()

    return (oFile)

def write_nc_mesh_zgr(lono,lato,dxo,dyo,zco,zgo,dzco,dzgo,ffo,bathyo,meshzo):
    oFile = Dataset(meshzo, 'w')

    # create dimensions
    oFile.createDimension('x', len(lono[0,0:-1]))
    oFile.createDimension('y', len(lato[0:-1,0]))
    oFile.createDimension('z', len(zco))
    oFile.createDimension('t', 1)

    # create variables
    e3t_0 = oFile.createVariable('e3t_0', float, ('t', 'z'))
    e3w_0 = oFile.createVariable('e3w_0', float, ('t', 'z'))
    e3t = oFile.createVariable('e3t', float, ('t', 'z', 'y', 'x'))
    e3u = oFile.createVariable('e3u', float, ('t', 'z', 'y', 'x'))
    e3v = oFile.createVariable('e3v', float, ('t', 'z', 'y', 'x'))
    e3w = oFile.createVariable('e3w', float, ('t', 'z', 'y', 'x'))

    gdept_0 = oFile.createVariable('gdept_0', float, ('t', 'z'))
    gdepw_0 = oFile.createVariable('gdepw_0', float, ('t', 'z'))
    gdept = oFile.createVariable('gdept', float, ('t', 'z', 'y', 'x'))
    gdepu = oFile.createVariable('gdepu', float, ('t', 'z', 'y', 'x'))
    gdepv = oFile.createVariable('gdepv', float, ('t', 'z', 'y', 'x'))
    gdepw = oFile.createVariable('gdepw', float, ('t', 'z', 'y', 'x'))

    mbathy = oFile.createVariable('mbathy', float, ('t', 'y', 'x'))

    nav_lat = oFile.createVariable('nav_lat', float, ('y', 'x'))
    nav_lon = oFile.createVariable('nav_lon', float, ('y', 'x'))
    nav_lev = oFile.createVariable('nav_lev', float, ('z'))

    time_counter = oFile.createVariable('time_counter', float, ('t'))

    # write output variables
    e3t_0[:] = np.array(dzco).astype(float)
    e3w_0[:] = np.array(dzgo[0:-1]).astype(float)
    gdept_0[:] = np.array(zco).astype(float)
    gdepw_0[:] = np.array(zgo[0:-1]).astype(float)
    mbathyo=np.zeros([len(lato[0:-1,0]),len(lono[0,0:-1])])
    e3to=np.zeros([1,len(zco),len(lato[0:-1,0]),len(lono[0,0:-1])])
    e3wo=np.zeros([1,len(zco),len(lato[0:-1,0]),len(lono[0,0:-1])])
    gdepto=np.zeros([1,len(zco),len(lato[0:-1,0]),len(lono[0,0:-1])])
    gdepwo=np.zeros([1,len(zco),len(lato[0:-1,0]),len(lono[0,0:-1])])
    for i in range(0,len(lono[0,0:-1])):
        for j in range(0,len(lato[0:-1,0])):
            e3to[0,:,j,i]=dzco
            e3wo[0,:,j,i]=dzgo[0:-1]
            gdepto[0,:,j,i]=zco
            gdepwo[0,:,j,i]=zgo[0:-1]
            a=[]
            if(bathyo[j,i]==0): mbathyo[j,i]=0
            if(bathyo[j,i]!=0): 
                a[:] = [x for x in zco if x<bathyo[j,i]]
                mbathyo[j,i]=len(a)
            del a
    e3t[:] = np.array(e3to).astype(float)
    e3u[:] = np.array(e3to).astype(float)
    e3v[:] = np.array(e3to).astype(float)
    e3w[:] = np.array(e3wo).astype(float) 
    gdept[:] = np.array(gdepto).astype(float)
    gdepu[:] = np.array(gdepwo).astype(float)
    gdepv[:] = np.array(gdepwo).astype(float)
    gdepw[:] = np.array(gdepwo).astype(float)
    mbathy[:] = np.array(mbathyo).astype(float)
    nav_lon[:] = np.array(lono[0:-1,0:-1]).astype(float)
    nav_lat[:] = np.array(lato[0:-1,0:-1]).astype(float)
    nav_lev[:] = np.array(zco).astype(float)
    time_counter = 0

    # close output file
    oFile.close()

    return (oFile)

def write_nc_mask(lono,lato,zo,masko,maskfo):
    oFile = Dataset(maskfo, 'w')

    # create dimensions
    oFile.createDimension('x', len(lono[0,0:-1]))
    oFile.createDimension('y', len(lato[0:-1,0]))
    oFile.createDimension('z', len(zo))
    oFile.createDimension('t', 1)

    # create variables
    fmask = oFile.createVariable('fmask', float, ('t', 'z', 'y', 'x'))
    tmask = oFile.createVariable('tmask', float, ('t', 'z', 'y', 'x'))
    umask = oFile.createVariable('umask', float, ('t', 'z', 'y', 'x'))
    vmask = oFile.createVariable('vmask', float, ('t', 'z', 'y', 'x'))

    fmaskutil = oFile.createVariable('fmaskutil', float, ('t', 'y', 'x'))
    tmaskutil = oFile.createVariable('tmaskutil', float, ('t', 'y', 'x'))
    umaskutil = oFile.createVariable('umaskutil', float, ('t', 'y', 'x'))
    vmaskutil = oFile.createVariable('vmaskutil', float, ('t', 'y', 'x'))

    nav_lat = oFile.createVariable('nav_lat', float, ('y', 'x'))
    nav_lon = oFile.createVariable('nav_lon', float, ('y', 'x'))
    nav_lev = oFile.createVariable('nav_lev', float, ('z'))

    time_counter = oFile.createVariable('time_counter', float, ('t'))

    # write output variables
    fmask[:] = np.array(masko).astype(float)
    tmask[:] = np.array(masko).astype(float)
    umask[:] = np.array(masko).astype(float)
    vmask[:] = np.array(masko).astype(float)
    fmaskutil[:] = np.array(np.squeeze(masko[0,:,:])).astype(float)
    tmaskutil[:] = np.array(np.squeeze(masko[0,:,:])).astype(float)
    umaskutil[:] = np.array(np.squeeze(masko[0,:,:])).astype(float)
    vmaskutil[:] = np.array(np.squeeze(masko[0,:,:])).astype(float)
    nav_lon[:] = np.array(lono[0:-1,0:-1]).astype(float)
    nav_lat[:] = np.array(lato[0:-1,0:-1]).astype(float)
    nav_lev[:] = np.array(zo).astype(float)
    time_counter = 0

    # close output file
    oFile.close()

    return (oFile)


def check_pdens_profile(lonnm,latnm,gdepw,tempnmf,salnmf):
    CT=np.zeros([len(gdepw)])
    for ii in range (0,len(lonnm[0])):
        for jj in range (0,len(latnm)):
            pres=sw.pres(gdepw,latnm[jj,ii])
            CT=sw.pden(np.squeeze(salnmf[:,jj,ii]),np.squeeze(tempnmf[:,jj,ii]),pres)
            for zz in range (1,len(gdepw)):
                if(CT[zz]<CT[zz-1]):
                    tempnmf[zz,jj,ii]=tempnmf[zz-1,jj,ii]
                    salnmf[zz,jj,ii]=salnmf[zz-1,jj,ii]

    return (tempnmf,salnmf)

def write_TS_IC_nc_output(lonnm, latnm, gdepw, tempnmfl, salnmfl, patho_folder, patho_name):
    oFile = Dataset(patho_folder+'/'+patho_name, 'w')

    # write attributes
    oFile.title = ('NEMO Temp. and Sal. initial conditions')
    oFile.description = 'Created with NPP package'
    oFile.institution = 'Euro-Mediterranean Centre for Climate Change - CMCC'
    oFile.creation_date = datetime.datetime.today().strftime('%Y/%m/%d %H:%M')

    # create dimensions
    oFile.createDimension('x', len(lonnm[0]))
    oFile.createDimension('y', len(latnm))
    oFile.createDimension('depth', len(gdepw))
    oFile.createDimension('time_counter', 1)

    # create variables
    lon = oFile.createVariable('lon', float, ('y', 'x'))
    lon.setncattr('units', 'degrees_east')
    lon.setncattr('long_name', 'Longitude')
    lon.setncattr('nav_model', 'Default grid')

    lat = oFile.createVariable('lat', float, ('y', 'x'))
    lat.setncattr('units', 'degrees_north')
    lat.setncattr('long_name', 'Latitude')
    lat.setncattr('nav_model', 'Default grid')

    deptht = oFile.createVariable('deptht', float, ('depth'))
    deptht.setncattr('units', 'meters')
    deptht.setncattr('long_name', 'Depth')
    deptht.setncattr('nav_model', 'Default grid')

    time_counter = oFile.createVariable('time_counter', float, ('time_counter'))
    time_counter.setncattr('units', 'seconds since 1990-01-01 00:00:00')
    time_counter.setncattr('calendar', 'noleap')
    time_counter.setncattr('title', 'Time')
    time_counter.setncattr('long_name', 'Time axis')
    time_counter.setncattr('time_origin', '1990-JAN-01 00:00:00')

    votemper = oFile.createVariable('votemper', float, ('depth', 'y', 'x'))
    votemper.setncattr('units','degC')
    votemper.setncattr('long_name', 'temperature')
    votemper.setncattr('title', 'sea_water_temperature')

    vosaline = oFile.createVariable('vosaline', float, ('depth', 'y', 'x'))
    vosaline.setncattr('units','psu')
    vosaline.setncattr('long_name', 'salinity')
    vosaline.setncattr('title', 'sea_water_salinity')

    # write output variables
    lon[:] = lonnm
    lat[:] = latnm
    deptht[:] = gdepw
    time_counter[:] = 1
    votemper[:] = tempnmfl
    vosaline[:] = salnmfl

    # close output file
    oFile.close()

    return (oFile)

def write_SF_nc_output_MFS(lonsf, latsf, ny, nm, nd, timef, mslf, tccf,\
                           u10f, v10f, t2mf, d2mf, precipf, patho):

    time_units='hours since '+ny+'-01-01 00:00:00'
    oFile = Dataset(patho, 'w')

    # write attributes
    oFile.title = ('NEMO Superficial Conditions')
    oFile.description = 'Created with NPP package'
    oFile.institution = 'Euro-Mediterranean Centre for Climate Change - CMCC'
    oFile.creation_date = datetime.datetime.today().strftime('%Y/%m/%d %H:%M')

    # create dimensions
    oFile.createDimension('x', len(lonsf))
    oFile.createDimension('y', len(latsf))
    oFile.createDimension('time_counter', len(timef))

    # create variables
    lon = oFile.createVariable('lon', float, ('x'))
    lon.setncattr('units', 'degrees_east')
    lon.setncattr('long_name', 'longitude')
    lon.setncattr('axis', 'X')

    lat = oFile.createVariable('lat', float, ('y'))
    lat.setncattr('units', 'degrees_north')
    lat.setncattr('long_name', 'latitude')
    lat.setncattr('axis', 'Y')

    time_counter = oFile.createVariable('time_counter', float, ('time_counter'))
    time_counter.setncattr('units', time_units)
    time_counter.setncattr('calendar', 'proleptic_gregorian')
    time_counter.setncattr('standard_name', 'time')
    time_counter.setncattr('axis', 'T')

    msl = oFile.createVariable('msl', float, ('time_counter', 'y', 'x'))
    msl.setncattr('units','Pa')
    msl.setncattr('long_name', 'Mean sea level pressure')
    msl.setncattr('standard_name', 'air_pressure_at_mean_sea_level')

    clc = oFile.createVariable('clc', float, ('time_counter', 'y', 'x'))
    clc.setncattr('units','(0 - 1)')
    clc.setncattr('long_name', 'Total cloud cover')
    clc.setncattr('standard_name', 'cloud_area_fraction')

    u10 = oFile.createVariable('u10', float, ('time_counter', 'y', 'x'))
    u10.setncattr('units','m s**-1')
    u10.setncattr('long_name', '10 metre U wind component')
    u10.setncattr('standard_name', 'u10')

    v10 = oFile.createVariable('v10', float, ('time_counter', 'y', 'x'))
    v10.setncattr('units','m s**-1')
    v10.setncattr('long_name', '10 metre V wind component')
    v10.setncattr('standard_name', 'v10')

    t2 = oFile.createVariable('t2', float, ('time_counter', 'y', 'x'))
    t2.setncattr('units','K')
    t2.setncattr('long_name', '2 metre temperature')
    t2.setncattr('standard_name', 't2')

    rh = oFile.createVariable('rh', float, ('time_counter', 'y', 'x'))
    rh.setncattr('units','K')
    rh.setncattr('long_name', '2 metre dewpoint temperature')
    rh.setncattr('standard_name', 'rh')

    precip = oFile.createVariable('precip', float, ('time_counter', 'y', 'x'))
    #precip.setncattr('units','Kg/m**2 s')
    precip.setncattr('units','m')
    precip.setncattr('long_name', 'Total precipitation')
    precip.setncattr('standard_name', 'precip')

    # write output variables
    lon[:] = lonsf
    lat[:] = latsf
    time_counter[:] = timef
    msl[:] = mslf
    clc[:] = tccf
    u10[:] = u10f
    v10[:] = v10f
    t2[:]  = t2mf
    rh[:]  = d2mf
    precip[:] = precipf
    # close output file
    oFile.close()

    return (oFile)

def write_SF_nc_output_ECMWF(lonsf, latsf, ny, nm, nd, timef, mslf, tccf, u10f, \
                             v10f, t2mf, d2mf, precipf, swrdf, lwrdf, patho):

    time_units='hours since '+ny+'-01-01 00:00:00'
    oFile = Dataset(patho, 'w')

    # write attributes
    oFile.title = ('NEMO Superficial Conditions')
    oFile.description = 'Created with NPP package'
    oFile.institution = 'Euro-Mediterranean Centre for Climate Change - CMCC'
    oFile.creation_date = datetime.datetime.today().strftime('%Y/%m/%d %H:%M')

    # create dimensions
    if(len(lonsf.shape)>1):
        oFile.createDimension('x', len(lonsf[0,:]))
        oFile.createDimension('y', len(latsf[:,0]))
    else:
        oFile.createDimension('x', len(lonsf))
        oFile.createDimension('y', len(latsf))
    oFile.createDimension('time_counter', len(timef))

    # create variables
    if(len(lonsf.shape)>1):
        lon = oFile.createVariable('lon', float, ('y','x'))
    else:
        lon = oFile.createVariable('lon', float, ('x'))
    lon.setncattr('units', 'degrees_east')
    lon.setncattr('long_name', 'longitude')
    lon.setncattr('axis', 'X')
 
    if(len(lonsf.shape)>1):
        lat = oFile.createVariable('lat', float, ('y','x'))
    else:
        lat = oFile.createVariable('lat', float, ('y'))
    lat.setncattr('units', 'degrees_north')
    lat.setncattr('long_name', 'latitude')
    lat.setncattr('axis', 'Y')

    time_counter = oFile.createVariable('time_counter', float, ('time_counter'))
    time_counter.setncattr('units', time_units)
    time_counter.setncattr('calendar', 'proleptic_gregorian')
    time_counter.setncattr('standard_name', 'time')
    time_counter.setncattr('axis', 'T')

    msl = oFile.createVariable('msl', float, ('time_counter', 'y', 'x'))
    msl.setncattr('units','Pa')
    msl.setncattr('long_name', 'Mean sea level pressure')
    msl.setncattr('standard_name', 'air_pressure_at_mean_sea_level')

    clc = oFile.createVariable('clc', float, ('time_counter', 'y', 'x'))
    clc.setncattr('units','(0 - 1)')
    clc.setncattr('long_name', 'Total cloud cover')
    clc.setncattr('standard_name', 'cloud_area_fraction')

    u10 = oFile.createVariable('u10', float, ('time_counter', 'y', 'x'))
    u10.setncattr('units','m s**-1')
    u10.setncattr('long_name', '10 metre U wind component')
    u10.setncattr('standard_name', 'u10')

    v10 = oFile.createVariable('v10', float, ('time_counter', 'y', 'x'))
    v10.setncattr('units','m s**-1')
    v10.setncattr('long_name', '10 metre V wind component')
    v10.setncattr('standard_name', 'v10')

    t2 = oFile.createVariable('t2', float, ('time_counter', 'y', 'x'))
    t2.setncattr('units','K')
    t2.setncattr('long_name', '2 metre temperature')
    t2.setncattr('standard_name', 't2')

    rh = oFile.createVariable('rh', float, ('time_counter', 'y', 'x'))
    rh.setncattr('units','K')
    rh.setncattr('long_name', '2 metre dewpoint temperature')
    rh.setncattr('standard_name', 'rh')

    precip = oFile.createVariable('precip', float, ('time_counter', 'y', 'x'))
    precip.setncattr('units','Kg/m**2 s')
    #precip.setncattr('units','m')
    precip.setncattr('long_name', 'Total precipitation')
    precip.setncattr('standard_name', 'precip')

    srad = oFile.createVariable('srad', float, ('time_counter', 'y', 'x'))
    srad.setncattr('units','W m**-2')
    srad.setncattr('long_name', 'Shortwave radiation')
    srad.setncattr('standard_name', 'srad')

    lrad = oFile.createVariable('lrad', float, ('time_counter', 'y', 'x'))
    lrad.setncattr('units','W m**-2')
    lrad.setncattr('long_name', 'Longwave radiation')
    lrad.setncattr('standard_name', 'lrad')

    # write output variables
    lon[:]  = lonsf
    lat[:]  = latsf
    time_counter[:] = timef
    msl[:]  = mslf
    clc[:]  = tccf
    u10[:]  = u10f
    v10[:]  = v10f
    t2[:]   = t2mf
    rh[:]   = d2mf
    precip[:] = precipf
    srad[:] = swrdf
    lrad[:] = lwrdf
    # close output file
    oFile.close()

    return (oFile)

def write_SF_nc_output_ECMWF_WRF(lonsf, latsf, ny, nm, nd, timef, mslf, u10f, \
                               v10f, t2mf, d2mf, precipf, swrdf, lwrdf, patho):

    time_units='hours since '+ny+'-01-01 00:00:00'
    oFile = Dataset(patho, 'w')

    # write attributes
    oFile.title = ('NEMO Superficial Conditions')
    oFile.description = 'Created with NPP package'
    oFile.institution = 'Euro-Mediterranean Centre for Climate Change - CMCC'
    oFile.creation_date = datetime.datetime.today().strftime('%Y/%m/%d %H:%M')

    # create dimensions
    if(len(lonsf.shape)>1):
        oFile.createDimension('x', len(lonsf[0,:]))
        oFile.createDimension('y', len(latsf[:,0]))
    else:
        oFile.createDimension('x', len(lonsf))
        oFile.createDimension('y', len(latsf))
    oFile.createDimension('time_counter', len(timef))

    # create variables
    if(len(lonsf.shape)>1):
        lon = oFile.createVariable('lon', float, ('y','x'))
    else:
        lon = oFile.createVariable('lon', float, ('x'))
    lon.setncattr('units', 'degrees_east')
    lon.setncattr('long_name', 'longitude')
    lon.setncattr('axis', 'X')

    if(len(lonsf.shape)>1):
        lat = oFile.createVariable('lat', float, ('y','x'))
    else:
        lat = oFile.createVariable('lat', float, ('y'))
    lat.setncattr('units', 'degrees_north')
    lat.setncattr('long_name', 'latitude')
    lat.setncattr('axis', 'Y')

    time_counter = oFile.createVariable('time_counter', float, ('time_counter'))
    time_counter.setncattr('units', time_units)
    time_counter.setncattr('calendar', 'proleptic_gregorian')
    time_counter.setncattr('standard_name', 'time')
    time_counter.setncattr('axis', 'T')

    msl = oFile.createVariable('msl', float, ('time_counter', 'y', 'x'))
    msl.setncattr('units','Pa')
    msl.setncattr('long_name', 'Mean sea level pressure')
    msl.setncattr('standard_name', 'air_pressure_at_mean_sea_level')

    u10 = oFile.createVariable('u10', float, ('time_counter', 'y', 'x'))
    u10.setncattr('units','m s**-1')
    u10.setncattr('long_name', '10 metre U wind component')
    u10.setncattr('standard_name', 'u10')

    v10 = oFile.createVariable('v10', float, ('time_counter', 'y', 'x'))
    v10.setncattr('units','m s**-1')
    v10.setncattr('long_name', '10 metre V wind component')
    v10.setncattr('standard_name', 'v10')

    t2 = oFile.createVariable('t2', float, ('time_counter', 'y', 'x'))
    t2.setncattr('units','K')
    t2.setncattr('long_name', '2 metre temperature')
    t2.setncattr('standard_name', 't2')

    rh = oFile.createVariable('rh', float, ('time_counter', 'y', 'x'))
    rh.setncattr('units','K')
    rh.setncattr('long_name', '2 metre dewpoint temperature')
    rh.setncattr('standard_name', 'rh')

    precip = oFile.createVariable('precip', float, ('time_counter', 'y', 'x'))
    precip.setncattr('units','Kg/m**2 s')
    precip.setncattr('long_name', 'Total precipitation')
    precip.setncattr('standard_name', 'precip')

    srad = oFile.createVariable('srad', float, ('time_counter', 'y', 'x'))
    srad.setncattr('units','W m**-2')
    srad.setncattr('long_name', 'Shortwave radiation')
    srad.setncattr('standard_name', 'srad')

    lrad = oFile.createVariable('lrad', float, ('time_counter', 'y', 'x'))
    lrad.setncattr('units','W m**-2')
    lrad.setncattr('long_name', 'Longwave radiation')
    lrad.setncattr('standard_name', 'lrad')

    # write output variables
    lon[:]  = lonsf
    lat[:]  = latsf
    time_counter[:] = timef
    msl[:]  = mslf
    u10[:]  = u10f
    v10[:]  = v10f
    t2[:]   = t2mf
    rh[:]   = d2mf
    precip[:] = precipf
    srad[:] = swrdf
    lrad[:] = lwrdf
    # close output file
    oFile.close()

    return (oFile)

def write_SF_nc_output_NCAR(lonsf, latsf, ny, nm, nd, timef, mslf, u10f, v10f,\
                            t2mf, d2mf, precipf, shwf, lgwf, snowf, patho):

    time_units='hours since '+ny+'-'+nm+'-'+nd+' 00:00:00'
    oFile = Dataset(patho, 'w')

    # write attributes
    oFile.title = ('NEMO Superficial Conditions')
    oFile.description = 'Created with NPP package'
    oFile.institution = 'Euro-Mediterranean Centre for Climate Change - CMCC'
    oFile.creation_date = datetime.datetime.today().strftime('%Y/%m/%d %H:%M')

    # create dimensions
    oFile.createDimension('x', len(lonsf))
    oFile.createDimension('y', len(latsf))
    oFile.createDimension('time_counter', len(timef))

    # create variables
    lon = oFile.createVariable('lon', float, ('x'))
    lon.setncattr('units', 'degrees_east')
    lon.setncattr('long_name', 'longitude')
    lon.setncattr('axis', 'X')

    lat = oFile.createVariable('lat', float, ('y'))
    lat.setncattr('units', 'degrees_north')
    lat.setncattr('long_name', 'latitude')
    lat.setncattr('axis', 'Y')

    time_counter = oFile.createVariable('time_counter', float, ('time_counter'))
    time_counter.setncattr('units', time_units)
    time_counter.setncattr('calendar', 'proleptic_gregorian')
    time_counter.setncattr('standard_name', 'time')
    time_counter.setncattr('axis', 'T')

    msl = oFile.createVariable('msl', float, ('time_counter', 'y', 'x'))
    msl.setncattr('units','Pa')
    msl.setncattr('long_name', 'Mean sea level pressure')
    msl.setncattr('standard_name', 'air_pressure_at_mean_sea_level')

    u10 = oFile.createVariable('u10', float, ('time_counter', 'y', 'x'))
    u10.setncattr('units','m s**-1')
    u10.setncattr('long_name', '10 metre U wind component')
    u10.setncattr('standard_name', 'u10')

    v10 = oFile.createVariable('v10', float, ('time_counter', 'y', 'x'))
    v10.setncattr('units','m s**-1')
    v10.setncattr('long_name', '10 metre V wind component')
    v10.setncattr('standard_name', 'v10')

    t2 = oFile.createVariable('t2', float, ('time_counter', 'y', 'x'))
    t2.setncattr('units','K')
    t2.setncattr('long_name', '2 metre temperature')
    t2.setncattr('standard_name', 't2')

    rh = oFile.createVariable('rh', float, ('time_counter', 'y', 'x'))
    rh.setncattr('units','K')
    rh.setncattr('long_name', '2 metre dewpoint temperature')
    rh.setncattr('standard_name', 'rh')

    precip = oFile.createVariable('precip', float, ('time_counter', 'y', 'x'))
    precip.setncattr('units','Kg/m**2 s')
    precip.setncattr('long_name', 'Total precipitation')
    precip.setncattr('standard_name', 'precip')

    srad = oFile.createVariable('srad', float, ('time_counter', 'y', 'x'))
    srad.setncattr('units','W m**-2')
    srad.setncattr('long_name', 'Surface solar radiation')
    srad.setncattr('standard_name', 'srad')

    trad = oFile.createVariable('trad', float, ('time_counter', 'y', 'x'))
    trad.setncattr('units','W m**-2')
    trad.setncattr('long_name', 'Surface thermal radiation')
    trad.setncattr('standard_name', 'trad')

    snow = oFile.createVariable('snow', float, ('time_counter', 'y', 'x'))
    snow.setncattr('units','Kg/m**2 s')
    snow.setncattr('long_name', 'Surface snow')
    snow.setncattr('standard_name', 'snow')

    # write output variables
    lon[:] = lonsf
    lat[:] = latsf
    time_counter[:] = timef
    msl[:] = mslf
    u10[:] = u10f
    v10[:] = v10f
    t2[:]  = t2mf
    rh[:]  = d2mf
    srad[:]= shwf
    trad[:]= lgwf
    snow[:]= snowf
    # close output file
    oFile.close()

    return (oFile)
