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
# 'iB2', 'iB2', 'iB2', 'Pcorrection_ground', 'iB2', 'iB2'
# series = dfmeta[['Date', 'iB2', 'iB2','iB2']]

print(list(dfmeta))
# dfmeta['iB2'] = dfmeta['iB2']
# print(dfmeta[['Date']][0:2])
# dfmeta = dfmeta[dfmeta.iB2 < 99]
# dfmeta = dfmeta[dfmeta.iB2 > 0]

# dfmeta = dfmeta[dfmeta.iB2 > -99]
dfmeta = dfmeta[dfmeta.iB2 > -1]
dfmeta = dfmeta[dfmeta.iB2 < 1]
# dfmeta = dfmeta[dfmeta.iB2 < 800]
#
# # some values are in K some in C, to convert them all in C
# dfmeta.loc[dfmeta.iB2 > k, 'iB2'] = dfmeta.loc[dfmeta.iB2 > k, 'iB2'] - k

# dfmeta['iB2'] = dfmeta['Phip']

print(list(dfmeta))

# dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
dfmeta['Date'] = pd.to_datetime(dfmeta['DateTime'], format='%Y-%m-%d')
# dfmeta['Date'] = dfmeta['Date'].dt.strftime('%Y-%m-%d')


# print(dfmeta[['Date','Datenf']][0:5])
dfmeta = dfmeta.set_index('Date').sort_index()


plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfmeta.index, dfmeta.iB2.mean()-2 * dfmeta.iB2.std(), dfmeta.iB2.mean()+ 2 *dfmeta.iB2.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
plt.plot(dfmeta.index, dfmeta.iB2,  label="iB2", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfmeta.iB2.median(), color='grey', label = "Median iB2 = "+ str(round(dfmeta.iB2.median(),2)))
ax.axhline(y=dfmeta.iB2.mean() + dfmeta.iB2.std(), color='#1f77b4',linestyle='--', label = "Mean iB2 + 1sigma")
ax.axhline(y=dfmeta.iB2.mean(), color='#1f77b4', label = "Mean iB2 = " + str(round(dfmeta.iB2.mean(),2)))
ax.axhline(y=dfmeta.iB2.mean() - dfmeta.iB2.std(), color='#1f77b4',linestyle='--', label = "Mean iB2 - 1sigma")
plt.title('Lerwick  iB2 values')
ax.legend(loc='best', frameon=True, fontsize='small')
plotname = 'iB2'
plt.ylim([-0.05, 0.6])
# #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()