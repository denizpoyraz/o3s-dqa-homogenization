import csv
import numpy as np
from io import StringIO
from woudc_extcsv import load, WOUDCExtCSVReaderError
import pandas as pd
import glob

#example path of where the WOUDC csv files are
path = '/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/version2/DQA/'

efile = open("errorfile.txt", "w")


allFiles = sorted(glob.glob(path + "*06*testwoudc.csv"))

# /home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/version2/DQA/20050406_testwoudc.csv


list_data = []
list_udata = []
dfm = pd.DataFrame()
fi = 0

for filename in allFiles:
    print(filename)
    # try except is applied for the cases when there is formatting error: WOUDCExtCSVReaderError
    extcsv_to = load(filename)

    try:
        extcsv_to = load(filename)
        # access all tables
        tables = extcsv_to.sections.keys()
        ## first copy the profile data and delete this from the keys to save the metadata. For Praha data it is 'PORFILE',
        # watch out that this naming may change from station to station
        profile_keys = extcsv_to.sections['PROFILE'].keys()
        Profile = extcsv_to.sections['PROFILE']['_raw']
        del extcsv_to.sections['PROFILE']
        # profile_uncertainity = extcsv_to.sections['PROFILE_UNCERTAINTY']['_raw']
        # del extcsv_to.sections['PROFILE_UNCERTAINTY']

    except WOUDCExtCSVReaderError:
        print('error')
        efile.write(filename  + '\n')
        tables = [0]


    msize = len(tables)
    print(msize)

    if msize == 1: continue

    for i in range(msize):
        dict = list(tables)[i]
        # print('dict',dict)
        keys = extcsv_to.sections[dict].keys()
        # print('keys', keys)
        ksize = len(keys)
        if ksize == 1:
            test = extcsv_to.sections[dict]['_raw']
            test_df = pd.read_csv(StringIO(test))
            tsize = len(test_df.columns)
            for t in range(tsize):
                cstr = test_df.columns.tolist()
                if(len(test_df) > 0):
                    dfm.at[fi, cstr[t]] = test_df.at[test_df.first_valid_index(),cstr[t]]
                if(len(test_df) == 0): continue

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
    list_data.append(df)

    filenamestr = filename.split('.csv')[0][-8:] + '_out'
    metastr = filename.split('.csv')[0][-8:] + '_metadata'

    df.to_csv(path + "out/" + filenamestr + ".csv")
    df.to_hdf(path + "out/" + filenamestr + ".hdf", key = 'df')

    dfmt = dfm[fi:fi+1]
    dfmt.to_csv(path + "out/" + metastr + ".csv")

    fi = fi + 1
    #
    # dfprofile_uncertainity = StringIO(profile_uncertainity)
    # df_uncer = pd.read_csv(dfprofile_uncertainity)
    # list_udata.append(df_uncer)

efile.close()



