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
dfm = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/NY_metadata_corrected.csv')

# dfm = dfm[dfm.DateTime > '1993-12-31']


print(list(dfm))
# print(dfm[['Date']][0:2])
# dfm = dfm[dfm.PLab < 50]
# dfm = dfm[dfm.PLab < '1200']
# dfm = dfm[dfm.PLab > 5]

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
dfm.loc[dfm['PLab'].isnull(), 'RH_is_NaN'] = 1
dfm = dfm[dfm['RH_is_NaN'] == 0]
dfm = dfm[dfm.PLab != 'missing']

# dfm['iB0'] = dfm['iB0'].astype(float)
dfm['PLab'] = dfm['PLab'].astype(float)
# dfm['iB1'] = dfm['iB1'].astype(float)

# dfm = dfm[dfm.PLab < 1200]
# dfm = dfm[dfm.PLab > 200]


# dfm.loc[dfm.PLab < 1, 'PLab'] = dfm.loc[dfm.PLab < 1, 'PLab'] * 100

# dfm1 = dfm[dfm.index < '2004']
# dfm2 = dfm[dfm.index >= '2004']


#
# print('ib0', dfm.PLab.median(), 'ib2', dfm.PLab.median())
# print('ib0', dfm.PLab.mean(), 'ib2', dfm.PLab.mean())
print('err', dfm.PLab.mean() - 2*dfm.PLab.std(), dfm.PLab.mean() + 2*dfm.PLab.std())
print(dfm.index)
series = dfm.index.tolist()
print(series)

plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfm.index, dfm.PLab.mean()-2 * dfm.PLab.std(), dfm.PLab.mean()+ 2 *dfm.PLab.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
plt.plot(dfm.index, dfm.PLab,  label="PLab", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfm.PLab.median(), color='grey', label = "Median PLab")
ax.axhline(y=dfm.PLab.mean() + dfm.PLab.std(), color='#1f77b4',linestyle='--', label = "Mean PLab + 1sigma")
ax.axhline(y=dfm.PLab.mean(), color='#1f77b4', label = "Mean PLab")
ax.axhline(y=dfm.PLab.mean() - dfm.PLab.std(), color='#1f77b4',linestyle='--', label = "Mean PLab - 1sigma")
# plt.ylim([-0.1, 0.35])
# plt.ylim([15, 40])

#
# plt.fill_between(dfm1.index, dfm1.PLab.mean()-2 * dfm1.PLab.std(), dfm1.PLab.mean()+ 2 *dfm1.PLab.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
# plt.plot(dfm1.index, dfm1.PLab,  label="PLab", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
# ax.axhline(y=dfm1.PLab.median(), color='grey', label = "Median PLab")
# ax.axhline(y=dfm1.PLab.mean() + dfm1.PLab.std(), color='#1f77b4',linestyle='--', label = "Mean PLab + 1sigma")
# ax.axhline(y=dfm1.PLab.mean(), color='#1f77b4', label = "Mean PLab")
# ax.axhline(y=dfm1.PLab.mean() - dfm1.PLab.std(), color='#1f77b4',linestyle='--', label = "Mean PLab - 1sigma")
#
# plt.fill_between(dfm2.index, dfm2.PLab.mean()-2 * dfm2.PLab.std(), dfm2.PLab.mean()+ 2 *dfm2.PLab.std(), facecolor='#1f77b4', alpha=.2)
# plt.plot(dfm2.index, dfm2.PLab,  label="PLab", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
# ax.axhline(y=dfm2.PLab.median(), color='grey')
# ax.axhline(y=dfm2.PLab.mean() + dfm2.PLab.std(), color='#1f77b4',linestyle='--')
# ax.axhline(y=dfm2.PLab.mean(), color='#1f77b4')
# ax.axhline(y=dfm2.PLab.mean() - dfm2.PLab.std(), color='#1f77b4',linestyle='--')
# # plt.ylim([-0.1, 0.3])


plt.title('Ny-Aalesund PLab time-series')

# ax.legend(loc='lower right', frameon=True, fontsize='small')
ax.legend(loc='best', frameon=True, fontsize='small')

plotname = 'PLab_corrected'
# #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.pdf')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()