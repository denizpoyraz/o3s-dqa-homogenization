import pandas as pd
import glob
from datetime import datetime
from re import search
import numpy as np
import matplotlib.pyplot as plt

k = 273.15

#organize data and metadata files, make them available for homogenization and also convert them to current

path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'

allFiles = sorted(glob.glob(path + 'Current/*rawcurrent.hdf'))


metadata = []

for (filename) in (allFiles):
    df = pd.read_hdf(filename)
    df = df.reset_index()


    # if df.loc[1, 'Date'] <= '20070104': continue

    print(filename )


    if (df.loc[1,'Date'] >= '20070104') :
        df['RadiosondeModel'] = 9999
        df['iB1'] = 9999
        df['RadiosondeSerial'] =9999

    dft = df.loc[0:0,['Pground', 'TLab', 'ULab', 'iB0', 'iB1', 'iB2', 'PF','SerialECC', 'SensorType',
                      'LaunchTime','SondeTotalO3','RadiosondeModel', 'RadiosondeSerial','PumpTempLoc','Date',
                      'SolutionVolume', 'SolutionConcentration']]
#
    metadata.append(dft)
#
name_out = 'Scoresby_MetadaAll'
dfall = pd.concat(metadata, ignore_index=True)

dfall.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/scoresby/metadata/' + name_out + ".csv")

dfmeta = pd.read_csv(path + 'metadata/Scoresby_MetadaAll.csv')

#now check if the current is calculated correctly assuming Vaisala software is used for current o partial pressure
# calculation-> checked in jupyter it is correct

#
# for (filename) in (allFiles):
#     df = pd.read_hdf(filename)
#     df = df.reset_index()
#
#
#     # if df.loc[1, 'Date'] <= '20070104': continue
#
#     print(filename )