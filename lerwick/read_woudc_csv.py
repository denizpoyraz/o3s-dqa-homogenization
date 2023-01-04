import csv
import numpy as np
from io import StringIO
from woudc_extcsv import load, WOUDCExtCSVReaderError
import woudc_extcsv
import pandas as pd
import glob
import re

#example path of where the WOUDC csv files are
path = '/home/poyraden/Analysis/Homogenization_public/Files/lerwick/WOUDC_CSV/original/'
pathn = '/home/poyraden/Analysis/Homogenization_public/Files/lerwick/WOUDC_CSV/'

name_out = 'lerwick_alldata'
name_mout = 'lerwick_metadata'
efile = open("errorfile.txt", "w")


allFiles = sorted(glob.glob(path + "/*.csv"))

# /home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/version2/DQA/20050406_testwoudc.csv


list_data = []
list_mdata = []

list_udata = []
dfm = pd.DataFrame()
fi = 0

for filename in allFiles:
    print('filename', filename)
    print(filename.split(".csv")[0].split("/")[-1])
    date = filename.split(".csv")[0].split("/")[-1]

    file1 = open(filename,'r')
    file2 = open(pathn + str(date) + ".csv",
                 'w')

    sfile = pathn + str(date) + ".csv"
    # reading each line from original
    # text file
    for line in file1.readlines():
        if not (line.startswith('*')) | (line.startswith('#FLIGHT_SUMMARY')) | (line.startswith('IntegratedO3')) :
            # printing those lines
            # print(line)
            # storing only those lines that
            # do not begin with "TextGenerator"
            file2.write(line)

    # close and save the files
    file2.close()
    file1.close()

    # filename2 = filename
    # file1 = open(filename,'r')
    # file2 = open(filename, 'w')
    tmp = filename.split('.')[0][-8:]
    print('tmp', tmp)
    # if tmp == 'MD010613': continue
    # # try except is applied for the cases when there is formatting error: WOUDCExtCSVReaderError
    # # extcsv_to = load(filename)
    extcsv_to = woudc_extcsv.load(sfile)
    tables = extcsv_to.sections.keys()
    profile_keys = extcsv_to.sections['PROFILE'].keys()
    Profile = extcsv_to.sections['PROFILE']['_raw']
    del extcsv_to.sections['PROFILE']

    msize = len(tables)
    # print(msize)

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

    filenamestr = tmp + '_out'
    metastr = tmp + '_metadata'

    print(filename)
    print(metastr)

    df.to_csv(pathn + "/read_out/" + filenamestr + ".csv")
    df.to_hdf(pathn + "/read_out/" + filenamestr + ".hdf", key = 'df')

    dfmt = dfm[fi:fi+1]
    dfmt.to_csv(pathn + "/read_out/" + metastr + ".csv")

    fi = fi + 1

    #
    # dfprofile_uncertainity = StringIO(profile_uncertainity)
    # df_uncer = pd.read_csv(dfprofile_uncertainity)
    # list_udata.append(df_uncer)

    list_data.append(df)
    list_mdata.append(dfmt)

# dfall = pd.concat(list_data, ignore_index=True)
dfmall = pd.concat(list_mdata, ignore_index=True)
# #
# # dfall.to_csv(path + "/DQM/" + name_out + ".csv")
# dfall.to_hdf(path + "/DQM/" + name_out + ".h5", key='df')
# dfmall.to_hdf(path + "/DQM/" + name_mout + ".h5", key='df')
dfmall.to_csv(pathn + "/DQM/" + name_mout + ".csv")

efile.close()

#
# for line in file1.readlines():
#
#     # reading all lines that begin
#     # with "TextGenerator"
#     x = re.findall("^*", line)
#
#     if not x:
#         # printing those lines
#         # print(line)
#
#         # storing only those lines that
#         # do not begin with "TextGenerator"
#         file2.write(line)
#
# # close and save the files
# file1.close()
# file2.close()

# try:
#     extcsv_to = load(filename)
#     # access all tables
#     tables = extcsv_to.sections.keys()
#     ## first copy the profile data and delete this from the keys to save the metadata. For Praha data it is 'PORFILE',
#     # watch out that this naming may change from station to station
#     profile_keys = extcsv_to.sections['PROFILE'].keys()
#     Profile = extcsv_to.sections['PROFILE']['_raw']
#     del extcsv_to.sections['PROFILE']
#     # profile_uncertainity = extcsv_to.sections['PROFILE_UNCERTAINTY']['_raw']
#     # del extcsv_to.sections['PROFILE_UNCERTAINTY']
#
# except WOUDCExtCSVReaderError:
#     print('ERROR')
#     efile.write(filename  + '\n')
#     tables = [0]
