

import pandas as pd
import glob
from datetime import datetime
from re import search
import numpy as np
import matplotlib.pyplot as plt

k = 273.15

filepath = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/nilu/'

dfm  = pd.read_csv(filepath + "Metadata/All_metadata.csv")
dfm['iB1'] = dfm['iB0']

path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'

dfmeta = pd.read_csv(path + 'CSV/DQM/valentia_metadata.csv')

print(len(dfmeta))

# dfmeta = dfmeta[dfmeta.PF < 50]
# dfmeta = dfmeta[dfmeta.PF > 20]
# dfmeta = dfmeta[dfmeta.iB1 < 0.5]
# dfmeta = dfmeta[dfmeta.PF > 20]
dfmeta = dfmeta[dfmeta.iB1 < 5]
dfm = dfm[dfm.iB1 < 5]


print(list(dfmeta))

# dfmeta['Sonde'] = dfmeta['SensorType']

# dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
dfmeta['Date'] = pd.to_datetime(dfmeta['Date'], format='%Y-%m-%d')
# dfmeta['Date'] = dfmeta['Date'].dt.strftime('%Y-%m-%d')
dfm['Date'] = pd.to_datetime(dfm['Date'], format='%Y%m%d')


print(dfmeta[['Date']][0:2])
print(dfm[['Date']][0:2])


dfmeta = dfmeta.set_index('Date').sort_index()
dfm = dfm.set_index('Date').sort_index()

dfm = dfm[dfm.TLab < 40]


# dfmeta = dfmeta[dfmeta.PF < 50]
# dfmeta = dfmeta[dfmeta.PF > 20]
# plt.close('all')
# fig, ax = plt.subplots()
# #
# plt.fill_between(dfmeta.index, dfmeta.PF.mean()-2 * dfmeta.PF.std(), dfmeta.PF.mean()+ 2 *dfmeta.PF.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
# plt.plot(dfmeta.index, dfmeta.PF,  label="PF", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
# ax.axhline(y=dfmeta.PF.median(), color='grey', label = "Median PF")
# ax.axhline(y=dfmeta.PF.mean() + dfmeta.PF.std(), color='#1f77b4',linestyle='--', label = "Mean PF + 1sigma")
# ax.axhline(y=dfmeta.PF.mean(), color='#1f77b4', label = "Mean PF")
# ax.axhline(y=dfmeta.PF.mean() - dfmeta.PF.std(), color='#1f77b4',linestyle='--', label = "Mean PF - 1sigma")
# plt.title('Valentia  PF values')
# ax.legend(loc='best', frameon=True, fontsize='small')
# plotname = 'PF'
# # # #
# plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')
# plt.show()

# plt.close('all')
# fig, ax = plt.subplots()
# #
# plt.fill_between(dfmeta.index, dfmeta.iB1.mean()-2 * dfmeta.iB1.std(), dfmeta.iB1.mean()+ 2 *dfmeta.iB1.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
# plt.plot(dfmeta.index, dfmeta.iB1,  label="iB1", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
# ax.axhline(y=dfmeta.iB1.median(), color='grey', label = "Median iB1 = "+ str(round(dfmeta.iB1.median(),2)))
# ax.axhline(y=dfmeta.iB1.mean() + dfmeta.iB1.std(), color='#1f77b4',linestyle='--', label = "Mean iB1 + 1sigma")
# ax.axhline(y=dfmeta.iB1.mean(), color='#1f77b4', label = "Mean iB1 = " + str(round(dfmeta.iB1.mean(),2)))
# ax.axhline(y=dfmeta.iB1.mean() - dfmeta.iB1.std(), color='#1f77b4',linestyle='--', label = "Mean iB1 - 1sigma")
# plt.title('Valentia  iB1 values')
# ax.legend(loc='best', frameon=True, fontsize='small')
# plotname = 'iB1'
# # # #
# plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')
# plt.show()

plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfm.index, dfm.Pground.mean()-2 * dfm.Pground.std(), dfm.Pground.mean()+ 2 *dfm.Pground.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
plt.plot(dfm.index, dfm.Pground,  label="Pground", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfm.Pground.median(), color='grey', label = "Median Pground = "+ str(round(dfm.Pground.median(),2)))
ax.axhline(y=dfm.Pground.mean() + dfm.Pground.std(), color='#1f77b4',linestyle='--', label = "Mean Pground + 1sigma")
ax.axhline(y=dfm.Pground.mean(), color='#1f77b4', label = "Mean Pground = " + str(round(dfm.Pground.mean(),2)))
ax.axhline(y=dfm.Pground.mean() - dfm.Pground.std(), color='#1f77b4',linestyle='--', label = "Mean Pground - 1sigma")
plt.title('Valentia  Pground values')
ax.legend(loc='best', frameon=True, fontsize='small')
plotname = 'Pground'
# # #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')
plt.show()