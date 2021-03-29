import pandas as pd
import glob
from datetime import datetime

from nilu_ndacc import read_nilu_functions 
from read_nilu_functions import organize_df, o3tocurrent



__MissingData__ = -32768.0
K = 273.15
station = 'Sodankyl'
# station = 'Uccle'

# efile = open("errorfile_" + station + ".txt", "w")

# SensorType = 'SPC-6A'

station = 'Lindenberg'
##read datafiles
allFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/" + station + "/LI080312.csv"))
# allFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_Analysis/Files/NDACC/ftp/ndacc/station/" + station + "/ames/o3sonde/ny17*.csv"))
# ny940502
# ny950423

# metaFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/" + station + "/metadata/*_md.csv"))

list_data = []
list_raw = []

f = 0
sensortype = [''] * len(allFiles)

for filename in (allFiles):

    name = filename.split(".")[-2].split("/")[-1][2:8]
    fname = filename.split(".")[-2].split("/")[-1]
    print(fname)
    ## problematic valentia files
    if (fname == 'va011219') or (fname == 'va040317') or (fname == 'va060208') or (fname == 'va060301') or (fname == 'va100130'): continue
    if (fname == 'le050525') or (fname == 'ny980212'): continue


    metafile = '/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/' + station + '/metadata/' + fname + "_md.csv"
    # metafile = '/home/poyraden/Analysis/Homogenization_Analysis/Files/NDACC/ftp/ndacc/station/' + station + '/ames/o3sonde/metadata/' + fname + "_md.csv"

    date = datetime.strptime(name, '%y%m%d')
    datef = date.strftime('%Y%m%d')

    # neumayer
    # clist =  ['Pressure at observation (hPa)', 'Time after launch (s)', 'Geopotential height (gpm)',
    #                                    'Temperature (C)', 'Relative humidity (%)', 'Temperature inside styrofoam box (C)',
    #                                    'Ozone partial pressure (mPa)', 'Horizontal wind direction (degrees)', 'Horizontal wind speed (m/s)']

    # clist2 = ['ElapTime', 'Press', 'GeopHgt', 'Temp',  'RH', 'PO3', 'DD', 'FF', 'GPSHgt','Lon','Lat','PmpT','OzI','Vpmp','Ipmp']
    clist2 = ['Time after launch (s)', 'Pressure at observation (hPa)', 'Geopotential height (gpm)', 'Temperature (C)',
              'Relative humidity (%)', 'Ozone partial pressure (mPa)', 'DD', 'FF', 'GPSHgt','Lon','Lat','Temperature inside styrofoam box (C)','OzI','Vpmp','Ipmp']

    # dfd = pd.read_csv(filename, header=None, names=clist)
    dfd = pd.read_csv(filename)
    print(list(dfd))

    dfd = dfd[1:]

    for i in list(dfd):
        dfd[i] = dfd[i].astype('float')

    if fname == 'le050219': dfd = dfd[:-2]

    if(len(dfd) < 300): continue
    if len(dfd.columns) < 8: continue
    try:
        dfm = pd.read_csv(metafile, index_col=0, names=['Parameter', 'Value'])
        if (len(dfm)) < 15:
            print('skip this dataset for now, use the mean of everything later')
            continue
    except FileNotFoundError:
        continue

    dfm = dfm.T
    dfm['Date'] = datef


    dfl = pd.DataFrame()

    dfl = organize_df(dfd, dfm)


    if(len(dfl) < 300): continue

    # print(fname, dfl.at[dfl.first_valid_index(),'SensorType'])
    try:
        sensortype[f] = dfl.at[dfl.first_valid_index(),'SensorType']
    except KeyError:
        sensortype[f] = sensortype[f-2]
        dfl['SensorType'] = sensortype[f-2]

    # for some files that the value were written wrong
    if (fname == 'le040317') or (fname == 'le040414') or (fname == 'le041110') or (fname == 'sc920408') \
            or (fname == 'sc991203') or (fname == 'sc050325') or (fname == 'sc050401') or (fname == 'sc051117')\
            or (fname == 'sc051208') or (fname == 'sc051229') :
        dfl['SensorType'] = 'SPC'
    if (fname == 'sc060202'):
        dfl['SensorType'] = 'DMT-Z'

    dfl = o3tocurrent(dfl)

    dfl['Date'] = datef

    # if np.isnan(dfl.at[dfl.first_valid_index(),'I']): print(dfl.at[dfl.first_valid_index(),'SensorType'])
    #
    # rawname = filename.split(".")[-2].split("/")[-1] + "_rawcurrent.csv"
    rawname = filename.split(".")[-2].split("/")[-1] + "_rawcurrent.hdf"
    metaname = filename.split(".")[-2].split("/")[-1] + "_metadata.csv"

    # pname = filename.split(".")[-2].split("s")[0]
    pname = '/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/' + station
    # pname = '/home/poyraden/Analysis/Homogenization_Analysis/Files/NDACC/ftp/ndacc/station/' + station + '/ames/o3sonde/'

    #
    dfl.to_hdf(pname + '/Current/' + rawname, key = 'df')
    dfm.to_csv(pname + '/Metadata/' + metaname)


    list_data.append(dfm)
    list_raw.append(dfl)

    f = f+1

# efile.close()


# dff = pd.concat(list_data,ignore_index=True)
# hdfall = pname + "All_metedata.hdf"
#
# dff.to_hdf(hdfall, key = 'df')
#
# dfr = pd.concat(list_raw,ignore_index=True)
# hdfraw = pname + "Sodankyl_rawdata.hdf"
#
# dfr.to_hdf(hdfraw, key = 'df')

