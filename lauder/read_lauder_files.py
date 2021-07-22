import pandas as pd
import numpy as np
import glob
from datetime import datetime
from re import search

#code to read in Lauder files provided by the station PI
path = "/home/poyraden/Analysis/Homogenization_public/Files/lauder/csv/"
allFiles = glob.glob("/home/poyraden/Analysis/Homogenization_public/Files/lauder/zipfiles/*")

# columnString = "Time Press Alt Temp RH O3 P TPump O3CellI EvapCath WindSp WindDir Lat Lon RH1 RH2 GPS Pres GPS Alt GPS Traw GPS Tcor GPS RH"
columnStr = ['Time', 'Press', 'Alt', 'Temp', 'RH', 'PO3', 'TPump', 'O3CellI', 'EvapCath', 'WindSp', 'WindDir', 'Lat', 'Lon',
             'RH1', 'RH2', 'GPSPres', 'GPSAlt', 'GPSTraw', 'GPSTcor', 'GPSRH']


# tmp = r'Time,   Press,     Alt,    Temp,      RH,    O3 P,  T Pump, O3CellI,EvapCath,  WindSp, WindDir,     Lat,     Lon,     RH1,     RH2,GPS Pres, GPS Alt,GPS Traw,GPS Tcor,  GPS RH'
tmp = r'EvapCath'
for filename in allFiles:
    print('one',filename)

    file = open(filename,'r', encoding="ISO-8859-1")
    all_lines = file.readlines()

    for lines,j in zip((all_lines), range(len(all_lines))):
        if search(tmp, all_lines[j]):
            line = j
            print(j, all_lines[j])

    # df = pd.read_csv(filename, sep = "\s *", engine="python", skiprows=line, names=columnStr)
    df = pd.read_csv(filename, sep = "\s *", engine="python", skiprows=line+2, names=columnStr)

    file2 = open(filename,'r', encoding="ISO-8859-1")

    metadata_var = [''] * line
    metadata = [''] * line
    metadata_lines = [''] * line
    metadata_all = [0] * line


    for i in range(line-2):
        metadata_lines[i] = file2.readline()
        if search('=', metadata_lines[i]):
            metadata_var[i] =  metadata_lines[i].split("=")[0]
            metadata[i] =  metadata_lines[i].split("=")[1]
            metadata[i] = metadata[i].rstrip("\n")

    metadata = np.array(metadata)

    dfm = pd.DataFrame(metadata, index = metadata_var)
    dfm = dfm.T
    # date = dfm.at[0,'Launch Date']
    date = datetime.strptime(dfm.at[df.first_valid_index(),'Launch Date'], '%Y-%m-%d')
    date2 = datetime.strftime(date, '%Y%m%d')
    # print(date, date2, dfm.at[0,'Launch Date'])
    # print(dfm[0:5])

    # df.to_hdf(path  + date2 + ".hdf", key='df')
    # dfm.to_csv(path  + date2 + "_metadata.csv")


