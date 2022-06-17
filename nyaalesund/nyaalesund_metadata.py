import pandas as pd
import glob
from datetime import datetime
from re import search
import numpy as np


dex = pd.ExcelFile('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/'
                   '1988-2012_nya_o3_parameter_list_ib.xlsx')

names = np.asarray(dex.sheet_names)
# print(names)
list_data = []

for i in range(len(names)):
    # if names[i] != '2005':continue
    print('names', names[i])
    df = dex.parse(names[i])
    df = df.T
    df = df.reset_index()
    df = df.drop([1,2])
    df = df.reset_index()
    df.columns = df.iloc[0]
    df = df.drop([0])
    df = df.reset_index()

    print(list(df))
    df = df.drop(columns=['index'])
    df['Date'] = df['Date 2nd prep.']
    df['Date_1stprep'] = df['Date 1st prep.']

    df = df.dropna(subset=['Date'])

    # df = df[df.Date.isnull() == False]

    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')

    df = df[~df.Date.isnull()]
    df = df.reset_index()
    df = df.drop(columns=[0, 'index'])
    df = df.reset_index(drop=True)


    dft = df[[ 'Serial number', 'Date manufactured','Lab pressure', 'Lab temp', 'Lab rel hum','Air flow s','Air flow c', 'Date',
               'Background Current ib', 'Surf.Pressure', 'Ground Ozone', 'Date_1stprep']].copy()

    print(len(list(dft)),print(list(dft)))
    print(dft.index)

    list_data.append(dft)
# # #
dffinal = pd.concat(list_data, ignore_index=0)

dffinal.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_8812_ib.csv')


#
# dex = pd.ExcelFile('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/1988-2012_nya_o3_parameter_list.xlsx')
#
# names = np.asarray(dex.sheet_names)
# # print(names)
# list_data = []
#
# for i in range(len(names)):
#     # if names[i] != '2005':continue
#     print(names[i])
#     df = dex.parse(names[i])
#     df = df.T
#     df = df.reset_index()
#     df = df.drop([0,2])
#     df = df.reset_index()
#     df.columns = df.iloc[0]
#     df = df.drop([0])
#     df = df.reset_index()
#
#     df = df.drop(columns=['index'])
#     df['Date'] = df['Date 2nd prep. ']
#     df = df.dropna(subset=['Date'])
#
#     # df = df[df.Date.isnull() == False]
#
#     df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
#
#     df = df[~df.Date.isnull()]
#     df = df.reset_index()
#     df = df.drop(columns=[1, 'index'])
#     df = df.reset_index(drop=True)
#
#
#     dft = df[[ 'Serial number', 'Date manufactured','ibs', 'ibc','Lab pressure', 'Lab temp', 'Lab rel hum','Air flow s','Air flow c', 'Date']].copy()
#
#     print(len(list(dft)),print(list(dft)))
#     print(dft.index)
#
#     list_data.append(dft)
# # # #
# dffinal = pd.concat(list_data, ignore_index=0)
#
# dffinal.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_8812.csv')

# path = '/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/'
#
# allFiles = sorted(glob.glob(path + "/Current/*_rawcurrent.hdf"))
#
# list_data = []
#
#
# size = len(allFiles)
# datelist = [0] * size
# j = 0
#
# bool_rscorrection = False
#
# for (filename) in (allFiles):
#     file = open(filename, 'r')
#
#     print(filename)
#
#     df = pd.read_hdf(filename)
#
#     # print(list(df))
#
#     try:
#         dfn = df.drop(['Pair', 'Time', 'Height', 'Tbox', 'TboxC', 'WindDirection', 'WindSpeed', 'O3', 'T', 'U', 'I'],
#                     axis=1)
#     except KeyError:
#         dfn = df.drop(['Pair', 'Time', 'Height', 'Tbox', 'TboxC', 'O3', 'T', 'U', 'I'],
#                       axis=1)
#
#     dft = dfn[10:11]
#     # dft = pd.DataFrame()
#     # dft.loc[0, ['HourLaunchTime', 'MinuteLaunchTime', 'SerialECC','RadiosondeModel', 'RadiosondeSerial']] = \
#     #     ['9999', '9999','9999','9999','9999']
#     #
#     # try:
#     #     dft.loc[0,['Date','BkgUsed', 'HourLaunchTime', 'MinuteLaunchTime', 'Longitude', 'Latitude', 'CorrectionFactor',
#     #                       'SerialECC', 'SensorType', 'InterfaceSerial','PF', 'iB0', 'iB2',
#     #                       'SolutionVolume', 'ibg', 'Pcor', 'Pground','TLab','ULab']] = \
#     #     df.loc[0:0,['Date','BkgUsed', 'HourLaunchTime', 'MinuteLaunchTime', 'Longitude', 'Latitude', 'CorrectionFactor',
#     #                       'SerialECC', 'SensorType', 'InterfaceSerial','PF', 'iB0', 'iB2',
#     #                       'SolutionVolume', 'ibg', 'Pcor', 'Pground','TLab','ULab']]
#     # except KeyError:
#     #     dft = df.loc[0:0,['Date','BkgUsed', 'HourLaunchTime', 'MinuteLaunchTime', 'Longitude', 'Latitude', 'CorrectionFactor',
#     #                       'SerialECC', 'SensorType', 'InterfaceSerial','PF', 'iB0', 'iB2',
#     #                       'SolutionVolume', 'ibg', 'Pcor']]
#     #     dft['Pground'] = 9999
#     #     dft['TLab'] = 9999
#     #     dft['ULab'] = 9999
#
#
#     list_data.append(dft)
# # # # #
# dffinal = pd.concat(list_data, ignore_index=0)
#
# dffinal.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_All.csv')