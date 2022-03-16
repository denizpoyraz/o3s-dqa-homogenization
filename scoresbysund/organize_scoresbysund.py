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

# for (filename) in (allFiles):
#     df = pd.read_hdf(filename)
#     df = df.reset_index()
#
#
#     # if df.loc[1, 'Date'] <= '20070104': continue
#
#     print(filename )
#
#
#     if (df.loc[1,'Date'] >= '20070104') :
#         df['RadiosondeModel'] = 9999
#         df['Pground'] = 9999
#         df['RadiosondeSerial'] =9999
#
#     dft = df.loc[0:1,['Pground', 'Pground', 'Pground', 'Pground', 'Pground', 'Pground', 'Pground','SerialECC', 'SensorType',
#                       'LaunchTime','SondeTotalO3','RadiosondeModel', 'RadiosondeSerial','PumpTempLoc','Date']]
# #
#     metadata.append(dft)
# #
# name_out = 'Scoresby_MetadaAll'
# dfall = pd.concat(metadata, ignore_index=True)

# dfall.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/scoresby/metadata/' + name_out + ".csv")

dfmeta = pd.read_csv(path + 'metadata/Scoresby_MetadaAll.csv')


print(list(dfmeta))

dfmeta = dfmeta[dfmeta.Pground !=  1000]
# dfmeta = dfmeta[dfmeta.Pground > 0]
#
# # some values are in K some in C, to convert them all in C
# dfmeta.loc[dfmeta.Pground > k, 'Pground'] = dfmeta.loc[dfmeta.Pground > k, 'Pground'] - k

# dfmeta['Pground'] = dfmeta['Phip']

print(list(dfmeta))

# dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
dfmeta['Date'] = pd.to_datetime(dfmeta['Date'], format='%Y%m%d')
# dfmeta['Date'] = dfmeta['Date'].dt.strftime('%Y-%m-%d')


print(dfmeta[['Date']][0:2])

dfmeta = dfmeta.set_index('Date').sort_index()


# print('ib0', dfmeta.Pground.median(), 'ib2', dfmeta.Pground.median())
# print('ib0', dfmeta.Pground.mean(), 'ib2', dfmeta.Pground.mean())
# print('err', dfmeta.Pground.mean() - 2*dfmeta.Pground.std(), dfmeta.Pground.mean() + 2*dfmeta.Pground.std())
# print(dfmeta.index)
# series = dfmeta.index.tolist()
# print(series)

plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfmeta.index, dfmeta.Pground.mean()-2 * dfmeta.Pground.std(), dfmeta.Pground.mean()+ 2 *dfmeta.Pground.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")

plt.plot(dfmeta.index, dfmeta.Pground,  label="Pground", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfmeta.Pground.median(), color='grey', label = "Median Pground")
ax.axhline(y=dfmeta.Pground.mean() + dfmeta.Pground.std(), color='#1f77b4',linestyle='--', label = "Mean Pground + 1sigma")
ax.axhline(y=dfmeta.Pground.mean(), color='#1f77b4', label = "Mean Pground")
ax.axhline(y=dfmeta.Pground.mean() - dfmeta.Pground.std(), color='#1f77b4',linestyle='--', label = "Mean Pground - 1sigma")
# plt.ylim([-0.1, 0.3])
# plt.fill_between(dfmeta.index, -0.04242420503016284, 0.11795465516255485, facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")


# plt.title('Lauder laboratory humidity values')
plt.title('Scoresbysund PLab values')

# ax.legend(loc='best', frameon=True, fontsize='small')
ax.legend(loc='lower right ', frameon=True, fontsize='small')

plotname = 'PLab'
# #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()