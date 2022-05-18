

import pandas as pd
import glob
from datetime import datetime
from re import search
import numpy as np
import matplotlib.pyplot as plt

k = 273.15


path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'

dfmeta = pd.read_csv(path + 'metadata/Scoresby_MetadaAll.csv')


print(list(dfmeta))

# dfmeta = dfmeta[dfmeta.Pground !=  1000.0]
# dfmeta = dfmeta[dfmeta.Pground < 10000]
dfmeta = dfmeta[dfmeta.iB2 < 1]

#
# # some values are in K some in C, to convert them all in C
# dfmeta.loc[dfmeta.Pground > k, 'Pground'] = dfmeta.loc[dfmeta.Pground > k, 'Pground'] - k

# dfmeta['Pground'] = dfmeta['Phip']

print(list(dfmeta))

# dfmeta['Sonde'] = dfmeta['SensorType']

# dfmeta['Date'] = dfmeta['Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
dfmeta['Date'] = pd.to_datetime(dfmeta['Date'], format='%Y%m%d')
# dfmeta['Date'] = dfmeta['Date'].dt.strftime('%Y-%m-%d')


print(dfmeta[['Date']][0:2])

dfmeta = dfmeta.set_index('Date').sort_index()


plt.close('all')
# fig, ax = plt.subplots()
#
# plt.fill_between(dfmeta.index, dfmeta.Pground.mean()-2 * dfmeta.Pground.std(), dfmeta.Pground.mean()+ 2 *dfmeta.Pground.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
# plt.plot(dfmeta.index, dfmeta.Pground,  label="Pground", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
# ax.axhline(y=dfmeta.Pground.median(), color='grey', label = "Median Pground")
# ax.axhline(y=dfmeta.Pground.mean() + dfmeta.Pground.std(), color='#1f77b4',linestyle='--', label = "Mean Pground + 1sigma")
# ax.axhline(y=dfmeta.Pground.mean(), color='#1f77b4', label = "Mean Pground")
# ax.axhline(y=dfmeta.Pground.mean() - dfmeta.Pground.std(), color='#1f77b4',linestyle='--', label = "Mean Pground - 1sigma")
# plt.title('Scoresbysund PLab values')
# # ax.legend(loc='best', frameon=True, fontsize='small')
# ax.legend(loc='lower right ', frameon=True, fontsize='small')
# plotname = 'PLab'

# plt.fill_between(dfmeta.index, dfmeta.iB2.mean()-2 * dfmeta.iB2.std(), dfmeta.iB2.mean()+ 2 *dfmeta.iB2.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
# plt.plot(dfmeta.index, dfmeta.iB2,  label="iB2", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
# ax.axhline(y=dfmeta.iB2.median(), color='grey', label = "Median iB2")
# ax.axhline(y=dfmeta.iB2.mean() + dfmeta.iB2.std(), color='#1f77b4',linestyle='--', label = "Mean iB2 + 1sigma")
# ax.axhline(y=dfmeta.iB2.mean(), color='#1f77b4', label = "Mean iB2")
# ax.axhline(y=dfmeta.iB2.mean() - dfmeta.iB2.std(), color='#1f77b4',linestyle='--', label = "Mean iB2 - 1sigma")
# plt.plot(dfmeta.index, dfmeta.SensorType,  label="SondeType", linestyle = 'None',color = 'red')


# fig, ax = plt.subplots() # Create the figure and axes object
# ax.plot(dfmeta.index, dfmeta.iB2, label="iB2", linestyle='None', color='#1f77b4', marker="o", markersize=3)
#
# ax2=ax.twinx()
# ax2.plot(dfmeta.index, dfmeta.SensorType, label="sensor", linestyle='None', color='red', marker="o", markersize=3)
#
#
#
# plt.title('Scoresbysund iB2, SensorType values')
# # ax.legend(loc='best', frameon=True, fontsize='small')
# ax.legend(loc='lower right ', frameon=True, fontsize='small')
# ax2.legend(loc='lower left ', frameon=True, fontsize='small')


fig, ax = plt.subplots(figsize=(12,5))
ax2 = ax.twinx()
ax.set_title('Scoresbysund iB2, SensorType ')
ax.set_xlabel('Year')
ax2.plot(dfmeta.index, dfmeta['SensorType'], color='red', marker='x', markersize=2, linestyle='None', label = 'Sensor Type')
ax.plot(dfmeta.index, dfmeta['iB2'],  color='#1f77b4', marker="o", markersize=3, linestyle='None', label = 'iB2')
ax.fill_between(dfmeta.index, dfmeta.iB2.mean()-2 * dfmeta.iB2.std(), dfmeta.iB2.mean()+ 2 *dfmeta.iB2.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")


ax.set_ylabel('iB2')
ax2.set_ylabel('Sensor Type')
ax.yaxis.set_label_coords(-.01, .55)
ax2.yaxis.set_label_coords(1.01, .5)

# ax.legend(['GDP Per Capita (US $)'])
# ax2.legend(['Annual Growth Rate (%)'], loc='upper center')
# ax.set_xticks(dfmeta['Date'].dt.date)
# ax.set_xticklabels(dfmeta['Date'].dt.year, rotation=90)
ax.yaxis.grid(color='lightgray', linestyle='dashed')
ax.legend(loc='best', frameon=True, fontsize='small')
ax2.legend(loc='center left', frameon=True, fontsize='small')

plt.tight_layout()

plotname = 'iB2_SensorType'
# #
plt.savefig(path + 'Plots/Metadata/' + plotname + '.eps')
plt.savefig(path + 'Plots/Metadata/' + plotname + '.png')
plt.show()