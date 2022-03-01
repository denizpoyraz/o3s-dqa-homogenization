import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText
from math import log
from datetime import time
from datetime import datetime
from scipy import signal
from scipy.interpolate import interp1d
from re import search

# make a readable column named metada data dfs

k = 273.15


path = "/home/poyraden/Analysis/Homogenization_public/Files/lauder/CSV/"

# dataFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_public/Files/lauder/csv/2012*hdf"))
metadataFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_public/Files/lauder/CSV/*metadata*csv"))

# for (fname,mdname) in zip(dataFiles, metadataFiles):
for mdname in (metadataFiles):

    # print('one',fname)
    print('one', mdname)

    # df = pd.read_hdf(fname)
    dfm = pd.read_csv(mdname)

    outname = mdname.split("_metadata.csv")[0].split('/')[-1]
    # print(outname)
    outname = str(outname) + "_md.csv"

    d = []

    # print(list(df))
    # print('out', list(dfm))

    listm = list(dfm)

    dfmeta = pd.DataFrame()
    # dfmeta = pd.DataFrame(columns=[['Date', 'LaunchTime', 'Phip', 'SondeSerial', 'SondeType', 'SensorResponseType',
    #                                 'OzoneScaling', 'SolutionConcentration', 'GroundPressureSensorCorrection',
    #                                 '10hPaPressureSensorCorrection',
    #                                 'TemperatureSensorCorrection', 'HumiditySensorCorrection',
    #                                 'HumiditySensorCorrection2', 'TOF', 'TOA'
    #                                                                     'NormalizationFactor',
    #                                 'PumpCorrectionCorrelation', 'ExtrapolationTechnique', 'Dobson', 'TLab', 'ULab',
    #                                 'RH_correction', 'iB0', 'iB1', 'iB2']])

    for i in range(len(listm)):



        if (search('Launch', listm[i])) and (search('Date', listm[i])):
            tmp = listm[i]
            # print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'Date'] = dfm.at[0, tmp]

        if (search('Launch', listm[i])) and (search('Time', listm[i])):
            tmp = listm[i]
            dfmeta.at[0,'LaunchTime'] = dfm.at[0, tmp]

        if (search('Flow', listm[i])) and (search('Rate', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'Phip'] = dfm.at[0, tmp]

        if (search('SondeID', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'SondeSerial'] = dfm.at[0, tmp]
            if dfm.at[0, tmp][0] == 'Z': dfmeta.at[0,'SondeType'] = 'DMT-Z'
            if dfm.at[0, tmp][0] == 'z': dfmeta.at[0,'SondeType'] = 'DMT-Z'
            if dfm.at[0, tmp][1] == 'Z': dfmeta.at[0,'SondeType'] = 'DMT-Z'
            if dfm.at[0, tmp][2] == 'z': dfmeta.at[0,'SondeType'] = 'DMT-Z'
            if (dfm.at[0, tmp][0] == 'Z') | (dfm.at[0, tmp][0] == 'z') | (dfm.at[0, tmp][1] == 'Z') | (dfm.at[0, tmp][1] == 'z'):
                dfmeta.at[0, 'Pump_loc'] = 'Z'

            if (dfm.at[0, tmp][1] == 'A') | (dfm.at[0, tmp][0] == '4') | (dfm.at[0, tmp][0] == '5') | (dfm.at[0, tmp][0] == '6'):
                dfmeta.at[0,'SondeType'] = 'SPC'
            if (dfm.at[0, tmp][0:2] == '4A'):dfmeta.at[0, 'Pump_loc'] = '4A'
            if (dfm.at[0, tmp][0:2] == '5A'):dfmeta.at[0, 'Pump_loc'] = '5A'
            if (dfm.at[0, tmp][0:2] == '6A'):dfmeta.at[0, 'Pump_loc'] = '6A'


        if (search('Sensor', listm[i]) and (search('response time', listm[i])) ):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'SensorResponseType'] = dfm.at[0, tmp]

        if (search('Ozone scaling', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'OzoneScaling'] = dfm.at[0, tmp]

        if (search('Solution', listm[i]) and (search('concentration in ', listm[i])) ):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'SolutionConcentration'] = dfm.at[0, tmp] * 10

        if (search('Ground pressure', listm[i]) and (search('sensor correction', listm[i]))):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'GroundPressureSensorCorrection'] = dfm.at[0, tmp]

        if (search('10hPa pressure', listm[i]) and (search('sensor correction', listm[i]))):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'10hPaPressureSensorCorrection'] = dfm.at[0, tmp]

        if (search('Temperature', listm[i]) and (search('sensor correction', listm[i]))):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'TemperatureSensorCorrection'] = dfm.at[0, tmp]

        if (search('Humidity sensor correction', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'HumiditySensorCorrection'] = dfm.at[0, tmp]

        if (search('Humidity2 sensor correction', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'HumiditySensorCorrection2'] = dfm.at[0, tmp]

        if (search('Total ozone', listm[i]) and (search('(TOF)', listm[i]))):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'TOF'] = dfm.at[0, tmp]

        if (search('Total ozone', listm[i]) and (search('(TOA)', listm[i]))):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'TOA'] = dfm.at[0, tmp]

        if (search('normalization factor', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'NormalizationFactor'] = dfm.at[0, tmp]

        if (search('Pump correction file', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'PumpCorrectionFile'] = dfm.at[0, tmp]

        if (search('Pump coefficient pc1', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'PumpcoefficientPC1'] = dfm.at[0, tmp]

        if (search('Pump coefficient pc2', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'PumpcoefficientPC2'] = dfm.at[0, tmp]

        if (search('Pump coefficient pc3', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'PumpcoefficientPC3'] = dfm.at[0, tmp]

        if (search('Pump correction correlation', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'PumpCorrectionCorrelation'] = dfm.at[0, tmp]

        if (search('Extrapolation technique', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'ExtrapolationTechnique'] = dfm.at[0, tmp]

        # time_dobson

        if (search('Raw Dobson', listm[i])):
            d.append(i)
            # tmp = listm[i]
            tmp = listm[d[0]]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'Dobson'] = dfm.at[0, tmp]

        if (search('Temperature during flow rate measurement', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'TLab'] = dfm.at[0, tmp]
            if (dfmeta.at[0, 'TLab'] < 320) & (dfmeta.at[0, 'TLab'] > 50):
                dfmeta.at[0, 'TLab'] = dfmeta.at[0, 'TLab'] - k

        if (search('Relative humidity during flow rate measurement', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'ULab'] = dfm.at[0, tmp]

        if (search('Humidity correction factor to flow rate', listm[i])):
            tmp = listm[i]
            #print(tmp, dfm.at[0, tmp])
            dfmeta.at[0,'RH_correction'] = dfm.at[0, tmp]



        dfmeta.at[0,'iB0'] = dfm.at[0, 'ib0']
        dfmeta.at[0,'iB1'] = dfm.at[0, 'ib1']
        dfmeta.at[0,'iB2'] = dfm.at[0, 'ib2']
        
        dfmeta.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/lauder/metadata/' + outname)





