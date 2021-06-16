import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/MLS/'
path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/MLS/'

### not all the data series have the same dates, raw + DQA and presto ones

df1 = pd.read_csv(path + 'MLS_UccleInterpolated_dqa_rs80_v04.csv')
df2 = pd.read_csv(path + 'MLS_UccleInterpolated_raw_rs80_v04.csv')

df1 = df1[df1.PreLevel < 216]
df1 = df1[df1.PreLevel >= 8]
df2 = df2[df2.PreLevel < 216]
df2 = df2[df2.PreLevel >= 8]

print(len(df1), len(df2))

l1 = df1.drop_duplicates(['Date']).Date.tolist()
l2 = df2.drop_duplicates(['Date']).Date.tolist()

common_dates12 = list(set(l1).intersection(set(l2)))
print(len(common_dates12))

df1 = df1[df1['Date'].isin(common_dates12)]
df2 = df2[df2['Date'].isin(common_dates12)]

print(len(df1), len(df2))

# # #
#
# print(len(df1), len(df2))

# df1 = pd.read_csv(path + 'MLS_SodankylaInterpolated_o3s_v05_rs80.csv')

# df1 = pd.read_csv(path + 'MLS_SodankylaInterpolated_o3s_v05.csv')
Plotname = 'DQA_vs_MLS_v04_rs80'
# plot_title = 'Sodankyla (tpump) - MLS comparison'
plot_title = 'Uccle O3S-DQA- MLS (v04) comparison'

# ytick_labels = [10, 20, 30, 40, 50]
# ytick_labels = [8, 10, 12, 14, 17, 21, 26, 31, 38, 46, 56]
ytick_labels = [8, 10, 12, 14, 17, 21, 26, 31, 38, 46, 56, 68, 82, 100, 121, 146, 177, 215]


# df1 = df1[df1.PreLevel < 57]
# df1 = df1[df1.PreLevel >= 8]

# df1 = df1[df1.PreLevel < 50]

df1 = df1[df1.PreLevel >= 8]
# df2 = df2[df2.PreLevel < 57]
# df2 = df2[df2.PreLevel >= 8]
#
# print(len(df1.drop_duplicates(['Date'])), len(df2.drop_duplicates(['Date'])) )

df1['RDif_UcIntLin'] = 100 * (np.asarray(df1.PO3_UcIntLin) - np.asarray(df1.PO3_MLS)) / np.asarray(df1.PO3_UcIntLin)
# df2['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin) - np.asarray(df2.PO3_MLS)) / np.asarray(df2.PO3_UcIntLin)

print('size bin', len(df1.drop_duplicates(['Date']).Date.tolist()) / 16)



# original
# xfreq = 38

xfreq = 134 #uccle

# for all range xtick labels

# weekly


# xtick_labels = ['2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2019']
# xtick_labels = ['2004', '2005', '2006', '2007', '2008', '2009','2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017' ,'2018','2019','2020']
# xtick_labels = ['2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
#                 '2017', '2018', '2019', '2020','2021']

##monthly
# xticks_labels = [' 2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018']
# xfreq = 47
# xfreq = 48
# xfreq = 11
# xfreq = 2

fig, ax = plt.subplots(figsize=(17, 9))

ax.set_yscale('log')

df1['DateTime'] = df1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
df1['Datenf'] = df1['DateTime'].apply(lambda x: x.strftime('%Y%m%d'))

df1['dtdate'] = df1['DateTime'].apply(lambda x: x.date())


print(df1[['DateTime','Datenf']][0:3])


t = df1.pivot_table(index='PreLevel', columns='dtdate', values='RDif_UcIntLin')
print(len(t.index), len(t.columns))

# sns.color_palette("vlag", as_cmap=True)
hm = sns.heatmap(t, vmin=-10, vmax=10, cmap="vlag", xticklabels=xfreq, yticklabels=1,
                 cbar_kws={'label': 'ECC - MLS / ECC (%)'})
# hm = sns.heatmap(t, vmin=-10, vmax=10, cmap="vlag",
#                  cbar_kws={'label': 'ECC - MLS / ECC (%)'})


# ax.set_xticklabels(xtick_labels, rotation=0)
ax.set_yticklabels(ytick_labels, rotation = 0)
# ax.set_xticklabels(df1['Date'].dt.strftime('%d-%m-%Y'))
# ax.xaxis.set_major_locator(fmt_half_year)
# fmt_half_year = mdates.MonthLocator(interval=12)
# ax.xaxis.set_major_locator(fmt_half_year)
# ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.xticks(rotation = 45)
plt.title(plot_title)

plt.xlabel(" ")
# ax.set_ylim([68,8])

plt.savefig(path + 'Plots/' + Plotname + '.png')
plt.savefig(path + 'Plots/' + Plotname + '.eps')
plt.savefig(path + 'Plots/' + Plotname + '.pdf')

plt.show()
