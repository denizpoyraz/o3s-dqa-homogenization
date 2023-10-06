import pandas as pd
import numpy as np
from re import search
import glob
from homogenization_functions import o3tocurrent


kelvin = 273.15

# filepath = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/missing_files/read_out/'
filepath = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/nilu/read_out/'
fileout = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/missing_files/organized/'

allFiles = sorted(glob.glob(filepath + "20201210*.csv"))
mFiles = sorted(glob.glob(filepath + "metadata/*.csv"))

dlist = ['Pair', 'Time', 'Height', 'TboxK', 'TboxC', 'WindDirection', 'WindSpeed',
         'O3', 'T', 'U', 'value_is_NaN', 'SensorType', 'SolutionVolume',
         'Cef', 'ibg', 'ibg_tmp', 'iB2', 'iB0', 'CorP', 'Pground', 'Pcor', 'I', 'Date']


mlist = ['BkgUsed', 'LaunchTime', 'Longitude', 'Latitude', 'SolutionVolume', 'SolutionConcentration',
         'PF', 'iB0', 'iB2', 'DurationSurfaceOzoneExposure', 'SurfaceOzone', 'Pground', 'SondeTotalO3',
         'TotalO3_Col2A', 'TotalO3_Col2B', 'CorrectionFactor', 'TLab', 'ULab', 'GroundEquipment', 'PumpTable',
         'BackgroundCorrection', 'PumpTempLoc', 'SerialECC', 'SensorType', 'InterfaceSerial', 'Date',
         'RadiosondeModel', 'RadiosondeSerial']

for (fname, mname) in zip(allFiles, mFiles):
    print(fname)
    print(mname)

    dft = pd.read_csv(fname)
    dfmt = pd.read_csv(mname)
    # print(list(dft))
    df = pd.DataFrame(columns=dlist)
    dfm = pd.DataFrame(columns=mlist)


    # df['Pair'] = dft['Pair']
    df['Pair'] = dft['Pressure at observation']
    df['Time'] = dft['Time']
    # df['Time'] = dft['Time after launch']
    df['Height'] = dft['Geopotential height']
    df['TboxC'] = dft[ 'Temperature inside styrofoam box']
    df['TboxK'] = df['TboxC'] + kelvin
    df['WindDirection'] = dft['Horizontal wind direction']
    df['WindSpeed'] = dft['Horizontal wind speed']
    df['O3'] = dft['Ozone partial pressure']
    df['T'] = dft['Temperature']
    df['U'] = dft['Relative humidity']

    dfm['Date'] = dfmt['date'].astype(int)
    datet = str(dfmt.at[0,'date'])
    df['Date'] = dfmt.at[0,'date']
    if dfm.at[0, 'Date'] < 20050222:

        dfm['SolutionConcentration'] = dfmt['Concentration of cathode solution (g/l)']
        dfm['PF'] = dfmt['Sensor air flow rate (ozonesonde pump only operating)(s)']
        dfm['iB0'] = dfmt['Background sensor current before cell is exposed to ozone (microamperes)']
        dfm['iB2'] = dfmt['Background sensor current in the end of the pre-flight calibration(microamperes)']
        dfm['DurationSurfaceOzoneExposure'] = dfmt['Time the sonde was run for surface ozone (min)']
        dfm['SurfaceOzone'] = dfmt['Surface ozone measured with the sonde prior to launch(mPa)']
        dfm['TotalO3_Col2A'] = dfmt['Total ozone measured with Dobson/Brewer (daily mean) (COL2A)']
        dfm['TotalO3_Col2B'] = dfmt['Total ozone measured with Dobson/Brewer (best value)(COL2B)']
        dfm['CorrectionFactor'] = dfmt['Correction factor (COL2A/COL1 or COL2B/COL1) (NOT APPLIED TO DATA)']


    clist = list(dfmt)
    for c in clist:
        if search('aunch time', c):
            dfm['LaunchTime'] = dfmt[c]
        if search('ongitude of station', c):
            dfm['Longitude'] = dfmt[c]
        if search('atitude of station', c):
            dfm['Latitude'] = dfmt[c]
        if search('mount of cathode solution', c):
            dfm['SolutionVolume'] = dfmt[c]
        if search('oncentration of cathode solution', c):
            dfm['SolutionConcentration'] = dfmt[c]
        if search('ensor air flow rate', c):
            dfm['PF'] = dfmt[c]
        if search('ackground sensor current before cell', c):
            dfm['iB0'] = dfmt[c]
        if search('ackground sensor current in the end ', c):
            dfm['iB2'] = dfmt[c]
        if search('Time the sonde was run for surface ozone', c):
            dfm['DurationSurfaceOzoneExposure'] = dfmt[c]
        if search('Surface ozone measured with the sonde prior to launch', c):
            dfm['SurfaceOzone'] = dfmt[c]
        if search('COL2A', c):
            dfm['TotalO3_Col2A'] = dfmt[c]
        if search('COL2B', c):
            dfm['TotalO3_Col2B'] = dfmt[c]
        if search('Correction factor', c):
            dfm['CorrectionFactor'] = dfmt[c]
        if search('Temperature in laboratory during sonde flow rate calibration', c):
            dfm['TLab'] = dfmt[c]
        if search('Relative humidity in laboratory', c):
            dfm['ULab'] = dfmt[c]
        if search('Ground equipment', c):
            dfm['GroundEquipment'] = dfmt[c]
        if search('Pump correction table', c):
            dfm['PumpTable'] = dfmt[c]
        if search('Background current correction method', c):
            dfm['BackgroundCorrection'] = dfmt[c]
        if search('Place of box temperature measurement', c):
            dfm['PumpTempLoc'] = dfmt[c]
        if search('Background surface pressure', c):
            dfm['Pground'] = dfmt[c]
        if search('Total ozone from sondeprofile', c):
            dfm['SondeTotalO3'] = dfmt[c]
        if search('Serial number of ECC', c):
            dfm['SerialECC'] = dfmt[c]
        if search('Serial number of interface card', c):
            dfm['InterfaceSerial'] = dfmt[c]
        if search('Serial number of RS-80', c):
            dfm['RadiosondeSerial'] = dfmt[c]


    if datet == '20210826':dfm['SerialECC'] = '6A36437'
    print(datet, dfm.at[dfm.first_valid_index(), 'SerialECC'])

    if (dfm.at[dfm.first_valid_index(), 'SerialECC'][0] == "4"): dfm.at[0, 'SensorType'] = 'SPC'
    if (dfm.at[dfm.first_valid_index(), 'SerialECC'][0] == "5"): dfm.at[0, 'SensorType'] = 'SPC'
    if (dfm.at[dfm.first_valid_index(), 'SerialECC'][0] == "6"): dfm.at[0, 'SensorType'] = 'SPC'
    if (dfm.at[dfm.first_valid_index(), 'SerialECC'][0] == "z") | \
            (dfm.at[dfm.first_valid_index(), 'SerialECC'][0] == "Z"): dfm.at[0, 'SensorType'] = 'DMT-Z'
    if (search('z', dfm.at[dfm.first_valid_index(), 'SerialECC'])) or (search('Z', dfm.at[dfm.first_valid_index(), 'SerialECC'])):
        dfm.at[0, 'SensorType'] = 'DMT-Z'
    print(dfm.at[0, 'SerialECC'], dfm.at[0, 'SensorType'])
    df['Pground'] = dfm.at[dfm.first_valid_index(), 'Pground']
    #now convert O3 to I
    try:
        df = o3tocurrent(df, dfm)  # byault uses ib2, check if another ib is used!
    except (ValueError, KeyError):
        print('BAD File, check FILE')

    dfm.to_csv(fileout + datet + "_metadata.csv")
    df.to_csv(fileout + datet + ".csv")
    df.to_hdf(fileout + datet + ".hdf", key='df')
