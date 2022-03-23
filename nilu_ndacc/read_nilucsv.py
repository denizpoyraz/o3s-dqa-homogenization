import pandas as pd
import glob
from datetime import datetime
from re import search


from nilu_ndacc.read_nilu_functions import organize_df, o3tocurrent, missing_tpump

K = 273.15
k = 273.15


filepath = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'

##read datafiles
allFiles = sorted(glob.glob(filepath + "Raw/*0603*.hdf"))

# print(allFiles)

list_metadata = []

f = 0
sensortype = [''] * len(allFiles)

for filename in (allFiles):
    # print('filename', filename)
    name = filename.split(".")[-2].split("/")[-1][2:8]
    fname = filename.split(".")[-2].split("/")[-1]
    # not to read metada files with _md extension
    if (search("md", fname)) or (search("metadata", fname)): continue
    # if (fname == 'so980827') | (fname == 'so990708'): continue #one problematic file in sodankyal
    print(fname)

    metafile = filepath + 'Raw/' + fname + "_md.csv"

    # extract the date from file name
    date = datetime.strptime(name, '%y%m%d')
    datef = date.strftime('%Y%m%d')

    dfd = pd.read_hdf(filename)
    # dfd = pd.read_csv(filename)
    # dfd = dfd[1:]

    for i in list(dfd):
        dfd[i] = dfd[i].astype('float')

    if (len(dfd) < 100): continue
    if len(dfd.columns) < 8: continue

    # read the metadata file
    try:
        dfm_tmp = pd.read_csv(metafile, index_col=0, names=['Parameter', 'Value'])
        if (len(dfm_tmp)) < 15:
            print('skip this dataset')
            continue
    except FileNotFoundError:
        continue

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
    dfl = dfl[dfl.O3 <  99]


    if len(dfl)< 100: continue
    # convert the partial pressure to current
    dfl = o3tocurrent(dfl, dfm)
    # set the date
    dfl['Date'] = datef
    dfm['Date'] = datef

    rawname = filename.split(".")[-2].split("/")[-1] + "_rawcurrent.hdf"
    metaname = filename.split(".")[-2].split("/")[-1] + "_metadata.csv"

    # dfl = dfl.drop(['SensorType', 'SolutionVolume', 'Cef', 'ibg'], axis=1)


    dfl.to_hdf(filepath + '/Current/test_' + rawname, key = 'df')
    dfm.to_csv(filepath + '/Metadata/test_' + metaname)

    list_metadata.append(dfm)

# save all the metada in one file, either in hdf format or csv format
dff = pd.concat(list_metadata, ignore_index=True)
hdfall = filepath + "Metadata/All_metadata.hdf"
csvall = filepath + "Metadata/All_metadata.csv"

dff.to_hdf(hdfall, key = 'df')
dff.to_csv(csvall)

