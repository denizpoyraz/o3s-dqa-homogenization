import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import glob
import matplotlib.dates as mdates


def Calc_average_profile_pressure(dft, xcolumn):
    # nd = len(dataframelist)

    # yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
    #         12, 10, 8, 6]

    yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400, 350, 325, 300, 275, 250, 240, 230, 220,
            210, 200,
            190, 180, 170, 160, 150, 140, 130, 125, 120, 115, 110, 105, 100, 95, 90, 85, 80, 75, 70, 65, 60, 55,
            50, 45, 40, 35, 30, 28, 26, 24, 22, 20, 19, 18, 17, 16, 15, 14, 13.5, 13, 12.5, 12, 11.5, 11, 10.5,
            10, 9.75, 9.50, 9.25, 9, 8.75, 8.5, 8.25, 8, 7.75, 7.5, 7.25, 7, 6.75, 6.50, 6.25, 6]

    # yref = [i * 250 for i in range(0, 160)]

    n = len(yref) - 1
    Ygrid = [-9999.0] * n

    Xgrid = [-9999.0] * n
    Xsigma = [-9999.0] * n
    #
    # Xgrid = [[-9999.0] * n for i in range(nd)]
    # Xsigma = [[-9999.0] * n for i in range(nd)]

    # for j in range(nd):
    #     dft.PFcor = dft[xcolumn]

    for i in range(n):
        dftmp1 = pd.DataFrame()
        dfgrid = pd.DataFrame()

        grid_min = yref[i + 1]
        grid_max = yref[i]
        Ygrid[i] = (grid_min + grid_max) / 2.0

        filta = dft.Pair >= grid_min
        filtb = dft.Pair < grid_max
        filter1 = filta & filtb
        dftmp1['X'] = dft[filter1][xcolumn]

        filtnull = dftmp1.X > -9999.0
        dfgrid['X'] = dftmp1[filtnull].X

        Xgrid[i] = np.nanmean(dfgrid.X)
        Xsigma[i] = np.nanstd(dfgrid.X)

    return Xgrid, Xsigma, Ygrid


path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'
dfm1 = pd.read_csv(path + 'joined_Metadata.csv')


## read TON values from R. Stauffer
de = pd.read_excel("/home/poyraden/Analysis/Homogenization_public/Files/valentia/sonde_tco_valentia.xlsx")
de['yyyymmddhh (UTC)'] = de['yyyymmddhh (UTC)'].astype(str)
de['Date'] = de['yyyymmddhh (UTC)'].apply(lambda x:x[0:8] )
de['DateTime'] = de['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))


dfm1['DateTime'] = dfm1['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
dfm1['Date'] = dfm1['DateTime'].dt.strftime('%Y-%m-%d')
#
#
dfm1 = dfm1[dfm1.TOCol < 999]
dfm1 = dfm1[dfm1.O3SondeTotal < 999]
dfm1 = dfm1[dfm1.O3SondeTotal_hom < 999]


# de = de[de.Date < '20201210' ]
print('dqa file', dfm1.DateTime.min(), dfm1.DateTime.max())
print('ton file', de.DateTime.min(), de.DateTime.max())
print(len(de), len(dfm1))

dfm1.loc[:,'DateTime2'] = dfm1.loc[:,'DateTime']
de.loc[:,'DateTime2'] = de.loc[:,'DateTime']
dfm1 = dfm1.set_index('DateTime2')
de = de.set_index('DateTime2')
common_index = set(dfm1.index).intersection(de.index)
df1 = dfm1.loc[common_index].copy()
df2 = de.loc[common_index].copy()
df2 = df2[~df2.index.duplicated(keep='first')]

print(len(common_index), len(df1), len(df2))
df2['O3SondeTotal'] = df1['O3SondeTotal']
df2['rdif_r'] = (df2['Sonde TCO'] - df1['O3SondeTotal']) /df1['O3SondeTotal'] * 100

df1['rdif_b_dqa'] = (df1['O3SondeTotal_hom'] - df1['TOCol']) / df1['O3SondeTotal_hom'] * 100
df1['rdif_b_ndacc'] = (df1['O3SondeTotal'] - df1['TOCol']) / df1['O3SondeTotal'] * 100


# 'OMI TCO', 'OMPS TCO', 'GOME-2A TCO', 'GOME-2B TCO'
df1['rdif_omi_hom'] = (df1['O3SondeTotal_hom'] - df2['OMI TCO'])/df1['O3SondeTotal_hom'] * 100
df1['rdif_omi'] = (df1['O3SondeTotal'] - df2['OMI TCO'])/df1['O3SondeTotal'] * 100
df2['rdif_omi_r'] = (df2['Sonde TCO'] - df2['OMI TCO'])/df2['Sonde TCO'] * 100


df1['rdif_omps_hom'] = (df1['O3SondeTotal_hom'] - df2['OMPS TCO'])/df1['O3SondeTotal_hom'] * 100
df1['rdif_omps'] = (df1['O3SondeTotal'] - df2['OMPS TCO'])/df1['O3SondeTotal'] * 100
df1['rdif_gomea_hom'] = (df1['O3SondeTotal_hom'] - df2['GOME-2A TCO'])/df1['O3SondeTotal_hom'] * 100
df1['rdif_gomea'] = (df1['O3SondeTotal'] - df2['GOME-2A TCO'])/df1['O3SondeTotal'] * 100
df1['rdif_gomeb_hom'] = (df1['O3SondeTotal_hom'] - df2['GOME-2B TCO'])/df1['O3SondeTotal_hom'] * 100
df1['rdif_gomeb'] = (df1['O3SondeTotal'] - df2['GOME-2B TCO'])/df1['O3SondeTotal'] * 100

df1['rdif_dqa'] = (df1['O3SondeTotal_hom'] - df1['O3SondeTotal'])/df1['O3SondeTotal_hom'] * 100

Plotname = 'TON_RDif_sonde_nors80'

fig, axs = plt.subplots(2, sharex=True, sharey=False, figsize=(17, 9))
fig.suptitle('Valentia TO values  ')

axs[0].plot(df1.DateTime, df1.O3SondeTotal_hom, label = 'O3Sonde DQA',  marker = "s", linestyle='None', markersize = 4)
# axs[0].plot(df1.DateTime, df1.O3Sonde_raw, label = 'O3Sonde Raw',  marker = ".", linestyle='None')
axs[0].plot(df1.DateTime, df1.O3SondeTotal, label = 'O3Sonde WOUDC ',  marker = ".",  linestyle='None')
axs[0].set_ylabel('O3 [DU]')
axs[0].set_ylim(100, 600)
axs[0].legend(loc="lower left")
#
axs[1].plot(df1.DateTime, df1.rdif_dqa, label = 'Rel. Dif.',  marker = ".", linestyle='None')
axs[1].set_ylabel('(DQA-WOUDC)/DQA[%]')
axs[1].legend(loc="lower left")
axs[1].set_ylim(-5, 5)
plt.axhline(y=0, color='grey', linestyle=':')

path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'
plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
plt.show()

#############

# df1 = df1[df1.DateTime > '20050101']
# df2 = df2[df2.DateTime > '20050101']

Plotname = 'TON_Brewer_comparison'

fig, axs = plt.subplots(2, sharex=True, sharey=False, figsize=(17, 9))
fig.suptitle('Valentia TO values sonde vs Brewer')
axs[0].plot(df1.DateTime, df1['TOCol'], label = 'Brewer TO',  marker = ".", linestyle='None')
# axs[0].plot(df1.DateTime, df1['O3SondeTotal'], label = 'O3SondeTotal',  marker = ".", linestyle='None')
axs[0].set_ylabel('O3 [DU]')

axs[0].legend(loc="upper right")
axs[0].set_ylim(100, 600)


axs[1].plot(df1.DateTime, df1['rdif_b_dqa'], label = 'RDif Sonde-DQA vs Brewer',  marker = ".", linestyle='None')
axs[1].plot(df1.DateTime, df1['rdif_b_ndacc'], label = 'RDif Sonde-WOUDC vs Brewer',  marker = ".", linestyle='None')
axs[1].legend(loc="upper right")
axs[1].set_ylim(-20, 20)
axs[1].axhline(y=0, color='grey', linestyle =":")
axs[1].set_ylabel('(Sonde-Brewer)/Sonde[%]')



#
# axs[2].plot(df1.DateTime, df1['rdif_b_ndacc'], label = 'RDif Sonde-WOUDC vs Brewer',  marker = ".", linestyle='None')
# axs[2].legend(loc="upper right")

path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'
plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/TON/  ' + Plotname + '.pdf')
#
plt.show()

Plotname = 'TON_satellite_one'
fig, axs = plt.subplots(2, sharex=True, sharey=False, figsize=(17, 9))
fig.suptitle('Valentia TO values')

# axs[0].plot(df1.DateTime, df1.rdif_dqa, label = 'RDif',  marker = ".", linestyle='None')
# axs[0].set_ylabel('RDif')
# axs[0].legend(loc="upper right")
# axs[0].set_ylim(-10, 10)


# axs[1].set_ylim(-10, 10)
axs[0].title.set_text('WOUDC')
# axs[1].plot(df1.DateTime, df1.rdif_omi_hom, label = 'rdif_omi_hom',  marker = ".", linestyle='None', markersize = 4)
axs[0].plot(df1.DateTime, df1.rdif_omi, label = 'OMI',  marker = ".", linestyle='None', markersize = 6)
axs[0].plot(df1.DateTime, df1.rdif_omps, label = 'OPMS',  marker = ".", linestyle='None', markersize = 6)
axs[0].plot(df1.DateTime, df1.rdif_gomea, label = 'GOME-2A',  marker = ".", linestyle='None', markersize = 6)
axs[0].plot(df1.DateTime, df1.rdif_gomeb, label = 'GOME-2B',  marker = ".", linestyle='None', markersize = 6)
axs[0].legend(loc="lower left")
axs[0].set_ylabel('(Sonde - Satellite)/Sonde[%]')

axs[0].set_ylim(-20, 20)
axs[0].axhline(y=0, color='grey', linestyle ="-")


# df1['rdif_omi_hom_ma'] = df1['rdif_omi_hom'].rolling(window=5).mean()
axs[1].title.set_text('DQA ')

axs[1].plot(df1.DateTime, df1.rdif_omi_hom, label = 'OMI',  marker = ".", linestyle='None', markersize = 6)
axs[1].plot(df1.DateTime, df1.rdif_omps_hom, label = 'OPMS',  marker = ".", linestyle='None', markersize = 6)
axs[1].plot(df1.DateTime, df1.rdif_gomea_hom, label = 'GOME-2A',  marker = ".", linestyle='None', markersize = 6)
axs[1].plot(df1.DateTime, df1.rdif_gomeb_hom, label = 'GOME-2B',  marker = ".", linestyle='None', markersize = 6)
axs[1].set_ylabel('(Sonde - Satellite)/Sonde[%]')

axs[1].set_ylim(-20, 20)
axs[1].axhline(y=0, color='grey', linestyle ="-")
axs[1].legend(loc="lower left")

path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'
plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
plt.show()

######


Plotname = 'TON_satellite_two'
fig, axs = plt.subplots(4, sharex=True, sharey=False, figsize=(17, 9))
fig.suptitle('Valentia TON values  ( )')

axs[0].plot(df1.DateTime, df1.rdif_omi, label = 'OMI vs WOUDC',  marker = ".", linestyle='None', markersize = 4)
axs[0].plot(df1.DateTime, df1.rdif_omi_hom, label = 'OMI vs DQA',  marker = ".", linestyle='None', markersize = 4)
axs[0].axhline(y=0, color='grey', linestyle ="-")
axs[0].set_ylabel('(Sonde - Satellite)/Sonde[%]')
axs[0].legend(loc="upper right")
axs[0].set_ylim(-10,10)


# axs[1].set_ylim(-10, 10)
# axs[1].plot(df1.DateTime, df1.rdif_omi_hom, label = 'rdif_omi_hom',  marker = ".", linestyle='None', markersize = 4)
axs[1].plot(df1.DateTime, df1.rdif_omps, label = 'OPMS vs WOUDC',  marker = ".", linestyle='None', markersize = 4)
axs[1].plot(df1.DateTime, df1.rdif_omps_hom, label = 'OPMS vs DQA',  marker = ".", linestyle='None', markersize = 4)
# axs[1].set_ylabel('(Sonde - Satellite)/Sonde[%]')
axs[1].legend(loc="lower left")
axs[1].set_ylim(-10,10)
axs[1].axhline(y=0, color='grey', linestyle ="-")


# df1['rdif_omi_hom_ma'] = df1['rdif_omi_hom'].rolling(window=5).mean()
axs[2].plot(df1.DateTime, df1.rdif_gomea, label = 'GOME-2A vs WOUDC',  marker = ".", linestyle='None', markersize = 4)
axs[2].plot(df1.DateTime, df1.rdif_gomea_hom, label = 'GOME-2A vs DQA',  marker = ".", linestyle='None', markersize = 4)
# axs[2].set_ylabel('(Sonde - Satellite)/Sonde[%]')
axs[2].legend(loc="lower left")
axs[2].set_ylim(-10,10)
axs[2].axhline(y=0, color='grey', linestyle ="-")

axs[3].plot(df1.DateTime, df1.rdif_gomeb, label = 'GOME-2B vs WOUDC',  marker = ".", linestyle='None', markersize = 4)
axs[3].plot(df1.DateTime, df1.rdif_gomeb_hom, label = 'GOME-2B vs DQA',  marker = ".", linestyle='None', markersize = 4)
axs[3].set_ylim(-10,10)
axs[3].axhline(y=0, color='grey', linestyle ="-")
axs[3].legend(loc="lower left")




path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'
plt.savefig(path + 'Plots/TON/' + Plotname + '.png')
plt.savefig(path + 'Plots/TON/' + Plotname + '.eps')
plt.show()

# Plotname = 'TON_satellite_two'
# fig, ax = plt.subplots(figsize=(17, 9))
# fig.suptitle('Valentia TON values')
# ax = df1['rdif_gomeb_hom'].plot.hist()
# plt.show()
#