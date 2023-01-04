import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime
import matplotlib.pyplot as plt


allFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_public/Files/valentia/DQA_nors80/*all_hom_nors80.hdf"))

list_data = []

km_low = [0, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
km_up = [i + 0.1 for i in km_low]
tpump = [0]* len(km_low)
tpump_cor = [0]*len(km_low)
stpump = ['tpump_' + str(i) for i in km_low]
stpump_cor = ['tpumpcor_' + str(i) for i in km_low]

avg_km = [0]*len(km_low)
avgcor_km = [0]*len(km_low)

min_km = [0]*len(km_low)
mincor_km = [0]*len(km_low)

max_km = [0]*len(km_low)
maxcor_km = [0]*len(km_low)

###
avg_kmcp = [0]*len(km_low)
avgcor_kmcp = [0]*len(km_low)

min_kmcp = [0]*len(km_low)
mincor_kmcp = [0]*len(km_low)

max_kmcp = [0]*len(km_low)
maxcor_kmcp = [0]*len(km_low)

middle = [0]*len(km_low)
#
#
# for (filename) in (allFiles):
#
#     df = pd.read_hdf(filename)
#     date = df.at[df.first_valid_index(), 'Date']
#     df['Alt'] = df['Height']/1000
#
#     # if date > '19940101':continue
#     print(filename)
#
#     # print((tpump_30))
#     dft = pd.DataFrame()
#
#     for k in range(len(km_low)):
#         # print(k)
#         tpump[k] = np.mean(df.loc[(df.Alt < km_up[k]) & (df.Alt > km_low[k]), 'TboxK'].tolist())
#         tpump_cor[k] = np.mean(df.loc[(df.Alt < km_up[k]) & (df.Alt > km_low[k]), 'Tpump_cor'].tolist())
#
#
#         dft.at[0,'Date'] = date
#         dft.at[0,stpump[k]] = tpump[k]
#         dft.at[0,stpump_cor[k]] = tpump_cor[k]
#
#     list_data.append(dft)
#
# dff = pd.concat(list_data, ignore_index=True)
# csvall =  "/home/poyraden/Analysis/Homogenization_public/Files/valentia/TPump_data.csv"
#
# # dff.to_hdf(hdfall, key = 'df')
# dff.to_csv(csvall)

#plotting
path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'
df = pd.read_csv( "/home/poyraden/Analysis/Homogenization_public/Files/valentia/TPump_data.csv")
dfcp = df.copy()
# df = df[df.Date > 19920101]
# dfcp = dfcp[dfcp.Date > 20160101]
# df = df[df.Date < 19970101]
# df = df[df.Date > 20160101]

# df['DateTime'] = pd.to_datetime(df['Date'], format='%Y%m%d')
df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

df['DateTimecp'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
#
# df = df.resample('M', on='DateTime').median()
# df['DateTimecp'] = pd.to_datetime(df['Date'], format='%Y%m%d')
# df['DateTimecp'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
#
df['Dt'] = df['DateTimecp'].apply(lambda x: x.date())
# df['Dt'] = df.index.apply(lambda x: x.date())

#
# df['value_is_NaN'] = 0
#
# df.loc[df['Date'].isnull(), 'value_is_NaN'] = 1
# df = df[df.value_is_NaN == 0]

for k in range(len(km_low)):

    print('woudc ', k, df[stpump[k]].median())
    print('daq ', k, df[stpump_cor[k]].median())
    medw = round(df[stpump[k]].median(), 2)
    medd = round(df[stpump_cor[k]].median(), 2)


    fig, ax = plt.subplots(figsize=(17, 9))
    plot_title = 'Valentia Pump temperature time series (' + str(km_low[k]) + 'km) WOUDC files'
    plt.title(plot_title)
    # plt.plot(df.index, df[stpump[k]], label = 'WOUDC, Median TPump = ' + str(df[stpump[k]].median()))
    # plt.plot(df.index, df[stpump_cor[k]], label = 'DQA, Median TPump = ' + str(df[stpump_cor[k]].median()))
    plt.plot(df.Dt, df[stpump[k]], label='WOUDC, Median TPump = ' + str(medw))
    plt.plot(df.Dt, df[stpump_cor[k]], label='DQA, Median TPump = ' + str(medd))
    ax.axhline(y=df[stpump[k]].median(), color='tab:blue', linestyle=":")
    ax.axhline(y=df[stpump_cor[k]].median(), color='tab:orange', linestyle=":")


    ax.legend(loc='best', frameon=True, fontsize='small')

    # plt.plot(df.Dt, df[stpump[k]])

    plt.ylim([260,330])

    # plt.savefig(path + 'Plots/TPump/Monthly_All_' + str(km_low[k]) + '.png')
    plt.savefig(path + 'Plots/TPump/All_v2_' + str(km_low[k]) + '.png')

    # plt.show()
    plt.close()
    #
    # fig, ax = plt.subplots(figsize=(17, 9))
    # plot_title = 'Valentia Pump temperature time series (' + str(km_low[k]) + 'km) DQA files'
    # plt.title(plot_title)
    # plt.ylim([260,330])
    #
    # # plt.plot(df.Dt, df[stpump_cor[k]], color = 'tab:orange')
    # plt.plot(df.index, df[stpump_cor[k]], color = 'tab:orange')
    #
    # plt.savefig(path + 'Plots/TPump/DQA_' + str(km_low[k]) + '.png')
    # # plt.show()
    # plt.close()

    #average profiles
    avg_km[k] = df[stpump[k]].mean()
    avgcor_km[k] = df[stpump_cor[k]].mean()

    min_km[k] = df[stpump[k]].min()
    mincor_km[k] = df[stpump_cor[k]].min()

    max_km[k] = df[stpump[k]].max()
    maxcor_km[k] = df[stpump_cor[k]].max()

    # average profiles
    avg_kmcp[k] = dfcp[stpump[k]].mean()
    avgcor_kmcp[k] = dfcp[stpump_cor[k]].mean()

    min_kmcp[k] = dfcp[stpump[k]].min()
    mincor_kmcp[k] = dfcp[stpump_cor[k]].min()

    max_kmcp[k] = dfcp[stpump[k]].max()
    maxcor_kmcp[k] = dfcp[stpump_cor[k]].max()

    # print(km_low[k])
    # print('before 2016', avg_km[k])
    # print('after 2016', avg_kmcp[k])
    # print('average',(avg_km[k] - avg_kmcp[k])/2 )
    middle[k] =(avg_km[k] - avg_kmcp[k])/2

print('middle', middle)

fig, ax = plt.subplots(figsize=(17, 9))
# plot_title = 'Valentia Pump temperature 2016-2022'
# plot_title = 'Valentia Pump temperature 1997-2015'
plot_title = 'Valentia Pump temperature '

plt.title(plot_title)
plt.ylabel('Altitude [km]')
plt.xlabel('Temperature [K]')

plt.xlim([280,305])
# plt.plot(avg_km, km_low, color = 'tab:blue', label = 'WOUDC before 2016')
# plt.plot( avgcor_km,km_low, color = 'tab:orange', label = 'DQA before 2016')
plt.plot(avg_km, km_low, label = 'WOUDC')
# plt.plot( avgcor_km,km_low,label = 'DQA before 2016')

# plt.plot(avg_kmcp, km_low, label = 'WOUDC after 2016')
plt.plot( avgcor_kmcp,km_low,label = 'DQA')
ax.legend(loc='best', frameon=True, fontsize='small')


# plt.savefig(path + 'Plots/TPump/Averaged_TPump_after2016.png')
# plt.savefig(path + 'Plots/TPump/Averaged_TPump_1997-2015.png')
plt.savefig(path + 'Plots/TPump/Averaged_TPump.png')


plt.show()
plt.close()

# fig, ax = plt.subplots(figsize=(17, 9))
# plot_title = 'Valentia Pump temperature minimum values'
# plt.title(plot_title)
# # plt.ylim([260,330])
# plt.plot(min_km, km_low, color = 'tab:blue', label = 'WOUDC')
# plt.plot( mincor_km,km_low, color = 'tab:orange', label = 'DQA')
# ax.legend(loc='best', frameon=True, fontsize='small')
#
# plt.savefig(path + 'Plots/TPump/Minimum_TPump_after1997.png')
# plt.show()
# plt.close()
#
# fig, ax = plt.subplots(figsize=(17, 9))
# plot_title = 'Valentia Pump temperature maximum values'
# plt.title(plot_title)
# # plt.ylim([260,330])
# plt.plot(max_km, km_low, color = 'tab:blue', label = 'WOUDC')
# plt.plot( maxcor_km,km_low, color = 'tab:orange', label = 'DQA')
# ax.legend(loc='best', frameon=True, fontsize='small')
#
# plt.savefig(path + 'Plots/TPump/Maximum_TPump_after1997.png')
# plt.show()
# plt.close()