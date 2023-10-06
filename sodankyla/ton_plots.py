import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import glob
import matplotlib.dates as mdates
#
path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
allFiles = sorted(glob.glob(path + 'DQA_nors80/*o3smetadata_nors80.csv'))

dfmeta = pd.DataFrame()
metadata = []
#
# for (filename) in (allFiles):
#     df = pd.read_csv(filename)
#
#     metadata.append(df)
#
# name_out = 'Sodankyla_Metada_DQA_nors80'
# dfall = pd.concat(metadata, ignore_index=True)
#
# dfall.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_nors80/' + name_out + ".csv")
# dfall.to_hdf('/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_nors80/' + name_out + ".h5", key = 'df')

dfm1 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_nors80/Sodankyla_Metada_DQA_nors80.csv')

print(list(dfm1))

# print('here', dfm1[(dfm1.O3ratio_hom > 2) & (dfm1.O3ratio_hom < 99)][['Date', 'O3ratio_hom']])
print('before', len(dfm1))

dfm1['Date'] = dfm1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
dfm1['DateTime'] = dfm1['Date'].dt.date
# dfm1['Date'] = dfm1['Date'].dt.strftime('%Y-%m-%d')
#
#

dfm1 = dfm1[dfm1.TotalO3_Col2A < 999]

print('after', len(dfm1))

# print('here 2 ', dfm1[['Date', 'O3ratio_hom']])


dfm1 = dfm1.reset_index()
# dfm1 = dfm1.set_index(dfm1['Date'])

print(dfm1.DateTime.dtypes)
print(list(dfm1))
print(dfm1.DateTime.min(), dfm1.DateTime.max())

dfm1['ratio'] = dfm1['TotalO3_Col2A']/dfm1['O3SondeTotal']
dfm1['ratio_hom'] = dfm1['TotalO3_Col2A']/dfm1['O3SondeTotal_hom']

dfm1['rdif_dqa'] = (dfm1['O3SondeTotal_hom'] - dfm1['O3SondeTotal'])/dfm1['O3SondeTotal_hom'] * 100





fig, axs = plt.subplots(2, sharex=True, sharey=False, figsize=(17, 9))
fig.suptitle('Sodankyla TO values ')
Plotname = 'TO_sonde_nors80'

axs[0].plot(dfm1.DateTime, dfm1.O3SondeTotal_hom, label = 'Homogenized',  marker = "s", linestyle='None', markersize = 4,color='C2')
axs[0].plot(dfm1.DateTime, dfm1.O3SondeTotal, label = 'Non-Homogenized',  marker = ".",  linestyle='None',color='C3')
axs[0].set_ylabel('O3 [DU]')
axs[0].set_ylim(100, 600)
axs[0].legend(loc="lower left")
#
axs[1].plot(dfm1.DateTime, dfm1.rdif_dqa, label = 'Rel. Dif.',  marker = ".", linestyle='None',color='C0')
axs[1].set_ylabel('(Hom. - Non-Hom.)/Hom.[%]')
axs[1].legend(loc="lower left")
axs[1].set_ylim(-5, 5)
axs[1].axhline(y=0, color='black', linestyle =":",linewidth='2.5')

# axs[2].plot(dfm1.DateTime, dfm1.rdif_dobson_dqa, label = 'Homogenized',  marker = ".", linestyle='None',color='C2')
# axs[2].plot(dfm1.DateTime, dfm1.rdif_dobson, label = 'Non-Homogenized',  marker = ".", linestyle='None',color='C3')
#
# axs[2].set_ylabel('(Sonde - Brewer)/Sonde[%]')
# axs[2].legend(loc="lower left")
# axs[2].set_ylim(-5, 5)
# axs[2].axhline(y=0, color='black', linestyle =":",linewidth='2.5')


path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
plt.show()


dfm1 = dfm1[dfm1.ratio < 2]
dfm1 = dfm1[dfm1.TotalO3_Col2A >20]
# print(dfm1.DateTime.min(), dfm1.DateTime.max())

Plotname = 'TON_sonde_ndacc_nors80'

fig, axs = plt.subplots(3, sharex=True, sharey=False, figsize=(17, 9))
fig.suptitle('Sodankyla TO and TON values')

axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_hom, label = 'O3Sonde DQA',  marker = "s", linestyle='None', markersize = 4)
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_raw, label = 'O3Sonde Raw',  marker = ".", linestyle='None')
axs[0].plot(dfm1.DateTime, dfm1.O3Sonde, label = 'O3Sonde NDACC',  marker = ".",  linestyle='None')

axs[0].set_ylabel('O3 [DU]')
axs[0].set_ylim(100, 500)

axs[0].legend(loc="upper right")

#

axs[1].plot(dfm1.DateTime, dfm1.TotalO3_Col2A, label = 'Brewer TO',  marker = ".", linestyle='None')
axs[1].set_ylabel('O3 [DU]')
axs[1].legend(loc="upper right")

axs[2].plot(dfm1.DateTime, dfm1.ratio_hom, label = 'TON DQA',  marker = "s", linestyle='None', markersize = 4)
axs[2].plot(dfm1.DateTime, dfm1.ratio, label = 'TON NDACC',  marker = ".", linestyle='None')

axs[2].set_ylabel('TON')
axs[2].legend(loc="upper right")
# axs[3].set_ylim(0.9, 1.1)
axs[2].set_ylim(0.7, 1.4)

axs[2].axhline(y=1, color='grey', linestyle ="-")

plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON_updated/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON_updated/  ' + Plotname + '.pdf')
#
plt.show()

