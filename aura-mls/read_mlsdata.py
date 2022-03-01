import pandas as pd
from datetime import time
from datetime import datetime
import numpy as np
import re
import glob
import math
from math import log

# First Code of MLS analysis
# read the MLS data and write it to a csv file

# path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/'


# dfmeta = pd.read_csv(path + '/Metadata/All_metadata.csv')
dfmeta = pd.read_csv(path + '/Madrid_Metadata.csv')
dfmeta = pd.read_csv(path + 'Madrid_Metadata.csv')

# dfmeta = pd.read_csv(path + 'metadata/Lauder_MetadaAll.csv')



# dfmeta['DateTime'] = dfmeta['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
# dfmeta['Date'] = dfmeta['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
# dfmeta['Date'] = dfmeta["DateTime"].dt.strftime('%Y%m%d')

dfmeta['Date'] = dfmeta['DateTime'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
# dfmeta = dfm = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/uccle/Raw_upd/All_metadata.csv')
# dfmeta = dfmeta.drop([869,925])
# dfmeta = dfmeta.reset_index()

# print(dfmeta.Datenf.min(), dfmeta.Datenf.max())


# name = 'AURA_MLSData_MatchedUccle_DQA_v05'
name = 'AURA_MLSData_MatchedMadrid_DQA_v04'

# fname = 'aura_mls_l2gpovp_o3_v05_uccle.txt'
# fname = 'aura_mls_l2gpovp_o3_v04_lauder.txt'
fname = 'aura_mls_l2gpovp_o3_v04_madrid.barajas.txt'


file = open(path + fname, "r")
file.readline()
file.readline()
Ref = file.readline().split(':')[1]
RefPres = [0] * 55
for ir in range(55):
    RefPres[ir] = float(Ref.split()[ir])

Pressurestr = [''] * 55;
PressurePrestr = [''] * 55

for ip in range(55):
    Pressurestr[ip] = 'Pressure_' + str(ip + 1)
    PressurePrestr[ip] = 'PressurePrecision_' + str(ip + 1)

columnString = "Datetime MJD2000 Year DOY sec Lat Lon Dis SZA QFlag Conv"
columnStr = columnString.split(" ")

# columnStr
columnStr = columnStr + Pressurestr + PressurePrestr

df = pd.read_csv(file, sep="\s *", engine="python", skiprows=18, header=None, names=columnStr)

for i in range(55):
    df[Pressurestr[i]] = df[Pressurestr[i]] * RefPres[i] * 100000
    df[PressurePrestr[i]] = df[PressurePrestr[i]] * RefPres[i] * 100000

# df.tmp = df.Datetime.str.split("T", n = 1, expand = True)
df['Date'] = df.Datetime.str.split("T", n=1, expand=True)[0]
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
df['Date'] = df['Date'].dt.strftime('%Y%m%d')

df['timetmp1'] = pd.to_timedelta(df["sec"], unit='s')
df['timetmp2'] = df['timetmp1'].astype('timedelta64[s]')
df['Time1'] = pd.to_datetime(df['timetmp2'])
df['Time2'] = [x.time() for x in df['Time1']]
df['DifLat'] = abs(50.80 - df['Lat'])
df['DifLon'] = abs(4.350 - df['Lon'])
df['Time'] = pd.to_timedelta(df["sec"], unit='s')

# df['Timenf'] = df['Time'].apply(lambda x: time.x())

df['Timenf'] = pd.to_datetime(df['Time'] + pd.Timestamp(0))
df['Timenf'] = [j.time() for j in df['Timenf']]


# now read metadata file and take the date, and only keep the mls dates that are in the metadata
# print(dfmeta.Datenf.min(), dfmeta.Datenf.max())
print(dfmeta.Date.min(), dfmeta.Date.max())
dfmeta.Datestr = dfmeta.Date.astype('int')
dfmeta.Datestr = dfmeta.Datestr.astype('str')

# dfmeta.Datestr = dfmeta.Date.astype('str')
dates_station = dfmeta.Datestr.tolist()
print('dates_station', dates_station)
print(df['Date'].dtypes)
print(df['Date'][0:2])
#skim mls data
df = df[df['Date'].isin(dates_station)]
dates_match = df.drop_duplicates(['Date']).Date.tolist()
print(dates_match)

# print(list(df))
#
# print(df[['sec','Date','Time','Timenf']][0:10])
# print(df.dtypes)

distance_list_night = []
distance_list_noon = []
time_list_night = []
time_list_noon = []

print(len(dates_match))

list_data = []

for im in range(len(dates_match)):
    # print(dates_match[im])
    dftmp = df[df['Date'] == dates_match[im]]
    df_night = dftmp[(dftmp['Timenf'] > time(0, 0, 0)) & (dftmp['Timenf'] < time(6, 0, 0))]
    df_noon = dftmp[(dftmp['Timenf'] > time(6, 0, 0))]
    distance = dftmp.Dis.tolist()
    distance_night = df_night.Dis.tolist()
    distance_noon = df_noon.Dis.tolist()
    # print(distance_night)
    # print(distance_noon) 

    if (len(distance_noon) == 0): distance_noon = distance
    if (len(distance_night) == 0): distance_night = distance

    if (im < 5):
        print(im, 'all', distance, dftmp['Timenf'])
        print(im, 'night', distance_night)
        print(im, 'noon', distance_noon)
    min_night = min(distance_night)
    min_noon = min(distance_noon)

    distance_list_night.append(min_night)
    distance_list_noon.append(min_noon)

    dfskim = df[(df['Date'] == dates_match[im]) & ((df['Dis'] == min_night) | (df['Dis'] == min_noon))]
    list_data.append(dfskim)
# #
dffinal = pd.concat(list_data, ignore_index=True)
#
# dffinal.to_csv(path +  name + ".csv")
# dffinal.to_hdf(path + name + ".h5", key='df', mode='w')
