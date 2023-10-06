import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import glob
import matplotlib.dates as mdates


# sname = 'lauder'
# scname = 'Lauder'
# sname = 'ny-aalesund'
# scname = 'Ny-Alesund'
sname = 'sodankyla'
scname = 'Sodankyla'
# sname = 'lerwick'
# scname = 'Lerwick'

name_out = f'{sname}_metada_dqa_nors80'
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/'

# allFiles = sorted(glob.glob(path + "DQA_nors80/*_o3smetadata*nors80.csv"))
# dfmeta = pd.DataFrame()
# metadata = []
#
# for (filename) in (allFiles):
#     # print(filename)
#     df = pd.read_csv(filename)
#     metadata.append(df)
# #
# dfall = pd.concat(metadata, ignore_index=True)
# dfall.to_csv(path + "DQA_nors80/" + name_out + "_till202.csv")

## read TON values from R. Stauffer
de = pd.read_csv(f"/home/poyraden/Analysis/Homogenization_public/Files/{sname}/{sname}_TON.csv")
de['DateTime'] = de['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))


dfm1 = pd.read_csv(f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/DQA_nors80/{name_out}_till202.csv')
print(list(dfm1))

dobson=True

dfm1['DateTime'] = dfm1['Date2']
dfm1['DateTime'] = dfm1['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
# dfm1['DateTime'] = dfm1['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d %H'))
dfm1['Date'] = dfm1['DateTime'].dt.strftime('%Y-%m-%d')
#
#
dfm1 = dfm1[dfm1.O3SondeTotal_hom < 999]
dfm1 = dfm1[dfm1.O3SondeTotal < 999]
dfm1 = dfm1[dfm1.O3SondeTotal > 99]
dfm1 = dfm1[dfm1.O3SondeTotal_hom > 99]




# de = de[de.Date < 20201210 ]
print('dqa file', dfm1.DateTime.min(), dfm1.DateTime.max())
print('ton file', de.DateTime.min(), de.DateTime.max())
print(len(de), len(dfm1))

dfm1['DateTime2'] = dfm1['DateTime']
de['DateTime2'] = de['DateTime']
dfm1 = dfm1.set_index('DateTime2')




# print(len(df1), len(df2))

dfm1['rdif_dqa'] = (dfm1['O3SondeTotal_hom'] - dfm1['O3SondeTotal'])/dfm1['O3SondeTotal_hom'] * 100


size_label = 22
size_title = 28
size_tick = 22
size_legend = 16

# df1 = df1[df1.DateTime > '19940101']
Plotname = 'TON_sonde_nors80'

if dobson: fig, axs = plt.subplots(3, sharex=True, sharey=False, figsize=(17, 9))
if not dobson: fig, axs = plt.subplots(2, sharex=True, sharey=False, figsize=(17, 9))
fig.suptitle(f'{scname} TO values', fontsize=size_title)

axs[0].plot(dfm1.DateTime, dfm1.O3SondeTotal_hom, label = 'Homogenized Sonde',
            marker = "s", linestyle='None', markersize = 4,color='C2')
# axs[0].plot(dfm1.DateTime, dfm1.O3Sonde_raw, label = 'O3Sonde Raw',  marker = ".", linestyle='None')
axs[0].plot(dfm1.DateTime, dfm1.O3SondeTotal, label = 'Non-Homogenized Sonde',  marker = ".",  linestyle='None',color='C3')
axs[0].set_ylabel('O3 [DU]', fontsize=size_label)
axs[0].set_ylim(100, 600)
axs[0].legend(loc="lower left", fontsize=size_legend,handletextpad=-0.5,markerscale=2)
axs[0].tick_params(axis='y', labelsize=size_tick)

#
axs[1].plot(dfm1.DateTime, dfm1.rdif_dqa, label = '(Hom. - Non-Hom.)/Hom.[%]',  marker = ".", linestyle='None',color='C0')
axs[1].set_ylabel('Rel. Dif. [%]', fontsize=size_label)
axs[1].legend(loc="lower left", fontsize=size_legend,handletextpad=-0.5,markerscale=2)
axs[1].set_ylim(-5,5)
axs[1].axhline(y=0, color='black', linestyle =":",linewidth='2.5')
# plt.yticks(fontsize=size_tick)
axs[1].tick_params(axis='y', labelsize=size_tick)

dfm1 = dfm1.sort_values(['Date'])
if dobson:
    # dfm1['TotalO3_Col2A'] = dfm1['COL2A']
    # dfm1['TotalO3_Col2A'] = dfm1['Dobson']
    # dfm1['TotalO3_Col2A'] = dfm1['COL2A']


    dfm1 = dfm1[dfm1.TotalO3_Col2A < 999]
    dfm1 = dfm1[dfm1.TotalO3_Col2A > 99]
    
    dfm1['rdif_dobson_dqa'] = (dfm1['O3SondeTotal_hom'] - dfm1['TotalO3_Col2A'])/dfm1['O3SondeTotal_hom'] * 100
    dfm1['rdif_dobson'] = (dfm1['O3SondeTotal'] - dfm1['TotalO3_Col2A'])/dfm1['O3SondeTotal'] * 100

    dfm1.reset_index()

    axs[2].plot(dfm1.DateTime, dfm1.rdif_dobson_dqa, label = 'Homogenized-Dobson',  marker = ".", linestyle='None',color='C2')
    dft = dfm1[dfm1.rdif_dobson_dqa.isnull()==False]
    dft['rdif_dobson_dqa'] = dft['rdif_dobson_dqa'].rolling(window=90, center=True).mean()
    axs[2].plot(dft.DateTime,dft.rdif_dobson_dqa, color = 'C2', linewidth='2.5' )

    axs[2].plot(dfm1.DateTime, dfm1.rdif_dobson, label='Non-Homogenized-Dobson', marker=".", linestyle='None',
                color='C3')
    dft = dfm1[dfm1.rdif_dobson.isnull() == False]
    dft['rdif_dobson'] = dft['rdif_dobson'].rolling(window=90, center=True).mean()
    axs[2].plot(dft.DateTime, dft.rdif_dobson, color='C3', linewidth='2.5')


    axs[2].set_ylabel('Rel. Dif. [%]', fontsize=size_label)
    axs[2].legend(loc="lower left", fontsize=size_legend, handletextpad=-0.5, markerscale=2)
    axs[2].set_ylim(-5, 5)
    axs[2].axhline(y=0, color='black', linestyle=":", linewidth='2.5')
    axs[2].tick_params(axis='y', labelsize=size_tick)

    # axs[3].plot(dfm1.DateTime, dfm1.rdif_dobson, label = 'Non-Homogenized-Dobson',  marker = ".", linestyle='None',color='C3')
    # dft = dfm1[dfm1.rdif_dobson.isnull()==False]
    # dft['rdif_dobson'] = dft['rdif_dobson'].rolling(window=90, center=True).mean()
    # axs[3].plot(dft.DateTime,dft.rdif_dobson, color = 'C3', linewidth='2.5' )

    # axs[3].set_ylabel('Rel. Dif. [%]',fontsize=size_label)
    # axs[3].legend(loc="lower left", fontsize=size_legend,handletextpad=-0.5,markerscale=2)
    # axs[3].set_ylim(-15, 15)
    # axs[3].axhline(y=0, color='black', linestyle =":",linewidth='2.5')
    # axs[3].tick_params(axis='y', labelsize=size_tick)
plt.xticks(fontsize=size_tick)

path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/'
plt.savefig(path + 'Plots/TON/test_' + Plotname + '.png')
plt.savefig(path + 'Plots/TON/test_' + Plotname + '.eps')
plt.show()




de = de.set_index('DateTime2')
common_index = set(dfm1.index).intersection(de.index)
df1 = dfm1.loc[common_index].copy()
df2 = de.loc[common_index].copy()

df1 = df1.drop_duplicates(['DateTime'])
df2 = df2.drop_duplicates(['DateTime'])

df1 = df1.drop_duplicates(['Date'])
df2 = df2.drop_duplicates(['Date'])

# 'OMI TCO', 'OMPS TCO', 'GOME-2A TCO', 'GOME-2B TCO'
df1['rdif_omi_hom'] = (df1['O3SondeTotal_hom'] - df2['OMI TCO'])/df1['O3SondeTotal_hom'] * 100
df1['rdif_omi'] = (df1['O3SondeTotal'] - df2['OMI TCO'])/df1['O3SondeTotal'] * 100


df1['rdif_omps_hom'] = (df1['O3SondeTotal_hom'] - df2['OMPS TCO'])/df1['O3SondeTotal_hom'] * 100
df1['rdif_omps'] = (df1['O3SondeTotal'] - df2['OMPS TCO'])/df1['O3SondeTotal'] * 100
df1['rdif_gomea_hom'] = (df1['O3SondeTotal_hom'] - df2['GOME-2A TCO'])/df1['O3SondeTotal_hom'] * 100
df1['rdif_gomea'] = (df1['O3SondeTotal'] - df2['GOME-2A TCO'])/df1['O3SondeTotal'] * 100
df1['rdif_gomeb_hom'] = (df1['O3SondeTotal_hom'] - df2['GOME-2B TCO'])/df1['O3SondeTotal_hom'] * 100
df1['rdif_gomeb'] = (df1['O3SondeTotal'] - df2['GOME-2B TCO'])/df1['O3SondeTotal'] * 100

# if dobson:
#     # df1['TotalO3_Col2A'] = df1['Dobson']
#     df1['TotalO3_Col2A'] = df1['COL2A']
#     #
#     # df1 = df1[df1.TotalO3_Col2A > 99]
#     # df1 = df1[df1.TotalO3_Col2A < 999]
#
#     df1['rdif_dobson_dqa'] = (df1['O3SondeTotal_hom'] - df1['TotalO3_Col2A'])/df1['O3SondeTotal_hom'] * 100
#     df1['rdif_dobson'] = (df1['O3SondeTotal'] - df1['TotalO3_Col2A'])/df1['O3SondeTotal'] * 100







#############

df1 = df1[df1.DateTime > '20050101']
df2 = df2[df2.DateTime > '20050101']




Plotname = 'TON_satellite_one'
fig, axs = plt.subplots(2, sharex=True, sharey=False, figsize=(17, 9))
fig.suptitle(f'{scname} TO values', fontsize=size_title)

# axs[0].plot(df1.DateTime, df1.rdif_dqa, label = 'RDif',  marker = ".", linestyle='None')
# axs[0].set_ylabel('RDif')
# axs[0].legend(loc="upper right")
# axs[0].set_ylim(-5,5)
df1 = df1.sort_values(['Date'])
df1.reset_index()

axs[0].set_title('Non-Homogenized', fontsize=size_label)
# plt.title('Non-Homogenized', fontsize=size_label)

axs[0].plot(df1.DateTime, df1.rdif_omi, label = 'OMI',  marker = ".", linestyle='None', markersize = 6, color = 'C0' )
dft = df1[df1.rdif_omi.isnull()==False]
dft['rdif_omi'] = dft['rdif_omi'].rolling(window=90, center=True).mean()
axs[0].plot(dft.DateTime,dft.rdif_omi, color = 'C0', linewidth='2.5' )

axs[0].plot(df1.DateTime, df1.rdif_omps, label = 'OPMS',  marker = ".", linestyle='None', markersize = 6, color='C1')
dft = df1[df1.rdif_omps.isnull()==False]
dft['rdif_omps'] = dft['rdif_omps'].rolling(window=90, center=True).mean()
axs[0].plot(dft.DateTime,dft.rdif_omps, color = 'C1', linewidth='2.5' )

axs[0].plot(df1.DateTime, df1.rdif_gomea, label = 'GOME-2A',  marker = ".", linestyle='None', markersize = 6,color='C2')
dft = df1[df1.rdif_gomea.isnull()==False]
dft['rdif_gomea'] = dft['rdif_gomea'].rolling(window=90, center=True).mean()
axs[0].plot(dft.DateTime,dft.rdif_gomea, color = 'C2', linewidth='2.5' )


axs[0].plot(df1.DateTime, df1.rdif_gomeb, label = 'GOME-2B',  marker = ".", linestyle='None', markersize = 6,color='C3')
dft = df1[df1.rdif_gomeb.isnull()==False]
dft['rdif_gomeb'] = dft['rdif_gomeb'].rolling(window=90, center=True).mean()
axs[0].plot(dft.DateTime,dft.rdif_gomeb, color = 'C3', linewidth='2.5' )


axs[0].legend(loc="lower left", fontsize=size_legend,handletextpad=0.1)
axs[0].set_ylabel('(Sonde - Satellite) [%]', fontsize=size_label)

axs[0].set_ylim(-15, 15)
axs[0].axhline(y=1, color='black', linestyle =":",linewidth='2.5')
axs[0].tick_params(axis='y', labelsize=size_tick)


# df1['rdif_omi_hom_ma'] = df1['rdif_omi_hom'].rolling(window=5).mean()
axs[1].set_title('Homogenized', fontsize=size_label)

axs[1].plot(df1.DateTime, df1.rdif_omi_hom, label = 'OMI',  marker = ".", linestyle='None', markersize = 6)
dft = df1[df1.rdif_omi_hom.isnull()==False]
dft['rdif_omi_hom'] = dft['rdif_omi_hom'].rolling(window=90, center=True).mean()
axs[1].plot(dft.DateTime,dft.rdif_omi_hom, color = 'C0', linewidth='2.5' )

axs[1].plot(df1.DateTime, df1.rdif_omps_hom, label = 'OPMS',  marker = ".", linestyle='None', markersize = 6)
dft = df1[df1.rdif_omps_hom.isnull()==False]
dft['rdif_omps_hom'] = dft['rdif_omps_hom'].rolling(window=90, center=True).mean()
axs[1].plot(dft.DateTime,dft.rdif_omps_hom, color = 'C1', linewidth='2.5' )

axs[1].plot(df1.DateTime, df1.rdif_gomea_hom, label = 'GOME-2A',  marker = ".", linestyle='None', markersize = 6)
dft = df1[df1.rdif_gomea_hom.isnull()==False]
dft['rdif_gomea_hom'] = dft['rdif_gomea_hom'].rolling(window=90, center=True).mean()
axs[1].plot(dft.DateTime,dft.rdif_gomea_hom, color = 'C2', linewidth='2.5' )


axs[1].plot(df1.DateTime, df1.rdif_gomeb_hom, label = 'GOME-2B',  marker = ".", linestyle='None', markersize = 6)
dft = df1[df1.rdif_gomeb_hom.isnull()==False]
dft['rdif_gomeb_hom'] = dft['rdif_gomeb_hom'].rolling(window=90, center=True).mean()
axs[1].plot(dft.DateTime,dft.rdif_gomeb_hom, color = 'C3', linewidth='2.5' )

axs[1].set_ylabel('(Sonde - Satellite) [%]', fontsize=size_label)

axs[1].set_ylim(-15, 15)
axs[1].axhline(y=0, color='black', linestyle =":",linewidth='2.5')
axs[1].legend(loc="lower left", fontsize=size_legend,handletextpad=-0.5, markerscale=2)

axs[1].tick_params(axis='y', labelsize=size_tick)
axs[1].tick_params(axis='x', labelsize=size_tick)


path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/'
plt.savefig(path + 'Plots/TON/' + Plotname + '_2.png')
plt.savefig(path + 'Plots/TON/' + Plotname + '_2.eps')
plt.show()

######


########################33


# Plotname = 'TON_satellite_two'
# fig, axs = plt.subplots(4, sharex=True, sharey=False, figsize=(17, 9))
# fig.suptitle(f'{scname} TON values', fontize=size_title)
#
# axs[0].plot(df1.DateTime, df1.rdif_omi, label = 'OMI vs NDACC',  marker = ".", linestyle='None', markersize = 4)
# axs[0].plot(df1.DateTime, df1.rdif_omi_hom, label = 'OMI vs DQA',  marker = ".", linestyle='None', markersize = 4)
# axs[0].axhline(y=0, color='black', linestyle ="-")
# axs[0].set_ylabel('(Sonde - Satellite)/Sonde[%]')
# axs[0].legend(loc="upper right")
# axs[0].set_ylim(-5,5)
#
#
# # axs[1].set_ylim(-5,5)
# # axs[1].plot(df1.DateTime, df1.rdif_omi_hom, label = 'rdif_omi_hom',  marker = ".", linestyle='None', markersize = 4)
# axs[1].plot(df1.DateTime, df1.rdif_omps, label = 'OPMS vs NDACC',  marker = ".", linestyle='None', markersize = 4)
# axs[1].plot(df1.DateTime, df1.rdif_omps_hom, label = 'OPMS vs DQA',  marker = ".", linestyle='None', markersize = 4)
# # axs[1].set_ylabel('(Sonde - Satellite)/Sonde[%]')
# axs[1].legend(loc="lower left")
# axs[1].set_ylim(-5,5)
# axs[1].axhline(y=0, color='black', linestyle =":")
#
#
# # df1['rdif_omi_hom_ma'] = df1['rdif_omi_hom'].rolling(window=5).mean()
# axs[2].plot(df1.DateTime, df1.rdif_gomea, label = 'GOME-2A vs NDACC',  marker = ".", linestyle='None', markersize = 4)
# axs[2].plot(df1.DateTime, df1.rdif_gomea_hom, label = 'GOME-2A vs DQA',  marker = ".", linestyle='None', markersize = 4)
# # axs[2].set_ylabel('(Sonde - Satellite)/Sonde[%]')
# axs[2].legend(loc="lower left")
# axs[2].set_ylim(-5,5)
# axs[2].axhline(y=0, color='black', linestyle ="-")
#
# axs[3].plot(df1.DateTime, df1.rdif_gomeb, label = 'GOME-2B vs NDACC',  marker = ".", linestyle='None', markersize = 4)
# axs[3].plot(df1.DateTime, df1.rdif_gomeb_hom, label = 'GOME-2B vs DQA',  marker = ".", linestyle='None', markersize = 4)
# axs[3].set_ylim(-5,5)
# axs[3].axhline(y=0, color='black', linestyle =":")
# axs[3].legend(loc="lower left")
#
#
#
#
# path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/'
# plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
# plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
# plt.show()

# Plotname = 'TON_satellite_two'
# fig, ax = plt.subplots(figsize=(17, 9))
# fig.suptitle('Scoresbysund TON values')
# ax = df1['rdif_gomeb_hom'].plot.hist()
# plt.show()
#