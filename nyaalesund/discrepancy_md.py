import pandas as pd
import glob
from datetime import datetime
from re import search
import numpy as np


dfs = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_8812.csv')

dfa = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_All.csv')

print(list(dfs))
print(list(dfa))



dfs['Date'] = pd.to_datetime(dfs['Date'], format='%Y-%m-%d')
dfs['Date'] = dfs['Date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
dfa['Date'] = pd.to_datetime(dfa['Date'], format='%Y%m%d')

dfa['Date'] = dfa['Date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))


df1 = dfs[['Date','ibs','Air flow s']].copy()
df1['Airflows'] = df1['Air flow s']

df2 = dfa[['Date','iB0','iB2','PF']]

l1 = df1['Date'].tolist()
l2 = df2['Date'].tolist()

print('len df1', len(df1))
print('len df2', len(df2))

common_dates12 = list(set(l1).intersection(set(l2)))
common_dates21 = list(set(l2).intersection(set(l1)))

print(len(common_dates12), len(common_dates21), common_dates12[0:3])

df1 = df1[df1['Date'].isin(common_dates12)]
df2 = df2[df2['Date'].isin(common_dates12)]

df1 = df1.sort_values('Date')
df2 = df2.sort_values('Date')

df1 = df1[df1.Date > '20030901']
df2 = df2[df2.Date > '20030901']

df1 = df1.reset_index()
df2 = df2.reset_index()


print('after')
print('len df1', len(df1))
print('len df2', len(df2))


dates = []
for j in range(len(df1)-1):
    if df1.loc[j,'Date'] == df1.loc[j+1, 'Date']:
        # print(j,df1.loc[j,'Date'], df1.loc[j+1,'Date'] )
        dates.append(df1.loc[j,'Date'])

print(dates)
dates.append('20090115')

df1c = df1[~df1['Date'].isin(dates)]
df2c = df2[~df2['Date'].isin(dates)]

df1c = df1c.reset_index()
df2c = df2c.reset_index()

df1c['Airflows'] = df1c['Airflows'].round(2)

print('len df1c', len(df1c))
print('len df2c', len(df2c))

df2c['ibs'] = df1c['ibs']
df2c['Airflows'] = df1c['Airflows']

df2c = df2c.reindex(columns=['Date', 'iB0', 'iB2','ibs','PF', 'Airflows'])
df2c['ibs'] = df2c['ibs'].astype(float)

df2c['dif_PF'] = df2c['PF'] - df2c['Airflows']
df2c['iB0-ibs'] = df2c['iB0'] - df2c['ibs']
df2c['iB2-ibs'] = df2c['iB2'] - df2c['ibs']

df2c[df2c['iB0-ibs'] == 0].to_excel('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_ib0ibs.xlsx')
df2c[df2c['iB2-ibs'] == 0].to_excel('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_ib2ibs.xlsx')
df2c[(df2c['iB0-ibs'] != 0) | (df2c['iB2-ibs'] != 0)].to_excel('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_ib_discrepancy.xlsx')
df2c[df2c['dif_PF'] != 0].to_excel('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_pf_discrepancy.xlsx')

df2c[df2c['iB0-ibs'] == 0].to_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_ib0ibs.csv')
df2c[df2c['iB2-ibs'] == 0].to_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_ib2ibs.csv')
df2c[(df2c['iB0-ibs'] != 0) | (df2c['iB2-ibs'] != 0)].to_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_ib_discrepancy.csv')
df2c[df2c['dif_PF'] != 0].to_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_pf_discrepancy.csv')