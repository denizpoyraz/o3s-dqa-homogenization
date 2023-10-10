import pandas as pd
import glob
from datetime import datetime
from re import search


from nilu_ndacc.read_nilu_functions import organize_lerwick, o3tocurrent, missing_tpump, o3tocurrent_stoich
# from nilu_ndacc.read_nilu_functions import organize_df, o3tocurrent, o3tocurrent_stoich, missing_tpump

K = 273.15
k = 273.15


# filepath = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
filepath = '/home/poyraden/Analysis/Homogenization_public/Files/lerwick/nilu/'
station_name = 'lerwick'

dfmeta = pd.read_csv(filepath + "Metadata/All_metadata_nilu.csv" )

##read datafiles
allFiles = sorted(glob.glob(filepath + "read_out/*.csv"))


list_mdata = []


for filename in (allFiles):
    name = filename.split(".")[-2].split("/")[-1][0:8]
    fname = filename.split(".")[-2].split("/")[-1]
    print(name, fname)

    if (search("md", fname)) or (search("metadata", fname)): continue
    if int(name) < 20040220:continue

    if fname == '20220105':continue

    metafile = filepath + 'read_out/' + name + "_metadata.csv"

    dfd = pd.read_csv(filename)
    dfm = pd.read_csv(metafile)
    # print(list(dfd))

    try:dfd['DateTime'] = pd.to_datetime(dfm.at[0,'date'], format='%Y%m%d')
    except KeyError:
        dfm.at[0, 'date'] = int(fname)
        dfd['DateTime'] = pd.to_datetime(dfm.at[0, 'date'], format='%Y%m%d')


    try:dfd['O3'] = dfd['Ozone partial pressure']
    except KeyError:dfd['O3'] = dfd['PO3']

    # input variables for hom.
    dfd['Tpump'] = dfd['Temperature inside styrofoam box'].astype(float) + k
    dfd['Eta'] = 1
    dfd['TboxK'] = dfd['Tpump']
    dfd['Height'] = dfd['Geopotential height']
    dfd['T'] = dfd['Temperature']
    dfd['U'] = dfd['Relative humidity']
    dfd['Time'] = dfd['Time after launch']
    #
    dfd = dfd.drop(['Temperature inside styrofoam box', 'Geopotential height','Temperature','Relative humidity',
                    'Time after launch'], axis = 1)

    # print(len(dfm.columns), list(dfm))
    msize = len(dfm.columns)
    dfm = dfm.drop(['Unnamed: 0'], axis = 1)
    dfmo = pd.DataFrame()
    dfmo['Pground'] = 9999
    dfmo = organize_lerwick(dfm)
    dfmo['DateTime'] = pd.to_datetime(dfm.at[0,'date'], format='%Y%m%d')

    dfl = o3tocurrent(dfd, dfmo, dfmeta)


    rawname = name + "_rawcurrent.hdf"
    metaname = name + "_metadata.csv"

    dfl = dfl.drop(['SensorType', 'SolutionVolume', 'Cef', 'ibg'], axis=1)


    dfl.to_hdf(filepath + '/Current/' + rawname, key = 'df')
    dfmo.to_csv(filepath + '/Metadata/' + metaname)

#     list_mdata.append(dfmo)
#
#
# dff = pd.concat(list_mdata, ignore_index=True)
# csvall = filepath + "Metadata/All_metadata_nilu.csv"
# #
# dff.to_csv(csvall)

