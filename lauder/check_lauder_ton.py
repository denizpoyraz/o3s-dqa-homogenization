import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime

dfmeta = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/lauder/DQA_nors80/Lauder_Metada_DQA_nors80.csv')
dfmeta['DateTime'] = pd.to_datetime(dfmeta['Date'], format='%Y%m%d')
dfmeta['Date'] = dfmeta['DateTime'].dt.strftime('%Y%m%d')

path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/'

allFiles = sorted(glob.glob(path + "DQA_nors80/*_all*.hdf"))

print(len(allFiles))
# metadata = []
# #
for (filename) in (allFiles):
    # print(filename)
    df = pd.read_hdf(filename)

    df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['Date'] = df['DateTime'].dt.strftime('%Y%m%d')
    datestr = df.at[0,'Date']

    dfm = dfmeta[dfmeta.Date == datestr]
    # dfm = dfm.reset_index()

    i_neg = len(df[df.I < 0])
    i_pos = len(df[df.I > 0])

    # print(filename, i_neg, i_pos,dfm.at[dfm.first_valid_index(),'O3Sonde_10hpa_hom'])

    if i_pos == 0:
        print(filename)
        continue

    if i_neg/i_pos > 0.1:
        print(filename)
        print(i_neg/i_pos, i_neg, i_pos, dfm.at[dfm.first_valid_index(),'O3Sonde_10hpa_hom'])
        # print(filename, i_neg, i_pos, dfm.at[dfm.first_valid_index(), 'O3Sonde_10hpa_hom'])