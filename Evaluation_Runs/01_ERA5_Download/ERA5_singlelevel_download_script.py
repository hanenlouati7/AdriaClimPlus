import cdsapi

c = cdsapi.Client()

yr_v = ['1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020' ,'2021','2022','2023']
mon_v = ['01','02','03','04','05','06','07','08','09','10','11','12']

for yr in yr_v:
    for mon in mon_v:
        c.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'variable': [
                    '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
                    '2m_temperature', 'land_sea_mask', 'mean_sea_level_pressure',
                    'total_cloud_cover', 'total_precipitation', 'leaf_area_index_high_vegetation',
                    'soil_temperature_level_1', 'soil_temperature_level_2', 'soil_temperature_level_3',
                    'soil_temperature_level_4',  'soil_type', 'surface_latent_heat_flux',
                    'surface_sensible_heat_flux', 'surface_solar_radiation_downwards',
                    'total_column_cloud_ice_water', 'total_column_cloud_liquid_water',
                    'sea_surface_temperature','volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2',
                    'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4', 'snow_depth', 'skin_temperature',
                    'surface_pressure','sea_ice_cover','geopotential'
                ],
                'year': yr,
                'month': mon,
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': [
                    '00:00', '06:00', '12:00',
                    '18:00',
                    #'00:00', '01:00', '02:00',
                    #'03:00', '04:00', '05:00',
                    #'06:00', '07:00', '08:00',
                    #'09:00', '10:00', '11:00',
                    #'12:00', '13:00', '14:00',
                    #'15:00', '16:00', '17:00',
                    #'18:00', '19:00', '20:00',
                    #'21:00', '22:00', '23:00',
                ],
                'area': [
                    55, 0, 25,
                    30,
                ],
                'format': 'grib',
            },
            yr+'/'+mon+'/ERA5_singlelevel_'+yr+'_'+mon+'.grib')
