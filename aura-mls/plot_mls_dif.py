import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText
import matplotlib.ticker
from math import log
from datetime import time
from datetime import datetime
from scipy import signal


def plotyearly(xarray,std_xarray,main_xarray,std_main_xarray,Yax,xranges,plotlabel,xtitle,ytitle,plotname, plottitle):
    # def plotyearly(mean_ucint, std_ucint, Y, date_label, 'Uccle-MLS (mPa)','P Air (hPa)','Dif_Uccle-MLS_UcIntLinPerYear'):

    fig,ax0=plt.subplots()
    plt.ylim(250,3)
    plt.xlim(xranges)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(plottitle)

    ax0.tick_params(axis='both',which='both',direction='in')
    ax0.yaxis.set_ticks_position('both')
    ax0.xaxis.set_ticks_position('both')
    ax0.yaxis.set_minor_locator(AutoMinorLocator(10))
    ax0.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax0.set_yscale('log')
    ax0.axvline(x=0,color='grey',linestyle='--')
    markerlist = ['o', 'v', '^', '<', '>', '8', 's', 'p', 'P', 'h', 'X', '+', 'd', 'D', '*', '_', '|', '1','2']

    for j in range(len(xarray)):
        print(j)
        plt.plot(xarray[j],Yax,label=plotlabel[j],linewidth=0.5,marker=markerlist[j])


    ax0.set_yticks([200,160,120,100,80,70,60,50,40,30,20,15,10,5])
    plt.ylim(250,4)

    ax0.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    # 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678

    ax0.errorbar(main_xarray,Yax,xerr=std_main_xarray,label='All',marker="x",color='black',
                 linewidth=2,elinewidth=0.01,capsize=4,capthick=2.0)

    std_p5 = [i + 5 for i in main_xarray]
    std_m5 = [i - 5 for i in main_xarray]

    print(std_main_xarray)
    print(main_xarray)
    print(std_p5)
    ax0.legend(loc='upper right',frameon=True,fontsize='x-small')

    ax0.axvspan(-5, 5, alpha=0.2, color='grey')
    # ax0.fill_between(std_m5, std_p5, 1)
    # ax0.fill_betweenx(Yax,  std_m5, std_p5, alpha=0.2, facecolor='k')

    # ax0.axvspan(-5, 5, alpha=0.2, color='grey')

    #    #
    plt.savefig('/home/poyraden/Analysis/Homogenization_public/Plots/Plots_hom_eu/yearly_' + plotname + '.eps')
    plt.savefig('/home/poyraden/Analysis/Homogenization_public/Plots/Plots_hom_eu/yearly_' + plotname + '.png')

    #
    # plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots_timenight/Dif_UcIntLinPerYear.pdf')
    # plt.savefig('/home/poyraden/Analysis/AURA_MLS/Plots/Plots/Plots_timenight/Dif_UcIntLinPerYear.eps')

    plt.show()

#######################################################################################################################
# #######################################

# sname = 'scoresby'
# scname='Scoresbysund'
# sccname='Scoresbysund'
sname = 'sodankyla'
scname='Sodankyla'
sccname = 'Sodankyla'

xlim = [-25,25]
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/MLS/'
#
tag = 'dqa'
dft = pd.read_csv(path + f'MLS_{scname}Interpolated_nors80_v05_{tag}.csv')

# df = pd.read_csv(path + f'MLS_{scname}Interpolated_nors80_v05_original.csv')
# tag = 'original'
print(len(dft.drop_duplicates(['Date'])))

# df = df[df.PreLevel < 217]
dft=dft[dft.PreLevel <= 260]
# df = df[(df.Date < 20170101) | (df.Date > 20173112)]

# df=dft.reset_index()
# df = df.drop(['index'])
df = dft
df['RDif_UcIntLin'] = 100 * (np.asarray(df.PO3_UcIntLin) - np.asarray(df.PO3_MLS)) / np.asarray(df.PO3_UcIntLin)

df = df.drop(df.loc[(df.PreLevel < 60) & (df.RDif_UcIntLin > -30),], axis=1, inplace=True)
# df=df.reset_index()

df['Date']=pd.to_datetime(df['Date'],format='%Y%m%d')
df['Year'] = pd.DatetimeIndex(df['Date']).year
# df['RDif_UcIntLin'] = 100 * (np.asarray(df.PO3_MLS) - np.asarray(df.PO3_UcIntLin)) / np.asarray(df.PO3_UcIntLin)

# df = df[(df.PreLevel < 60) & (df.RDif_UcIntLin > -30)]
# df = df[df.Year < 2006]
df=df.reset_index()


dfd={}

# to bi fixed: replace 15 with datsize and 17 with prelevelsize

datestr=[''] * 21

date_label=[''] * 21

for d in range(2004,2023):
    i=d - 2004
    datestr[i]=datetime(d,1,1)
    date_label[i]=str(d)
    print(i,d,datestr[i], date_label[i])

datesize=19
pre_level =[215.443,177.828,146.78,121.153,100.0,82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,
   17.7828,14.678,12.1153,10.0000,8.25404,6.81292,5.62341]

presize=len(pre_level)

for dj in range(datesize):
    print(dj)
    dfd[dj]=df[(df.Date >= datestr[dj]) & (df.Date < datestr[dj + 1])]
    dfd[dj] = dfd[dj].reset_index()


rdif2_ucint=[]
main_rdif2_ucint=[]

# always 15,15, first date then pressure index
for dd in range(datesize):


    rdif2_ucint.append([])

    for t in range(presize):
        rdif2_ucint[dd].append([])
        main_rdif2_ucint.append([])


mean_ucint2=np.zeros((datesize,presize))

mean_r2ucint=np.zeros((datesize,presize))

main_mean_r2ucint=np.zeros(presize);


main_std_r2ucint=np.zeros(presize);


std_r2ucint=np.zeros((datesize,presize))

print('first filling')

print(datesize, presize)

for di in range(datesize):
    # print('di',di)
    for j in range(presize):
        # print(j)
        # # print(dfd[di].loc[dfd[di].PreLevel == pre_level[j],'RDif_UcIntLin'])
        # rdif2_ucint[di][j].append((dfd[di][dfd[di].PreLevel == pre_level[j]]['RDif_UcIntLin']).tolist()) #original
        #
        # main_rdif2_ucint[j].append(dfd[di].loc[dfd[di].PreLevel == pre_level[j],'RDif_UcIntLin']) # original paper

        for i in range(0,len(dfd[di]),presize):

            rdif2_ucint[di][j].append(dfd[di].at[i+j,'RDif_UcIntLin']) #original

            t = int(i+j)

            main_rdif2_ucint[j].append(dfd[di].at[i+j,'RDif_UcIntLin']) # original paper
dfm = {}

for m in range(len(pre_level)):

    dfm[m]=df[df.PreLevel == pre_level[m]]
    dfm[m] = dfm[m].reset_index()

for ld in range(presize):
    # for the all years
    main_std_r2ucint[ld]=np.nanstd(dfm[ld]['RDif_UcIntLin'])

    main_mean_r2ucint[ld]=np.nanmedian(dfm[ld]['RDif_UcIntLin'])
# print('here 0 ', len(main_rdif2_ucint[0]), np.nanmean(main_rdif2_ucint[0]), main_rdif2_ucint[0])
# print('here 1', len(main_rdif2_ucint[1]), np.nanmean(main_rdif2_ucint[1]), main_rdif2_ucint[1])

print('end of first filling')
## testing

for ld in range(presize):
    # for the all years
    # main_mean_r2ucint[ld]=np.nanmean(main_rdif2_ucint[ld])
    # main_std_r2ucint[ld]=np.nanstd(main_rdif2_ucint[ld])


    for l in range(datesize):
        # for the indivudual years

        # mean_ucint2[l,ld] = np.nanmean(dif_ucint2[l][ld])
        # mean_r2ucint[l,ld] = np.nanmean(rdif2_ucint[l][ld])
        mean_r2ucint[l,ld]=np.NaN if (rdif2_ucint[l][ld] != rdif2_ucint[l][ld]) else np.nanmean(rdif2_ucint[l][ld])
        # std_r2ucint[l,ld] = np.nanstd(rdif2_ucint[l][ld])
        std_r2ucint[l,ld]=np.NaN if (rdif2_ucint[l][ld] != rdif2_ucint[l][ld]) else np.nanstd(rdif2_ucint[l][ld])
#



print('two')

#
Y=[215.443,177.828,146.78,121.153,100.0,82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,
   17.7828,14.678,12.1153,10.0000,8.25404,6.81292,5.62341]
#


print('mean_r2ucint 0', mean_r2ucint[0][0])
print('std_r2ucint 0', std_r2ucint[0][0])
print('mean_r2ucint 1', mean_r2ucint[1][0])
print('std_r2ucint 1', std_r2ucint[1][0])
print('main_mean_r2ucint', main_mean_r2ucint[0:2])
print('main_std_r2ucint', main_std_r2ucint[0:2])

if tag == 'dqa': plottitle = f' Homogenized {sccname}'
else: plottitle = f' Non-Homogenized {sccname} '
print('mean_r2ucint', len(mean_r2ucint))
plotyearly(mean_r2ucint,std_r2ucint,main_mean_r2ucint,main_std_r2ucint,Y,[-60,60],date_label,
          f'ECC - MLS [%]','P Air [hPa]',f'RDif_MLS-{sccname}_PerYear_{tag}',plottitle)


