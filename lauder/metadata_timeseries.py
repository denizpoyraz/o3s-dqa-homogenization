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
path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/'
allFiles = sorted(glob.glob(path + 'metadata/*_md.csv'))


# dfmeta = pd.DataFrame()
# metadata = []
#
# for (filename) in (allFiles):
#     print(filename)
#     df = pd.read_csv(filename)
#
#     metadata.append(df)
#
# name_out = 'Lauder_MetadaAll'
# dfall = pd.concat(metadata, ignore_index=True)
#
# dfall.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/lauder/metadata/' + name_out + ".csv")



dfmeta = pd.read_csv(path + 'metadata/Lauder_MetadaAll.csv')

# series = dfmeta[['Date', 'TLab', 'TLab','TLab']]

print(list(dfmeta))
# print(dfmeta[['Date']][0:2])
# dfmeta = dfmeta[dfmeta.TLab < 2]
# dfmeta = dfmeta[dfmeta.TLab > -99]
# dfmeta = dfmeta[dfmeta.TLab < 2]
dfmeta = dfmeta[dfmeta.ULab < 800]
# dfmeta = dfmeta[dfmeta.TLab < 800]
#
# # some values are in K some in C, to convert them all in C
# dfmeta.loc[dfmeta.TLab > k, 'TLab'] = dfmeta.loc[dfmeta.TLab > k, 'TLab'] - k

dfmeta['PF'] = dfmeta['Phip']

print(list(dfmeta))

# dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
dfmeta['Date'] = pd.to_datetime(dfmeta['Date'], format='%Y-%m-%d')
# dfmeta['Date'] = dfmeta['Date'].dt.strftime('%Y-%m-%d')


print(dfmeta[['Date']][0:2])


# date = datetime.strptime(date_tmp, '%y%m%d')

# print(dfmeta[['Date','Datenf']][0:5])
dfmeta = dfmeta.set_index('Date').sort_index()


# print('ib0', dfmeta.ULab.median(), 'ib2', dfmeta.ULab.median())
# print('ib0', dfmeta.ULab.mean(), 'ib2', dfmeta.ULab.mean())
print('err', dfmeta.TLab.mean() - 2*dfmeta.TLab.std(), dfmeta.TLab.mean() + 2*dfmeta.TLab.std())
print(dfmeta.index)
series = dfmeta.index.tolist()
print(series)

plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfmeta.index, dfmeta.ULab.mean()-2 * dfmeta.ULab.std(), dfmeta.ULab.mean()+ 2 *dfmeta.ULab.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")

plt.plot(dfmeta.index, dfmeta.ULab,  label="ULab", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfmeta.ULab.median(), color='grey', label = "Median ULab")
ax.axhline(y=dfmeta.ULab.mean() + dfmeta.ULab.std(), color='#1f77b4',linestyle='--', label = "Mean ULab + 1sigma")
ax.axhline(y=dfmeta.ULab.mean(), color='#1f77b4', label = "Mean ULab")
ax.axhline(y=dfmeta.ULab.mean() - dfmeta.ULab.std(), color='#1f77b4',linestyle='--', label = "Mean ULab - 1sigma")
# plt.ylim([-0.1, 0.3])
# plt.fill_between(dfmeta.index, -0.04242420503016284, 0.11795465516255485, facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")


# plt.title('Lauder laboratory humidity values')
plt.title('Lauder ULab values')

# ax.legend(loc='best', frameon=True, fontsize='small')
ax.legend(loc='lower right ', frameon=True, fontsize='small')

plotname = 'ULab'
# #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()