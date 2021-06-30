import pandas as pd
import numpy as np
from re import search
import glob
from datetime import datetime

path = "/home/poyraden/Analysis/Homogenization_public/Files/uccle/"

allFiles = sorted(glob.glob(path + "/dat/*.dat"))

list_data = []

columnString = "Time Height P T U Winddir Windv Tbox Tboxcor I Phi PO3_dqar dPO3_dqar"
columnStr = columnString.split(" ")
print(columnStr)

columnMeta = ['mDate', 'mRadioSondeNr', 'PF', 'iB0', 'iB1', 'CorrectionFactor', 'SerialECC', 'InterfaceNr','DateTime','Datenf']

dfmeta = pd.read_csv("/home/poyraden/Analysis/Homogenization_public/Files/uccle/ECCprop.txt", sep = r"\t" , engine="python",skiprows=1, names=columnMeta)
# dfmeta['DateTime'] = dfmeta['mDate'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d%H'))
dfmeta['DateTime'] = pd.to_datetime(dfmeta['mDate'], format='%Y%m%d%H')
dfmeta['Datenf'] = dfmeta['DateTime'].apply(lambda x: x.strftime('%Y%m%d'))


# total ozone file to ad to metadata
file = open('/home/poyraden/Analysis/Homogenization_public/Files/uccle/O3totres_O3SDQA.dat','r')
all_lines = file.readlines()

ocolumns = "Date TO_Brewer RO_aboveburst TON"
ocolumns = ocolumns.split(" ")
dfo = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/uccle/O3totres_O3SDQA.dat', sep = r"\s *" , engine="python", names=ocolumns)
# dfo['Datetmp'] = dfo.Date.apply(lambda x: str(x)[0:6])
# dfo['Time'] = dfo.Date.apply(lambda x: str(x)[6:11])
j = 0
for il in all_lines:
    tmp = il.split("\n")[0]
    tmp = tmp[0:11]
    date = tmp[0:6]
    hour = tmp[6:11]
    dtdate = pd.to_datetime(date, format='%y%m%d')
    dthour = pd.to_datetime(hour, format='%H.%M')
    dfo.at[j, 'Datenf'] = dtdate
    dfo.at[j, 'LaunchTime'] = hour
    j = j+1

dfo['DatenTime'] = dfo['Datenf'].apply(lambda x: x.strftime('%Y%m%d'))


# print(dfmeta[0:3])

for filename in allFiles:
    file = open(filename,'r')
    # print(filename)
    date_tmp  = filename.split('.dat')[0].split("/")[-1]
    if len(date_tmp) != 12: continue
    date = datetime.strptime(date_tmp, '%Y%m%d%H%M')
    datef = date.strftime('%Y%m%d')
    hourf = date.strftime('%H%M')
    print(datef)
    if datef < '19961001':continue #before this date it is BrewerMast


    #
    df = pd.read_csv(filename, sep="\s *", engine="python", names=columnStr)
    df['Date'] = datef



    # if datef == '19970212': datef = '19970211'
    # else: datef = datef

    dfm = pd.DataFrame()
    dfm2 = pd.DataFrame()
    dfm = dfmeta[dfmeta.Datenf == datef]
    dfm = dfm.reset_index()
    dfm2 = dfo[dfo.DatenTime == datef]
    dfm2 = dfm2.reset_index()


    if len(dfm2) == 0:
        dfm.at[0, 'TO_Brewer'] = 9999
        dfm.at[0, 'RO_aboveburst'] = 9999
        dfm.at[0, 'TON'] = 9999
        dfm.at[0, 'LaunchTime'] = 9999
        dfm.at[0, 'Date'] = 9999
        dfm.at[0,'SondeO3'] = 9999
        dfm.at[0,'IntegratedO3'] = 9999

    if len(dfm2) == 1:
        dfm.at[0, 'TO_Brewer'] = dfm2.at[0, 'TO_Brewer']
        dfm.at[0, 'RO_aboveburst'] = dfm2.at[0, 'RO_aboveburst']
        dfm.at[0, 'TON'] = dfm2.at[0, 'TON']
        dfm.at[0, 'LaunchTime'] = dfm2.at[0, 'LaunchTime']
        dfm.at[0, 'Date'] = dfm2.at[0, 'Datenf']
        dfm.at[0, 'SondeO3'] = dfm.at[0, 'TO_Brewer'] / dfm.at[0, 'TON']
        dfm.at[0, 'IntegratedO3'] = dfm.at[0, 'SondeO3'] - dfm.at[0, 'RO_aboveburst']

    # print(dfm.at[dfm.first_valid_index(),'Datenf'], dfm2.at[dfm2.first_valid_index(),'DatenTime'], )

    # print(list(dfm2))
    rsmodel = ''
    pumplocation = ''
    if datef <= '20070901': rsmodel = 'RS80'
    if datef > '20070901': rsmodel == 'RS92'
    if datef < '19981201': pumplocation = "inthebox"
    if datef >= '19981201': pumplocation = "inthepump"

    if dfm.at[0,'iB1'] == -1: dfm.at[0,'iB1'] = 9999

    dfm.at[0,'RadiosondeModel'] = rsmodel
    dfm.at[0, 'TpumpLocation'] = pumplocation
    dfm.at[0,'SolutionType'] = "0.5%"
    dfm.at[0,'SolutionVolume'] = "3.0"

    df.to_hdf(path + '/Raw_upd/' + datef + ".hdf", key='df')
    dfm.to_csv(path + '/Raw_upd/' + datef + "_md.csv")

    list_data.append(dfm)

dff = pd.concat(list_data, ignore_index=True)
# hdfall = path + "All_metadata.hdf"
csvall = path + "/Raw_upd/All_metadata.csv"

# dff.to_hdf(hdfall, key = 'df')
dff.to_csv(csvall)





