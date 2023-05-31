from matplotlib import gridspec
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import glob

def cal_dif(df, var1, var2, adif, rdif):

    df[adif] = df[var1] - df[var2]
    df[rdif] = (df[var1] - df[var2])/df[var2] * 100

    return df[adif], df[rdif]

cbl = ['#e41a1c', '#a65628','#dede00', '#4daf4a', '#377eb8', '#984ea3']
sname = 'scoresby'
# sname = 'uccle'
# dates = '20051020'
dates = '20050105'

df1 = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/scoresby/DQA_nors80/Scoresby_AllData_DQA_nors80.hdf')
df1 = df1[df1.Date == dates]
# dates = '20100726'


df1['adif_o3'], df1['rdif_o3'] = cal_dif(df1, 'O3c','O3','adif_o3','rdif_o3')

# df1 = pd.read_csv(f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/DQA_nors80/20100726_all_hom_nors80.csv')
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/'

Plotname = f'{dates}_AllPeriod_DQA_NDACC_profile_witherror'
# Plotname = 'RS80'

# fig, ax = plt.subplots(figsize=(10, 8))
# fig.suptitle(f'Scoresbysund {dates}', fontsize = 16)
# # fig.suptitle(f'Uccle {dates}', fontsize = 16)
# 
# 
# # ax.plot(o3, y,  label = '1994-2021 WOUDC corrections', marker = 's', markersize = 6)
# ax.plot(df1.O3c, df1.Pair , label = 'Homogenized', color = cbl[3],linewidth=1.5 )
# plt.fill_betweenx(df1.Pair,df1.O3c + ( df1.O3c * df1.dO3), df1.O3c - ( df1.O3c * df1.dO3), alpha=0.3, facecolor=cbl[3],
#                   edgecolor=cbl[3])
# # ax.plot(df1.O3c*df1.dEta, df1.Pair , label = 'Unc. Conversion Eff.', color = cbl[0],linewidth=1.5 )
# # ax.plot(df1.O3c*df1.dIall, df1.Pair , label = 'Unc. Current and Bkg', color = cbl[1n],linewidth=1.5 )
# 
# # ax.plot(o3c2, y , label = '1989-2007 DQA and RS80 corrections  TO=' + str(intc2), marker = 'd', markersize = 6)
# 
# # ax.plot(df1.O3, df1.Pair,  label = 'Non-Homogenized')
# # ax.errorbar(df1.O3c,  df1.Pair, xerr=df1.dO3, label='Homogenized', linewidth=1, elinewidth=0.5, capsize=1,
# #             capthick=0.5)
# 
# # ax.errorbar(df1.O3c, df1.Pair, xerr=df1.dO3, label='Homogenized', marker=".",linestyle='none', elinewidth=0.5, capsize=1,
# #             capthick=0.5)
# 
# # ax.plot(o3, y,  label = '1989-2021 NDACC corrections TO=' + str(intnd), marker = 's', markersize = 6)
# # ax.plot(o3nc, y , label = '1994-2021 No Correction', marker = 'd', markersize = 6)
# 
# ax.set_ylim(1000, 5)
# ax.set_yscale('log')
# ax.legend(loc="best")
# ax.set_ylabel('Pressure [hPa]')
# ax.set_xlabel('PO3 [mPa]')
# #
# plt.savefig(path + 'Plots/' + Plotname + '.png')
# plt.savefig(path + 'Plots/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/  ' + Plotname + '.pdf')
# 
# plt.show()

fig = plt.figure(figsize=(15, 12))
# plt.suptitle("GridSpec Inside GridSpec")
# plt.suptitle(maintitle, fontsize=14)

gs = gridspec.GridSpec(1, 2, width_ratios=[2, 2])
gs.update(wspace=0.0005, hspace=0.05)
ax0 = plt.subplot(gs[0])
# ax0.set_yscale('log')
ax0.set_ylim(1000, 5)
ax0.set_ylabel('Pressure [hPa]')
ax0.set_xlabel('PO3 [mPa]')
ax0.plot(df1.O3c, df1.Pair , label = 'Homogenized')
ax0.plot(df1.O3, df1.Pair,  label = 'Non-Homogenized')
ax0.legend(loc="best")


ax1 = plt.subplot(gs[1])
ax1.set_yticklabels([])
ax1.set_ylim(1000, 5)
# ax1.set_yscale('log')

ax1.plot(df1.rdif_o3, df1.Pair,  label = 'Relative Difference')
ax1.set_xlabel('Homogenized - Non-Homogenized [%]')
ax1.legend(loc="best")

plt.savefig(path + 'Plots/NoLog_Profile_with RDif.png')

plt.show()