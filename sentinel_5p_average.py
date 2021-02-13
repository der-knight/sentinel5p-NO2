#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#download data
os.environ['HTTP_PROXY']= '10.10.78.61:3128'
os.environ['HTTPS_PROXY']= '10.10.78.61:3128'
get_ipython().system("'sentinel/dhusget.sh' -d 'https://s5phub.copernicus.eu/dhus/' -u 's5pguest' -p 's5pguest' -m 'Sentinel-5' -S 2020-11-01T00:00:00.000Z -E 2020-11-30T20:00:00.000Z -F 'platformname:Sentinel-5 AND producttype:L2__NO2___ AND processinglevel:L2 AND processingmode:Offline' -l 100 -c 68.14712,7.798000:97.34466,38.090000 -o 'product'")


# In[4]:


#working with single sentinel file
FName='S5P_OFFL_L2__NO2____20200101T073846_20200101T092016_11491_01_010302_20200103T003802.nc'
FIn = xr.open_dataset(FName,'PRODUCT');
FIn


# In[5]:


FIn.data_vars


# In[6]:


FIn.coords


# In[7]:


VarTime=FIn.time.values


# In[8]:


date=VarTime.astype('datetime64[D]')
Lon=FIn['longitude']
Lat=FIn['latitude']
VarNO2=FIn['nitrogendioxide_tropospheric_column']
FIn.close()
print(VarNO2)


# In[32]:


fig=plt.figure(figsize=(40,15)) # create a figure frame and set up the figure size
ax = plt.axes(projection=ccrs.PlateCarree()) # Creates an empty subplot 
# Plot VarNO2 where we remove the time dimension `VarNO2[0]`
extent = [60,100,0,40]
VarNO2[0].plot.pcolormesh(ax=ax, x='longitude', y='latitude',                           add_colorbar=True, cmap='seismic',                            transform=ccrs.PlateCarree(),vmin=0,vmax=0.0005) 
ax.set_extent(extent)
ax.add_feature(cartopy.feature.RIVERS) # add river
ax.set_title('S-5p L2 NO$_2$ ({}) '.format(str(date[0]))) # add title
ax.coastlines('10m')  # add coastline
ax.stock_img() # add the color of earth
ax.gridlines()  # add grid line


# In[ ]:


input_files='S5P*.nc'
export_path='sentinel.nc'
Converted_NO2_2020 = harp.import_product(input_files,                       operations= "latitude >= 7.8[degree_north] ; latitude <= 38[degree_north] ;                       longitude>=65 [degree_east];longitude<=98 [degree_east];tropospheric_NO2_column_number_density_validity>75;                       bin_spatial(600,7.8, .05,660 , 65, .05);                       derive(latitude {latitude}); derive(longitude {longitude});                       keep(latitude,longitude,tropospheric_NO2_column_number_density,weight)",                       post_operations="bin(); squash(time, (latitude,longitude))"                   
                      )
        
harp.export_product(Converted_NO2_2020, export_path,file_format="netcdf")


# In[34]:


file=xr.open_dataset('1.nc')
no2=file['tropospheric_NO2_column_number_density']*10**3


# In[57]:


fig=plt.figure(figsize=(40,15)) # create a figure frame and set up the figure size
ax = plt.axes(projection=ccrs.PlateCarree()) # Creates an empty subplot 
extent = [60,100,0,40]
no2[0].plot.pcolormesh(ax=ax, x='longitude', y='latitude',                           add_colorbar=True, cmap='seismic',                            transform=ccrs.PlateCarree(),vmin=0,vmax=0.2) 
ax.set_extent(extent)
ax.add_feature(cartopy.feature.RIVERS) # add river
ax.set_title('S-5p L2 NO$_2$ ({}) '.format(str(date[0]))) # add title
ax.coastlines('10m')  # add coastline
ax.stock_img() # add the color of earth
ax.gridlines()  # add grid line


# In[55]:


weight=file['weight']
fig=plt.figure(figsize=(40,15)) # create a figure frame and set up the figure size
ax = plt.axes(projection=ccrs.PlateCarree()) # Creates an empty subplot 
extent = [60,100,0,40]
weight[0].plot.pcolormesh(ax=ax, x='longitude', y='latitude',                           add_colorbar=True, cmap='seismic',                            transform=ccrs.PlateCarree(),vmin=20,vmax=31) 
ax.set_extent(extent)
ax.add_feature(cartopy.feature.RIVERS) # add river
ax.set_title('S-5p L2 NO$_2$ ({}) '.format(str(date[0]))) # add title
ax.coastlines('10m')  # add coastline
ax.stock_img() # add the color of earth
ax.gridlines()  # add grid line


# In[25]:



