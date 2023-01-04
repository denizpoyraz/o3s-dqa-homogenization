# code to organize lerwicj data-files.
# use woudc files until 2004 and after nilu files
# for the metadata use nilu main data, for the missing ib2 and pf use median
# for TLab, PLab, ULab calculate climatological means

K = 273.15
k = 273.15


import pandas as pd
import glob
from datetime import datetime
from re import search
from functions.homogenization_functions import assign_missing_ptupf, assign_missing_ptupf_byvalue, \
    missing_station_values,missing_station_values_afterdate
from nilu_ndacc.read_nilu_functions import organize_lerwick, o3tocurrent

filepath = '/home/poyraden/Analysis/Homogenization_public/Files/lerwick/'
station_name = 'lerwick'

dfm_main = pd.read_csv(filepath + "nilu/Metadata/All_metadata_nilu.csv")
dfm_main['Date'] = dfm_main['DateTime'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
dfm_main['Date'] = dfm_main['Date'].dt.strftime('%Y%m%d')
pfmean = dfm_main[dfm_main.Date >= '20040219']['PF'].median()
ib2mean = dfm_main[dfm_main.Date >= '20040219']['iB2'].median()
print(pfmean, ib2mean)

wfiles = sorted(glob.glob(filepath + "/WOUDC_CSV/read_out/*_out.csv"))
nfiles = sorted(glob.glob(filepath + "/nilu/read_out/*.csv"))

for filename in (wfiles):
    name = filename.split(".")[-2].split("/")[-1][0:8]
    fname = filename.split(".")[-2].split("/")[-1]
    print(filename)
    print(name, type(name), fname)

    if int(name) > 20040219:continue

    dfm = pd.DataFrame()
    dfm.at[0,'SensorType'] = 'SPC'
    dfm.at[0,'iB2'] = ib2mean
    dfm.at[0,'PF'] = pfmean
    dfm.at[0, 'SolutionVolume'] = 3.0

    df = pd.read_csv(filename)
    df['TboxK'] = df['SampleTemperature'] + K
    df['Pair'] = df['Pressure']
    df['O3'] = df['O3PartialPressure']
    dfl = o3tocurrent(df, dfm, dfm_main)
    print(list(dfl))

    #now organize the maning of df and do the same for nilu files
    # and write them all in one df and save as metadata and current df files.



