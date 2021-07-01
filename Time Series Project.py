# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 12:38:34 2020

@author: mumta
"""

import numpy as np
import pandas as pd

#####################    reading files

stat_1 = 'C:/Users/mumta/Desktop/Times series analysis Py/'
at = pd.read_csv(stat_1+"weste_product_2010_air_temperature.csv", sep=";",decimal=",",
                 header=0,
              parse_dates=['Datum'],
                 index_col=2)

stat_2 = 'C:/Users/mumta/Desktop/Times series analysis Py/'
p = pd.read_csv(stat_2+"weste_product_2010_precipitation.csv", sep=";",decimal=",",
                 header=0,
                 parse_dates=['Datum'],
                 index_col=2)

stat_3 = 'C:/Users/mumta/Desktop/Times series analysis Py/'
st= pd.read_csv(stat_3+"weste_product_2010_soil_temperature.csv", sep=";",decimal=",",
                 header=0,
                 parse_dates=['Datum'],
                 index_col=2)

#################      extract relevant column
  


at_2C= at.iloc[:,2]
p_2C = p.iloc[:,2]
st_2C = st.iloc[:,2]




#################     Gap and Irregularities


date_range = pd.date_range('2010-01-01 00:00:00', '2010-12-31 23:00:00', freq='60Min')


s= at.iloc[:,2]




mean_air_temperature = s.resample('y').mean()

s.index = pd.DatetimeIndex(s.index)

s = s.reindex(date_range, fill_value=0)
print(s)











print(sp.asfreq('D'))
























import pandas as pd

df = pd.read_csv('Input.csv')

# Generate df_borders - NaN readings for start / end of each area / date


df_start = at_2C[['area','date']].drop_duplicates()
df_end = df_start.copy()
df_start['hour'] = '07:00:00'
df_end['hour'] = '13:00:00'
df_borders = pd.concat([df_start,df_end])

# Compute Datetime column and drop hour column, for both DataFrames
df['Datetime'] = pd.to_datetime(df.date + ' ' + df.hour)
df.drop('hour', inplace=True, axis = 1)
df_borders['Datetime'] = pd.to_datetime(df_borders.date + ' ' + df_borders.hour)
df_borders.drop('hour', inplace=True, axis = 1)

# Add NaN readings
df = df.append(df_borders, sort=False, ignore_index=True)\
    .drop_duplicates(subset=['area', 'Datetime'])

# Generate the full set of readings
df = df.groupby(['area', 'date'])\
    .apply(lambda x : x.set_index('Datetime').resample('H').mean().fillna(0))\
    .reset_index()
df.drop('date', inplace=True, axis = 1)

# Result
print(df)












