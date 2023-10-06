import pandas as pd
import glob
from datetime import datetime
from re import search
import numpy as np
import matplotlib.pyplot as plt

k = 273.15

# path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/CSV/'
# all data and metadata files read from woudc formotted files
# allFiles = sorted(glob.glob(path + 'Current/*rawcurrent.hdf'))

# dfa = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/valentia/CSV/DQM/valentia_alldata_woudc.h5')
# dfam = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/valentia/CSV/DQM/valentia_metadata_till2022.csv')
# # # now correct naming and make new dataframe
# dfml = pd.DataFrame()
#
# dfml['Phip'] = 100 / dfam['AUXILIARY_DATA_PumpRate']
# dfml['iB1'] = dfam['AUXILIARY_DATA_ib1']
# dfml['iB2'] = dfam['AUXILIARY_DATA_ib2']
# dfml['EccModel'] = dfam['INSTRUMENT_Model']
# dfml['SondeSerial'] = dfam['INSTRUMENT_Number']
# dfml['Date'] = dfam['TIMESTAMP_Date']
# dfml['PF'] = dfam['AUXILIARY_DATA_PumpRate']
#
# dfml = dfml.sort_values('Date')
# dfml = dfml.drop_duplicates(['Date', 'SondeSerial'])
# dfml = dfml.reset_index()
#
# dfml.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/valentia/CSV/DQM/valentia_metadata_till2022.csv')

# merge 2 dataframes to one
k = 273.15

filepath = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/nilu/'
#
dfn  = pd.read_csv(filepath + "Metadata/All_metadata_nilu.csv")
dfn['iB1'] = dfn['iB0']
#
dfn = dfn[(dfn.iB1 < 1) & (dfn.iB2 < 1) & (dfn.PF > 20) & dfn.PF < 35]


path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'

dfw = pd.read_csv(path + 'CSV/DQM/valentia_metadata_till2022.csv')
#
dfw['Date'] = pd.to_datetime(dfw['Date'], format='%Y-%m-%d')
dfn['Date'] = pd.to_datetime(dfn['Date'], format='%Y%m%d')

dfw['TLab'] = 9999
dfw['ULab'] = 9999
dfw['Pground'] = 9999
dfw['Col2A'] = 9999
dfw['Col2B'] = 9999
dfw['InterfaceSerial'] = 9999
dfw['RadiosondeModel'] = 9999
dfw['RadiosondeSerial'] = 9999


for j in range(len(dfn)):

    dfw.loc[(dfw.Date == dfn.at[j,'Date']),'TLab' ] = dfn.at[j, 'TLab']
    dfw.loc[(dfw.Date == dfn.at[j,'Date']),'ULab' ] = dfn.at[j, 'ULab']
    dfw.loc[(dfw.Date == dfn.at[j,'Date']),'Pground' ] = dfn.at[j, 'Pground']
    dfw.loc[(dfw.Date == dfn.at[j,'Date']),'Col2A' ] = dfn.at[j, 'TotalO3_Col2A']
    dfw.loc[(dfw.Date == dfn.at[j,'Date']),'Col2B' ] = dfn.at[j, 'TotalO3_Col2B']
    dfw.loc[(dfw.Date == dfn.at[j,'Date']),'InterfaceSerial' ] = dfn.at[j, 'InterfaceSerial']
    dfw.loc[(dfw.Date == dfn.at[j,'Date']),'RadiosondeModel' ] = dfn.at[j, 'RadiosondeModel']
    dfw.loc[(dfw.Date == dfn.at[j,'Date']),'RadiosondeSerial' ] = dfn.at[j, 'RadiosondeSerial']

dfw.to_csv(path + 'joined_Metadata.csv')

dfw = pd.read_csv(path + 'joined_Metadata.csv')

dfw['TOCol'] = 9999
#add TO values from WOUDC TO df to joined metadata

dft = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/valentia/WOUDC_TO/TO/to_valentia_alldata.csv')


print(len(dfw), len(dft))

for j in range(len(dft)):

    # print(j, dft.at[j,'Date'],dft.at[j, 'ColumnO3']  )
    dfw.loc[(dfw.Date == dft.at[j,'Date']),'TOCol' ] = dft.at[j, 'ColumnO3']

dfw.to_csv(path + 'joined_Metadata_till2022.csv')

# #now also add SondeTOC and SondeTOC homogenized from homogenized metada
#
# path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'
# allFiles = sorted(glob.glob(path + "DQA_nors80/*_o3smetadata_nors80.csv"))
#
# # dfmeta = pd.DataFrame()
# # metadata = []
# #
# # for (filename) in (allFiles):
# #     print(filename)
# #     df = pd.read_csv(filename)
# #
# #     metadata.append(df)
#
# name_out = 'ValentiaMetada_DQA_nors80'
# # dfall = pd.concat(metadata, ignore_index=True)
# #
# # dfall.to_csv(path + "DQA_nors80/" + name_out + ".csv")
# # dfall.to_hdf(path + "DQA_nors80/" + name_out + ".h5", key = 'df')
#
# dfma = pd.read_csv(path + "DQA_nors80/" + name_out + ".csv")
# dfma['DateTime'] = dfma['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
# dfma['Date'] = dfma['DateTime'].dt.strftime('%Y-%m-%d')
#
# # now merge sonde TOC to dfw
# dfw = pd.read_csv(path + 'joined_Metadata.csv')
# print(len(dfw), len(dfma))
# #
# dfw['O3SondeTotal'] = 9999
# dfw['O3SondeTotal_hom'] = 9999
#
# for j in range(len(dfma)):
#
#     # print(j, dft.at[j,'Date'],dft.at[j, 'ColumnO3']  )
#     dfw.loc[(dfw.Date == dfma.at[j,'Date']),'O3SondeTotal' ] = dfma.at[j, 'O3SondeTotal']
#     dfw.loc[(dfw.Date == dfma.at[j,'Date']),'O3SondeTotal_hom' ] = dfma.at[j, 'O3SondeTotal_hom']
#
#
# dfw.to_csv(path + 'joined_Metadata.csv')