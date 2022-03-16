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

    yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600,  550, 500, 450,  400, 350, 325, 300, 275, 250, 240, 230, 220, 210, 200,
            190, 180, 170, 160, 150, 140, 130, 125, 120, 115, 110, 105,  100,95, 90, 85, 80, 75, 70, 65, 60, 55,
            50, 45, 40,  35, 30, 28, 26, 24, 22,  20, 19, 18, 17, 16, 15,  14, 13.5, 13, 12.5,  12, 11.5, 11, 10.5,
            10, 9.75, 9.50, 9.25, 9, 8.75, 8.5, 8.25,  8, 7.75, 7.5, 7.25,  7, 6.75, 6.50, 6.25, 6]

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

        filta = dft.Pair >= grid_min
        filtb = dft.Pair < grid_max
        filter1 = filta & filtb
        dftmp1['X'] = dft[filter1][xcolumn]

        filtnull = dftmp1.X > -9999.0
        dfgrid['X'] = dftmp1[filtnull].X

        Xgrid[i] = np.nanmean(dfgrid.X)
        Xsigma[i] = np.nanstd(dfgrid.X)


    return Xgrid, Xsigma, Ygrid



path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
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

df1 = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Madrid_AllData_DQA_nors80.hdf')



# if date2 < '1998-12-02':
#     string_pump_location = 'case3'
# if date2 >= '1998-12-02':
#     string_pump_location = 'InternalPump'

# if date2 <= '2006-03-01':
#     # rsmodel = 'RS80'
#     bool_rscorrection = True
# if date2 >= '2006-03-08 ':
#     bool_rscorrection = False

df1 = df1[df1.Date > '1998-12-02' ]
df1 = df1[df1.Date < '2005-06-01' ]


# print(len(df1), len(df2))
# df1['DQA_minus_WOUDC'] = df1['O3Sonde_hom_burst'] - df1['O3Sonde_burst']

# df1 = df1[df1.DQA_minus_WOUDC < 0]

# df1r = df1[df1.Date < '2006-03-01' ]
# df2 = df2[df2.Date < '2006-03-01' ]

# o3, o3err, y = Calc_average_profile_pressure(df1r, 'O3c')
# o3c, o3cerr, y = Calc_average_profile_pressure(df2, 'O3c')

o3, o3err, y = Calc_average_profile_pressure(df1, 'O3')
o3c, o3cerr, y = Calc_average_profile_pressure(df1, 'O3c')
o3nc, o3ncerr, y = Calc_average_profile_pressure(df1, 'O3_nc')

# o3c2, o3cerr2, y = Calc_average_profile_pressure(df2, 'O3c')

# dfp = pd.DataFrame()
# dfp['o3c'] = o3c
# dfp['y'] = y
# dfp['o3nc'] = o3nc
# dfp['o3'] = o3
#
# # dfp['y'] = y
# int1 =  int((3.9449 * (dfp.o3.shift() + dfp.o3) * np.log(dfp.y.shift() / dfp.y)).sum())
# int2 =  int((3.9449 * (dfp.o3c.shift() + dfp.o3c) * np.log(dfp.y.shift() / dfp.y)).sum())
# int3 =  int((3.9449 * (dfp.o3nc.shift() + dfp.o3nc) * np.log(dfp.y.shift() / dfp.y)).sum())

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'

Plotname = 'AllPeriod_DQA_WOUDC'
# Plotname = 'RS80'

fig, ax = plt.subplots(figsize=(17, 9))

# ax.plot(o3c, y,  label = '> 2008 DQA TO=' + str(int2), marker = 's', markersize = 6)
# ax.plot(o3, y , label = ' > 2008 WOUDC TO=' + str(int1), marker = 'd', markersize = 6)
# ax.plot(o3nc, y,  label = '> 2008 Raw TO=' + str(int3), marker = 's', markersize = 6)

# ax.plot(o3c, y,  label = '1998-2006 DQA TO=' + str(int2), marker = 's', markersize = 6)
# ax.plot(o3, y , label = ' 1998-2006 WOUDC TO=' + str(int1), marker = 'd', markersize = 6)
# ax.plot(o3nc, y,  label = '1998-2006 Raw TO=' + str(int3), marker = 's', markersize = 6)

# ax.plot(o3, y,  label = '1994-2021 WOUDC corrections', marker = 's', markersize = 6)
ax.plot(o3c, y , label = '1994-2021 DQA corrections', marker = 'd', markersize = 6)
ax.plot(o3, y,  label = '1994-2021 WOUDC corrections', marker = 's', markersize = 6)

# ax.plot(o3nc, y , label = '1994-2021 No Correction', marker = 'd', markersize = 6)

ax.set_ylim(1000, 5)
ax.set_yscale('log')
ax.legend(loc="best")
ax.set_ylabel('Pressure [hPa]')
ax.set_xlabel('PO3 [mPa]')
#
# plt.savefig(path + 'Plots/' + Plotname + '.png')
# plt.savefig(path + 'Plots/' + Plotname + '.eps')
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
# plt.savefig(path + 'Plots/' + Plotname + '.png')
# plt.savefig(path + 'Plots/' + Plotname + '.eps')
# plt.savefig(path + 'Plots/  ' + Plotname + '.pdf')
#
# plt.show()