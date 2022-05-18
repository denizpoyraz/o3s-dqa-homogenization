import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import glob

def Calc_average_profile_pressure(dft, xcolumn):
    # nd = len(dataframelist)

    # yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
    #         12, 10, 8, 6]

    # yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600,  550, 500, 450,  400, 350, 325, 300, 275, 250, 240, 230, 220, 210, 200,
    #         190, 180, 170, 160, 150, 140, 130, 125, 120, 115, 110, 105,  100,95, 90, 85, 80, 75, 70, 65, 60, 55,
    #         50, 45, 40,  35, 30, 28, 26, 24, 22,  20, 19, 18, 17, 16, 15,  14, 13.5, 13, 12.5,  12, 11.5, 11, 10.5,
    #         10, 9.75, 9.50, 9.25, 9, 8.75, 8.5, 8.25,  8, 7.75, 7.5, 7.25,  7, 6.75, 6.50, 6.25, 6]

    yref = [1000.000, 825.404, 681.292, 562.341, 464.159, 383.119, 316.228, 261.016, 215.443, 177.828, 146.780,
             121.153, 100.000,
             82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.6780, 12.1153, 10.0000,
             8.25404,
             6.81292, 5.62341]

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


        grid_min = yref[i+1]
        grid_max = yref[i]
        Ygrid[i] = (grid_min + grid_max) / 2.0

        # filta = dft.Pair >= grid_min
        # filtb = dft.Pair < grid_max

        filta = dft.Pair >= grid_min
        filtb = dft.Pair < grid_max

        filter1 = filta & filtb
        dftmp1['X'] = dft[filter1][xcolumn]

        filtnull = dftmp1.X > -9999.0
        dfgrid['X'] = dftmp1[filtnull].X

        Xgrid[i] = np.nanmean(dfgrid.X)
        Xsigma[i] = np.nanstd(dfgrid.X)


    return Xgrid, Xsigma, Ygrid



path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/'
# allFiles = sorted(glob.glob(path + "/DQA_nors80/*all_hom_nors80.hdf"))
#
# listall = []
#
# for (filename) in (allFiles):
#     df = pd.read_hdf(filename)
#
#     listall.append(df)
#
# name_out = 'Madrid_AllData_DQA_nors80'
# dfall = pd.concat(listall, ignore_index=True)
#
# dfall.to_csv(path + "/DQA_nors80/" + name_out + ".csv")
# dfall.to_hdf(path + "/DQA_nors80/" + name_out + ".hdf", key = 'df')

# df1 = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Madrid_AllData_DQA_nors80.hdf')

df1 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/lauder/DQA_nors80/Binned/test_LauderInterpolated_dqa_nors80.csv')
df2 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/lauder/DQA_rs80/Binned/test_LauderInterpolated_dqa_rs80.csv')
df3 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/lauder/MLS/new_MLS_LauderInterpolated_nors80_v04_dqa.csv')
df4 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/lauder/MLS/new_MLS_LauderInterpolated_rs80_v04_dqa.csv')


df1['Pair'] = df1['PreLevel']
df2['Pair'] = df2['PreLevel']
df3['Pair'] = df3['PreLevel']
df4['Pair'] = df4['PreLevel']


# df2 = df2[df2.Date >= "2004-08-03"]
# df1 = df1[df1.Date >= "2004-08-03"]

df1 = df1[df1.PO3_UcIntLin < 99]
df2 = df2[df2.PO3_UcIntLin < 99]
df3 = df3[df3.PO3_UcIntLin < 99]
df4 = df4[df4.PO3_UcIntLin < 99]



#
o3, o3err, y = Calc_average_profile_pressure(df1, 'PO3_UcIntLin_dqa')
o3_rs80, o3err_rs80, y = Calc_average_profile_pressure(df2, 'PO3_UcIntLin_dqa')
o3_t, o3err_t, y = Calc_average_profile_pressure(df3, 'PO3_UcIntLin')
o3_trs80, o3err_t, y = Calc_average_profile_pressure(df4, 'PO3_UcIntLin')
o3_mls, o3err_t, y = Calc_average_profile_pressure(df3, 'PO3_MLS')


# o3, o3err, y = Calc_average_profile_pressure(df2, 'PO3_UcIntLin')
# o3_mls, o3err_mls, y = Calc_average_profile_pressure(df2, 'PO3_MLS')

# print(o3)
# print(o3_mls)

path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/'

# Plotname = 'AllPeriod_MLS_rs80'
# Plotname = 'RS80'
# Plotname = 'AllPeriod_DQA_rs80'
Plotname = 'MLSPeriod_DQA_rs80'

# ptitle = 'Lauder DQA Homogenization vs MLS v04'
# ptitle = 'Lauder DQA Homogenization with and without RS80'
ptitle = 'Lauder DQA Homogenization with and without RS80 vs MLS v04'


fig, ax = plt.subplots(figsize=(15, 10))


#
# ax.plot(o3, y , label = ' DQA corrections', marker = 'd', markersize = 6, linestyle='-')
# ax.plot(o3_rs80, y,  label = 'DQA and RS80 corrections', marker = 's', markersize = 6, linestyle='-')
ax.plot(o3_t, y , label = '  DQA corrections', marker = 'd', markersize = 6, linestyle='-')
ax.plot(o3_trs80, y , label = ' DQA corrections and RS80 mls file', marker = 'd', markersize = 6, linestyle='-')
ax.plot(o3_mls, y , label = 'MLS v04', marker = 'd', markersize = 6, linestyle='-')

# ax.plot(o3, y , label = 'Lauder DQA corrections')
# ax.plot(o3_mls, y,  label = 'MLS v04')
# ax.plot(o3nc, y , label = '1994-2021 No Correction', marker = 'd', markersize = 6)

# ax.set_ylim(1000, 5)
ax.set_ylim(350, 5)

ax.set_yscale('log')
ax.legend(loc="best")
ax.set_ylabel('Pressure [hPa]')
ax.set_xlabel('PO3 [mPa]')
ax.set_title(ptitle)

#
plt.savefig(path + 'Plots/' + Plotname + '.png')
plt.savefig(path + 'Plots/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/  ' + Plotname + '.pdf')

plt.show()

# Plotname = 'RDif_98-21_PumpLocation_case5'
# # Plotname = 'RS80'
#
#
# # rdif = (o3 - o3c)/o3c * 100
#
# rdif = [((i - j)/j)*100 for i,j in zip(o3, o3c)]
#
#
# fig, ax = plt.subplots(figsize=(17, 9))
#
# ax.plot(rdif, y,  label = '1998-2021 pump location correction', marker = 's', markersize = 6)
# # ax.plot(o3, y,  label = '1994-2006 RS80 correction', marker = 's', markersize = 6)
# # ax.plot(o3c, y , label = '1994-2006 no RS80 correction', marker = 'd', markersize = 6)
# ax.set_ylim(1000, 5)
# # ax.set_yscale('log')
# ax.legend(loc="best")
# ax.set_ylabel('Pressure [hPa]')
# # ax.set_xlabel('PO3 [mPa]')
#

# plt.show()