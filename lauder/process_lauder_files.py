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

path = "/home/poyraden/Analysis/Homogenization_public/Files/lauder/csv/"

dataFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_public/Files/lauder/csv/2000*hdf"))
metadataFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_public/Files/lauder/csv/2000*csv"))

for (fname,mdname) in zip(dataFiles, metadataFiles):
    print('one',fname)
    print('one', mdname)

    df = pd.read_hdf(fname)
    dfm = pd.read_csv(mdname)


    # print(list(df))
    print('out', list(dfm))

    listm = list(dfm)

    for i in range(len(listm)):

        dfmeta = pd.DataFrame()

        if (search('Launch', listm[i])) and (search('Date', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['Date'] = dfm.at[0, tmp]

        if (search('Launch', listm[i])) and (search('Time', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['LaunchTime'] = dfm.at[0, tmp]
            print('TEST', dfm.at[0, tmp][0:2])

        if (search('Flow', listm[i])) and (search('Rate', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['Phip'] = dfm.at[0, tmp]

        if (search('SondeID', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['SondeSerial'] = dfm.at[0, tmp]
            if dfm.at[0, tmp][0] == 'Z': dfmeta['SondeType'] = 'DMT-Z'
            if (dfm.at[0, tmp][1] == 'A') | (dfm.at[0, tmp][0] == '4') | (dfm.at[0, tmp][0] == '5') | (dfm.at[0, tmp][0] == '6'):
                dfmeta['SondeType'] = 'SPC'

        if (search('Sensor', listm[i]) and (search('response time', listm[i])) ):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['SensorResponseType'] = dfm.at[0, tmp]

        if (search('Ozone scaling', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['OzoneScaling'] = dfm.at[0, tmp]

        if (search('Solution', listm[i]) and (search('concentration in ', listm[i])) ):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['SolutionConcentration'] = dfm.at[0, tmp] * 10

        if (search('Ground pressure', listm[i]) and (search('sensor correction', listm[i]))):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['GroundPressureSensorCorrection'] = dfm.at[0, tmp]

        if (search('10hPa pressure', listm[i]) and (search('sensor correction', listm[i]))):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['10hPaPressureSensorCorrection'] = dfm.at[0, tmp]

        if (search('Temperature', listm[i]) and (search('sensor correction', listm[i]))):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['TemperatureSensorCorrection'] = dfm.at[0, tmp]

        if (search('Humidity sensor correction', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['HumiditySensorCorrection'] = dfm.at[0, tmp]

        if (search('Humidity2 sensor correction', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['HumiditySensorCorrection2'] = dfm.at[0, tmp]

        if (search('Total ozone', listm[i]) and (search('(TOF)', listm[i]))):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['TOF'] = dfm.at[0, tmp]

        if (search('Total ozone', listm[i]) and (search('(TOA)', listm[i]))):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['TOA'] = dfm.at[0, tmp]

        if (search('normalization factor', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['NormalizationFactor'] = dfm.at[0, tmp]

        if (search('Pump correction file', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['PumpCorrectionFile'] = dfm.at[0, tmp]

        if (search('Pump coefficient pc1', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['PumpcoefficientPC1'] = dfm.at[0, tmp]

        if (search('Pump coefficient pc2', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['PumpcoefficientPC2'] = dfm.at[0, tmp]

        if (search('Pump coefficient pc3', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['PumpcoefficientPC3'] = dfm.at[0, tmp]

        if (search('Pump correction correlation', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['PumpCorrectionCorrelation'] = dfm.at[0, tmp]

        if (search('Extrapolation technique', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['ExtrapolationTechnique'] = dfm.at[0, tmp]

        time_dobson
        if (search('Raw Dobson', listm[i])):
            tmp = listm[i]
            print(tmp, dfm.at[0, tmp])
            dfmeta['Dobson'] = dfm.at[0, tmp]

        dfmeta['iB0'] = dfm.at[0, 'ib0']
        dfmeta['iB1'] = dfm.at[0, 'ib1']
        dfmeta['iB2'] = dfm.at[0, 'ib2']



