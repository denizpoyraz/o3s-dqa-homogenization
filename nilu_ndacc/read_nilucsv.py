import pandas as pd
import glob
from datetime import datetime
from re import search


# from nilu_ndacc.read_nilu_functions import organize_df, o3tocurrent, missing_tpump, o3tocurrent_stoich
from nilu_ndacc.read_nilu_functions import organize_df, o3tocurrent, o3tocurrent_stoich, missing_tpump

K = 273.15
k = 273.15


# filepath = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
filepath = '/home/poyraden/Analysis/Homogenization_public/Files/lerwick/nilu/'
station_name = 'lerwick'

# dfmeta = pd.read_csv(filepath + "Metadata/All_metadata_ndacc_ib2.csv" )

##read datafiles
allFiles = sorted(glob.glob(filepath + "read_out/*.csv"))

# print(allFiles)

list_metadata = []

f = 0
sensortype = [''] * len(allFiles)

for filename in (allFiles):
    print('filename', filename)
    name = filename.split(".")[-2].split("/")[-1][2:8]
    fname = filename.split(".")[-2].split("/")[-1]
    print(name, fname)
    # not to read metada files with _md extension
    if (search("md", fname)) or (search("metadata", fname)): continue
    if (fname == 'va060118') | (fname == 'va060301'): continue #one problematic file in sodankyal

    metafile = filepath + 'read_out/' + fname + "_metadata.csv"

    # extract the date from file name
    date = datetime.strptime(name, '%y%m%d')
    datef = date.strftime('%Y%m%d')

    dfd = pd.read_csv(filename)
    # dfd = pd.read_csv(filename)
    # dfd = dfd[1:]

    for i in list(dfd):
        dfd[i] = dfd[i].astype('float')

    if (len(dfd) < 100): continue
    if len(dfd.columns) < 8: continue

    # read the metadata file
    print('metafile', metafile)
    if station_name != 'lerwick':
        try:
            dfm_tmp = pd.read_csv(metafile, index_col=0, names=['Parameter', 'Value'])
            if (len(dfm_tmp)) < 15:
                print('skip this dataset')
                continue
        except FileNotFoundError:
            print('why error ')
            continue

    if station_name == 'lerwick':
        dfm_tmp = pd.read_csv(metafile)
        # if (len(dfm_tmp)) < 15:
        #     print('skip this dataset')
        #     continue



    print(fname)

    if station_name != 'lerwick':
        dfm_tmp = dfm_tmp.T

    dfl = pd.DataFrame()
    dfm = pd.DataFrame()

    # using the data and metadata make a new dataframe from them
    dfl, dfm = organize_df(dfd, dfm_tmp)
    dfm['Date'] = datef
    # print(dfm.at[dfm.first_valid_index(), 'SensorType'])
    #
    # print('dfl', list(dfl))
    # print('dfm', list(dfm))

    if (len(dfl) < 100): continue

    # if datef < '20151217':continue

    print(fname)


    # print(dfm.at[dfm.first_valid_index(), 'SensorType'])

    # for some files that the value were written wrong
    try:
        sensortype[f] = dfm.at[dfm.first_valid_index(), 'SensorType']
        # print('try', sensortype[f])
    except KeyError:
        sensortype[f] = sensortype[f - 2]
        dfm['SensorType'] = sensortype[f - 2]
        print('except', sensortype[f], sensortype[f-2])

    f = f + 1
    #
    #additional part to filter missing pump temperature values,
    # that causes wrong I value calculations
    try: dfl = missing_tpump(dfl)
    #for the cases where interpolation is not possible, because the values are missing from the beginning
    except ValueError:
        dfl = dfl
        print('not possible to interpolate')
        dfl = dfl[dfl.TboxC < 99]
        dfl = dfl.reset_index()
    dfl['TboxK'] = dfl['TboxC'] + k

    #check for missing/wrong O3 values
    dfl = dfl[dfl.O3 > 0]
    dfl = dfl[dfl.O3 < 99]

    dfl = dfl[dfl.Pair > 0]

    if len(dfl)< 100: continue
    # convert the partial pressure to current
    #for scoresbysund transfer functions have been used for ensci 1.0% to spc1.0 after 20151217
    # dfl = o3tocurrent(dfl, dfm, dfmeta)
    # if (datef >= '20151217') & (station_name == 'scoresby'):
    #     dfl = o3tocurrent_stoich(dfl, dfm)

    # set the date
    dfl['Date'] = datef
    dfm['Date'] = datef

    rawname = filename.split(".")[-2].split("/")[-1] + "_rawcurrent.hdf"
    metaname = filename.split(".")[-2].split("/")[-1] + "_metadata.csv"

    # dfl = dfl.drop(['SensorType', 'SolutionVolume', 'Cef', 'ibg'], axis=1)


    dfl.to_hdf(filepath + '/Current/' + rawname, key = 'df')
    dfm.to_csv(filepath + '/Metadata/' + metaname)

    list_metadata.append(dfm)

# save all the metada in one file, either in hdf format or csv format
dff = pd.concat(list_metadata, ignore_index=True)
hdfall = filepath + "Metadata/All_metadata_nilu.hdf"
csvall = filepath + "Metadata/All_metadata_nilu.csv"

dff.to_hdf(hdfall, key = 'df')
dff.to_csv(csvall)

