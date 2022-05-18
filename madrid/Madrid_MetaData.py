import numpy as np
import pandas as pd

import glob

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'


columnString = "Year DateTime O3ratio BrewO3 ResidO3 PLab TLab ULab iB0 iB1 iB2 PF PumpT400hpa PumpT200hpa PumpT50hpa PumpT25hpa Psup O3STotal"
columnStr = columnString.split(" ")

dfmeta = pd.read_excel("/home/poyraden/Analysis/Homogenization_public/Files/madrid/Madrid_1992-2020_O3S-Parameters_20210422.xls", skiprows = 1,names=columnStr, dtype=str)
# dfmeta = pd.read_excel("/home/poyraden/Analysis/Homogenization_public/Files/madrid/Madrid_2005-2019_O3S-Parameters.xls", sheet_name ='Parametros')

dfmeta['DateTime'] = dfmeta['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d %H'))
dfmeta['Date'] = dfmeta['DateTime'].dt.strftime('%d/%m/%Y')
dfmeta['Datef2'] = dfmeta['DateTime'].dt.strftime('%Y-%m-%d')
# dfmeta['iB2'] = dfmeta['iB2'].astype(float)
dfmeta = dfmeta.drop('Date',1)
dfmeta = dfmeta.drop('Datef2',1)

print(dfmeta.dtypes)

# dfmeta = [dfmeta[i].astype(float) for i in list(dfmeta) if (i != 'DateTime')]

print(list(dfmeta))


# dfmeta.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/Madrid_1992-2020_MetaData.csv')
dfmeta.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/Madrid_Metadata.csv')

allFiles = sorted(glob.glob(path + "CSV/out/*.hdf"))

listall = []

for (filename) in (allFiles):
    df = pd.read_hdf(filename)
    # print(filename)

    listall.append(df)

name_out = 'Madrid_AllData_woudc'
dfall = pd.concat(listall, ignore_index=True)

dfall.to_hdf(path + "DQA_nors80/" + name_out + ".hdf", key = 'df')