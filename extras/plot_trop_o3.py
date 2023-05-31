import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
# import datetime as dt
import glob
from re import search
from datetime import datetime
# import matplotlib.dates as mdates
# from datetime import datetime
from functions.homogenization_functions import o3_integrate

def cal_dif(df, var1, var2, adif, rdif):

    df[adif] = df[var1] - df[var2]
    df[rdif] = (df[var1] - df[var2])/df[var2] * 100

    return df[adif], df[rdif]


#
station = 'scoresbysund'
fname = 'scoresby'
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{fname}/'
allFiles = sorted(glob.glob(path + 'DQA_nors80/*all_hom_nors80.hdf'))
# metafiles = sorted(glob.glob(path + 'DQA_nors80/*o3smetadata_nors80.csv'))
trop_p = 300
if station == 'scoresbysund':trop_p = 400
dfmeta = pd.DataFrame()
metadata = []
#
# for (filename) in (allFiles):
#     print(filename)
#     df = pd.read_hdf(filename)
#     if (search('trop', filename)) or (search('test', filename)):continue
#     # print(filename.split("_all")[0].split('DQA_nors80/')[1])
#     date = filename.split("_all")[0].split('DQA_nors80/')[1]
#     mname = f'/home/poyraden/Analysis/Homogenization_public/Files/{fname}/DQA_nors80/{date}_o3smetadata_nors80.csv'
#     dfmt = pd.read_csv(mname)
#     df = df[df.O3 >= 0]
#     df = df[df.O3c >= 0]
#
#     df150 = df[df['Pair'] >= trop_p]
#
#     dfm = pd.DataFrame()
#
#     dfm.at[0,'O3Sonde_fixedtpp'] = o3_integrate(df150, 'O3')
#     dfm.at[0,'O3Sonde_hom_fixedtpp'] = o3_integrate(df150, 'O3c')
#     # dfm['O3Sonde_wma'] = o3_integrate(dfa, 'O3')
#     # dfm['O3Sonde_hom_wmo'] = o3_integrate(dfa, 'O3c')
#     # dfm['Trop_Level'] = trop_level
#     dfm['date'] = date
#     dfm['DateTime'] =  dfm['date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
#     try:
#         dfm['O3SondeTotal'] = dfmt.at[0,'O3SondeTotal']
#     except KeyError: dfm['O3SondeTotal'] = 9999
#     try:
#         dfm['O3SondeTotal_hom'] = dfmt.at[0,'O3SondeTotal_hom']
#     except KeyError: dfm['O3SondeTotal_hom'] = 9999
#
#
#
#     metadata.append(dfm)
#
name_out = f'{station}_Metada_DQA_nors80_Trop'
# dfall = pd.concat(metadata, ignore_index=True)
#
# dfall.to_csv(f'/home/poyraden/Analysis/Homogenization_public/Files/{fname}/DQA_nors80/' + name_out + ".csv")

dft = pd.read_csv(f'/home/poyraden/Analysis/Homogenization_public/Files/{fname}/DQA_nors80/{name_out}.csv')
print(list(dft))

dft['DateTime'] = dft['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d %H'))
dft['Date'] = dft['DateTime'].dt.strftime('%Y-%m-%d')
dft= dft[dft.date > 19920101]
print(list(dft))
dft = dft[dft['O3SondeTotal'] < 999]
dft = dft[dft['O3SondeTotal'] > 9]

dft['adif_o3_trop'], dft['rdif_o3_trop'] = cal_dif(dft, 'O3Sonde_hom_fixedtpp','O3Sonde_fixedtpp','adif_o3_trop','rdif_o3_trop')
dft['adif_o3_total'], dft['rdif_o3_total'] = cal_dif(dft, 'O3SondeTotal_hom','O3SondeTotal','adif_o3_total','rdif_o3_trop')

cbl = ['#e41a1c', '#a65628','#dede00', '#4daf4a', '#377eb8', '#984ea3']

Plotname = f'TO_TCO_{station}'

fig, axs = plt.subplots(2, sharex=True, sharey=False, figsize=(17, 9))
# fig.suptitle('Scoresbysund TO and TCO Values', fontsize = 16)
fig.suptitle('Scoresbysund TCO Values', fontsize = 16)

axs[0].set_ylim(0, 60)
axs[0].set_ylabel('O3 [DU]')

axs[0].plot(dft.DateTime, dft.O3Sonde_fixedtpp, color = cbl[3], label = 'TCO (fixed hpa)',  marker = "s", linestyle='None', markersize = 4)
axs[0].plot(dft.DateTime, dft.O3Sonde_hom_fixedtpp,color = cbl[0], label = 'Homogenized TCO (fixed hpa)',  marker = "o", linestyle='None', markersize = 3)
axs[0].legend(loc="upper right")

# axs[0].plot(dft.DateTime, dft.O3SondeTotal, color = cbl[1], label = 'TO',  marker = "s", linestyle='None', markersize = 4)
# axs[0].plot(dft.DateTime, dft.O3SondeTotal_hom,color = cbl[2], label = 'Homogenized TO',  marker = "o", linestyle='None', markersize = 4)
#
axs[1].set_ylabel('Hom. vs Non-Hom. [%]')

axs[1].plot(dft.DateTime, dft.rdif_o3_trop,  color = cbl[4], label = 'Rel. Dif. Hom. vs Non-hom. TCO',  marker = ".", linestyle='None')
axs[1].set_ylim(-8, 13)

# axs[1].set_ylabel('O3 [DU]')
axs[1].legend(loc="upper right")
axs[1].axhline(y=1, color='grey', linestyle ="-")

# axs[2].plot(dft.DateTime, dft.O3SondeTotal, color = cbl[3], label = 'TO',  marker = "s", linestyle='None', markersize = 4)
# axs[2].plot(dft.DateTime, dft.O3SondeTotal_hom,color = cbl[2], label = 'Homogenized TO',  marker = "o", linestyle='None', markersize = 2)
# axs[2].legend(loc="upper right")

#

# axs[3].plot(dft.DateTime, dft.rdif_o3_total,  color = cbl[3], label = 'Rel. Dif. Hom. vs Non-hom. TO',  marker = ".", linestyle='None')
# axs[3].legend(loc="upper right")
# axs[3].set_ylim(-8, 13)
# axs[3].axhline(y=1, color='grey', linestyle ="-")
# axs[3].set_ylabel('Hom. vs Non-Hom. [%]')

path = f'/home/poyraden/Analysis/Homogenization_public/Files/{fname}/'
plt.savefig(path + 'Plots/2_' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON_v2/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON_v2/  ' + Plotname + '.pdf')

plt.show()
# plt.close()
