import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Binned/'
df1 = pd.read_csv(path + 'MadridInterpolated_dqa_nors80_v2.csv')
# df1 = pd.read_csv(path + 'UccleInterpolated_dqa_nors80.csv')

# df1['DateTime'] = df1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y-%m-%d')

df1['date'] = df1['DateTime'].apply(lambda x: x.date())
df1.date = pd.to_datetime(df1.date)

df1 = df1.set_index('date')
# df2 = df2.set_index('date')

# l1 = df1.drop_duplicates(['Date']).Date.tolist()
# l2 = df2.drop_duplicates(['Date']).Date.tolist()
#
# common_dates12 = list(set(l1).intersection(set(l2)))
# print(len(common_dates12), common_dates12[0:3])

# df1 = df1[df1['Date'].isin(common_dates12)]
# df2 = df2[df2['Date'].isin(common_dates12)]

# df1 = df1[df1['Date'].isin(common_dates12)]
# df2 = df2[df2['Date'].isin(common_dates12)]
# print(len(df1.drop_duplicates(['Date'])), len(df2.drop_duplicates(['Date'])))

df1 = df1[df1.PreLevel > 7]

df1['PreLevel'] = df1['PreLevel'].astype(int)
df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y-%m-%d')



# Plotname = 'RS80_vs_noRS80'
# heatmap_label = 'RS80 - NoRS80 / NoRS80  (%)'
# ptitle = 'Effect of RS80 Radiosonde Correction'
# # #
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_dqa)) / np.asarray(df1.PO3_UcIntLin_dqa)

# (2 - 1) / 1
# Plotname = 'Eta_vs_Raw_alltimerange'
# heatmap_label = 'Eta - NoCorrection / NoCorrection  (%)'
# ptitle = 'Effect of Conversion Efficiency Correction'
#
# Plotname = 'EtaBkg_vs_Eta_alltimerange'
# heatmap_label = 'EtaBkg - Eta / Eta  (%)'
# ptitle = 'Effect of Background Current Correction'

# Plotname = 'EtaBkgTpump_vs_EtaBkg_alltimerange'
# heatmap_label = 'EtaBkgTpump - EtaBkg / EtaBkg  (%)'
# ptitle = 'Effect of Pump Temperature Correction'

# Plotname = 'EtaBkgTpumpPhigr_vs_EtaBkgTpump_alltimerange'
# heatmap_label = 'EtaBkgTpumpPhigr - EtaBkgTpump / EtaBkgTpump  (%)'
# ptitle = 'Effect of Pump Flow Rate (temperature) Correction'
#
# Plotname = 'EtaBkgTpumpPhigrPhiEff_vs_EtaBkgTpumpPhigr_alltimerange'
# heatmap_label = 'EtaBkgTpumpPhigrPhiEff - EtaBkgTpumpPhigr / EtaBkgTpumpPhigr  (%)'
# ptitle = 'Effect of Pump Flow Efficiency Correction'
# #
# Plotname = 'DQA_vs_Raw_alltimerange_unzoom'
# heatmap_label = 'DQA - NoCorrection / NoCorrection  (%)'
# ptitle = 'Effect all DQA Corrections'

# Plotname = 'DQA_vs_NDACC_alltimerange'
# heatmap_label = 'DQA - NDACC / NDACC  (%)'
# ptitle = 'DAQ-O3S vs NDACC-O3S'

# Plotname = 'DQA_vs_WOUDC_alltimerange'
# heatmap_label = 'DQA - WOUDC / WOUDC  (%)'
# ptitle = 'DAQ-O3S vs WOUDC'

Plotname = 'WOUDC_vs_WOUDCorig_alltimerange'
heatmap_label = 'DQA - WOUDC / WOUDC  (%)'
ptitle = 'DAQ-O3S vs WOUDC'

min = -3
max = 3
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_eta) - np.asarray(df1.PO3_UcIntLin_nc)) / np.asarray(df1.PO3_UcIntLin_nc)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkg) - np.asarray(df1.PO3_UcIntLin_eta)) / np.asarray(df1.PO3_UcIntLin_eta)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkgtpump) - np.asarray(df1.PO3_UcIntLin_etabkg)) / np.asarray(df1.PO3_UcIntLin_etabkg)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr) - np.asarray(df1.PO3_UcIntLin_etabkgtpump)) / np.asarray(df1.PO3_UcIntLin_etabkgtpump)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr)) / np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_nc)) / np.asarray(df1.PO3_UcIntLin_nc)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_woudc) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)
# df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_woudc_v2) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)



t = df1.pivot_table(index='PreLevel', columns='DateTime', values='RDif_UcIntLin', fill_value = 0, dropna = False)
min_dist_days = t.columns.to_series().diff()
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
ax.set_xticklabels(labels, rotation=0)

plt.yticks(fontsize=6)
# ax.set_yticklabels(ytick_labels, rotation = 0)
plt.xticks(rotation = 90)
plt.xticks(fontsize=8)
plt.xlabel(" ")

plt.title(ptitle)

plt.savefig(path + 'Plots/' + Plotname + '_rs.png')
plt.savefig(path + 'Plots/' + Plotname + '_rs.eps')
plt.savefig(path + 'Plots/' + Plotname + '_rs.pdf')

plt.show()

