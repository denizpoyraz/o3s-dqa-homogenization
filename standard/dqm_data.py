import pandas as pd
import numpy as np
from re import search
from datetime import datetime
import matplotlib as plt
from functions.dqm_functions import read_woudc, calc_average_profile_pressure
import glob


# read woudc files
# check metadata:
# important variables needed for O3 calculation: background current,
# calculate the averaged values of each variable

path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/WOUDC_nors80/DQM/'
name = 'lauder_alldata'
namem = 'lauder_allmetadata'

df1 = pd.read_hdf(path + name + '.h5')
print(list(df1))

df1['Pair'] = df1['Pressure']


o3, o3err, y = calc_average_profile_pressure(df1, 'O3PartialPressure')
eo3, eo3err, y = calc_average_profile_pressure(df1, 'UncO3PartialPressure')
current, currenterr, y = calc_average_profile_pressure(df1, 'SondeCurrent')
temp, temperr, y = calc_average_profile_pressure(df1, 'TemperatureSonde')

df1 = pd.DataFrame()
df1['o3c'] = o3
df1['y'] = y

# df2 = pd.DataFrame()
# df1['o3nc'] = o3nc
# df1['y'] = y

int1 =  int((3.9449 * (df1.o3.shift() + df1.o3) * np.log(df1.y.shift() / df1.y)).sum())
# int2 =  int((3.9449 * (df1.o3nc.shift() + df1.o3nc) * np.log(df1.y.shift() / df1.y)).sum())

Plotname = 'After_1998_hom_vs_raw'
# Plotname = 'RS80'

fig, ax = plt.subplots(figsize=(17, 9))


ax.plot(o3, y,  label = ' > 1998 DQA ' + 'TO=' + str(int1), marker = 's', markersize = 6)
# ax.plot(o3nc, y,  label = ' > 1998 Raw ' + 'TO=' + str(int2), marker = 's', markersize = 6)

# ax.plot(o3, y , label = ' < 1995 WOUDC', marker = 'd', markersize = 6)
# ax.plot(o3nc, y,  label = '< 1995 Raw', marker = 's', markersize = 6)

# ax.plot(o3, y,  label = '1994-2006 RS80 correction', marker = 's', markersize = 6)
# ax.plot(o3c, y , label = '1994-2006 no RS80 correction', marker = 'd', markersize = 6)
ax.set_ylim(1000, 5)
ax.set_yscale('log')
ax.legend(loc="best")
ax.set_ylabel('Pressure [hPa]')
ax.set_xlabel('PO3 [mPa]')

# plt.savefig(path + 'Plots/' + Plotname + '.png')
# plt.savefig(path + 'Plots/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/  ' + Plotname + '.pdf')

plt.show()
