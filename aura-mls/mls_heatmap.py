import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


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
    ax.figure.axes[-1].yaxis.label.set_size(14)

    labels = ['',2005, '', '', '', '', 2010, '', '', '',
              '', 2015, '', '', '', '', 2020, '','']
    # try:
    ax.set_xticklabels(labels, rotation=0, fontsize=14)
    plt.xticks(rotation=0)
    plt.yticks(fontsize=14, rotation = 0)
    ax.set_yticklabels(['', 10, '', '', '', 21, '', 31, '', '', 56, '',
                        '', 100, '', '', '', 215])
    # 8.25404, 10.0, 12.1153, 14.678, 17.7828, 21.5443, \
    # 26.1016, 31.6228, 38.3119, 46.4159, 56.2341, 68.1292, 82.5404, 100.0, 121.153, 146.78, 177.828, 215.443

    ax.set_ylabel('Pressure [hPa]', rotation=90, fontsize = 14)

    plt.xlabel(" ")

    plt.title(ptitlet, fontsize = 18)
    #
    plt.savefig(path + 'Plots/' + Plotname + '.png')
    plt.savefig(path + 'Plots/' + Plotname + '.eps')
    # # plt.savefig(path + 'Plots/' + Plotname + '.pdf')

    plt.show()

#{sodankyla, lauder, uccle, madrid, ny-aalesund, scoresby, valentia, lerwick}
# sname = 'sodankyla'
# scname='Sodankyla'
# sname = 'ny-aalesund'
# scname='Ny-Alesund'
# sname = 'scoresby'
# scname='Scoresbysund'
# sname = 'madrid'
# scname='Madrid'
sname = 'lerwick'
scname='Lerwick'
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/MLS/'


# df1 = pd.read_csv(path + f'MLS_{scname}Interpolated_nors80_v05_dqa.csv')
# Plotname = 'DQA_vs_MLS_v05'
# ptitle = f'{scname} Homogenized - MLS (v05)'

df1 = pd.read_csv(path + f'MLS_{scname}Interpolated_nors80_v05_original.csv')
Plotname = 'Original_vs_MLS_v05'
ptitle = f'{scname} Non-Homogenized - MLS (v05)'


df1 = df1[df1.PreLevel < 216]
df1 = df1[df1.PreLevel >= 8]

df1 = df1[df1.PO3_UcIntLin < 99]
df1 = df1[df1.PO3_MLS < 99]

df1 = df1[df1.PreLevel >= 8]

df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin) - np.asarray(df1.PO3_MLS)) / np.asarray(df1.PO3_UcIntLin)


df1 = df1[df1.Date < 20230101]

df1['DateTime'] = df1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
# df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y%m%d')

df1['Date'] = df1['DateTime'].apply(lambda x: x.date())
df1['PreLevel'] = df1['PreLevel'].astype(int)


heatmap_label = 'ECC - MLS / ECC (%)'

min = -10
max = 10

df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin) - np.asarray(df1.PO3_MLS)) / np.asarray(df1.PO3_UcIntLin)
plot_rdif(df1, ptitle)

#
# # fig, ax = plt.subplots(figsize=(17, 9))
# fig, ax = plt.subplots()
#
# # ax.set_yscale('log')
# t = df1.pivot_table(index='PreLevel', columns='DateTime', values='RDif_UcIntLin', fill_value = 0, dropna = False)
#
# min_dist_days = t.columns.to_series().diff()
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
# sns.color_palette("vlag", as_cmap=True)
# hm = sns.heatmap(t, vmin=-10, vmax=10, cmap="vlag", xticklabels=xfreq,  square=True,
#                  cbar_kws={'label': 'ECC - MLS / ECC (%)'})
#
# ax.set_xticklabels(labels, rotation=0)
# plt.yticks(fontsize=10)
# # ax.set_yticklabels(ytick_labels, rotation = 0)
# # plt.xticks(rotation = 45)
# plt.xticks(fontsize=10)
#
# plt.title(plot_title)
#
#
# plt.xlabel(" ")
# # ax.set_ylim([68,8])
# #
# plt.savefig(path + 'Plots/' + Plotname + '.png')
# plt.savefig(path + 'Plots/' + Plotname + '.eps')
# # plt.savefig(path + 'Plots/' + Plotname + '.pdf')
#
# plt.show()

##########################################################################################################################################################
