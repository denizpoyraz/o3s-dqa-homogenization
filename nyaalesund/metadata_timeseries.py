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
# dfm = pd.read_csv(path + 'Raw/Metadata/All_metadata.csv')

# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# dfm = pd.read_csv(path + 'Madrid_Metadata.csv')

path = '/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/'
dfm = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/NY_metadata.csv')

# dfm = dfm[dfm.DateTime > '1993-12-31']


print(list(dfm))
# print(dfm[['Date']][0:2])
# dfm = dfm[dfm.RHLab < 50]
# dfm = dfm[dfm.RHLab < 0.1]
# dfm = dfm[dfm.RHLab > 5]

print(list(dfm))

## dfm['Date'] = dfm['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
dfm['Date']  = dfm['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
# dfm['Date'] = dfm['Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))

print(dfm[['Date']][0:2])
print('dtypes', dfm.dtypes)


# date = datetime.strptime(date_tmp, '%y%m%d')

# print(dfm[['Date','Datenf']][0:5])
dfm = dfm.set_index('Date').sort_index()

dfm['RH_is_NaN'] = 0
dfm.loc[dfm['RHLab'].isnull(), 'RH_is_NaN'] = 1
dfm = dfm[dfm['RH_is_NaN'] == 0]
dfm = dfm[dfm.RHLab != 'missing']

# dfm['iB0'] = dfm['iB0'].astype(float)
dfm['RHLab'] = dfm['RHLab'].astype(float)
# dfm['iB1'] = dfm['iB1'].astype(float)

dfm.loc[dfm.RHLab < 1, 'RHLab'] = dfm.loc[dfm.RHLab < 1, 'RHLab'] * 100

# dfm1 = dfm[dfm.index < '2004']
# dfm2 = dfm[dfm.index >= '2004']


#
# print('ib0', dfm.RHLab.median(), 'ib2', dfm.RHLab.median())
# print('ib0', dfm.RHLab.mean(), 'ib2', dfm.RHLab.mean())
print('err', dfm.RHLab.mean() - 2*dfm.RHLab.std(), dfm.RHLab.mean() + 2*dfm.RHLab.std())
print(dfm.index)
series = dfm.index.tolist()
print(series)

plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfm.index, dfm.RHLab.mean()-2 * dfm.RHLab.std(), dfm.RHLab.mean()+ 2 *dfm.RHLab.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
plt.plot(dfm.index, dfm.RHLab,  label="RHLab", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfm.RHLab.median(), color='grey', label = "Median RHLab")
ax.axhline(y=dfm.RHLab.mean() + dfm.RHLab.std(), color='#1f77b4',linestyle='--', label = "Mean RHLab + 1sigma")
ax.axhline(y=dfm.RHLab.mean(), color='#1f77b4', label = "Mean RHLab")
ax.axhline(y=dfm.RHLab.mean() - dfm.RHLab.std(), color='#1f77b4',linestyle='--', label = "Mean RHLab - 1sigma")
# plt.ylim([-0.1, 0.35])
# plt.ylim([15, 40])

#
# plt.fill_between(dfm1.index, dfm1.RHLab.mean()-2 * dfm1.RHLab.std(), dfm1.RHLab.mean()+ 2 *dfm1.RHLab.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
# plt.plot(dfm1.index, dfm1.RHLab,  label="RHLab", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
# ax.axhline(y=dfm1.RHLab.median(), color='grey', label = "Median RHLab")
# ax.axhline(y=dfm1.RHLab.mean() + dfm1.RHLab.std(), color='#1f77b4',linestyle='--', label = "Mean RHLab + 1sigma")
# ax.axhline(y=dfm1.RHLab.mean(), color='#1f77b4', label = "Mean RHLab")
# ax.axhline(y=dfm1.RHLab.mean() - dfm1.RHLab.std(), color='#1f77b4',linestyle='--', label = "Mean RHLab - 1sigma")
#
# plt.fill_between(dfm2.index, dfm2.RHLab.mean()-2 * dfm2.RHLab.std(), dfm2.RHLab.mean()+ 2 *dfm2.RHLab.std(), facecolor='#1f77b4', alpha=.2)
# plt.plot(dfm2.index, dfm2.RHLab,  label="RHLab", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
# ax.axhline(y=dfm2.RHLab.median(), color='grey')
# ax.axhline(y=dfm2.RHLab.mean() + dfm2.RHLab.std(), color='#1f77b4',linestyle='--')
# ax.axhline(y=dfm2.RHLab.mean(), color='#1f77b4')
# ax.axhline(y=dfm2.RHLab.mean() - dfm2.RHLab.std(), color='#1f77b4',linestyle='--')
# # plt.ylim([-0.1, 0.3])


plt.title('Ny-Aalesund RHLab time-series')

# ax.legend(loc='lower right', frameon=True, fontsize='small')
ax.legend(loc='best', frameon=True, fontsize='small')

plotname = 'RHLab'
# #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.pdf')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()