import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_nors80/Binned/'
path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/DQA_nors80/Binned/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Binned/'


# df1 = pd.read_csv(path + 'new_LauderInterpolated_dqa_nors80.csv')
df1 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/lauder/DQA_rs80/Binned/new_LauderInterpolated_dqa_rs80.csv')

# df1 = pd.read_csv(path + 'SodankylaInterpolated_dqa_nors80.csv')
# df1 = pd.read_csv(path + 'new_LauderInterpolated_dqa_nors80.csv')

df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y-%m-%d')
df2['DateTime'] = pd.to_datetime(df2['Date'], format='%Y-%m-%d')

# df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y%m%d') #sodankyla

df1['date'] = df1['DateTime'].apply(lambda x: x.date())

df1 = df1[df1.PreLevel > 7]

df1 = df1[df1.Date > '2008-01-01']
df2 = df2[df2.Date > '2008-01-01']

df1['PreLevel'] = df1['PreLevel'].astype(int)

Plotname = 'RS80_vs_noRS80'
heatmap_label = 'RS80 - NoRS80 / NoRS80  (%)'
ptitle = 'Effect of RS80 Radiosonde Correction'
# # #
df1['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_dqa)) / np.asarray(df1.PO3_UcIntLin_dqa)

# (2 - 1) / 1
# Plotname = 'Eta_vs_Raw_alltimerange'
# heatmap_label = 'Conversion Efficiency - NoCorrection / NoCorrection  (%)'
# ptitle = 'Effect of Conversion Efficiency Correction'
# min = -5
# max = 5
# #
# Plotname = 'EtaBkg_vs_Eta_alltimerange'
# # heatmap_label = 'Conversion and Background Cor. - Conversion Cor. / Conversion Cor.  (%)'
# heatmap_label = 'Eta Bkg Cor. - Eta Cor. / Eta Cor.  (%)'
# ptitle = 'Effect of Background Current Correction'
# min = -5
# max = 5
# # #
# Plotname = 'EtaBkgTpump_vs_EtaBkg_alltimerange'
# heatmap_label = 'Eta Bkg Tpump Cor. - Eta Bkg Cor. / Eta Bkg Cor.  (%)'
# ptitle = 'Effect of Pump Temperature Correction'
# min = -5
# max = 5
#
# Plotname = 'EtaBkgTpumpPhigr_vs_EtaBkgTpump_alltimerange'
# heatmap_label = 'Eta Bkg Tpump Phigr Cor. - Eta Bkg Tpump Cor. / Eta Bkg Tpump Cor. (%)'
# ptitle = 'Effect of Pump Flow Rate (humidity) Correction'
# min = -5
# max = 5
# # # #
# Plotname = 'EtaBkgTpumpPhigrPhiEff_vs_EtaBkgTpumpPhigr_alltimerange'
# heatmap_label = 'Eta Bkg Tpump Phigr PhiEff Cor. - Eta Bkg Tpump Phigr Cor. / Eta Bkg Tpump Phigr Cor.  (%)'
# ptitle = 'Effect of Pump Flow Efficiency Correction'
# min = -5
# max = 5
# # # #
# Plotname = 'DQA_vs_Raw_alltimerange'
# heatmap_label = 'DQA - No Correction / No Correction  (%)'
# ptitle = 'Effect all DQA Corrections'
# min = -10
# max = 10
# Plotname = 'DQA_vs_NDACC_alltimerange'
# # heatmap_label = 'DQA - Previous Version / Previos Version  (%)'
# # ptitle = 'DAQ-O3S vs Previous Version-O3S'
# heatmap_label = 'DQA - NIWA Version / NIWA Version  (%)'
# ptitle = 'DQA-O3S vs NIWA-O3S'
# min = -5
# max = 5
# #
# Plotname = 'DQA_vs_WOUDC_alltimerange'
# heatmap_label = 'DQA - WOUDC / WOUDC  (%)'
# ptitle = 'DAQ-O3S vs WOUDC'
# min = -10
# max = 10

# Plotname = 'WOUDC_vs_DQAprev_alltimerange'
# heatmap_label = 'DQA - DQA(previous version) / DQA(previous version)  (%)'
# ptitle = 'DAQ-O3S vs DQA-previous'
# min = -3
# max = 3


# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_eta) - np.asarray(df1.PO3_UcIntLin_nc)) / np.asarray(df1.PO3_UcIntLin_nc)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkg) - np.asarray(df1.PO3_UcIntLin_eta)) / np.asarray(df1.PO3_UcIntLin_eta)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkgtpump) - np.asarray(df1.PO3_UcIntLin_etabkg)) / np.asarray(df1.PO3_UcIntLin_etabkg)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr) - np.asarray(df1.PO3_UcIntLin_etabkgtpump)) / np.asarray(df1.PO3_UcIntLin_etabkgtpump)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr)) / np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_nc)) / np.asarray(df1.PO3_UcIntLin_nc)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_woudc) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_woudc_v2) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)



t = df1.pivot_table(index='PreLevel', columns='DateTime', values='RDif_UcIntLin', fill_value = 0, dropna = False)
# t = df1.pivot_table(index='PreLevel', columns='date2', values='RDif_UcIntLin', fill_value = 0, dropna = False)

min_dist_days = t.columns.to_series().diff()
# print('min_dist_days', min_dist_days)
min_mean = min_dist_days.median()
print('min distance 2 launches', min_mean )
#resample to see missing dates
t = t.T.resample(min_mean).mean().T

x_min_mean = int(str(min_mean.days))
labels = t.columns.year.unique()
xfreq = int(365/x_min_mean)
print('xfreq', xfreq)



df1.Date = pd.to_datetime(df1.Date)
#Plotting
# ########################################################################################################################
fig, ax = plt.subplots(figsize=(17, 9))
ax.set_yscale('log')

ax = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", cbar_kws={'label': heatmap_label}, xticklabels=xfreq)
# ax = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", cbar_kws={'label': heatmap_label})

ax.set_xticklabels(labels, rotation=0)

plt.yticks(fontsize=6)
# ax.set_yticklabels(ytick_labels, rotation = 0)
plt.xticks(rotation = 90)
# plt.xticks(fontsize=4)
plt.xlabel(" ")

plt.title(ptitle)
#
plt.savefig(path + 'Plots_new/' + Plotname + '.png')
plt.savefig(path + 'Plots_new/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/' + Plotname + '.pdf')

plt.show()

####################################################

# df2['date'] = df2['DateTime'].apply(lambda x: x.date())
#
# # df1 = df1[df1.date2 > '1993']
#
# df1.date = pd.to_datetime(df1.date)
#
# df1 = df1.set_index('date')
#
# l1 = df1.drop_duplicates(['Date']).Date.tolist()
# l2 = df2.drop_duplicates(['Date']).Date.tolist()
#
# common_dates12 = list(set(l1).intersection(set(l2)))
# print(len(common_dates12), common_dates12[0:3])
#
# # l3 = dfm.drop_duplicates(['DateTime']).Date.tolist()
# # print('l3', len(l3), l3)
# common_datesall = common_dates12
#
# # df1 = df1[df1['Date'].isin(common_dates12)]
# # df2 = df2[df2['Date'].isin(common_dates12)]
#
# df1 = df1[df1['Date'].isin(common_datesall)]
# df2 = df2[df2['Date'].isin(common_datesall)]
# # dfm = dfm[dfm['Date'].isin(common_datesall)]
#
#
# df1 = df1[df1.PreLevel > 7]
# df2 = df2[df2.PreLevel > 7]
#
# df1['PreLevel'] = df1['PreLevel'].astype(int)
# df2['PreLevel'] = df2['PreLevel'].astype(int)
#
# # # df1 = df1[df1.Date != '1986-09-04']
# # # df2 = df2[df2.Date != '1986-09-04']
# #
# print(len(df1), len(df2))
# d1 = df1.drop_duplicates(['Date'])['Date'].tolist()
# d2 = df2.drop_duplicates(['Date'])['Date'].tolist()
#
# print(len(d1), len(d2))
# #
# prelevel = df1[df1.Date == '1986-08-03'].PreLevel.tolist()
# print(prelevel)
# # df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y-%m-%d')
#
# for d in range(len(d1)):
#     for p in range(len(prelevel)):
#         # print('df1',d1[d], df1.loc[(df1.Date == d1[d]) & (df1.PreLevel == prelevel[p]),'PO3_UcIntLin_dqa'].tolist())
#         #
#         # print('df2',d1[d], df2.loc[(df2.Date == d1[d]) & (df2.PreLevel == prelevel[p]),'PO3_UcIntLin_dqa'].tolist())
#
#         if (len(df1.loc[(df1.Date == d1[d]) & (df1.PreLevel == prelevel[p]),'PO3_UcIntLin_dqa'].tolist())) != (len(df2.loc[(df2.Date == d1[d]) & (df2.PreLevel == prelevel[p]),'PO3_UcIntLin_dqa'].tolist())):
#             # print(d1[d], prelevel[p])
#             df1.drop(df1.loc[(df1['Date'] == d1[d]) & (df1['PreLevel'] == prelevel[p])].index, inplace=True)
#             df2.drop(df2.loc[(df2['Date'] == d1[d]) & (df2['PreLevel'] == prelevel[p])].index, inplace=True)
#
#         # if df2.loc[(df2.Date == d1[d]) & (df2.PreLevel == prelevel[p]),'PO3_UcIntLin_dqa'].isnull() :
#         #     print(d1[d], prelevel[p])
#
#
# print(len(df1), len(df2))