import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/MLS/'
# df1 = pd.read_csv(path + 'MLS_SodankylaInterpolated_dqaprevious_nors80_v04.csv')
# path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/MLS/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/MLS/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/MLS/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/MLS/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/MLS/'
path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/MLS/'

# .csv
# df1 = pd.read_csv(path + 'MLS_NyalesundInterpolated_nors80_v04_dqa.csv')
df1 = pd.read_csv(path + 'MLS_ValentiaInterpolated_nors80_v04_dqa.csv')

# df1 = pd.read_csv(path + 'MLS_LauderInterpolated_nors80_v04_dqa.csv')
# df1 = pd.read_csv(path + 'MLS_ScoresbyInterpolated_nors80_v04_dqa.csv')

# df1 = pd.read_csv(path + 'MLS_ScoresbyInterpolated_nors80_v04_ndacc.csv')
# df1 = pd.read_csv(path + 'MLS_ScoresbyInterpolated_nors80_v04_dqa.csv')
# df1 = pd.read_csv(path + 'MLS_UccleInterpolated_nors80_v04_dqa.csv')

# df1 = pd.read_csv(path + 'MLS_UccleInterpolated_nors80_v04_dqa.csv')

# df1 = pd.read_csv(path + 'MLS_MadridInterpolated_nors80_v04_dqa.csv')

df1 = df1[df1.PreLevel < 216]
df1 = df1[df1.PreLevel >= 8]

df1 = df1[df1.PO3_UcIntLin < 99]
df1 = df1[df1.PO3_MLS < 99]


# Plotname = 'Raw_vs_MLS_v04_nors80'
# Plotname = 'PRESTO_vs_MLS_v04_nors80'
# Plotname = 'Raw_vs_MLS_v04_nors80'

# Plotname = 'WOUDC_vs_MLS_v04_nors80'

# Plotname = 'DQA_vs_MLS_v04_nors80'
# Plotname = 'NDACC_vs_MLS_v04_nors80'
# Plotname = 'NIWA_vs_MLS_v04_nors80'
# Plotname = 'DQA_vs_MLS_v04_nors80_new'
# Plotname = 'Raw_vs_MLS_v04_nors80_new'
Plotname = 'DQA_vs_MLS_v04_nors80'

# plot_title = 'Madrid DQA (RS80) - MLS (v04) comparison'
# plot_title = 'Uccle DQA (RS80) - MLS (v04) comparison'

# plot_title = 'Madrid WOUDC - MLS (v04) comparison'

# plot_title = 'Lauder (tpump) - MLS comparison'
# plot_title = 'Lauder O3S-Previous Version - MLS (v04) comparison'
# plot_title = 'Sodankyla O3S-NDACC - MLS (v04) comparison'
# plot_title = 'Lauder O3S-Raw - MLS (v04) comparison'
# plot_title = 'Lauder DQA (RS80) - MLS (v04) comparison'
# plot_title = 'Lauder DQA - MLS (v04) comparison'
# plot_title = 'NyAlesund DQA - MLS (v04) comparison'
# plot_title = 'NyAlesund NDACC - MLS (v04) comparison'
plot_title = 'Valentia DQA - MLS (v04) comparison'

# plot_title = 'Scoresbysund DQA - MLS (v04) comparison'
# plot_title = 'Scoresbysund DQA - MLS (v04) comparison'

# plot_title = 'Uccle DQA - MLS (v04) comparison'
# plot_title = 'Uccle PRESTO - MLS (v04) comparison'
# plot_title = 'Uccle Raw - MLS (v04) comparison'

# plot_title = 'Scoresbysund NDACC - MLS (v04) comparison'

# plot_title = 'Lauder NIWA - MLS (v04) comparison'

# plot_title = 'Sodankyla O3S-DQA - MLS (v04) comparison'
# plot_title = 'Sodankyla Raw (no correction) - MLS (v04) comparison'

# plot_title = 'Sodankyla O3S-DQA (previous version) - MLS (v04) comparison'

# df1 = df1[df1.PreLevel < 57]
# df1 = df1[df1.PreLevel >= 8]



df1 = df1[df1.PreLevel >= 8]

df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin) - np.asarray(df1.PO3_MLS)) / np.asarray(df1.PO3_UcIntLin)
# df2['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin) - np.asarray(df2.PO3_MLS)) / np.asarray(df2.PO3_UcIntLin)

# df1['DateTime'] = df1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y%m%d')

df1['Date'] = df1['DateTime'].apply(lambda x: x.date())
df1['PreLevel'] = df1['PreLevel'].astype(int)


fig, ax = plt.subplots(figsize=(17, 9))
ax.set_yscale('log')
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


# sns.color_palette("vlag", as_cmap=True)
hm = sns.heatmap(t, vmin=-10, vmax=10, cmap="vlag", xticklabels=xfreq,  square=True,
                 cbar_kws={'label': 'ECC - MLS / ECC (%)'})

ax.set_xticklabels(labels, rotation=0)
plt.yticks(fontsize=10)
# ax.set_yticklabels(ytick_labels, rotation = 0)
# plt.xticks(rotation = 45)
plt.xticks(fontsize=10)

plt.title(plot_title)


plt.xlabel(" ")
# ax.set_ylim([68,8])
#
plt.savefig(path + 'Plots/' + Plotname + '.png')
plt.savefig(path + 'Plots/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/' + Plotname + '.pdf')

plt.show()

##########################################################################################################################################################