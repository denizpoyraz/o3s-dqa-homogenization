import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import glob
import matplotlib.dates as mdates
#
path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
allFiles = sorted(glob.glob(path + 'DQA_nors80/*o3smetadata_nors80.csv'))


# dfmeta = pd.DataFrame()
# metadata = []
#
# for (filename) in (allFiles):
#     df = pd.read_csv(filename)
#
#     metadata.append(df)
#
# name_out = 'Sodankyla_Metada_DQA_nors80'
# dfall = pd.concat(metadata, ignore_index=True)
#
# dfall.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_nors80/' + name_out + ".csv")
# dfall.to_hdf('/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_nors80/' + name_out + ".h5", key = 'df')

dfm1 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_nors80/Sodankyla_Metada_DQA_nors80.csv')

print(list(dfm1))

print('here', dfm1[(dfm1.O3ratio_hom > 2) & (dfm1.O3ratio_hom < 99)][['Date', 'O3ratio_hom']])
print('before', len(dfm1))

dfm1['Date'] = dfm1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
dfm1['Date'] = dfm1['Date'].dt.date
# dfm1['Date'] = dfm1['Date'].dt.strftime('%Y-%m-%d')
#

dfm1 = dfm1[dfm1.O3Sonde_hom != 0]
dfm1 = dfm1[dfm1.O3Sonde_hom < 999]
dfm1 = dfm1[dfm1.O3Sonde < 999]
dfm1 = dfm1[dfm1.O3ratio_hom < 999]
dfm1 = dfm1[dfm1.O3ratio < 999]
dfm1 = dfm1[dfm1.O3ratio_raw < 999]
dfm1 = dfm1[dfm1.O3Sonde_raw < 999]
dfm1 = dfm1[dfm1.O3Sonde_burst_hom < 999]
dfm1 = dfm1[dfm1.O3Sonde_burst_raw < 999]
dfm1 = dfm1[dfm1.O3Sonde_10hpa_hom < 999]
dfm1 = dfm1[dfm1.O3Sonde_10hpa_raw < 999]
dfm1 = dfm1[dfm1.TotalO3_Col2A > 0]
dfm1 = dfm1[dfm1.TotalO3_Col2A < 999]

print('here 2 ', dfm1[['Date', 'O3ratio_hom']])


dfm1 = dfm1.reset_index()
# dfm1 = dfm1.set_index(dfm1['Date'])

print(dfm1.Date.dtypes)
print(list(dfm1))

print(dfm1.Date.min(), dfm1.Date.max())

Plotname = 'TON_sonde_all_v3'

fig, axs = plt.subplots(4, sharex=True, sharey=False, figsize=(17, 9))
# fig.suptitle('Sharing both axes')
# axs[0].plot(x, y ** 2)
# axs[1].plot(x, 0.3 * y, 'o')
# axs[2].plot(x, y, '+')

# axs.plot(dfm1.Date, dfm1.O3Sonde_burst, label = 'O3Sonde DQA(rvm) burst',  marker = ".")
axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst_hom, label = 'O3Sonde DQA burst',  marker = "s", linestyle='None', markersize = 4)
axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst_raw, label = 'O3Sonde Raw burst',  marker = ".", linestyle='None')
axs[0].set_ylabel('O3 [DU]')
axs[0].legend(loc="upper right")


axs[1].plot(dfm1.Date, dfm1.O3Sonde_10hpa_hom, label = 'O3Sonde DQA 10hPa',  marker = "s", linestyle='None', markersize = 4)
axs[1].plot(dfm1.Date, dfm1.O3Sonde_10hpa_raw, label = 'O3Sonde Raw 10hPa',  marker = ".", linestyle='None')
axs[1].set_ylabel('O3 [DU]')
axs[1].legend(loc="upper right")


axs[2].plot(dfm1.Date, dfm1.TotalO3_Col2A, label = 'Brewer TO',  marker = ".", linestyle='None')
axs[2].set_ylabel('O3 [DU]')
axs[2].legend(loc="upper right")

axs[3].plot(dfm1.Date, dfm1.O3ratio_hom, label = 'TON DQA',  marker = "s", linestyle='None', markersize = 4)
axs[3].plot(dfm1.Date, dfm1.O3ratio, label = 'TON Raw ',  marker = ".", linestyle='None')
axs[3].set_ylabel('TON')
axs[3].legend(loc="upper right")
# axs[3].set_ylim(0.9, 1.1)
# axs[3].set_ylim(0.5, 5)

axs[3].axhline(y=1, color='grey', linestyle ="-")

# axs[3].xaxis.set_major_locator(mdates.YearLocator(2))
# axs[3].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
#



# axs.plot(dfm1.Date, dfm1.O3Sonde_burst, label = 'O3Sonde WOUDC burst',  marker = ".")
# axs.plot(dfm1.Date, dfm1.O3Sonde_burst_hom, label = 'O3Sonde DQA burst',  marker = ".")
# axs.plot(dfm1.Date, dfm1.O3Sonde_burst_raw, label = 'O3Sonde Raw burst',  marker = ".")

# axs[0].plot(dfw.Date, dfw.O3sonde_int_woudc, label = 'O3 Sonde from metadata (O3S - Residual)', marker = ".", color = '#ff7f0e')
# axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst , label = 'O3 Sonde WOUDC int until burst', marker = ".", color = '#1f77b4')
# axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst_hom , label = 'O3 Sonde DQA int until burst', marker = ".", color = '#bcbd22')
# axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst , label = 'O3 Sonde WOUDC int until burst', marker = ".")
# axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst_hom , label = 'O3 Sonde DQA int until burst', marker = ".")
# axs.set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs.set_ylim(150, 450)
# axs.set_xlim('1994-01-01', '2021-01-01')
path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')

plt.show()
plt.close()



# Plotname = 'TON_allplots_rs80_bkgcor'
#
# fig, axs = plt.subplots(5, sharex=False, sharey=False, figsize=(17, 9))
# # fig.suptitle('Sharing both axes')
# # axs[0].plot(x, y ** 2)
# # axs[1].plot(x, 0.3 * y, 'o')
# # axs[2].plot(x, y, '+')
#
# axs[0].plot(dfm1.Date, dfm1.O3Sonde, label = 'O3Sonde')
# axs[0].plot(dfm1.Date, dfm1.O3Sonde_hom, label = 'O3Sonde_DQA')
# # axs[0].plot(dfm1.Date, dfm1.Brewer, label = 'Brewer')
# axs[0].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs[0].set_xticklabels(xtick_labels, rotation=0)
# axs[0].set_ylabel('O3 [DU]')
# axs[0].legend(loc="upper right")
#
# axs[1].plot(dfm1.Date, dfm1.O3SondeTotal, label = 'O3Sonde + ROC')
# axs[1].plot(dfm1.Date, dfm1.O3SondeTotal_hom, label = 'O3Sonde_DQA + ROC')
# axs[1].plot(dfm1.Date, dfm1.BrewO3, label = 'Brewer')
# axs[1].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs[1].set_xticklabels(xtick_labels, rotation=0)
# axs[1].set_ylabel('O3 [DU]')
# axs[1].legend(loc="upper right")
#
# axs[2].plot(dfm1.Date, dfm1.O3Sonde - dfm1.O3Sonde_hom, label = 'O3Sonde diff (no dqa - dqa)')
# axs[2].plot(dfm1.Date, dfm1.O3SondeTotal - dfm1.O3SondeTotal_hom, label = 'O3Sonde + ROC diff (no dqa - dqa)')
# # axs[2].plot(dfm1.Date, dfm1.BrewO3, label = 'Brewer')
# axs[2].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs[2].set_xticklabels(xtick_labels, rotation=0)
# # axs[2].set_ylabel('O3 [DU]')
# axs[2].legend(loc="upper right")
#
# axs[3].plot(dfm1.Date, dfm1.BrewO3, label = 'Brewer')
# axs[3].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs[3].set_xticklabels(xtick_labels, rotation=0)
# axs[3].set_ylabel('O3 [DU]')
# axs[3].legend(loc="upper right")
#
# axs[4].plot(dfm1.Date, dfm1.O3ratio, label = 'O3 Ratio')
# axs[4].plot(dfm1.Date, dfm1.O3ratio_hom, label = 'O3 Ratio DQA')
# axs[4].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs[4].set_xticklabels(xtick_labels, rotation=0)
# axs[4].set_ylabel('O3 ratio')
# axs[4].axhline(y=1, color='grey', linestyle=':')
# axs[4].legend(loc="upper right")
#
# # path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
# # plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
# # plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
# # plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')
#
# plt.show()


# dfm1 = dfm1[dfm1.o3max < 999]
# dfm1 = dfm1[dfm1.o3max_hom < 999]
# dfm1 = dfm1[dfm1.o3min_raw < 999]
# dfm1 = dfm1[dfm1.o3min < 999]
# dfm1 = dfm1[dfm1.o3min_hom < 999]
# dfm1 = dfm1[dfm1.o3min > 0]


# Plotname = 'TON_sonde_10hpa'
# # Plotname = 'burst'
#
#
# fig, ax1 = plt.subplots(figsize=(17, 9))
#
# ax1.plot(dfm1.Date, dfm1.O3Sonde, label = 'O3 Sonde WOUDC until 10hPa', marker = ".")
# ax1.plot(dfm1.Date, dfm1.O3Sonde_hom, label = 'O3 Sonde DQA until 10hPa', marker = ".")
# # # ax1.plot(dfm1.Date, dfm1.O3Sonde_raw - dfm1.ROC, label = 'O3 Sonde Raw', marker = ".")
# # ax1.plot(dfw.Date, dfw.O3sonde_int_woudc, label = 'O3 Sonde from metadata (O3S - Residual)', marker = ".")
# # ax1.plot(dfm1.Date, dfm1.O3Sonde_burst , label = 'O3 Sonde WOUDC int until burst', marker = ".")
# # ax1.plot(dfm1.Date, dfm1.O3Sonde_burst_hom , label = 'O3 Sonde DQA int until burst', marker = ".")
# # ax1.plot(dfm1.Date, dfm1.burst , label = 'burst pressure', marker = ".")
# ## ax1.plot(dfm1.Date, dfm1.O3Sonde , label = 'O3 Sonde WOUDC', marker = ".")
# # ax1.plot(dfm1.Date, dfm1.O3Sonde_hom, label = 'O3 Sonde DQA', marker = ".")
# # ax1.plot(dfm1.Date, dfm1.O3Sonde_raw, label = 'O3 Sonde Raw', marker = ".")
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
# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
# plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')
#
# plt.show()
# plt.close()

# Plotname = 'TON_sonde_10hpa_stepbystep_corrections_v2_unzoom'
#
# fig, axs = plt.subplots(6, sharex=True, sharey=False, figsize=(17, 9))
# # fig.suptitle('Sharing both axes')
# # axs[0].plot(x, y ** 2)
# # axs[1].plot(x, 0.3 * y, 'o')
# # axs[2].plot(x, y, '+')
#
# axs[0].plot(dfm1.Date, 100*(dfm1.O3Sonde_10hpa_etabkg - dfm1.O3Sonde_10hpa_raw)/dfm1.O3Sonde_10hpa_raw ,
#             label = 'Effect of Bkg corr. on TO [%] ',  marker = ".", linestyle='None')
# axs[0].set_ylabel('%')
# # axs[0].set_ylim(-5, 5)
# axs[0].legend(loc="upper right")
# # axs[0].xaxis.set_major_locator(mdates.MonthLocator(interval=12))
#
#
# axs[1].plot(dfm1.Date, 100*(dfm1.O3Sonde_10hpa_etabkgtpump - dfm1.O3Sonde_10hpa_etabkg)/dfm1.O3Sonde_10hpa_etabkg ,
#             label = 'Effect of Pump Temp. corr. on TO [%] ',  marker = ".", linestyle='None')
# axs[1].set_ylabel('%')
# # axs[1].set_ylim(0, 5)
# axs[1].legend(loc="upper right")
#
# axs[2].plot(dfm1.Date, 100*(dfm1.O3Sonde_10hpa_etabkgtpumpphigr - dfm1.O3Sonde_10hpa_etabkgtpump)/dfm1.O3Sonde_10hpa_etabkgtpump ,
#             label = 'Effect of PF humidity corr. on TO [%] ',  marker = ".", linestyle='None')
# axs[2].set_ylabel('%')
# # axs[2].set_ylim(-5, 5)
# axs[2].legend(loc="upper right")
#
# axs[3].plot(dfm1.Date, 100*(dfm1.O3Sonde_10hpa_hom - dfm1.O3Sonde_10hpa_etabkgtpumpphigr)/dfm1.O3Sonde_10hpa_etabkgtpumpphigr ,
#             label = 'Effect of PF Eff. corr. on TO [%] ',  marker = ".", linestyle='None')
# # axs[3].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[3].set_ylabel('%')
# # axs[3].set_ylim(1, 3)
# axs[3].legend(loc="upper right")
#
# axs[4].plot(dfm1.Date, (dfm1.O3Sonde_10hpa_hom - dfm1.O3Sonde_10hpa_raw)/dfm1.O3Sonde_10hpa_raw * 100 ,
#             label = 'O3Sonde DQA - Raw [%]', marker = ".", linestyle='None')
# # axs[4].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[4].set_ylabel('%')
# # axs[4].set_ylim(0, 8)
# axs[4].legend(loc="upper right")
# axs[4].xaxis.set_major_locator(mdates.YearLocator(2))
# axs[4].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
#
# axs[5].plot(dfm1.Date, (dfm1.O3Sonde_10hpa_hom - dfm1.O3Sonde_10hpa)/dfm1.O3Sonde_10hpa * 100 ,
#             label = 'O3Sonde DQA - DQA(rvm) [%]', marker = ".", linestyle='None')
# axs[5].set_ylabel('%')
# axs[5].set_ylim(-5, 8)
# axs[5].legend(loc="upper right")
# axs[5].xaxis.set_major_locator(mdates.YearLocator(2))
# axs[5].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
#
# left = dt.date(1996, 10, 1)
# right = dt.date(2021, 1, 31)
# axs[5].set_xbound(left, right)
#
#
# # axs[5].plot(dfm1.Date, (dfm1.O3Sonde_burst- dfm1.O3Sonde_burst)/dfm1.O3Sonde_burst * 100 , label = 'O3Sonde DQA - WOUDC [%]', marker = ".")
# # # axs[5].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # # ax5[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# # axs[5].set_ylabel('%')
# # axs[5].set_ylim(-5, 5)
# # axs[5].legend(loc="upper right")
#
# # plt.xticks(rotation = 45)
#
# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
# plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')
#
# plt.show()
# plt.close()
