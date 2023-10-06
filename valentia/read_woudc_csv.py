import csv
import numpy as np
from io import StringIO
from woudc_extcsv import load, WOUDCExtCSVReaderError
import pandas as pd
import glob
import woudc_extcsv

#example path of where the WOUDC csv files are
# path = '/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/version2/DQA/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/CSV/'
path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/CSV/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/WOUDC_nors80/'

name_out = 'valentia_alldata_till2022'
name_mout = 'valentia_metadata_till2022'
efile = open("errorfile.txt", "w")


allFiles = sorted(glob.glob(path + "/*.csv"))

# /home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/version2/DQA/20050406_testwoudc.csv


list_data = []
list_mdata = []

list_udata = []
dfm = pd.DataFrame()
fi = 0

for filename in allFiles:
    print(filename)
    tmp = filename.split('.')[0][-8:]
    if tmp == 'MD010613': continue
    # try except is applied for the cases when there is formatting error: WOUDCExtCSVReaderError
    # extcsv_to = load(filename)

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
        print('one')

    except woudc_extcsv.WOUDCExtCSVReaderError:
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
        # print('len(keys))', len(keys))
        if ksize == 1:
            test = extcsv_to.sections[dict]['_raw']
            test_df = pd.read_csv(StringIO(test))
            tsize = len(test_df.columns)
            # print('tsize', tsize)
            for t in range(tsize):
                cstr = test_df.columns.tolist()
                # print('t', t, cstr)
                if(len(test_df) > 0):
                    dfm.at[fi, cstr[t]] = test_df.at[test_df.first_valid_index(),cstr[t]]
                if(len(test_df) == 0): continue

        for j in range(1, ksize):
            mstr = dict
            kstr = list(keys)[j]
            if kstr == '_raw': kstr = ""
            astr = mstr + '_' + kstr
            # print('j', j, astr)
            dfm.at[fi, astr] = extcsv_to.sections[dict][list(keys)[j]]

    dfprofile = StringIO(Profile)
    df = pd.read_csv(dfprofile)
    df['Date'] = dfm.at[fi, 'TIMESTAMP_Date']
    df['Station'] = dfm.at[fi, 'DATA_GENERATION_Agency']

    filenamestr = tmp + '_out'
    metastr = tmp + '_metadata'

    # print(filename)
    # print(metastr)

    # print('two')
    df.to_csv(path + "/read_out/" + filenamestr + ".csv")
    df.to_hdf(path + "/read_out/" + filenamestr + ".hdf", key = 'df')
    # print('three')
    dfmt = dfm[fi:fi+1]
    dfmt.to_csv(path + "/read_out/" + metastr + ".csv")

    fi = fi + 1

    #
    # dfprofile_uncertainity = StringIO(profile_uncertainity)
    # df_uncer = pd.read_csv(dfprofile_uncertainity)
    # list_udata.append(df_uncer)

    list_data.append(df)
    list_mdata.append(dfm)
    # print('four')

dfall = pd.concat(list_data, ignore_index=True)
dfmall = pd.concat(list_mdata, ignore_index=True)
# #
dfall.to_csv(path + "/DQM/" + name_out + ".csv")
# dfall.to_hdf(path + "/DQM/" + name_out + ".h5", key='df')
# dfmall.to_hdf(path + "/DQM/" + name_mout + ".h5", key='df')
dfmall.to_csv(path + "/DQM/" + name_mout + ".csv")

efile.close()



