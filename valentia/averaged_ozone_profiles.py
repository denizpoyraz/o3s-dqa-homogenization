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


# dfm = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/uccle/DQA_nors80/Valentia_Metada_DQA_nors80.csv')


path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'
allFiles = sorted(glob.glob(path + "DQA_nors80/*all_hom_nors80.hdf"))
#
listall = []

# for (filename) in (allFiles):
#     df = pd.read_hdf(filename)
#
#     listall.append(df)
#
# name_out = 'Valentia_AllData_DQA_nors80'
# dfall = pd.concat(listall, ignore_index=True)
#
# dfall.to_hdf(path + "DQA_nors80/" + name_out + ".hdf", key = 'df')

df = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/valentia/DQA_nors80/Valentia_AllData_DQA_nors80.hdf')
# df2 = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/valentia/DQA/Valentia_AllData_DQA_nors80.hdf')



o3, o3err, y = Calc_average_profile_pressure(df, 'O3')
o3c, o3cerr, y = Calc_average_profile_pressure(df, 'O3c')
o3nc, o3cerr, y = Calc_average_profile_pressure(df, 'O3_nc')

# o3c2, o3cerr2, y = Calc_average_profile_pressure(df2, 'O3c')

df1 = pd.DataFrame()
df1['o3c'] = o3c
df1['y'] = y
df1['o3'] = o3

# df2 = pd.DataFrame()
df1['o3nc'] = o3nc
# df1['y'] = y

int1 =  int((3.9449 * (df1.o3c.shift() + df1.o3c) * np.log(df1.y.shift() / df1.y)).sum())
int2 =  int((3.9449 * (df1.o3.shift() + df1.o3) * np.log(df1.y.shift() / df1.y)).sum())
int3 =  int((3.9449 * (df1.o3nc.shift() + df1.o3nc) * np.log(df1.y.shift() / df1.y)).sum())

print('before 1998',     int1)
print('after 1998',     int2)
print('after 1998',     int3)

# o3nc, o3ncerr, y = Calc_average_profile_pressure(df1, 'O3_nc')

path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'

Plotname = 'hom_vs_woudc'
# Plotname = 'RS80'

fig, ax = plt.subplots(figsize=(17, 9))

ax.plot(o3c, y,  label = ' DQA ' + 'TO=' + str(int1), marker = 's', markersize = 6)
ax.plot(o3, y,  label = 'WOUDC ' + 'TO=' + str(int2), marker = 'o', markersize = 6)
# ax.plot(o3nc, y,  label = ' Raw ' + 'TO=' + str(int3), marker = 's', markersize = 6)

# ax.plot(o3c, y,  label = ' DQA ' + 'TO=' + str(int1), marker = 's', markersize = 6, linestyle='None')
# ax.plot(o3, y,  label = 'WOUDC ' + 'TO=' + str(int2), marker = 'o', markersize = 6, linestyle='None')

ax.set_ylim(1000, 5)
ax.set_yscale('log')
ax.legend(loc="best")
ax.set_ylabel('Pressure [hPa]')
ax.set_xlabel('PO3 [mPa]')

plt.savefig(path + 'Plots/' + Plotname + '.png')
plt.savefig(path + 'Plots/' + Plotname + '.eps')
plt.savefig(path + 'Plots/  ' + Plotname + '.pdf')

plt.show()

