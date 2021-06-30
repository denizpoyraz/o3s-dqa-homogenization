import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime

## need to run this part once, to make df of all the data
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# allFiles = sorted(glob.glob(path + "DQA_upd/*_o3sdqa_rs80_bkgupd.hdf"))
#
# dfa = pd.DataFrame()
# alldata = []
#
# for (filename) in (allFiles):
#     print(filename)
#     df = pd.read_hdf(filename)
#
#     alldata.append(df)
#
# name_out = 'Madrid_AllData_DQA_final'
# dfall = pd.concat(alldata, ignore_index=True)
#
# dfall.to_hdf("/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_upd/Madrid_AllData_DQA_final.hdf", key = 'df')

dfmain = pd.read_hdf("/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_upd/Madrid_AllData_DQA_final.hdf")

print(list(dfmain))

df = dfmain[['Date', 'Pressure', 'SampleTemperature']]
df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

dft = {}
dfmean = {}

for i in range(1,13):
    dft[i-1] = df[df.DateTime.dt.month == i]
    dfmean[i-1] = dft[i-1].groupby(['Pressure']).mean()

    print(i, len(dft[i-1]))