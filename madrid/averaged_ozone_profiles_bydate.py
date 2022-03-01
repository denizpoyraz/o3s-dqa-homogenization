import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import glob

from functions.homogenization_functions import o3_integrate

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


dfm = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA/Madrid_Metada_DQA.csv')

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# allFiles = sorted(glob.glob(path + "DQA_final/*all_hom_nors80.hdf"))
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

# dfall.to_csv(path + "DQA/" + name_out + ".csv")
# dfall.to_hdf(path + "DQA_final/" + name_out + ".hdf", key = 'df')

df1 = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_final/Madrid_AllData_DQA_nors80.hdf')
# df2 = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA/Madrid_AllData_DQA_nors80.hdf')


df1 = df1[(df1.Date > '1997-12-31') & (df1.Date < '2005-12-31') ]

# df1 = df1[(df1.Date > '2010-12-31')]


dates = df1.drop_duplicates(['Date'])['Date'].tolist()

dfm1 = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_final/Madrid_Metada_DQA_nors80.csv')

print(list(dfm1))
print(len(dates))

dfm1['o3max'] = 9999
dfm1['o3max_raw'] = 9999
dfm1['o3max_hom'] = 9999

dfm1['o3min'] = 9999
dfm1['o3min_raw'] = 9999
dfm1['o3min_hom'] = 9999

for i in dates:
    print(i)
    dt = df1[df1.Date == i]
    dfm1.loc[dfm1.Date == i, 'o3max'] = dt.O3.max()
    dfm1.loc[dfm1.Date == i, 'o3max_raw'] = dt.O3_nc.max()
    dfm1.loc[dfm1.Date == i, 'o3max_hom'] = dt.O3c.max()

    dfm1.loc[dfm1.Date == i, 'o3min'] = dt.O3.min()
    dfm1.loc[dfm1.Date == i, 'o3min_raw'] = dt.O3_nc.min()
    dfm1.loc[dfm1.Date == i, 'o3min_hom'] = dt.O3c.min()

    #adding to the metadata

    # if i == '1998-04-17':
    # plotting part
    name = 'Profile_' + str(i)

    # o3, o3err, y = Calc_average_profile_pressure(dt, 'O3')
    # o3c, o3cerr, y = Calc_average_profile_pressure(dt, 'O3c')
    # o3nc, o3ncerr, y = Calc_average_profile_pressure(dt, 'O3_nc')
    #
    # dfp = pd.DataFrame()
    # dfp['o3c'] = o3c
    # dfp['y'] = y
    # dfp['o3nc'] = o3nc
    # dfp['o3'] = o3
    #
    # intw = int((3.9449 * (dfp.o3.shift() + dfp.o3) * np.log(dfp.y.shift() / dfp.y)).sum())
    # intc = int((3.9449 * (dfp.o3c.shift() + dfp.o3c) * np.log(dfp.y.shift() / dfp.y)).sum())
    # intnc = int((3.9449 * (dfp.o3nc.shift() + dfp.o3nc) * np.log(dfp.y.shift() / dfp.y)).sum())



    intw = int(o3_integrate(dt, 'O3'))
    intc = int(o3_integrate(dt, 'O3c'))
    intnc = int(o3_integrate(dt, 'O3_nc'))

    fig, ax = plt.subplots(figsize=(17, 9))

    ax.plot(dt.O3c, dt.Pair, label= str(i) +' DQA, TO = ' + str(intc), marker='s', markersize=2)
    ax.plot(dt.O3, dt.Pair, label= str(i) + ' WOUDC, TO = ' + str(intw), marker='d', markersize=2)
    ax.plot(dt.O3_nc, dt.Pair, label= str(i) + ' Raw, TO = ' + str(intnc), marker='s', markersize=2)

    # ax.plot(o3, y,  label = '1994-2006 RS80 correction', marker = 's', markersize = 6)
    # ax.plot(o3c, y , label = '1994-2006 no RS80 correction', marker = 'd', markersize = 6)
    ax.set_ylim(1000, 5)
    ax.set_yscale('log')
    ax.legend(loc="best")
    ax.set_ylabel('Pressure [hPa]')
    ax.set_xlabel('PO3 [mPa]')

    # plt.savefig(path + 'Plots/Day_Profile/' + name + '.png')
    # plt.savefig(path + 'Plots/Day_Profile/' + name + '.eps')
    # plt.savefig(path + 'Plots/Day_Profile/  ' + name + '.pdf')

    # plt.show()


# dfm1.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_final/Madrid_Metada_DQA_nors80_updated.csv')