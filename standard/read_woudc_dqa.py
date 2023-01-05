import csv
import numpy as np
from io import StringIO
# from woudc_extcsv import load, WOUDCExtCSVReaderError
import pandas as pd
import glob
import os
#code to read homogenized woudc files processes by KMI

station_name = 'uccle'
folder = f'/home/poyraden/Analysis/Homogenization_public/Files/{station_name}/WOUDC_nors80/'
# f_write_to_woudc_csv(os.path.join(pathfile, datestr + "_o3sdqa" + file_ext + ".hdf"))

allFiles = sorted(glob.glob(f"{folder}*.csv"))

dfm = pd.DataFrame()
fi = 0

for filename in allFiles:
    print(filename)
    extcsv_to = load(filename)

    # access all tables
    tables = extcsv_to.sections.keys()
    ## first copy the profile data and delete this from the keys to save the metadata
    # watch out that this naming may change from station to station
    profile_keys = extcsv_to.sections['PROFILE'].keys()
    Profile = extcsv_to.sections['PROFILE']['_raw']
    del extcsv_to.sections['PROFILE']

    # print(tables)
    # print(profile_keys)
    # print(Profile)
    msize = len(tables)
    # print(msize)

    if msize == 1: continue

    for i in range(msize):
        dict = list(tables)[i]
        print('dict',dict)
        keys = extcsv_to.sections[dict].keys()
        print('keys', keys)
        ksize = len(keys)
        if ksize == 1:
            test = extcsv_to.sections[dict]['_raw']
            test_df = pd.read_csv(StringIO(test))
            tsize = len(test_df.columns)
            for t in range(tsize):
                cstr = test_df.columns.tolist()
                print('cstr', cstr[t])
                if (len(test_df) > 0):
                    dfm.at[fi, cstr[t]] = test_df.at[test_df.first_valid_index(), cstr[t]]
                if (len(test_df) == 0): continue

        for j in range(1, ksize):
            mstr = dict
            kstr = list(keys)[j]
            if kstr == '_raw': kstr = ""
            astr = mstr + '_' + kstr
            dfm.at[fi, astr] = extcsv_to.sections[dict][list(keys)[j]]

    dfprofile = StringIO(Profile)
    df = pd.read_csv(dfprofile)
    df['Date'] = dfm.at[fi, 'TIMESTAMP_Date']
    df['Station'] = dfm.at[fi, 'DATA_GENERATION_Agency']

    print('df', df[0:10])
    print(dfm)
