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

    yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600,  550, 500, 450,  400, 350, 325, 300, 275, 250, 240, 230, 220, 210, 200,
            190, 180, 170, 160, 150, 140, 130, 125, 120, 115, 110, 105,  100,95, 90, 85, 80, 75, 70, 65, 60, 55,
            50, 45, 40,  35, 30, 28, 26, 24, 22,  20, 19, 18, 17, 16, 15,  14, 13.5, 13, 12.5,  12, 11.5, 11, 10.5,
            10, 9.75, 9.50, 9.25, 9, 8.75, 8.5, 8.25,  8, 7.75, 7.5, 7.25,  7, 6.75, 6.50, 6.25, 6]

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


        grid_min = yref[i+1]
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
# allFiles = sorted(glob.glob(path + "DQA_nors80/*_o3smetadata_nors80.csv"))
#
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
# dfm2 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_upd/Madrid_Metada_DQA_rs80.csv')
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

Plotname = 'TON_factor_nolines'

fig, axs = plt.subplots(1, sharex=True, sharey=False, figsize=(17, 9))
# fig.suptitle('Sharing both axes')
# axs[0].plot(x, y ** 2)
# axs[1].plot(x, 0.3 * y, 'o')
# axs[2].plot(x, y, '+')
#
# axs.plot(dfm1.DateTime, dfm1.O3Sonde_10hpa, label = 'O3Sonde WOUDC 10 hPa',  marker = ".")
# axs.plot(dfm1.DateTime, dfm1.O3Sonde_hom_10hpa, label = 'O3Sonde DQA 10 hPa',  marker = ".")
# axs.plot(dfm1.DateTime, dfm1.O3Sonde_10hpa_raw, label = 'O3Sonde Raw 10 hPa',  marker = ".")

dfm1['R'] = (dfm1.O3Sonde_hom_10hpa - dfm1.O3Sonde_10hpa)/ dfm1.O3Sonde_hom_10hpa * 100

axs.plot(dfm1.DateTime, dfm1.R, label = 'RMI - WOUDC / RMI',  marker = ".")



# axs.plot(dfm1.DateTime, dfm1.O3ratio, label = 'TON WOUDC',  marker = ".",  linestyle = 'None')
# axs.plot(dfm1.DateTime, dfm1.O3ratio_hom, label = 'TON DQA',  marker = ".", linestyle = 'None')

# axs.plot(dfm1.DateTime, dfm1.O3ratio, label = 'TON WOUDC',  marker = ".")
# axs.plot(dfm1.DateTime, dfm1.O3ratio_hom, label = 'TON DQA',  marker = ".")
# axs.plot(dfm1.DateTime, dfm1.O3ratio_raw, label = 'TON Raw',  marker = ".", linestyle = 'None')
axs.axhline(y=1, color='grey', linestyle=':')

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
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON_updated/  ' + Plotname + '.pdf')

plt.show()
plt.close()

Plotname = 'TON_allplots_v3'

fig, axs = plt.subplots(4, sharex=False, sharey=False, figsize=(17, 9))
# fig.suptitle('Sharing both axes')
# axs[0].plot(x, y ** 2)
# axs[1].plot(x, 0.3 * y, 'o')
# axs[2].plot(x, y, '+')

#original
axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_hom_10hpa, label = 'O3Sonde DQA 10hPa',  marker = ".")
axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_10hpa, label = 'O3Sonde WOUDC 10hPa',  marker = ".")
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_10hpa_raw, label = 'O3Sonde Raw 10hPa',  marker = ".")
axs[0].xaxis.set_major_locator(mdates.YearLocator(1))
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axs[0].set_ylabel('O3 [DU]')
axs[0].legend(loc="upper right")



axs[1].plot(dfm1.DateTime, dfm1.O3SondeTotal_hom, label = 'Total O3 DQA',  marker = ".")
# axs[1].plot(dfm1.DateTime, dfm1.O3SondeTotal, label = 'Total O3 WOUDC',  marker = ".")
axs[1].plot(dfm1.DateTime, dfm1.O3SondeTotal_raw, label = 'Total O3 Raw',  marker = ".")
axs[1].xaxis.set_major_locator(mdates.YearLocator(1))
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axs[1].set_ylabel('O3 [DU]')
axs[1].legend(loc="upper right")
#
# axs[1].plot(dfm1.DateTime, dfm1.O3SondeTotal, label = 'O3Sonde + ROC')
# axs[1].plot(dfm1.DateTime, dfm1.O3SondeTotal_hom, label = 'O3Sonde_DQA + ROC')
axs[2].plot(dfm1.DateTime, dfm1.BrewO3, label = 'Brewer', marker = ".")
axs[2].xaxis.set_major_locator(mdates.YearLocator(1))
axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axs[2].set_ylabel('O3 [DU]')
axs[2].legend(loc="upper right")
#
# axs[2].plot(dfm1.DateTime, dfm1.O3Sonde - dfm1.O3Sonde_hom, label = 'O3Sonde diff (no dqa - dqa)')
# axs[2].plot(dfm1.DateTime, dfm1.O3SondeTotal - dfm1.O3SondeTotal_hom, label = 'O3Sonde + ROC diff (no dqa - dqa)')
# # axs[2].plot(dfm1.DateTime, dfm1.BrewO3, label = 'Brewer')
# axs[2].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs[2].set_xticklabels(xtick_labels, rotation=0)
# # axs[2].set_ylabel('O3 [DU]')
# axs[2].legend(loc="upper right")
#
# axs[3].plot(dfm1.DateTime, dfm1.BrewO3, label = 'Brewer')
# axs[3].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs[3].set_xticklabels(xtick_labels, rotation=0)
# axs[3].set_ylabel('O3 [DU]')
# axs[3].legend(loc="upper right")
#
axs[3].plot(dfm1.DateTime, dfm1.O3ratio_hom, label = 'O3 Ratio DQA', marker = ".")
# axs[3].plot(dfm1.DateTime, dfm1.O3ratio, label = 'O3 Ratio WOUDC', marker = ".")
axs[3].plot(dfm1.DateTime, dfm1.O3ratio_raw, label = 'O3 Ratio Raw', marker = ".")
axs[3].xaxis.set_major_locator(mdates.YearLocator(1))
axs[3].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axs[3].set_ylabel('O3 ratio')
axs[3].axhline(y=1, color='grey', linestyle=':')
axs[3].legend(loc="upper right")
#
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON_updated/  ' + Plotname + '.pdf')
#
plt.show()


# axs[0].plot(dfw.Date, dfw.O3sonde_int_woudc, label = 'O3 Sonde from metadata (O3S - Residual)', marker = ".", color = '#ff7f0e')
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_burst , label = 'O3 Sonde WOUDC int until burst', marker = ".", color = '#1f77b4')
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_hom_burst , label = 'O3 Sonde DQA int until burst', marker = ".", color = '#bcbd22')
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_burst , label = 'O3 Sonde WOUDC int until burst', marker = ".")
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_hom_burst , label = 'O3 Sonde DQA int until burst', marker = ".")

# axs[1].plot(dfm1.DateTime, dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst , label = 'O3Sonde DQA - WOUDC', marker = ".")
# axs[1].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # axs[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[1].set_ylabel('O3 [DU]')
# # axs[1].set_ylim(11, 3)
# axs[1].legend(loc="upper right")

# axs[1].plot(dfm1.DateTime, 100 * (dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst)/dfm1.O3Sonde_burst , label = 'O3Sonde DQA - WOUDC [%]', marker = ".")
# axs[1].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[1].set_ylabel('%')
# # axs[2].set_ylim(11, 3)
# axs[1].legend(loc="upper right")
#
# # axs[3].plot(dfm1.DateTime, dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst_raw , label = 'O3Sonde DQA - Raw', marker = ".")
# # axs[3].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# # axs[3].set_ylabel('O3 [DU]')
# # # axs[2].set_ylim(11, 3)
# # axs[3].legend(loc="upper right")
#
# axs[2].plot(dfm1.DateTime, (dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst_raw)/dfm1.O3Sonde_burst_raw * 100 , label = 'O3Sonde DQA - Raw [%]', marker = ".")
# axs[2].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[2].set_ylabel('%')
# # axs[2].set_ylim(11, 3)
# axs[2].legend(loc="upper right")
#
# axs[3].plot(dfm1.DateTime, dfm1.o3max, label = 'O3S Max WOUDC', marker = ".")
# axs[3].plot(dfm1.DateTime, dfm1.o3max_hom, label = 'O3S Max DQA', marker = ".")
# axs[3].plot(dfm1.DateTime, dfm1.o3max_raw, label = 'O3S Max Raw', marker = ".")
# axs[3].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[3].set_ylabel('O3 [DU]')
# # axs[2].set_ylim(11, 3)
# axs[3].legend(loc="upper right")
#
# axs[4].plot(dfm1.DateTime, (dfm1.o3max_hom - dfm1.o3max)/dfm1.o3max * 100, label = 'DQA - WOUDC (o3max) [%]', marker = ".")
# axs[4].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[4].set_ylabel('%')
# # axs[2].set_ylim(11, 3)
# axs[4].legend(loc="upper right")
#
# # axs[5].plot(dfm1.DateTime, (dfm1.o3min_hom - dfm1.o3min)/dfm1.o3min * 100, label = 'DQA - WOUDC (o3min) [%]', marker = ".")
# # axs[5].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# # axs[5].set_ylabel('%')
# # # axs[2].set_ylim(11, 3)
# # axs[5].legend(loc="upper right")

#
# fig, ax1 = plt.subplots(figsize=(17, 9))
#
# ax1.plot(dfm1.DateTime, dfm1.O3Sonde, label = 'O3 Sonde WOUDC until 10hPa', marker = ".")
# ax1.plot(dfm1.DateTime, dfm1.O3Sonde_hom, label = 'O3 Sonde DQA until 10hPa', marker = ".")
# # # ax1.plot(dfm1.DateTime, dfm1.O3Sonde_raw - dfm1.ROC, label = 'O3 Sonde Raw', marker = ".")
# # ax1.plot(dfw.Date, dfw.O3sonde_int_woudc, label = 'O3 Sonde from metadata (O3S - Residual)', marker = ".")
# # ax1.plot(dfm1.DateTime, dfm1.O3Sonde_burst , label = 'O3 Sonde WOUDC int until burst', marker = ".")
# # ax1.plot(dfm1.DateTime, dfm1.O3Sonde_hom_burst , label = 'O3 Sonde DQA int until burst', marker = ".")
# # ax1.plot(dfm1.DateTime, dfm1.burst , label = 'burst pressure', marker = ".")
# ## ax1.plot(dfm1.DateTime, dfm1.O3Sonde , label = 'O3 Sonde WOUDC', marker = ".")
# # ax1.plot(dfm1.DateTime, dfm1.O3Sonde_hom, label = 'O3 Sonde DQA', marker = ".")
# # ax1.plot(dfm1.DateTime, dfm1.O3Sonde_raw, label = 'O3 Sonde Raw', marker = ".")
# # ax1.plot(dfw.Date, dfw.O3sonde_total_woudc, label = 'O3 Sonde from metadata', marker = ".")
#
# # ax1.plot(dfm.Date, dfm.BrewO3, label = 'Brewer')
# # ax1.plot(dfm.Date, dfm.O3ratio, label = 'O3 Ratio')
# # ax1.plot(dfm.Date, dfm.O3ratio_hom, label = 'O3 Ratio DQA')
# ax1.set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax1.set_xticklabels(xtick_labels, rotation=0)
# plt.xticks(rotation = 45)
#
# ax1.set_ylabel('O3 [DU]')
# # ax1.set_ylabel('P Air [hPa]')
#
# # ax1.set_ylabel('O3 ratio')
# # ax1.set_ylim(0.8,1.2)
#
# ax1.axhline(y=1, color='grey', linestyle=':')
# ax1.legend(loc="upper right")
#
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON_updated/  ' + Plotname + '.pdf')
#
# plt.show()
# plt.close()

# Plotname = 'TON_sonde_burst_stepbystep_corrections_zoom'
#
# fig, axs = plt.subplots(6, sharex=True, sharey=False, figsize=(17, 9))
# # fig.suptitle('Sharing both axes')
# # axs[0].plot(x, y ** 2)
# # axs[1].plot(x, 0.3 * y, 'o')
# # axs[2].plot(x, y, '+')
#
# axs[0].plot(dfm1.DateTime, 100*(dfm1.O3Sonde_burst_etabkg - dfm1.O3Sonde_burst_raw)/dfm1.O3Sonde_burst_raw , label = 'Effect of Bkg corr. on TO [%] ',  marker = ".")
# # axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_burst_etabkgtpump, label = 'O3Sonde  Pump Temp. corr.',  marker = ".")
# # axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_burst_etabkgtpumpphigr, label = 'O3Sonde Pump grounf corr.',  marker = ".")
# # axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_burst_etabkgtpumpphigref, label = 'O3Sonde Pump Eff. corr.',  marker = ".")
# axs[0].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs[0].set_ylabel('%')
# axs[0].set_ylim(-5, 5)
#
# axs[0].legend(loc="upper right")
#
# axs[1].plot(dfm1.DateTime, 100*(dfm1.O3Sonde_burst_etabkgtpump - dfm1.O3Sonde_burst_etabkg)/dfm1.O3Sonde_burst_etabkg ,
#             label = 'Effect of Pump Temp. corr. on TO [%] ',  marker = ".")
# axs[1].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # axs[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[1].set_ylabel('%')
# axs[1].set_ylim(0, 5)
# axs[1].legend(loc="upper right")
#
# axs[2].plot(dfm1.DateTime, 100*(dfm1.O3Sonde_burst_etabkgtpumpphigr - dfm1.O3Sonde_burst_etabkgtpump)/dfm1.O3Sonde_burst_etabkgtpump ,
#             label = 'Effect of PF humidity corr. on TO [%] ',  marker = ".")
# axs[2].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[2].set_ylabel('%')
# axs[2].set_ylim(-5, 5)
# axs[2].legend(loc="upper right")
#
# axs[3].plot(dfm1.DateTime, 100*(dfm1.O3Sonde_burst_etabkgtpumpphigref - dfm1.O3Sonde_burst_etabkgtpumpphigr)/dfm1.O3Sonde_burst_etabkgtpumpphigr ,
#             label = 'Effect of PF Eff. corr. on TO [%] ',  marker = ".")
# axs[3].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[3].set_ylabel('%')
# axs[3].set_ylim(-5, 5)
# axs[3].legend(loc="upper right")
#
# axs[4].plot(dfm1.DateTime, (dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst_raw)/dfm1.O3Sonde_raw * 100 , label = 'O3Sonde DQA - Raw [%]', marker = ".")
# axs[4].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[4].set_ylabel('%')
# axs[4].set_ylim(-5, 5)
# axs[4].legend(loc="upper right")
#
# axs[5].plot(dfm1.DateTime, (dfm1.O3Sonde_hom_burst- dfm1.O3Sonde_burst)/dfm1.O3Sonde_burst * 100 , label = 'O3Sonde DQA - WOUDC [%]', marker = ".")
# axs[5].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax5[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[5].set_ylabel('%')
# axs[5].set_ylim(-5, 5)
# axs[5].legend(loc="upper right")
#
# plt.xticks(rotation = 45)
#
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON_updated/  ' + Plotname + '.pdf')
#
# plt.show()
# plt.close()