import pandas as pd
import glob
from datetime import datetime
from re import search


# from nilu_ndacc.read_nilu_functions import organize_df, o3tocurrent, missing_tpump, o3tocurrent_stoich
from nilu_ndacc.read_nilu_functions import organize_df_nya, o3tocurrent_nya, o3tocurrent_stoich, missing_tpump

K = 273.15
k = 273.15


filepath = '/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/'
station_name = 'ny-aalesund'

path_to_file = filepath + '/bad_values.txt'

fw = open(path_to_file, 'w')

# dfmeta = pd.read_csv(filepath + "Metadata/All_metadata_ndacc_ib2.csv" )

##read datafiles
allFiles = sorted(glob.glob(filepath + "CSV/*.csv"))
columnStr1 = ['Pair', 'Time', 'Alt', 'Temp', 'RH','TPump', 'O3', 'WindDir','WindSp']
columnStr2 = ['Time', 'Pair', 'Alt', 'Temp', 'RH', 'O3','WindDir','WindSp', 'GPSAlt','Lon', 'Lat', 'TPump', 'I',
             'VoltBattery', 'PumpI']
# print(allFiles)

dfmeta = pd.read_csv(filepath + 'NY_metadata_corrected.csv')

dfmeta['ib2_mean'] = dfmeta['iB2'].mean()

list_metadata = []

f = 0
sensortype = [''] * len(allFiles)

for filename in (allFiles):
    name = filename.split(".")[-2].split("/")[-1][2:8]
    fname = filename.split(".")[-2].split("/")[-1]
    # not to read metada files with _md extension
    if (search("md", fname)) or (search("metadata", fname)): continue
    # if (fname == 'so980827') | (fname == 'so990708'): continue #one problematic file in sodankyal
    print('filename', filename)

    metafile = filepath + 'CSV/' + fname + "_md.csv"

    # extract the date from file name
    date = datetime.strptime(name, '%y%m%d')
    datef = date.strftime('%Y%m%d')


    if int(datef) <= 20170313:
        # dfd = pd.read_csv(filename, names = columnStr1, header = None, engine="python", sep = '\t')
        dfd = pd.read_csv(filename, names = columnStr1, engine="python",  header = None)
        # dfd = pd.read_csv(filename)
        dfd = dfd[1:]

    if int(datef) > 20170313:
        # print('why not', datef)
        dfd = pd.read_csv(filename, names = columnStr2, header = None, engine="python")
        dfd = dfd[1:]

    for i in list(dfd):
        try:
            dfd[i] = dfd[i].astype('float')
        except ValueError:
            'Pair', 'Time', 'Alt', 'Temp', 'RH', 'TPump', 'O3'
            dfd['Pair'] = dfd['Pair'].astype('float')
            dfd['Time'] = dfd['Time'].astype('float')
            dfd['Alt'] = dfd['Alt'].astype('float')
            dfd['Temp'] = dfd['Temp'].astype('float')
            dfd['RH'] = dfd['RH'].astype('float')
            dfd['TPump'] = dfd['TPump'].astype('float')
            dfd['O3'] = dfd['O3'].astype('float')

            dfd['WindDir'] = 9999
            dfd['WindSp'] = 9999


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
    # print(datef)
    # using the data and metadata make a new dataframe from them
    dfl, dfm = organize_df_nya(dfd, dfm_tmp, datef)
    dfm['Date'] = datef
    # print(dfm.at[dfm.first_valid_index(), 'SensorType'])
    #
    # print('dfl', list(dfl))
    # print('dfm', list(dfm))

    if (len(dfl) < 100): continue

    # print(fname)


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
    # print('out function one', list(dfmeta))
    dfl, dfm = o3tocurrent_nya(dfl, dfm, dfmeta)
    # if (datef >= '20151217') & (station_name == 'scoresby'):
    #     dfl = o3tocurrent_stoich(dfl, dfm)

    # set the date

    dfl['Date'] = datef
    dfm['Date'] = datef

    rawname = filename.split(".")[-2].split("/")[-1] + "_rawcurrent.hdf"
    metaname = filename.split(".")[-2].split("/")[-1] + "_metadata.csv"

    # dfl = dfl.drop(['SensorType', 'SolutionVolume', 'Cef', 'ibg'], axis=1)


    ###check some values
    if len(dfl[dfl['ibg'] > 0.8]) > 0:
        fw.write(datef, 'check ibg')
        fw.write('\n')
    if (len(dfl[dfl.Ical > 30])):
        print(datef +  ' check I')
        fw.write(datef + ' check I')
        fw.write('\n')
    if (len(dfl[dfl.O3 > 30])):
        fw.write(datef + '  check O3')
        fw.write('\n')


    dfl.to_hdf(filepath + '/Current/' + rawname, key = 'df')
    dfm.to_csv(filepath + '/Metadata/' + metaname)

    list_metadata.append(dfm)

# save all the metada in one file, either in hdf format or csv format
# dff = pd.concat(list_metadata, ignore_index=True)
# hdfall = filepath + "Metadata/All_metadata.hdf"
# csvall = filepath + "Metadata/All_metadata.csv"
# #
# dff.to_hdf(hdfall, key = 'df')
# dff.to_csv(csvall)

