import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import glob

# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# allFiles = sorted(glob.glob(path + "DQA/*o3smetadata_rs80*.csv"))
#
# dfmeta = pd.DataFrame()
# metadata = []
#
# for (filename) in (allFiles):
#     df = pd.read_csv(filename)
#
#     metadata.append(df)
#
# name_out = 'Madrid_Metada_DQA'
# dfall = pd.concat(metadata, ignore_index=True)
#
# dfall.to_csv(path + "DQA/" + name_out + ".csv")
# dfall.to_hdf(path + "DQA/" + name_out + ".h5", key = 'df')

dfm = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA/Madrid_Metada_DQA.csv')
print(list(dfm))
print('before', len(dfm))
dfm = dfm[dfm.O3Sonde_hom != 0]
dfm = dfm[dfm.O3Sonde_hom < 999]
dfm = dfm[dfm.O3Sonde < 999]
dfm = dfm[dfm.O3ratio_hom < 999]
dfm = dfm[dfm.O3ratio < 999]


print('after', len(dfm))

# Plotname = 'TON_extreme valuescleaned'

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA/Binned/'

df2 = pd.read_csv(path + 'MadridInterpolated_dqa_nors80.csv')
df1 = pd.read_csv(path + 'MadridInterpolated_dqa_rs80.csv')

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
dfm = dfm[dfm['Date'].isin(common_datesall)]


xfreq = 32 #madrid ymd3

# xfreq = 50 #sodankyla all range
# xfreq = 38
# for all range xtick labels
# xtick_labels = [1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
#                 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
xtick_labels = ['1994', '1995', '1996', '1997', '1998', '1999','2001', '2005', '2006', '2007', '2008', '2009', '2010',
                '2011', '2012', '2013', '2014', '2015','2019', '2020', '2021']

print('size bin', len(dfm)/len(xtick_labels))

Plotname = 'TON_sonde_zoom'

fig, ax1 = plt.subplots(figsize=(17, 9))

ax1.plot(dfm.Date, dfm.O3Sonde, label = 'O3 Sonde')
ax1.plot(dfm.Date, dfm.O3Sonde_hom, label = 'O3 Sonde DQA')
# ax1.plot(dfm.Date, dfm.BrewO3, label = 'Brewer')
# ax1.plot(dfm.Date, dfm.O3ratio, label = 'O3 Ratio')
# ax1.plot(dfm.Date, dfm.O3ratio_hom, label = 'O3 Ratio DQA')
ax1.set_xticks(np.arange(0, len(dfm)+1, xfreq))
ax1.set_xticklabels(xtick_labels, rotation=0)
ax1.set_ylabel('O3 [DU]')
# ax1.set_ylabel('O3 ratio')
# ax1.set_ylim(0.8,1.2)

ax1.axhline(y=1, color='grey', linestyle=':')
ax1.legend(loc="upper right")

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')

plt.show()


Plotname = 'TON_allplots'

fig, axs = plt.subplots(5, sharex=False, sharey=False, figsize=(17, 9))
# fig.suptitle('Sharing both axes')
# axs[0].plot(x, y ** 2)
# axs[1].plot(x, 0.3 * y, 'o')
# axs[2].plot(x, y, '+')

axs[0].plot(dfm.Date, dfm.O3Sonde, label = 'O3Sonde')
axs[0].plot(dfm.Date, dfm.O3Sonde_hom, label = 'O3Sonde_DQA')
# axs[0].plot(dfm.Date, dfm.Brewer, label = 'Brewer')
axs[0].set_xticks(np.arange(0, len(dfm)+1, xfreq))
axs[0].set_xticklabels(xtick_labels, rotation=0)
axs[0].set_ylabel('O3 [DU]')
axs[0].legend(loc="upper right")

axs[1].plot(dfm.Date, dfm.O3SondeTotal, label = 'O3Sonde + ROC')
axs[1].plot(dfm.Date, dfm.O3SondeTotal_hom, label = 'O3Sonde_DQA + ROC')
axs[1].plot(dfm.Date, dfm.BrewO3, label = 'Brewer')
axs[1].set_xticks(np.arange(0, len(dfm)+1, xfreq))
axs[1].set_xticklabels(xtick_labels, rotation=0)
axs[1].set_ylabel('O3 [DU]')
axs[1].legend(loc="upper right")

axs[2].plot(dfm.Date, dfm.O3Sonde - dfm.O3Sonde_hom, label = 'O3Sonde diff (no dqa - dqa)')
axs[2].plot(dfm.Date, dfm.O3SondeTotal - dfm.O3SondeTotal_hom, label = 'O3Sonde + ROC diff (no dqa - dqa)')
# axs[2].plot(dfm.Date, dfm.BrewO3, label = 'Brewer')
axs[2].set_xticks(np.arange(0, len(dfm)+1, xfreq))
axs[2].set_xticklabels(xtick_labels, rotation=0)
# axs[2].set_ylabel('O3 [DU]')
axs[2].legend(loc="upper right")

axs[3].plot(dfm.Date, dfm.BrewO3, label = 'Brewer')
axs[3].set_xticks(np.arange(0, len(dfm)+1, xfreq))
axs[3].set_xticklabels(xtick_labels, rotation=0)
axs[3].set_ylabel('O3 [DU]')
axs[3].legend(loc="upper right")

axs[4].plot(dfm.Date, dfm.O3ratio, label = 'O3 Ratio')
axs[4].plot(dfm.Date, dfm.O3ratio_hom, label = 'O3 Ratio DQA')
axs[4].set_xticks(np.arange(0, len(dfm)+1, xfreq))
axs[4].set_xticklabels(xtick_labels, rotation=0)
axs[4].set_ylabel('O3 ratio')
axs[4].axhline(y=1, color='grey', linestyle=':')
axs[4].legend(loc="upper right")

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')

plt.show()