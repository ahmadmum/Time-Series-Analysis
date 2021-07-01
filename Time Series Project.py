# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 13:41:12 2020

@author: mumta
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
from matplotlib.cm import get_cmap
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib import dates as d
import datetime as dt
import windrose
from windrose import WindroseAxes
from datetime import datetime, timedelta

data_1 = 'C:/Users/mumta/Desktop/Time Series Analysis/Time series analysis R/DWDFile_Assignment1/'
df_1 = pd.read_csv(data_1+"weste_product_2010_air_temperature.csv", sep=";",decimal=",",
                 header=0,
                 parse_dates=['Datum'],
                 index_col=2)
df_1.isnull().sum()
df_1 = df_1.drop(["Unnamed: 11"],axis=1)
            
data_2 = 'C:/Users/Ingenious/Desktop/PythonFiles/'
df_2 = pd.read_csv(data_2+"weste_product_2010_precipitation.csv", sep=";",decimal=",",
                 header=0,
                 parse_dates=['Datum'],
                 index_col=2)
df_2.isnull().sum()
df_2 = df_2.drop(["Unnamed: 11"],axis=1)

data_3 = 'C:/Users/Ingenious/Desktop/PythonFiles/'
df_3 = pd.read_csv(data_3+"weste_product_2010_soil_temperature.csv", sep=";",decimal=",",
                 header=0,
                 parse_dates=['Datum'],
                 index_col=2)
df_3.isnull().sum()
df_3 = df_3.drop(["Unnamed: 11"],axis=1)

            
####### Extract Columns of ta,ts and precipitation values
ta_temp = df_1.iloc[:,2]
ts_temp = df_3.iloc[:,2]
precip = df_2.iloc[:,2]

##Temperature
###First Step, check the hourly gap
ta_temp = ta_temp.reset_index()
deltas = ta_temp['Datum'].diff()[1:]
total_gaps = deltas[deltas > timedelta(hours=1)]
print(total_gaps)

###Second Step, check the dates
ta_temp['hour'] = ta_temp.Datum.dt.hour
ta_temp['diff'] = ta_temp['hour'].diff()[1:]
date_gaps = ta_temp.iloc[4579:4581,:]


###########Extraaaa


##Soil
###First Step, check the hourly gap
ts_temp = ts_temp.reset_index()
deltas_s = ts_temp['Datum'].diff()[1:]
total_gaps_s = deltas_s[deltas_s > timedelta(hours=1)]
print(total_gaps_s)

###Second Step, check the dates
ts_temp['hour'] = ts_temp.Datum.dt.hour
ts_temp['diff'] = ts_temp['hour'].diff()[1:]
date_gaps_s = ts_temp.iloc[4578:4580,:]

##Precip
###First Step, check the hourly gap
precip = precip.reset_index()
deltas_p = precip['Datum'].diff()[1:]
total_gaps_p = deltas_p[deltas_p > timedelta(hours=1)]
print(total_gaps_p)

###Second Step, check the dates
precip['hour'] = precip.Datum.dt.hour
precip['diff'] = precip['hour'].diff()[1:]
date_gaps_p = precip.iloc[4578:4580,:]

########Calculate mean, minimum and maximum values of whole time series data
mean_ta_temp = ta_temp.resample('Y').mean()
mean_ts_temp = ts_temp.resample('Y').mean()
mean_precip = precip.resample('Y').mean()
 
ta_temp_min = ta_temp.min(axis=0)
ts_temp_min = ts_temp.min(axis=0)
precip_min  = precip.min(axis=0)

ta_temp_max = ta_temp.max(axis=0)
ts_temp_max = ts_temp.max(axis=0)
precip_max = precip.max(axis=0)

########sum of whole precipitation data
precip_sum = precip.resample('Y').sum()

#######Calculate Monthly min, max and mean values
monthly_ta_temp = ta_temp.reset_index()
monthly_ta_temp['Month'] = monthly_ta_temp['Datum'].dt.month
monthly_ta_temp = monthly_ta_temp.set_index('Datum')

month_ta_temp = monthly_ta_temp['2010-01-01':'2010-12-31']

monthly_ta_temp_mean = month_ta_temp.resample('M').mean()
monthly_ta_temp_min = month_ta_temp['Wert'].groupby(month_ta_temp.index.month).min()
monthly_ta_temp_max = month_ta_temp['Wert'].groupby(month_ta_temp.index.month).max()


#####Subset air temperature data to june
air_temp_june = monthly_ta_temp['2010-06-01':'2010-06-30']
air_temp_june_d = air_temp_june.resample('D').mean()
air_temp_june_w = air_temp_june.resample('W').mean()

##############
month_ta_temp = monthly_ta_temp['2010-01-01':'2010-12-31']
month_ta_temp_d = monthly_ta_temp.resample('D').mean()
month_ta_temp_w = monthly_ta_temp.resample('W').mean()



monthly_ts_temp = ts_temp.reset_index()
monthly_ts_temp['Month'] = monthly_ts_temp['Datum'].dt.month
monthly_ts_temp = monthly_ts_temp.set_index('Datum')

month_ts_temp = monthly_ts_temp['2010-01-01':'2010-12-31']

monthly_ts_temp_mean = month_ts_temp.resample('M').mean()
monthly_ts_temp_min = month_ts_temp['Wert'].groupby(month_ts_temp.index.month).min()
monthly_ts_temp_max = month_ts_temp['Wert'].groupby(month_ts_temp.index.month).max()

####Subset Soil Temperature Data to June
soil_temp_june =monthly_ts_temp['2010-06-01':'2010-06-30']

#########Sum of Monthly Precipitaion Data
monthly_precip = precip.reset_index()
monthly_precip['Month'] = monthly_precip['Datum'].dt.month
monthly_precip = monthly_precip.set_index('Datum')

month_precip = monthly_precip['2010-01-01':'2010-12-31']

monthly_precip_sum = precip_sum = precip.resample('M').sum()






######3Calculate Daily min max and mean value
daily_ta_temp = ta_temp.reset_index()
daily_ta_temp['Day'] = daily_ta_temp['Datum'].dt.day
daily_ta_temp = daily_ta_temp.set_index('Datum')

day_ta_temp = daily_ta_temp['2010-01-01':'2010-12-31']


daily_ta_temp_mean = day_ta_temp.resample('D').mean()





daily_ts_temp = ts_temp.reset_index()
daily_ts_temp['Day'] = daily_ts_temp['Datum'].dt.day
daily_ts_temp = daily_ts_temp.set_index('Datum')

day_ts_temp = daily_ts_temp['2010-01-01':'2010-12-31']

daily_ts_temp_mean = day_ts_temp.resample('D').mean()


######Conversion of daily air temperature into hourly
hourly_ta_temp = ta_temp.reset_index()
hourly_ta_temp['Hour'] = hourly_ta_temp['Datum'].dt.hour
hourly_ta_temp = hourly_ta_temp.set_index('Datum')

hour_ta_temp = hourly_ta_temp['2010-01-01':'2010-12-31']


######## Calculate Daily sum of precipitation
daily_precip = precip.reset_index()
daily_precip['Day'] = daily_precip['Datum'].dt.day
daily_precip = daily_precip.set_index('Datum')

day_precip = daily_precip['2010-01-01':'2010-12-31']

daily_precip_sum = day_precip.resample('D').sum()

weekly_ta_temp = ta_temp.reset_index()
weekly_ta_temp['week'] = weekly_ta_temp['Datum'].dt.week
weekly_ta_temp = weekly_ta_temp.set_index('Datum')

week_ta_temp = weekly_ta_temp['2010-01-01':'2010-12-31']

weekly_air_temp_june =weekly_ta_temp['2010-06-01':'2010-06-30']

weekly_ta_temp_mean = week_ta_temp.resample('W').mean()
weekly_ta_temp_min = week_ta_temp['Wert'].groupby(week_ta_temp.index.week).min()
weekly_ta_temp_max = week_ta_temp['Wert'].groupby(week_ta_temp.index.week).max()




weekly_ts_temp = ts_temp.reset_index()
weekly_ts_temp['week'] = weekly_ts_temp['Datum'].dt.week
weekly_ts_temp = weekly_ts_temp.set_index('Datum')

week_ts_temp = weekly_ts_temp['2010-01-01':'2010-12-31']

weekly_ts_temp_mean = week_ts_temp.resample('W').mean()
weekly_ts_temp_min = week_ts_temp['Wert'].groupby(week_ts_temp.index.week).min()
weekly_ts_temp_max = week_ts_temp['Wert'].groupby(week_ts_temp.index.week).max()

####Weekly sum of precipitation
weekly_precip = precip.reset_index()
weekly_precip['Day'] = weekly_precip['Datum'].dt.week
weekly_precip = weekly_precip.set_index('Datum')

week_precip = weekly_precip['2010-01-01':'2010-12-31']
weekly_precip_min = week_precip['Wert'].groupby(week_precip.index.week).min()
weekly_precip_max = week_precip['Wert'].groupby(week_precip.index.week).max()

#####Weekly Sum of Precipitation
weekly_precip_sum = week_precip.resample('W').sum()

######Plotting
##fig = plt.figure(figsize=(10,10))
##fig.plot(ta_temp, 'r', label='ta_temp')

#####Plot ta temp, ts temp and precipitation for whole time series

######One Plot with the soil and air temperature in june 2010


fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(2,1,1)


ax.plot(air_temp_june['Wert'],'r', label='June_ta')
ax.plot(soil_temp_june['Wert'],'b', label='June_ts',linestyle='--')


ax.legend()
ax.set_xlabel('June')
ax.set_ylabel('degree C')

######Plot Soil and Air Temperature


fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)

ax1.plot(ta_temp, 'r', label='ta_temp')
ax2.plot(ts_temp, 'b', label='ts_temp')


ax1.legend()
ax1.set_title('Yearly_Air_Temperature')
ax1.set_xlabel('Year')
ax1.set_ylabel('Air_Temperature')

ax2.legend()
ax2.set_title('Yearly_Soil_Temperature')
ax2.set_xlabel('Year')
ax2.set_ylabel('Soil_Temperature')

######Plot with Hourly, weekly and daily air temperature
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
ax1.plot(daily_ta_temp, 'r', label='day_ta_temp')
ax2.plot(weekly_ta_temp, 'b', label='week_ta_temp')
ax3.plot(hourly_ta_temp, 'g', label='hour_ta_temp')

ax1.legend()
ax1.set_title('Daily_Air_Temperature')
ax1.set_xlabel('Day')
ax1.set_ylabel('Air_Temperature')

ax2.legend()
ax2.set_title('Weekly_Air_Temperature')
ax2.set_xlabel('Week')
ax2.set_ylabel('Air_Temperature')

ax3.legend()
ax3.set_title('Hourly_Air_Temperature')
ax3.set_xlabel('Hour')
ax3.set_ylabel('Air_Temperature')

####Extrraaaaaaaaa
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(311)

ax1.plot(air_temp_june['Wert'], 'r', label='day_ta_temp')
ax1.plot(air_temp_june_d['Wert'], 'b', label='week_ta_temp')
ax1.plot(air_temp_june_w['Wert'], 'g', label='hour_ta_temp')

ax1.legend()
ax1.set_title('Daily_Air_Temperature')
ax1.set_xlabel('Day')
ax1.set_ylabel('Air_Temperature')

ax2.legend()
ax2.set_title('Weekly_Air_Temperature')
ax2.set_xlabel('Week')
ax2.set_ylabel('Air_Temperature')

ax3.legend()
ax3.set_title('Hourly_Air_Temperature')
ax3.set_xlabel('Hour')
ax3.set_ylabel('Air_Temperature')

##########
#######Plot air and soil temperature data for the month of june
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax1.plot(air_temp_june, 'r', label='June_Air_Temp')
ax2.plot(soil_temp_june, 'b', label='June_Soil_Temp')


ax1.legend()
ax1.set_title('June_Air_Temperature')
ax1.set_xlabel('June')
ax1.set_ylabel('Air_Temperature')

ax2.legend()
ax2.set_title('June_Soil_Temperature')
ax2.set_xlabel('June')
ax2.set_ylabel('Soil_Temperature')