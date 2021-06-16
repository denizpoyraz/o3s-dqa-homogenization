import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


dfm = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA/Madrid_Metada_DQA.csv')
# dfm['DateTime'] = dfm['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d %H:%M:%S'))
# # dfm['Date'] = dfm['DateTime'].apply(lambda _: datetime.strftime(_, '%Y-%m-%d'))
# dfm['Date'] = dfm['DateTime'].apply(lambda x: x.strftime('%Y-%m-%d'))

# dfm['Date'] = dfm['DateTime'].apply(lambda x: x.date())

# path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/Binned/'
# df1 = pd.read_csv(path + 'UccleInterpolated_dqa_nors80.csv')
# df2 = pd.read_csv(path + 'UccleInterpolated_dqa_rs80.csv')

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA/Binned/'

df1 = pd.read_csv(path + 'MadridInterpolated_dqa_nors80.csv')
df2 = pd.read_csv(path + 'MadridInterpolated_dqa_rs80.csv')

# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/Binned/'
# df1 = pd.read_csv(path + 'SodankylaInterpolated_dqa_nors80.csv')
# df2 = pd.read_csv(path + 'SodankylaInterpolated_dqa_rs80.csv')


# # #
l1 = df1.drop_duplicates(['Date']).Date.tolist()
l2 = df2.drop_duplicates(['Date']).Date.tolist()

common_dates12 = list(set(l1).intersection(set(l2)))
print(len(common_dates12), common_dates12[0:3])

l3 = dfm.drop_duplicates(['DateTime']).Date.tolist()
print('l3', len(l3), l3)
common_datesall = list(set(l3).intersection(set(common_dates12)))

# df1 = df1[df1['Date'].isin(common_dates12)]
# df2 = df2[df2['Date'].isin(common_dates12)]

df1 = df1[df1['Date'].isin(common_datesall)]
df2 = df2[df2['Date'].isin(common_datesall)]
dfm = dfm[dfm['Date'].isin(common_datesall)]


print(len(df1.drop_duplicates(['Date'])), len(df2.drop_duplicates(['Date'])), len(dfm.drop_duplicates(['Date'])))

df1 = df1[df1.PreLevel > 7]
df2 = df2[df2.PreLevel > 7]

# Plotname = 'RS80_vs_noRS80'
# heatmap_label = 'RS80 - NoRS80 / NoRS80  (%)'
# ptitle = 'Effect of RS80 Radiosonde Correction'
# #
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin_nc) - np.asarray(df1.PO3_UcIntLin_nc)) / np.asarray(df1.PO3_UcIntLin_nc)

# df1['DateTime'] = df1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
df1['DateTime'] = df1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
df1['DateTime2'] = df1["DateTime"].dt.strftime('%Y-%m-%d')



# # (2 - 1) / 1
# Plotname = 'Eta_vs_Raw_alltimerange'
# heatmap_label = 'Eta - NoCorrection / NoCorrection  (%)'
# ptitle = 'Effect of Conversion Efficiency Correction'
#
# Plotname = 'EtaBkg_vs_Eta_alltimerange'
# heatmap_label = 'EtaBkg - Eta / Eta  (%)'
# ptitle = 'Effect of Background Current Correction'

# Plotname = 'EtaBkgTpump_vs_EtaBkg_alltimerange_zoom'
# heatmap_label = 'EtaBkgTpump - EtaBkg / EtaBkg  (%)'
# ptitle = 'Effect of Pump Temperature Correction'

# Plotname = 'EtaBkgTpumpPhigr_vs_EtaBkgTpump_alltimerange'
# heatmap_label = 'EtaBkgTpumpPhigr - EtaBkgTpump / EtaBkgTpump  (%)'
# ptitle = 'Effect of Pump Flow Rate (humidity) Correction'
#
# Plotname = 'EtaBkgTpumpPhigrPhiEff_vs_EtaBkgTpumpPhigr_alltimerange'
# heatmap_label = 'EtaBkgTpumpPhigrPhiEff - EtaBkgTpumpPhigr / EtaBkgTpumpPhigr  (%)'
# ptitle = 'Effect of Pump Flow Efficiency Correction'

# Plotname = 'DQA_vs_Raw_alltimerange'
# heatmap_label = 'DQA - NoCorrection / NoCorrection  (%)'
# ptitle = 'Effect all DQA Corrections'

# Plotname = 'DQA_vs_NDACC_alltimerange'
# heatmap_label = 'DQA - NDACC / NDACC  (%)'
# ptitle = 'DAQ-O3S vs NDACC-O3S'

Plotname = 'DQA_vs_WOUDC_alltimerange_dropnan'
heatmap_label = 'DQA - WOUDC / WOUDC  (%)'
ptitle = 'DAQ-O3S vs WOUDC-O3S'

min = -8
max = 8
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_eta) - np.asarray(df1.PO3_UcIntLin_nc)) / np.asarray(df1.PO3_UcIntLin_nc)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkg) - np.asarray(df1.PO3_UcIntLin_eta)) / np.asarray(df1.PO3_UcIntLin_eta)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkgtpump) - np.asarray(df1.PO3_UcIntLin_etabkg)) / np.asarray(df1.PO3_UcIntLin_etabkg)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr) - np.asarray(df1.PO3_UcIntLin_etabkgtpump)) / np.asarray(df1.PO3_UcIntLin_etabkgtpump)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr)) / np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_nc)) / np.asarray(df1.PO3_UcIntLin_nc)
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)

print('size bin', len(df1.drop_duplicates(['Date']).Date.tolist()) / 24)

df1['PreLevel'] = df1['PreLevel'].astype(int)
print('Date min, max', df1.Date.min(), df1.Date.max())

# df1 = df1[(df1['Date'] > 19981101) & (df1['Date'] < 19981212)]

# t = df1.pivot_table(index='PreLevel', columns='Date', values='RDif_UcIntLin')
t = df1.pivot_table(index='PreLevel', columns='DateTime2', values='RDif_UcIntLin', fill_value = 0, dropna = False)

print('dropna true', len(t.index), len(t.columns))

t = df1.pivot_table(index='PreLevel', columns='DateTime2', values='RDif_UcIntLin', fill_value = 0, dropna = True)

print('dropna false', len(t.index), len(t.columns))
print('size bin',  len(df1.drop_duplicates(['Date']).Date.tolist()) , len(df1), len(df1.drop_duplicates(['Date']).Date.tolist()) / 25)


# xfreq = 134 #uccle mls range
# xfreq = 55 #uccle all range
# xfreq = 53 #uccle all range
# xfreq = 35 #madrid
# xfreq = 39 #madrid ymd2
xfreq = 46 #madrid ymd3

# xfreq = 50 #sodankyla all range
# xfreq = 38
# for all range xtick labels
# xtick_labels = [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
#                 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
xtick_labels = ['1994', '1995', '1996', '1997', '1998', '1999','2001', '2005', '2006', '2007', '2008', '2009', '2010',
                '2011', '2012', '2013', '2014', '2015','2019', '2020', '2021']


#Plotting
# ########################################################################################################################
#original plot without second TO plot
fig, ax = plt.subplots(figsize=(17, 9))
ax.set_yscale('log')
# hm = sns.heatmap(t, vmin=-10, vmax=10 , cmap="vlag", xticklabels=xfreq, yticklabels=2, square=True,
#                  cbar_kws={'label': heatmap_label})
# hm = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", cbar_kws={'label': heatmap_label})
hm = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", xticklabels=xfreq,
                 cbar_kws={'label': heatmap_label})

# ax.set_xticklabels(xtick_labels, rotation=0)
plt.yticks(fontsize=6)
# ax.set_yticklabels(ytick_labels, rotation = 0)
# plt.xticks(rotation = 45)
plt.xticks(fontsize=8)
plt.xlabel(" ")
# ax.set_ylim([68,8])
plt.title(ptitle)

plt.savefig(path + 'Plots/' + Plotname + '.png')
plt.savefig(path + 'Plots/' + Plotname + '.eps')
plt.savefig(path + 'Plots/' + Plotname + '.pdf')

plt.show()
 ########################################################################################################################
# fig, ax1 = plt.subplots(figsize=(17, 9))
#
# plt.plot(dfm.Date, dfm.O3ratio)
# plt.plot(dfm.Date, dfm.O3ratio_hom)
# plt.xticks(np.arange(0, len(dfm)+1, xfreq))
# ax1.set_xticklabels(xtick_labels, rotation=0)
#
#
# plt.show()


# # two plots one for TO plt
#
#
# fig = plt.figure(figsize=(17,9))
# ax1 = plt.subplot(2, 1, 1)
# ax1.set_yscale('log')
# # hm = sns.heatmap(t, vmin=-10, vmax=10 , cmap="vlag", xticklabels=xfreq, yticklabels=2, square=True,
# #                  cbar_kws={'label': heatmap_label})
# # hm = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", cbar_kws={'label': heatmap_label})
# hm = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", xticklabels=xfreq,
#                  cbar_kws={'label': heatmap_label})
#
# ax1.set_xticklabels(xtick_labels, rotation=0)
# plt.yticks(fontsize=6)
# # ax.set_yticklabels(ytick_labels, rotation = 0)
# # plt.xticks(rotation = 45)
# plt.xticks(fontsize=8)
# plt.xlabel(" ")
# # ax.set_ylim([68,8])
# plt.title(ptitle)
#
# x0,x1 = ax1.get_xlim()
# y0,y1 = ax1.get_ylim()
# # ax1.set_aspect((x1-x0)/(y1-y0))
# ax1.set_aspect('equal')
#
# ax2 = plt.subplot(2, 1, 2)
# plt.plot(dfm.Date, dfm.O3ratio)
# plt.plot(dfm.Date, dfm.O3ratio_hom)
# plt.xticks(np.arange(0, len(dfm)+1, xfreq))
# ax2.set_xticklabels(xtick_labels, rotation=0)
# ax2.set_aspect('equal')
#
#
# plt.show()

# gs_top = plt.GridSpec(2, 1, height_ratios=[3,1], hspace=0.05)
# gs_bottom = plt.GridSpec(2, 1, height_ratios=[3,1], hspace=0.25)
#
# fig = plt.figure(figsize=(17, 9))
# # fig, (ax, ax1    ) = plt.subplots(2,1, figsize=(17,9), gridspec_kw={'height_ratios':[3, 1]})
# ax = fig.add_subplot(gs_top[0,:])
# ax.set_yscale('log')
# # hm = sns.heatmap(t, vmin=-10, vmax=10 , cmap="vlag", xticklabels=xfreq, yticklabels=2, square=True,
# #                  cbar_kws={'label': heatmap_label})
# # hm = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", cbar_kws={'label': heatmap_label})
# hm = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", xticklabels=xfreq,
#                  cbar_kws={'label': heatmap_label})
#
# ax.set_xticklabels(xtick_labels, rotation=0)
# plt.yticks(fontsize=6)
# # ax.set_yticklabels(ytick_labels, rotation = 0)
# # plt.xticks(rotation = 45)
# plt.xticks(fontsize=8)
# plt.xlabel(" ")
# # ax.set_ylim([68,8])
# plt.title(ptitle)
#
# ax1 = fig.add_subplot(gs_bottom[1,:])
# plt.plot(dfm.Date, dfm.O3ratio)
# plt.plot(dfm.Date, dfm.O3ratio_hom)
# plt.xticks(np.arange(0, len(dfm)+1, xfreq))
# ax1.set_xticklabels(xtick_labels, rotation=0)
# x0,x1 = ax1.get_xlim()
# y0,y1 = ax1.get_ylim()
# ax1.set_aspect(1)
#
#
#
# # plt.savefig(path + 'Plots/' + Plotname + '.png')
# # plt.savefig(path + 'Plots/' + Plotname + '.eps')
# # plt.savefig(path + 'Plots/' + Plotname + '.pdf')
#
# plt.show()
