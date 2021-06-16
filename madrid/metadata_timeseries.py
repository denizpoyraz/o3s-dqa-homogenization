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

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
dfm = pd.read_csv(path + 'Madrid_Metadata.csv')

dfm = dfm[dfm.DateTime > '1993-12-31']


print(list(dfm))
# print(dfm[['Date']][0:2])
# dfm = dfm[dfm.PF < 50]
dfm = dfm[dfm.iB2 < 0.1]
# dfm = dfm[dfm.iB2 > 5]

print(list(dfm))

## dfm['Date'] = dfm['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
# dfm['Date']  = dfm['Datenf'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
dfm['Date'] = dfm['DateTime'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))

print(dfm[['Date']][0:2])
print('dtypes', dfm.dtypes)


# date = datetime.strptime(date_tmp, '%y%m%d')

# print(dfm[['Date','Datenf']][0:5])
dfm = dfm.set_index('Date').sort_index()

dfm['iB0'] = dfm['iB0'].astype(float)
dfm['iB2'] = dfm['iB2'].astype(float)
dfm['iB1'] = dfm['iB1'].astype(float)

#
# print('ib0', dfm.iB2.median(), 'ib2', dfm.iB2.median())
# print('ib0', dfm.iB2.mean(), 'ib2', dfm.iB2.mean())
# print('err', dfm.iB2.mean() - 2*dfm.iB2.std(), dfm.iB2.mean() + 2*dfm.iB2.std())
print(dfm.index)
series = dfm.index.tolist()
print(series)

plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfm.index, dfm.iB1.mean()-2 * dfm.iB1.std(), dfm.iB1.mean()+ 2 *dfm.iB1.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")

plt.plot(dfm.index, dfm.iB1,  label="iB1", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfm.iB1.median(), color='grey', label = "Median iB1")
ax.axhline(y=dfm.iB1.mean() + dfm.iB1.std(), color='#1f77b4',linestyle='--', label = "Mean iB1 + 1sigma")
ax.axhline(y=dfm.iB1.mean(), color='#1f77b4', label = "Mean iB1")
ax.axhline(y=dfm.iB1.mean() - dfm.iB1.std(), color='#1f77b4',linestyle='--', label = "Mean iB1 - 1sigma")
# plt.ylim([-0.1, 0.3])
# plt.fill_between(dfm.index, -0.04242420503016284, 0.11795465516255485, facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")


# plt.title('Madrid iB2 values for homogenization')
plt.title('Madrid iB1 time-series')

# ax.legend(loc='lower right', frameon=True, fontsize='small')
ax.legend(loc='best', frameon=True, fontsize='small')

plotname = 'iB1'
# #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.pdf')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()