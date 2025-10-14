##################################################################
##################################################################
import pylab as py
import matplotlib.pyplot as plt
import numpy as np
import netCDF4
######
nc1=netCDF4.Dataset('depth_ADRb.020_04_notime.nc')
nc2=netCDF4.Dataset('depth_ADRb.020_03s_notime.nc')
nc3=netCDF4.Dataset('depth_ADR.raw_notime.nc')
##
nd1=netCDF4.Dataset('depth_ADR.diff_smoothed_Murat_unsmoothed.nc')
nd2=netCDF4.Dataset('depth_ADR.diff_smoothed_VSC_unsmoothed.nc')
nd3=netCDF4.Dataset('depth_ADR.diff_Murat_unsmoothed_VSC_unsmoothed.nc')
######
lon1 = nc1.variables['nav_lon'][:]
lat1 = nc1.variables['nav_lat'][:]
mask = nc1.variables['Bathymetry'][:]
lon3 = nc3.variables['nav_lon'][:]
lat3 = nc3.variables['nav_lat'][:]
##
bathy1 = nc1.variables['Bathymetry'][:]
bathy2 = nc2.variables['Bathymetry'][:]
bathy3 = nc3.variables['Bathymetry'][:]
##
diff1 = nd1.variables['Bathymetry'][:]
diff1[mask==0]=np.nan
diff2 = nd2.variables['Bathymetry'][:]
diff2[mask==0]=np.nan
diff3 = nd3.variables['Bathymetry'][:]
diff3[mask==0]=np.nan
######
plt.figure()
plt.contour(lon1,lat1,bathy1,levels=[0],colors='r')
plt.contour(lon1,lat1,bathy2,levels=[0],colors='b')
plt.contour(lon3,lat3,bathy3,levels=[0],colors='k')
plt.title('Smoothed (red) - Murat Unsmoothed (blue) - Vladimir Unsmoothed (black)')
plt.savefig('Bathymetry_contours.png',dpi=150)

plt.figure()
plt.pcolor(lon1,lat1,diff1,vmin=-100,vmax=100)
plt.title('Diff. Bathymetry: smoothed - Murat unsmoothed')
plt.colorbar()
plt.savefig('Bathymetry_diff_smoothed_Murat_unsmoothed.png',dpi=150) 
##
plt.figure()
plt.pcolor(lon1,lat1,diff2,vmin=-100,vmax=100)
plt.title('Diff. Bathymetry: smoothed - Vladimir unsmoothed')
plt.colorbar()
plt.savefig('Bathymetry_diff_smoothed_Vladimir_unsmoothed.png',dpi=150)
##
plt.figure()
plt.pcolor(lon1,lat1,diff3,vmin=-100,vmax=100)
plt.title('Diff. Bathymetry: Murat unsmoothed - Vladimir unsmoothed')
plt.colorbar()
plt.savefig('Bathymetry_diff_Murat_unsmoothed_Vladimir_unsmoothed.png',dpi=150)
plt.show()
######
