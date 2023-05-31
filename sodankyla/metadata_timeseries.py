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

path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
dfmeta = pd.read_csv(path + 'Metadata/All_metadata.csv')

# series = dfmeta[['Date', 'iB1', 'ULab','ULab']]

print(list(dfmeta))
# print(dfmeta[['Date']][0:2])
dfmeta = dfmeta[dfmeta.ULab < 99]
# dfmeta = dfmeta[dfmeta.ULab < 2]
dfmeta = dfmeta[dfmeta.ULab > 10]

print(list(dfmeta))

## dfmeta['Date'] = dfmeta['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
# dfmeta['Date']  = dfmeta['Datenf'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))

print(dfmeta[['Date']][0:2])


# date = datetime.strptime(date_tmp, '%y%m%d')

# print(dfmeta[['Date','Datenf']][0:5])
dfmeta = dfmeta.set_index('Date').sort_index()


# print('ib0', dfmeta.ULab.median(), 'ib2', dfmeta.ULab.median())
# print('ib0', dfmeta.ULab.mean(), 'ib2', dfmeta.ULab.mean())
print('err', dfmeta.ULab.mean() - 2*dfmeta.ULab.std(), dfmeta.ULab.mean() + 2*dfmeta.ULab.std())
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


plt.title('Sodankyla ULab values')
ax.legend(loc='upper right', frameon=True, fontsize='small')

plotname = 'ULab'
# #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.pdf')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()