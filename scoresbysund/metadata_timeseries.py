import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime
import matplotlib.pyplot as plt

# from Homogenisation_Functions import po3tocurrent, absorption_efficiency, stoichemtry_conversion, conversion_efficiency, background_correction, \
#     pumptemp_corr, pf_efficiencycorrection, currenttopo3, pf_groundcorrection

k = 273.15
#
# path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/'
# dfmeta = pd.read_csv(path + 'Raw/Metadata/All_metadata.csv')

path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'


# allFiles = sorted(glob.glob(path + "Metadata/*.csv"))
#
# dfmeta = pd.DataFrame()
# metadata = []
#
# for (filename) in (allFiles):
#     print(filename)
#     df = pd.read_csv(filename)
#
#     metadata.append(df)
#
# name_out = 'All_metadata'
# dfall = pd.concat(metadata, ignore_index=True)
# dfall.to_csv(path + "Metadata/" + name_out + ".csv")



# dfmeta = pd.read_csv(path + 'Metadata/All_metadata.csv')

dfmeta = pd.read_csv(path + 'metadata/Scoresby_MetadaAll.csv')


# series = dfmeta[['Date', 'iB1', 'iB2','iB2']]

# print(list(dfmeta))
# print(dfmeta[['Date']][0:2])
# dfmeta = dfmeta[dfmeta.iB1 < 2]
dfmeta = dfmeta[dfmeta.iB2 < 1]
# dfmeta = dfmeta[dfmeta.iB2 > 5]

print(list(dfmeta))

## dfmeta['Date'] = dfmeta['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
# dfmeta['Date']  = dfmeta['Datenf'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))

# dfmeta = dfmeta[dfmeta.Date > '2017-01-01']
print(dfmeta[['Date']][0:2])


# date = datetime.strptime(date_tmp, '%y%m%d')

# print(dfmeta[['Date','Datenf']][0:5])
dfmeta = dfmeta.set_index('Date').sort_index()


# print('ib0', dfmeta.iB2.median(), 'ib2', dfmeta.iB2.median())
# print('ib0', dfmeta.iB2.mean(), 'ib2', dfmeta.iB2.mean())
print('err', dfmeta.iB2.mean() - 2*dfmeta.iB2.std(), dfmeta.iB2.mean() + 2*dfmeta.iB2.std())
# print(dfmeta.index)
series = dfmeta.index.tolist()
# print(series)

plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfmeta.index, dfmeta.iB2.mean()-2 * dfmeta.iB2.std(), dfmeta.iB2.mean()+ 2 *dfmeta.iB2.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")

plt.plot(dfmeta.index, dfmeta.iB2,  label="iB2", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfmeta.iB2.median(), color='grey', label = "Median iB2")
ax.axhline(y=dfmeta.iB2.mean() + dfmeta.iB2.std(), color='#1f77b4',linestyle='--', label = "Mean iB2 + 1sigma")
ax.axhline(y=dfmeta.iB2.mean(), color='#1f77b4', label = "Mean iB2")
ax.axhline(y=dfmeta.iB2.mean() - dfmeta.iB2.std(), color='#1f77b4',linestyle='--', label = "Mean iB2 - 1sigma")
# plt.ylim([-0.1, 0.3])
# plt.fill_between(dfmeta.index, -0.04242420503016284, 0.11795465516255485, facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")


plt.title('Scoresbysund iB2 values')
ax.legend(loc='upper right', frameon=True, fontsize='small')

plotname = 'iB2'
#
# plt.savefig(path + 'Plots/Metadata/' + plotname + '.pdf')
# plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
# plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()