import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime
import matplotlib.pyplot as plt

k = 273.15
#
# first make a DF of all the metadata


path = '/home/poyraden/Analysis/Homogenization_public/Files/lerwick/'
station_name = 'lerwick'

dfmeta = pd.read_csv(path + "nilu/Metadata/All_metadata_nilu.csv" )

print(list(dfmeta))
# 'Pground', 'iB2', 'iB2', 'Pcorrection_ground', 'Pground', 'Pground'
# series = dfmeta[['Date', 'Pground', 'Pground','Pground']]

print(list(dfmeta))
# dfmeta['Pground'] = dfmeta['iB0']
# print(dfmeta[['Date']][0:2])
# dfmeta = dfmeta[dfmeta.Pground < 2]
# dfmeta = dfmeta[dfmeta.Pground > -99]
# dfmeta = dfmeta[dfmeta.Pground < 2]
dfmeta = dfmeta[dfmeta.Pground < 9999]
# dfmeta = dfmeta[dfmeta.Pground < 800]
#
# # some values are in K some in C, to convert them all in C
# dfmeta.loc[dfmeta.Pground > k, 'Pground'] = dfmeta.loc[dfmeta.Pground > k, 'Pground'] - k

# dfmeta['Pground'] = dfmeta['Phip']

print(list(dfmeta))

# dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
dfmeta['Date'] = pd.to_datetime(dfmeta['DateTime'], format='%Y-%m-%d')
# dfmeta['Date'] = dfmeta['Date'].dt.strftime('%Y-%m-%d')


# print(dfmeta[['Date','Datenf']][0:5])
dfmeta = dfmeta.set_index('Date').sort_index()


plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfmeta.index, dfmeta.Pground.mean()-2 * dfmeta.Pground.std(), dfmeta.Pground.mean()+ 2 *dfmeta.Pground.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
plt.plot(dfmeta.index, dfmeta.Pground,  label="Pground", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfmeta.Pground.median(), color='grey', label = "Median Pground = "+ str(round(dfmeta.Pground.median(),2)))
ax.axhline(y=dfmeta.Pground.mean() + dfmeta.Pground.std(), color='#1f77b4',linestyle='--', label = "Mean Pground + 1sigma")
ax.axhline(y=dfmeta.Pground.mean(), color='#1f77b4', label = "Mean Pground = " + str(round(dfmeta.Pground.mean(),2)))
ax.axhline(y=dfmeta.Pground.mean() - dfmeta.Pground.std(), color='#1f77b4',linestyle='--', label = "Mean Pground - 1sigma")
plt.title('Lerwick  Pground values')
ax.legend(loc='best', frameon=True, fontsize='small')
plotname = 'Pground'
# plt.ylim([-0.05, 0.6])
# #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()