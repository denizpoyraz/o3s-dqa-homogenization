import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import glob
import matplotlib.dates as mdates


def Calc_average_profile_pressure(dft, xcolumn):
    # nd = len(dataframelist)

    # yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
    #         12, 10, 8, 6]

    yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 325, 300, 275, 250, 240, 230, 220,
            210, 200,
            190, 180, 170, 160, 150, 140, 130, 125, 120, 115, 110, 105, 100, 95, 90, 85, 80, 75, 70, 65, 60, 55,
            50, 45, 40, 35, 30, 28, 26, 24, 22, 20, 19, 18, 17, 16, 15, 14, 13.5, 13, 12.5, 12, 11.5, 11, 10.5,
            10, 9.75, 9.50, 9.25, 9, 8.75, 8.5, 8.25, 8, 7.75, 7.5, 7.25, 7, 6.75, 6.50, 6.25, 6]

    # yref = [i * 250 for i in range(0, 160)]

    n = len(yref) - 1
    Ygrid = [-9999.0] * n

    Xgrid = [-9999.0] * n
    Xsigma = [-9999.0] * n
    #
    # Xgrid = [[-9999.0] * n for i in range(nd)]
    # Xsigma = [[-9999.0] * n for i in range(nd)]

    # for j in range(nd):
    #     dft.PFcor = dft[xcolumn]

    for i in range(n):
        dftmp1 = pd.DataFrame()
        dfgrid = pd.DataFrame()

        grid_min = yref[i + 1]
        grid_max = yref[i]
        Ygrid[i] = (grid_min + grid_max) / 2.0

        filta = dft.Pair >= grid_min
        filtb = dft.Pair < grid_max
        filter1 = filta & filtb
        dftmp1['X'] = dft[filter1][xcolumn]

        filtnull = dftmp1.X > -9999.0
        dfgrid['X'] = dftmp1[filtnull].X

        Xgrid[i] = np.nanmean(dfgrid.X)
        Xsigma[i] = np.nanstd(dfgrid.X)

    return Xgrid, Xsigma, Ygrid


path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
allFiles = sorted(glob.glob(path + "DQA_nors80/*_o3smetadata_nors80.csv"))

# dfmeta = pd.DataFrame()
# metadata = []
#
# for (filename) in (allFiles):
#     print(filename)
#     df = pd.read_csv(filename)
#
#     metadata.append(df)
#
# name_out = 'Madrid_Metada_DQA_nors80'
# dfall = pd.concat(metadata, ignore_index=True)
#
# dfall.to_csv(path + "DQA_nors80/" + name_out + ".csv")
# dfall.to_hdf(path + "DQA_nors80/" + name_out + ".h5", key = 'df')

dfm1 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Madrid_Metada_DQA_nors80.csv')

# /home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Madrid_Metada_DQA_nors80_updated.csv

print(list(dfm1))
#
# dfm2 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_upd/Madrid_Metada_DQA_nors80.csv')
# #
# dfw = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/Madrid_Metadata.csv')
# # print('dfw', list(dfw))
# dfw['DateTime'] = dfw['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d %H'))
# dfw['Date'] = dfw['DateTime'].dt.strftime('%Y-%m-%d')

dfm1['DateTime'] = dfm1['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d %H'))
dfm1['Date'] = dfm1['DateTime'].dt.strftime('%Y-%m-%d')
#
#
# dfw['O3sonde_int_woudc'] = dfw['O3STotal'] - dfw['ResidO3']
# # dfw['O3sonde_total_woudc'] = dfw['O3sonde_int_woudc'] + dfw['ROC']
#
# print(len(dfm1), len(dfm2))
#
# l1 = dfm1.drop_duplicates(['Date']).Date.tolist()
# l2 = dfm2.drop_duplicates(['Date']).Date.tolist()
# common_dates12 = list(set(l1).intersection(set(l2)))
#
# dfm1 = dfm1[dfm1['Date'].isin(common_dates12)]
# dfm2 = dfm2[dfm2['Date'].isin(common_dates12)]
#
# print(list(dfm1))
# print('before', len(dfm1))
dfm1 = dfm1[dfm1.O3Sonde_hom != 0]
dfm1 = dfm1[dfm1.O3Sonde_hom < 999]
dfm1 = dfm1[dfm1.O3Sonde < 999]
dfm1 = dfm1[dfm1.O3Sonde > 0]

dfm1 = dfm1[dfm1.O3ratio_hom < 999]
dfm1 = dfm1[dfm1.O3ratio < 999]
dfm1 = dfm1[dfm1.O3ratio_raw < 999]
dfm1 = dfm1[dfm1.O3Sonde_raw < 999]
# # dfm1 = dfm1[dfm1.o3max_raw < 999]
# dfm1 = dfm1[dfm1.o3max < 999]
# dfm1 = dfm1[dfm1.o3max_hom < 999]
# dfm1 = dfm1[dfm1.o3min_raw < 999]
# dfm1 = dfm1[dfm1.o3min < 999]
# dfm1 = dfm1[dfm1.o3min_hom < 999]
# dfm1 = dfm1[dfm1.o3min > 0]

# Plotname = 'TON_sonde_10hpa'
# # Plotname = 'burst'
#


print(dfm1.DateTime.min(), dfm1.DateTime.max())

Plotname = 'TON_factor_DQAvsRaw_nolines'

fig, axs = plt.subplots(1, sharex=True, sharey=False, figsize=(17, 9))
# fig.suptitle('Sharing both axes')
# axs[0].plot(x, y ** 2)
# axs[1].plot(x, 0.3 * y, 'o')
# axs[2].plot(x, y, '+')
#
# axs.plot(dfm1.DateTime, dfm1.O3Sonde_10hpa, label = 'O3Sonde WOUDC 10 hPa',  marker = ".")
# axs.plot(dfm1.DateTime, dfm1.O3Sonde_hom_10hpa, label = 'O3Sonde DQA 10 hPa',  marker = ".")
# axs.plot(dfm1.DateTime, dfm1.O3Sonde_10hpa_raw, label = 'O3Sonde Raw 10 hPa',  marker = ".")

# dfm1['R'] = (dfm1.O3Sonde_hom_10hpa - dfm1.O3Sonde_10hpa_raw) / dfm1.O3Sonde_10hpa_raw * 100

axs.plot(dfm1.DateTime, dfm1.O3SondeTotal_hom, label='DQA - WOUDC / DQA', marker=".", linestyle='None')

# axs.plot(dfm1.DateTime, dfm1.O3ratio, label = 'TON WOUDC',  marker = ".",  linestyle = ''None'')
# axs.plot(dfm1.DateTime, dfm1.O3ratio_hom, label = 'TON DQA',  marker = ".", linestyle = ''None'')

# axs.plot(dfm1.DateTime, dfm1.O3ratio, label = 'TON WOUDC',  marker = ".")
# axs.plot(dfm1.DateTime, dfm1.O3ratio_hom, label = 'TON DQA',  marker = ".")
# axs.plot(dfm1.DateTime, dfm1.O3ratio_raw, label = 'TON Raw',  marker = ".", linestyle = ''None'')
# axs.axhline(y=1, color='grey', linestyle=':')

# axs.set_xticks(np.arange(0, len(dfm1)+1, xfreq))
axs.set_ylabel('%')
# axs.set_ylim(0.9, 1.1)

# axs.set_ylabel('O3 [DU]')
# axs.set_ylim(150, 450)
axs.xaxis.set_major_locator(mdates.YearLocator(1))
axs.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# axs.set_xlim('1994-01-01', '2021-01-01')

axs.legend(loc="upper right")

#
# plt.xticks(rotation = 45)

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON_updated/  ' + Plotname + '.pdf')

plt.show()
plt.close()

dfm1['ratio'] = dfm1['BrewO3']/dfm1['O3SondeTotal']
dfm1['ratio_raw'] = dfm1['BrewO3']/dfm1['O3SondeTotal_raw']
dfm1['ratio_hom'] = dfm1['BrewO3']/dfm1['O3SondeTotal_hom']

dfm1 = dfm1[dfm1.ratio < 2]
dfm1 = dfm1[dfm1.ratio > 0.5]


print(dfm1.DateTime.min(), dfm1.DateTime.max())

Plotname = 'TON_sonde_woudc_nors80'

fig, axs = plt.subplots(3, sharex=True, sharey=False, figsize=(17, 9))
fig.suptitle('Madrid TO and TON values')

axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_hom, label = 'O3Sonde DQA',  marker = "s", linestyle='None', markersize = 4)
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_raw, label = 'O3Sonde Raw',  marker = ".", linestyle='None')
axs[0].plot(dfm1.DateTime, dfm1.O3Sonde, label = 'O3Sonde WOUDC',  marker = ".",  linestyle='None')

axs[0].set_ylabel('O3 [DU]')
axs[0].set_ylim(100, 500)

axs[0].legend(loc="upper right")

#

axs[1].plot(dfm1.DateTime, dfm1.BrewO3, label = 'Brewer TO',  marker = ".", linestyle='None')
axs[1].set_ylabel('O3 [DU]')
axs[1].legend(loc="upper right")

axs[2].plot(dfm1.DateTime, dfm1.ratio_hom, label = 'TON DQA',  marker = "s", linestyle='None', markersize = 4)
# axs[2].plot(dfm1.DateTime, dfm1.ratio_raw, label = 'TON Raw ',  marker = ".", linestyle='None')
axs[2].plot(dfm1.DateTime, dfm1.ratio, label = 'TON WOUDC',  marker = ".", linestyle='None')

axs[2].set_ylabel('TON')
axs[2].legend(loc="upper right")
# axs[3].set_ylim(0.9, 1.1)
axs[2].set_ylim(0.7, 1.4)

axs[2].axhline(y=1, color='grey', linestyle ="-")

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON_updated/  ' + Plotname + '.pdf')
#
plt.show()



# Plotname = 'TON_allplots_woudc'
#
# fig, axs = plt.subplots(4, sharex=False, sharey=False, figsize=(17, 9))
# # fig.suptitle('Sharing both axes')
# # axs[0].plot(x, y ** 2)
# # axs[1].plot(x, 0.3 * y, 'o')
# # axs[2].plot(x, y, '+')
#
# # original
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_hom_10hpa, label='O3Sonde DQA 10hPa', marker=".")
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_10hpa, label='O3Sonde WOUDC 10hPa', marker=".")
# # axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_10hpa_raw, label = 'O3Sonde Raw 10hPa',  marker = "." )
# axs[0].xaxis.set_major_locator(mdates.YearLocator(1))
# axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# axs[0].set_ylabel('O3 [DU]')
# axs[0].legend(loc="upper right")
#
# axs[1].plot(dfm1.DateTime, dfm1.O3SondeTotal_hom, label='Total O3 DQA', marker=".")
# axs[1].plot(dfm1.DateTime, dfm1.O3SondeTotal, label='Total O3 WOUDC', marker=".")
# # axs[1].plot(dfm1.DateTime, dfm1.O3SondeTotal_raw, label = 'Total O3 Raw',  marker = "." )
# axs[1].xaxis.set_major_locator(mdates.YearLocator(1))
# axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# axs[1].set_ylabel('O3 [DU]')
# axs[1].legend(loc="upper right")
# #
# axs[2].plot(dfm1.DateTime, dfm1.O3SondeTotal, label='O3Sonde WOUDC + ROC', marker=".")
# # axs[2].plot(dfm1.DateTime, dfm1.O3SondeTotal_hom, label = 'O3Sonde_DQA + ROC',  marker = ".", linestyle = ''None'')
# # axs[2].plot(dfm1.DateTime, dfm1.BrewO3, label = 'Brewer', marker = ".",  linestyle = ''None'')
# # axs[2].plot(dfm1.DateTime, dfm1.O3SondeTotal_hom, label = 'O3Sonde_DQA + ROC',  marker = "." )
# axs[2].plot(dfm1.DateTime, dfm1.BrewO3, label='Brewer', marker=".")
# axs[2].xaxis.set_major_locator(mdates.YearLocator(1))
# axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# axs[2].set_ylabel('O3 [DU]')
# axs[2].legend(loc="upper right")
#
# #
# axs[3].plot(dfm1.DateTime, dfm1.O3ratio_hom, label='O3 Ratio DQA', marker=".")
# # axs[3].plot(dfm1.DateTime, dfm1.O3ratio, label = 'O3 Ratio WOUDC', marker = ".")
# axs[3].plot(dfm1.DateTime, dfm1.O3ratio_raw, label='O3 Ratio Raw', marker=".")
# axs[3].xaxis.set_major_locator(mdates.YearLocator(1))
# axs[3].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# axs[3].set_ylabel('O3 ratio')
# axs[3].axhline(y=1, color='grey', linestyle=':')
# axs[3].legend(loc="upper right")
# #
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.eps')
# # plt.savefig(path + 'Plots/TON_updated/  ' + Plotname + '.pdf')
# #
# plt.show()

