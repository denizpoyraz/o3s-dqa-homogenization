import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

def plot_rdif(dft, ptitlet):

    t = dft.pivot_table(index='PreLevel', columns='DateTime', values='RDif_UcIntLin', fill_value=0, dropna=True)
    # t = df1.pivot_table(index='PreLevel', columns='date2', values='RDif_UcIntLin', fill_value = 0, dropna = False)

    min_dist_days = t.columns.to_series().diff()
    print('min_dist_days', min_dist_days)
    min_mean = min_dist_days.median()
    print('min distance 2 launches', min_mean)
    # resample to see missing dates
    t = t.T.resample(min_mean).mean().T

    x_min_mean = int(str(min_mean.days))
    labels = t.columns.year.unique()
    print('labels', labels)
    xfreq = int(365 / x_min_mean)
    print('xfreq', xfreq)

    dft.Date = pd.to_datetime(dft.Date)
    # Plotting
    # ########################################################################################################################
    fig, ax = plt.subplots(figsize=(17, 9))
    ax.set_yscale('log')

    ax = sns.heatmap(t, vmin=min, vmax=max, cmap="vlag", cbar_kws={'label': heatmap_label}, xticklabels=xfreq)
    # ax = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", cbar_kws={'label': heatmap_label})

    # labels = [1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
    #  2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015,
    #  2016, 2017, 2018, 2019, 2020, 2021]
    ax.set_xticklabels(labels, rotation=0)
    # ax.set_xticklabels([1992, 1993, 1994, 1995, 1996, 1997, 1998], rotation=0)


    plt.yticks(fontsize=6)
    # ax.set_yticklabels(ytick_labels, rotation = 0)
    plt.xticks(rotation=90)
    # plt.xticks(fontsize=4)
    plt.xlabel(" ")

    plt.title(ptitlet)
    #
    plt.savefig(path + 'Plots/f_' + Plotname + '.png')
    plt.savefig(path + 'Plots/f_' + Plotname + '.eps')
    # # plt.savefig(path + 'Plots/' + Plotname + '.pdf')

    plt.show()


# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_nors80/Binned/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/DQA_rs80/Binned/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_rs80/Binned/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/DQA_rs80/Binned/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/DQA_rs80/Binned/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/DQA_nors80/Binned/'
path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/MLS/'

# df2 = pd.read_csv(path + 'MLS_ScoresbyInterpolated_rs80_v04_dqa_tpumpmm_v2.csv')
df1 = pd.read_csv(path + 'MLS_ScoresbyInterpolated_rs80_v04_dqa_plusp201606.csv')
# df1 = pd.read_csv(path + 'MLS_ScoresbyInterpolated_nors80_v04_ndacc.csv')



df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y%m%d')
# df2['DateTime'] = pd.to_datetime(df2['Date'], format='%Y%m%d')

# df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y%m%d') #sodankyla

df1['date'] = df1['DateTime'].apply(lambda x: x.date())
# df2['date'] = df2['DateTime'].apply(lambda x: x.date())

df1 = df1[df1.PreLevel > 7]
df1 = df1[df1.PreLevel < 216]

# df2 = df2[df2.PreLevel > 7]
# df2 = df2[df2.PreLevel < 216]

# df1 = df1[df1.Date > '2008-01-01']
# df2 = df2[df2.Date > '2008-01-01']

df1['PreLevel'] = df1['PreLevel'].astype(int)
# df2['PreLevel'] = df2['PreLevel'].astype(int)

# Plotname = 'DQA_vs_MLS_v04_after2016'
plot_title = 'Scoresbysund DQA (plus pre. corr. after 2016 corr.) - MLS (v04) comparison'
Plotname = 'DQA_vs_MLS_v04_after2016_plusp'
# Plotname = 'NDACC_vs_MLS_v04_nors80'
# Plotname = 'effectof_tpump_mm'


# plot_title = 'Scoresbysund NDACC  - MLS (v04) comparison'
# plot_title = 'effect of Tpump correction'


df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin) - np.asarray(df1.PO3_MLS)) / np.asarray(df1.PO3_UcIntLin)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin) - np.asarray(df2.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)

df1['DateTime'] = df1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
# df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y%m%d')
heatmap_label = 'DQA - MLS / DQA  (%)'

df1['Date'] = df1['DateTime'].apply(lambda x: x.date())
df1['PreLevel'] = df1['PreLevel'].astype(int)

min = -10
max = 10
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin) - np.asarray(df1.PO3_MLS)) / np.asarray(df1.PO3_UcIntLin)
plot_rdif(df1, plot_title)
#
# Plotname = 'RS80_vs_noRS80'
# heatmap_label = 'RS80 - NoRS80 / NoRS80  (%)'
# ptitle = 'Effect of RS80 Radiosonde Correction'
# # #
# min = -5
# max = 5
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_dqa)) / np.asarray(df1.PO3_UcIntLin_dqa)
# plot_rdif(df1, ptitle)
#######################
##########################
############################

##########
################33
################33
########################

Plotname = 'DQA_vs_NDACC_final'
heatmap_label = 'DQA - Previous Version / Previous Version  (%)'
ptitle = 'DAQ-O3S vs Previous Version-O3S'
# heatmap_label = 'DQA - NIWA Version / NIWA Version  (%)'
ptitle = 'DQA-O3S vs Previous Version-O3S'
min = -5
max = 5
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_ndaccrmi) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)



plot_rdif(df1, ptitle)

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



#########################################################

# t = df1.pivot_table(index='PreLevel', columns='DateTime', values='RDif_UcIntLin', fill_value = 0, dropna = True)
# # t = df1.pivot_table(index='PreLevel', columns='date2', values='RDif_UcIntLin', fill_value = 0, dropna = False)
#
# min_dist_days = t.columns.to_series().diff()
# # print('min_dist_days', min_dist_days)
# min_mean = min_dist_days.median()
# print('min distance 2 launches', min_mean )
# #resample to see missing dates
# t = t.T.resample(min_mean).mean().T
#
# x_min_mean = int(str(min_mean.days))
# labels = t.columns.year.unique()
# xfreq = int(365/x_min_mean)
# print('xfreq', xfreq)
#
#
#
# df1.Date = pd.to_datetime(df1.Date)
# #Plotting
# # ########################################################################################################################
# fig, ax = plt.subplots(figsize=(17, 9))
# ax.set_yscale('log')
#
# ax = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", cbar_kws={'label': heatmap_label}, xticklabels=xfreq)
# # ax = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", cbar_kws={'label': heatmap_label})
#
# ax.set_xticklabels(labels, rotation=0)
#
# plt.yticks(fontsize=6)
# # ax.set_yticklabels(ytick_labels, rotation = 0)
# plt.xticks(rotation = 90)
# # plt.xticks(fontsize=4)
# plt.xlabel(" ")
#
# plt.title(ptitle)
# #
# # plt.savefig(path + 'Plots_new/' + Plotname + '.png')
# # plt.savefig(path + 'Plots_new/' + Plotname + '.eps')
# # # plt.savefig(path + 'Plots/' + Plotname + '.pdf')
#
# plt.show()

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