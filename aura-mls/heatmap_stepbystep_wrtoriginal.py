import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import ScalarFormatter, MultipleLocator, FormatStrFormatter

import datetime

def plot_rdif(dft, ptitlet):

    t = dft.pivot_table(index='PreLevel', columns='DateTime', values='RDif_UcIntLin', fill_value=0, dropna=True)
    # t = df1.pivot_table(index='PreLevel', columns='date2', values='RDif_UcIntLin', fill_value = 0, dropna = False)
    # print(dft.drop_duplicates('PreLevel')['PreLevel'])
    ytick = dft.drop_duplicates('PreLevel')['PreLevel'].tolist()
    print(ytick)
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
    ylabels = dft.drop_duplicates('PreLevel')['PreLevel'].tolist()
    dft.Date = pd.to_datetime(dft.Date)
    # Plotting
    # ########################################################################################################################
    fig, ax = plt.subplots(figsize=(17, 9))
    ax.set_yscale('log')
    # ax.set_ylim(1000, 8)

    ax = sns.heatmap(t, vmin=min, vmax=max, cmap="vlag", cbar_kws={'label': heatmap_label}, xticklabels=xfreq)
    # ax = sns.heatmap(t, vmin=min, vmax=max , cmap="vlag", cbar_kws={'label': heatmap_label})
    ax.figure.axes[-1].yaxis.label.set_size(14)
    # #
    # labels = [1992, 1993,1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
    #         2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
    #         2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

    # # try:
    labels = ['','', '', '', 1995, '', '', '', '', 2000, '', '',
            '', '', 2005, '', '', '', '', 2010, '', '', '',
            '', 2015, '', '', '', '', 2020, '','']
    # labels = [ '', 1995, '', '', '', '', 2000, '', '',
    #         '', '', 2005, '', '', '', '', 2010, '', '', '',
    #         '', 2015, '', '', '', '', 2020, '','']
    # [1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996,
    #  1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
    #  2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
    #  2019, 2020, 2021]
    ax.set_xticklabels(labels,rotation=0, fontsize = 14)
    plt.xticks(rotation=0)

    plt.xlabel(" ")

    # plt.xticks(rotation=0)
    # ax.set_xticklabels([1992, 1993, 1994, 1995, 1996, 1997, 1998], rotation=0)
    ax.set_ylabel('Pressure [hPa]', rotation=90, fontsize = 14)
    # ax.set_ylabel(fontsize = 14)

    plt.yticks(fontsize=14, rotation = 0)
    ax.set_yticklabels(['', 10, '', '', '', 20, '', '', '', '', 50, '','', 100, '', '', '', 200, '', '', '', '', 500, '', '', 1000])
    # ax.set_yticklabels(['', 10, '', '', '', 20, '', '', '', '', 50, '','', 100, '', '', '', 200, '', '', '', '', 500, '', 800])

    # ax.set_yticklabels(ylabels, rotation = 0)
    # plt.xticks(fontsize=4)

    plt.title(ptitlet, fontsize = 18)
    #
    # plt.savefig(path + 'Plots/till2022_' + Plotname + '.png')
    plt.savefig(path + 'Plots/test_' + Plotname + '.png')

    plt.show()

#{sodankyla, lauder, uccle, madrid, ny-aalesund, scoresby, valentia, lerwick, ny-aalesund}
#{Scoresbysund, Ny-Alesund
sname = 'scoresby'
sbname = 'Scoresbysund'
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/DQA_nors80/Binned/'


post='_till2022'
# post=''
df1 = pd.read_csv(path + f'{sbname}Interpolated_dqa_nors80{post}.csv')
# df1 = pd.read_csv(path + 'NyalesundInterpolated_dqa_nors80_till2022_no2021.csv')






df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y%m%d')
# df1['DateTime'] = pd.to_datetime(df1['Date'], format='%Y-%m-%d')

df1['date'] = df1['DateTime'].apply(lambda x: x.date())

# df1 = df1[df1.PreLevel > 10]

df1 = df1[df1.Date < 20230101]
df1 = df1[df1.Date > 19910101]

df1['PreLevel'] = df1['PreLevel'].astype(int)
df1 = df1[df1.PreLevel > 7]

Plotname = 'DQA_vs_NDACC_alltimerange'
heatmap_label = 'Homogenized - Non-Homogenized / Non-Homogenized (%)'
heatmap_label = r'Ozone diff. (%)'

ptitle = f'Homogenized vs Non-Homogenized {sbname}'+r' O$_3$'
min=-5
max=5
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)
plot_rdif(df1, ptitle)




# (2 - 1) / 1
Plotname = 'Eta_vs_Original_alltimerange'
# heatmap_label = 'Conversion Efficiency - NoCorrection / NoCorrection  (%)'
ptitle = f'{sbname} Conversion Efficiency Correction w.r.t. Non-Homogenized series'
min=-5
max=5
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_eta) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)
plot_rdif(df1, ptitle)

# #
Plotname = 'EtaBkg_vs_Original_alltimerange'
# heatmap_label = 'Conversion and Background Cor. - Conversion Cor. / Conversion Cor.  (%)'
# heatmap_label = 'Eta Bkg Cor. - Eta Cor. / Eta Cor.  (%)'
ptitle = f'{sbname} Background Current Correction w.r.t. Non-Homogenized series'
min=-5
max=5
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkg) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)
print(df1[df1.RDif_UcIntLin < 0].drop_duplicates(['date'])[['date','RDif_UcIntLin']])
plot_rdif(df1, ptitle)

# # #
Plotname = 'EtaBkgTpump_vs_Original_alltimerange'
# heatmap_label = 'Eta Bkg Tpump Cor. - Eta Bkg Cor. / Eta Bkg Cor.  (%)'
ptitle = f'{sbname} Pump Temperature Correction w.r.t. Non-Homogenized series'
min=-5
max=5
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkgtpump) - np.asarray(df1.PO3_UcIntLin)) / np.asarray(df1.PO3_UcIntLin)
plot_rdif(df1, ptitle)

#
Plotname = 'EtaBkgTpumpPhigr_vs_Original_alltimerange'
# heatmap_label = 'Eta Bkg Tpump Phigr Cor. - Eta Bkg Tpump Cor. / Eta Bkg Tpump Cor. (%)'
ptitle = f'{sbname} Pump Flow Rate (humidity) Correction w.r.t. Non-Homogenized series'
min=-5
max=5
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_etabkgtpumpphigr) - np.asarray(df1.PO3_UcIntLin)) \
                       / np.asarray(df1.PO3_UcIntLin)
plot_rdif(df1, ptitle)

# # # #
Plotname = 'EtaBkgTpumpPhigrPhiEff_vs_Original_alltimerange'
# heatmap_label = 'Eta Bkg Tpump Phigr PhiEff Cor. - Eta Bkg Tpump Phigr Cor. / Eta Bkg Tpump Phigr Cor.  (%)'
ptitle = f'{sbname} Pump Flow Efficiency Correction w.r.t. Non-Homogenized series'
min=-5
max=5
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin)) \
                       / np.asarray(df1.PO3_UcIntLin)
plot_rdif(df1, ptitle)

# # # #
Plotname = 'DQA_vs_Raw_alltimerange'
# heatmap_label = 'DQA - No Correction / No Correction  (%)'
ptitle = f'{sbname} Effect all DQA Corrections'
min=-5
max=5
df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin_dqa) - np.asarray(df1.PO3_UcIntLin_nc)) / np.asarray(df1.PO3_UcIntLin_nc)
plot_rdif(df1, ptitle)

## end of main code ############

