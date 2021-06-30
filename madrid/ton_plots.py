import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import glob

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
allFiles = sorted(glob.glob(path + "DQA_final/*_o3smetadata_nors80.csv"))

dfmeta = pd.DataFrame()
metadata = []

for (filename) in (allFiles):
    df = pd.read_csv(filename)

    metadata.append(df)

name_out = 'Madrid_Metada_DQA_nors80'
dfall = pd.concat(metadata, ignore_index=True)

dfall.to_csv(path + "DQA_final/" + name_out + ".csv")
dfall.to_hdf(path + "DQA_final/" + name_out + ".h5", key = 'df')

# dfm1 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_upd/Madrid_Metada_DQA_rs80_bkgupd.csv')
dfm1 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_final/Madrid_Metada_DQA_nors80_updated.csv')

# /home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_final/Madrid_Metada_DQA_nors80_updated.csv

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
dfm1 = dfm1[dfm1.O3ratio_hom < 999]
dfm1 = dfm1[dfm1.O3ratio < 999]
dfm1 = dfm1[dfm1.O3ratio_raw < 999]
dfm1 = dfm1[dfm1.O3Sonde_raw < 999]
dfm1 = dfm1[dfm1.o3max_raw < 999]
dfm1 = dfm1[dfm1.o3max < 999]
dfm1 = dfm1[dfm1.o3max_hom < 999]
dfm1 = dfm1[dfm1.o3min_raw < 999]
dfm1 = dfm1[dfm1.o3min < 999]
dfm1 = dfm1[dfm1.o3min_hom < 999]
dfm1 = dfm1[dfm1.o3min > 0]


# dfm2 = dfm2[dfm2.O3Sonde_hom != 0]
# dfm2 = dfm2[dfm2.O3Sonde_hom < 999]
# dfm2 = dfm2[dfm2.O3Sonde < 999]
# dfm2 = dfm2[dfm2.O3ratio_hom < 999]
# dfm2 = dfm2[dfm2.O3ratio < 999]
# dfm2 = dfm2[dfm2.O3ratio_raw < 999]
# dfm2 = dfm2[dfm2.O3Sonde_raw < 999]


# print('after', len(dfm1), len(dfm2))

# Plotname = 'TON_extreme valuescleaned'

# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_upd/Binned/'
#
# df1 = pd.read_csv(path + 'MadridInterpolated_dqa_rs80.csv')
# df2 = pd.read_csv(path + 'MadridInterpolated_dqa_rs80.csv')
#
# # path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/Binned/'
# # df1 = pd.read_csv(path + 'SodankylaInterpolated_dqa_rs80.csv')
# # df2 = pd.read_csv(path + 'SodankylaInterpolated_dqa_rs80.csv')


# # # #
# l1 = dfm1.drop_duplicates(['Date']).Date.tolist()
# l2 = dfm2.drop_duplicates(['Date']).Date.tolist()
#
# common_dates12 = list(set(l1).intersection(set(l2)))
# # dfm1 = dfm1[dfm1['Date'].isin(common_dates12)]
# # dfm2 = dfm2[dfm2['Date'].isin(common_dates12)]
# # print(len(common_dates12), common_dates12[0:3])
#
# l3 = dfw.drop_duplicates(['Date']).Date.tolist()
# print('l3', len(l3), l3)
# common_datesall = list(set(l3).intersection(set(common_dates12)))
# dfm1 = dfm1[dfm1['Date'].isin(common_datesall)]
# dfm2 = dfm2[dfm2['Date'].isin(common_datesall)]
# dfw = dfw[dfw['Date'].isin(common_datesall)]

# print('last', len(dfm1), len(dfm2), len(dfw))

# dfm1 = dfm1.reset_index()
# dfm2 = dfm2.reset_index()
# dfw = dfw.reset_index()

# dfw['O3sonde_total_woudc'] = dfw['O3sonde_int_woudc'] + dfm1['ROC']


xfreq = 32 #madrid ymd3
xfreq = 20 #madrid ymd3

# xfreq = 50 #sodankyla all range
# xfreq = 38
# for all range xtick labels
# xtick_labels = [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
#                 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
# xtick_labels = ['1994', '1995', '1996', '1997', '1998', '1999','2001', '2005', '2006', '2007', '2008', '2009', '2010',
#                 '2011', '2012', '2013', '2014', '2015','2019', '2020', '2021']

# print('size bin', len(dfm1)/len(xtick_labels))

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
# # ax1.plot(dfm1.Date, dfm1.O3Sonde_hom_burst , label = 'O3 Sonde DQA int until burst', marker = ".")
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
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')
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
# axs[0].plot(dfm1.Date, 100*(dfm1.O3Sonde_burst_etabkg - dfm1.O3Sonde_burst_raw)/dfm1.O3Sonde_burst_raw , label = 'Effect of Bkg corr. on TO [%] ',  marker = ".")
# # axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst_etabkgtpump, label = 'O3Sonde  Pump Temp. corr.',  marker = ".")
# # axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst_etabkgtpumpphigr, label = 'O3Sonde Pump grounf corr.',  marker = ".")
# # axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst_etabkgtpumpphigref, label = 'O3Sonde Pump Eff. corr.',  marker = ".")
# axs[0].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# axs[0].set_ylabel('%')
# axs[0].set_ylim(-5, 5)
#
# axs[0].legend(loc="upper right")
#
# axs[1].plot(dfm1.Date, 100*(dfm1.O3Sonde_burst_etabkgtpump - dfm1.O3Sonde_burst_etabkg)/dfm1.O3Sonde_burst_etabkg ,
#             label = 'Effect of Pump Temp. corr. on TO [%] ',  marker = ".")
# axs[1].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # axs[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[1].set_ylabel('%')
# axs[1].set_ylim(0, 5)
# axs[1].legend(loc="upper right")
#
# axs[2].plot(dfm1.Date, 100*(dfm1.O3Sonde_burst_etabkgtpumpphigr - dfm1.O3Sonde_burst_etabkgtpump)/dfm1.O3Sonde_burst_etabkgtpump ,
#             label = 'Effect of PF humidity corr. on TO [%] ',  marker = ".")
# axs[2].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[2].set_ylabel('%')
# axs[2].set_ylim(-5, 5)
# axs[2].legend(loc="upper right")
#
# axs[3].plot(dfm1.Date, 100*(dfm1.O3Sonde_burst_etabkgtpumpphigref - dfm1.O3Sonde_burst_etabkgtpumpphigr)/dfm1.O3Sonde_burst_etabkgtpumpphigr ,
#             label = 'Effect of PF Eff. corr. on TO [%] ',  marker = ".")
# axs[3].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[3].set_ylabel('%')
# axs[3].set_ylim(-5, 5)
# axs[3].legend(loc="upper right")
#
# axs[4].plot(dfm1.Date, (dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst_raw)/dfm1.O3Sonde_raw * 100 , label = 'O3Sonde DQA - Raw [%]', marker = ".")
# axs[4].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[4].set_ylabel('%')
# axs[4].set_ylim(-5, 5)
# axs[4].legend(loc="upper right")
#
# axs[5].plot(dfm1.Date, (dfm1.O3Sonde_hom_burst- dfm1.O3Sonde_burst)/dfm1.O3Sonde_burst * 100 , label = 'O3Sonde DQA - WOUDC [%]', marker = ".")
# axs[5].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax5[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[5].set_ylabel('%')
# axs[5].set_ylim(-5, 5)
# axs[5].legend(loc="upper right")
#
# plt.xticks(rotation = 45)
#
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')
#
# plt.show()
# plt.close()


print(dfm1.DateTime.min(), dfm1.DateTime.max())

Plotname = 'TON_sonde_burst_v2'

fig, axs = plt.subplots(1, sharex=True, sharey=False, figsize=(17, 9))
# fig.suptitle('Sharing both axes')
# axs[0].plot(x, y ** 2)
# axs[1].plot(x, 0.3 * y, 'o')
# axs[2].plot(x, y, '+')

# axs.plot(dfm1.Date, dfm1.O3Sonde_burst, label = 'O3Sonde WOUDC burst',  marker = ".")
# axs.plot(dfm1.Date, dfm1.O3Sonde_hom_burst, label = 'O3Sonde DQA burst',  marker = ".")
# axs.plot(dfm1.Date, dfm1.O3Sonde_burst_raw, label = 'O3Sonde Raw burst',  marker = ".")

axs.plot(dfm1.DateTime, dfm1.O3Sonde_burst, label = 'O3Sonde WOUDC burst',  marker = ".")
axs.plot(dfm1.DateTime, dfm1.O3Sonde_hom_burst, label = 'O3Sonde DQA burst',  marker = ".")
axs.plot(dfm1.DateTime, dfm1.O3Sonde_burst_raw, label = 'O3Sonde Raw burst',  marker = ".")

# axs[0].plot(dfw.Date, dfw.O3sonde_int_woudc, label = 'O3 Sonde from metadata (O3S - Residual)', marker = ".", color = '#ff7f0e')
# axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst , label = 'O3 Sonde WOUDC int until burst', marker = ".", color = '#1f77b4')
# axs[0].plot(dfm1.Date, dfm1.O3Sonde_hom_burst , label = 'O3 Sonde DQA int until burst', marker = ".", color = '#bcbd22')
# axs[0].plot(dfm1.Date, dfm1.O3Sonde_burst , label = 'O3 Sonde WOUDC int until burst', marker = ".")
# axs[0].plot(dfm1.Date, dfm1.O3Sonde_hom_burst , label = 'O3 Sonde DQA int until burst', marker = ".")
# axs.set_xticks(np.arange(0, len(dfm1)+1, xfreq))
axs.set_ylabel('O3 [DU]')
axs.set_ylim(150, 450)
# axs.set_xlim('1994-01-01', '2021-01-01')

axs.legend(loc="upper right")

# axs[1].plot(dfm1.Date, dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst , label = 'O3Sonde DQA - WOUDC', marker = ".")
# axs[1].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # axs[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[1].set_ylabel('O3 [DU]')
# # axs[1].set_ylim(11, 3)
# axs[1].legend(loc="upper right")

# axs[1].plot(dfm1.Date, 100 * (dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst)/dfm1.O3Sonde_burst , label = 'O3Sonde DQA - WOUDC [%]', marker = ".")
# axs[1].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[1].set_ylabel('%')
# # axs[2].set_ylim(11, 3)
# axs[1].legend(loc="upper right")
#
# # axs[3].plot(dfm1.Date, dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst_raw , label = 'O3Sonde DQA - Raw', marker = ".")
# # axs[3].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# # axs[3].set_ylabel('O3 [DU]')
# # # axs[2].set_ylim(11, 3)
# # axs[3].legend(loc="upper right")
#
# axs[2].plot(dfm1.Date, (dfm1.O3Sonde_hom_burst - dfm1.O3Sonde_burst_raw)/dfm1.O3Sonde_burst_raw * 100 , label = 'O3Sonde DQA - Raw [%]', marker = ".")
# axs[2].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[2].set_ylabel('%')
# # axs[2].set_ylim(11, 3)
# axs[2].legend(loc="upper right")
#
# axs[3].plot(dfm1.Date, dfm1.o3max, label = 'O3S Max WOUDC', marker = ".")
# axs[3].plot(dfm1.Date, dfm1.o3max_hom, label = 'O3S Max DQA', marker = ".")
# axs[3].plot(dfm1.Date, dfm1.o3max_raw, label = 'O3S Max Raw', marker = ".")
# axs[3].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[3].set_ylabel('O3 [DU]')
# # axs[2].set_ylim(11, 3)
# axs[3].legend(loc="upper right")
#
# axs[4].plot(dfm1.Date, (dfm1.o3max_hom - dfm1.o3max)/dfm1.o3max * 100, label = 'DQA - WOUDC (o3max) [%]', marker = ".")
# axs[4].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# axs[4].set_ylabel('%')
# # axs[2].set_ylim(11, 3)
# axs[4].legend(loc="upper right")
#
# # axs[5].plot(dfm1.Date, (dfm1.o3min_hom - dfm1.o3min)/dfm1.o3min * 100, label = 'DQA - WOUDC (o3min) [%]', marker = ".")
# # axs[5].set_xticks(np.arange(0, len(dfm1)+1, xfreq))
# # # ax2[1].set_xticklabels(xtick_labels, rotation=45)plt.xticks(rotation = 45)
# # axs[5].set_ylabel('%')
# # # axs[2].set_ylim(11, 3)
# # axs[5].legend(loc="upper right")
#
# plt.xticks(rotation = 45)
#
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')

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
# # path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# # plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
# # plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
# # plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')
#
# plt.show()