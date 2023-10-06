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

    # if (msize != 23) & (msize != 58) & (msize != 63) & (msize != 55):
    #     print('check md', msize, filename)
##63
#['Unnamed: 0', 'date', 'DateTime', 'Number of levels', 'Launch time (Decimal UT hours from 0 hours on day given by DATE)',
# 'East Longitude of station (decimal degrees)', 'Latitude of station (decimal degrees)', 'Wind speed at ground at launch (m/s)', '
# Temperature at ground at launch (C)', 'Free lift for rubber balloon (g)', 'Dummy weight for plastic balloon (g)',
# 'Balloon volume for plastic balloon (m^3)', 'Balloon weight for rubber balloon (g)', 'Interface parameter U1',
# 'Interface parameter U2', 'Interface parameter R1', 'Interface parameter R2', 'Interface parameter R3',
# 'Interface parameter K0', 'Interface parameter K1', 'Interface parameter K2', 'Amount of cathode solution (cm3)',
# 'Concentration of cathode solution (g/l)', 'Sensor air flow rate (calibrator and ozonesonde pumps operating) (sec/100cm^3)',
# 'Sensor air flow rate (ozonesonde pump only operating) (sec/100cm^3)',
# 'Background sensor current before cell is exposed to ozone (microamperes)',
# 'Background sensor current in the end of the pre-flight calibration (microamperes',
# 'Time the sonde was run for surface ozone (min)', 'Surface ozone measured with the sonde prior to launch (mPa)',
# 'Background surface pressure (hPa)', 'Pressure correction at ground', 'Temperature correction at ground',
# 'Humidity correction at ground', 'Total ozone from sondeprofile (COL1)',
# 'Total ozone measured with Dobson/Brewer (daily mean) (COL2A)',
# 'Total ozone measured with Dobson/Brewer (best value) (COL2B)', 'Correction factor (COL2A/COL1 or COL2B/COL1) (NOT APPLIED TO DATA)',
# 'Temperature in laboratory during sonde flow rate calibration', 'Relative humidity in laboratory during sonde flow rate calibration',
# 'Temperature at sonde inlet tube prior to launch (C)', 'Temperature at sonde pump prior to launch', 'Reserved', 'Interface parameter Iref_0c',
# 'Interface parameter Iref_lin', 'Interface parameter Iref_quad', 'Interface parameter Rntc_25oC', 'Ground equipment', 'Pump correction table',
# 'Background current correction method', 'Vertical averaging/smoothing method', 'Place of box temperature measurement', 'Name of raw data file',
# 'Lifting gas', 'Balloon material (RUBBER or PLASTIC)', 'Balloon brand (e.g. TOTEX, RAVEN)', 'Balloon type (e.g. TX1200, CL0019)',
# 'Reason for discontinuation', 'Weather condition at launch', 'Balloon pretreatment', 'Serial number of ECC',
# 'Serial number of interface card', 'Serial number of sonde', 'Ozone sensor type']




#len 58
# ['Unnamed: 0', 'date', 'DateTime', 'Number of levels', 'Launch time (Decimal UT hours from 0 hours on day given by DATE)',
# 'East Longitude of station (decimal degrees)', 'Latitude of station (decimal degrees)', 'Wind speed at ground at launch (m/s)',
# 'Temperature at ground at launch (C)', 'Free lift for rubber balloon (g)', 'Dummy weight for plastic balloon (g)',
# 'Balloon volume for plastic balloon (m^3)', 'Balloon weight for rubber balloon (g)', 'Interface parameter U1',
# 'Interface parameter U2', 'Interface parameter R1', 'Interface parameter R2', 'Interface parameter R3',
# 'Interface parameter K0', 'Interface parameter K1', 'Interface parameter K2', 'Amount of cathode solution (cm3)',
# 'Concentration of cathode solution (g/l)', 'Sensor air flow rate (calibrator and ozonesonde pumps operating) (sec/100cm^3)',
# 'Sensor air flow rate (ozonesonde pump only operating) (sec/100cm^3)',
# 'Background sensor current before cell is exposed to ozone (microamperes)',
# 'Background sensor current in the end of the pre-flight calibration (microamperes',
# 'Time the sonde was run for surface ozone (min)', 'Surface ozone measured with the sonde prior to launch (mPa)',
# 'Background surface pressure (hPa)', 'Pressure correction at ground', 'Temperature correction at ground',
# 'Humidity correction at ground', 'Total ozone from sondeprofile (COL1)',
# 'Total ozone measured with Dobson/Brewer (daily mean) (COL2A)', 'Total ozone measured with Dobson/Brewer (best value) (COL2B)',
# 'Correction factor (COL2A/COL1 or COL2B/COL1) (NOT APPLIED TO DATA)',
# 'Temperature in laboratory during sonde flow rate calibration',
# 'Relative humidity in laboratory during sonde flow rate calibration',
# 'Temperature at sonde inlet tube prior to launch (C)',
# 'Temperature at sonde pump prior to launch', 'Reserved', 'Ground equipment', 'Pump correction table',
# 'Background current correction method', 'Vertical averaging/smoothing method', 'Place of box temperature measurement',
# 'Name of raw data file', 'Lifting gas', 'Balloon material (RUBBER or PLASTIC)', 'Balloon brand (e.g. TOTEX, RAVEN)',
# 'Balloon type (e.g. TX1200, CL0019)', 'Reason for discontinuation', 'Weather condition at launch', 'Balloon pretreatment',
# 'Serial number of ECC', 'Serial number of interface card', 'Serial number of sonde']

##23
# ['Unnamed: 0', 'date', 'DateTime', 'Number of pressure levels', 'Launch time (UT hours from 0 hours on day given by DATE)',
# 'East Longitude of station (degrees)', 'Latitude of station', 'Wind speed at ground at launch (m/s)',
# 'Temperature at ground at launch (C)', 'Free lift for rubber balloon (g)', 'Dummy weight for plastic balloon  (g)',
# 'Balloon volume for plastic balloon  (m^3)', 'Balloon weight for rubber balloon (g)', 'Lifting gas',
# 'Balloon material (RUBBER or PLASTIC)', 'Balloon brand (e.g. TOTEX, RAVEN)', 'Balloon type, (e.g. TX1200, CL0019)', '
# Reason for discontinuation', 'Weather condition at launch', 'Balloon pretreatment', 'Serial number of ECC',
# 'Serial number of interface card', 'Serial number of RS-80']
