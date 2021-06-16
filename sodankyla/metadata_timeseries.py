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

# series = dfmeta[['Date', 'iB1', 'iB2','iB2']]

print(list(dfmeta))
# print(dfmeta[['Date']][0:2])
dfmeta = dfmeta[dfmeta.iB1 < 2]
# dfmeta = dfmeta[dfmeta.iB1 < 0.1]
# dfmeta = dfmeta[dfmeta.iB2 > 5]

print(list(dfmeta))

## dfmeta['Date'] = dfmeta['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
# dfmeta['Date']  = dfmeta['Datenf'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))

print(dfmeta[['Date']][0:2])


# date = datetime.strptime(date_tmp, '%y%m%d')

# print(dfmeta[['Date','Datenf']][0:5])
dfmeta = dfmeta.set_index('Date').sort_index()


# print('ib0', dfmeta.iB2.median(), 'ib2', dfmeta.iB2.median())
# print('ib0', dfmeta.iB2.mean(), 'ib2', dfmeta.iB2.mean())
print('err', dfmeta.iB1.mean() - 2*dfmeta.iB1.std(), dfmeta.iB1.mean() + 2*dfmeta.iB1.std())
print(dfmeta.index)
series = dfmeta.index.tolist()
print(series)

plt.close('all')
fig, ax = plt.subplots()
#
plt.fill_between(dfmeta.index, dfmeta.iB1.mean()-2 * dfmeta.iB1.std(), dfmeta.iB1.mean()+ 2 *dfmeta.iB1.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")

plt.plot(dfmeta.index, dfmeta.iB1,  label="iB1", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
ax.axhline(y=dfmeta.iB1.median(), color='grey', label = "Median iB1")
ax.axhline(y=dfmeta.iB1.mean() + dfmeta.iB1.std(), color='#1f77b4',linestyle='--', label = "Mean iB1 + 1sigma")
ax.axhline(y=dfmeta.iB1.mean(), color='#1f77b4', label = "Mean iB1")
ax.axhline(y=dfmeta.iB1.mean() - dfmeta.iB1.std(), color='#1f77b4',linestyle='--', label = "Mean iB1 - 1sigma")
# plt.ylim([-0.1, 0.3])
# plt.fill_between(dfmeta.index, -0.04242420503016284, 0.11795465516255485, facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")


plt.title('Sodankyla iB1 values')
ax.legend(loc='upper right', frameon=True, fontsize='small')

plotname = 'iB1'
#
plt.savefig(path + 'Plots/Metadata/' + plotname + '.pdf')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')


plt.show()