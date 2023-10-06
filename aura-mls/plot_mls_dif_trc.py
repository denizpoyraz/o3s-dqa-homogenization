import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.ticker
from datetime import datetime

##code copied from uccle paper, not written new

def plotyearly(main_xarray,std_main_xarray,main_xarray2,std_main_xarray2,main_xarray3,std_main_xarray3,
               Yax,xranges,xtitle,ytitle,plotname,plottitle):
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

    ax0.set_yticks([200,160,120,100,80,70,60,50,40,30,20,15,10,5])
    plt.ylim(250,4)

    ax0.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    # 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678

    ax0.errorbar(main_xarray2,Yax,xerr=std_main_xarray2,label='Non-Homogenized',marker="x",color='red',
                 linewidth=2,elinewidth=0.01,capsize=4,capthick=2.0)

    ax0.errorbar(main_xarray,Yax,xerr=std_main_xarray,label='Homogenized',marker="o",color='green',
                 linewidth=2,elinewidth=0.01,capsize=4,capthick=2.0)
    ax0.errorbar(main_xarray3,Yax,xerr=std_main_xarray3,label='Homogenized+TRC',marker="o",color='C0',
                 linewidth=2,elinewidth=0.01,capsize=4,capthick=2.0)

    std_p5 = [i + 5 for i in main_xarray]
    std_m5 = [i - 5 for i in main_xarray]

    print(std_main_xarray)
    print(main_xarray)
    print(std_p5)
    ax0.legend(loc='lower right',frameon=True,fontsize='x-small')

    ax0.axvspan(-5, 5, alpha=0.2, color='grey')


    #    #
    # plt.savefig('/home/poyraden/Analysis/Homogenization_public/Plots/Plots_hom_eu/till2015_' + plotname + '.pdf')
    # plt.savefig('/home/poyraden/Analysis/Homogenization_public/Plots/Plots_hom_eu/' + plotname + '.eps')
    plt.savefig('/home/poyraden/Analysis/Homogenization_public/Plots/Plots_hom_eu/v2' + plotname + '.png')


    plt.show()

#######################################################################################################################
# #######################################
#
# sname = 'ny-aalesund'
# scname='Ny-Aalesund'
# sccname = 'Ny-Alesund'
sname = 'sodankyla'
scname='Sodankyla'
sccname = 'Sodankyla'
# sname = 'scoresby'
# scname='Scoresbysund'
# sccname='Scoresbysund'

# check for period beofr 2015
# sname = 'lauder'
# scname='Lauder'
# sccname='Lauder'
# sname = 'lerwick'
# scname='Lerwick'
# sccname='Lerwick'
# sname = 'uccle'
# scname='Uccle'
# sccname='Uccle'
xlim = [-40,40]
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/MLS/'

df = pd.read_csv(path + f'MLS_{scname}Interpolated_nors80_v05_dqa.csv')
# df=pd.read_csv("/home/poyraden/Analysis/AURA_MLS/MLS_UccleInterpolated_2004-2018_Dif_test.csv") #paper

ptitle = f'{scname} Homogenized - MLS (v05)'
tag = 'trc'
plot_name = f'{sname}_rdif_MLS_v05_{tag}'

df2 = pd.read_csv(path + f'MLS_{scname}Interpolated_nors80_v05_original.csv')

df3 = pd.read_csv(path + f'MLS_{scname}Interpolated_nors80_v05_dqa_trc.csv')


print(len(df.drop_duplicates(['Date'])))

df=df[df.PreLevel <= 260]
df2=df2[df2.PreLevel <= 260]
df3=df3[df3.PreLevel <= 260]

df = df[df.PO3_UcIntLin < 99]
df = df[df.PO3_MLS < 99]
df = df[df.PO3_UcIntLin > 0]
df = df[df.PO3_MLS > 0]

df2 = df2[df2.PO3_UcIntLin < 99]
df2 = df2[df2.PO3_MLS < 99]

df3 = df3[df3.PO3_UcIntLin < 99]
df3 = df3[df3.PO3_MLS < 99]

# df = df[df.Date < 20150101]
# df2 = df2[df2.Date < 20150101]

#
df=df.reset_index()
df2=df2.reset_index()
df3=df3.reset_index()

df['Date']=pd.to_datetime(df['Date'],format='%Y%m%d')
df['Year'] = pd.DatetimeIndex(df['Date']).year
# df['RDif_UcIntLin'] = 100 * (np.asarray(df.PO3_MLS) - np.asarray(df.PO3_UcIntLin)) / np.asarray(df.PO3_UcIntLin)
df['RDif_UcIntLin'] = 100 * (np.asarray(df.PO3_UcIntLin) - np.asarray(df.PO3_MLS)) / np.asarray(df.PO3_UcIntLin)

df2['Date']=pd.to_datetime(df2['Date'],format='%Y%m%d')
df2['Year'] = pd.DatetimeIndex(df2['Date']).year
# df2['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_MLS) - np.asarray(df2.PO3_UcIntLin)) / np.asarray(df2.PO3_UcIntLin)
df2['RDif_UcIntLin'] = 100 * (np.asarray(df2.PO3_UcIntLin) - np.asarray(df2.PO3_MLS)) / np.asarray(df2.PO3_UcIntLin)


df3['Date']=pd.to_datetime(df3['Date'],format='%Y%m%d')
df3['Year'] = pd.DatetimeIndex(df3['Date']).year
df3['RDif_UcIntLin'] = 100 * (np.asarray(df3.PO3_UcIntLin) - np.asarray(df3.PO3_MLS)) / np.asarray(df3.PO3_UcIntLin)

print(df.Date.min(), df.Date.max())
print('Check size', len(df), len(df2))

dfd={}
dfd2={}
dfd3={}

# to bi fixed: replace 15 with datsize and 17 with prelevelsize



pre_level =[215.443,177.828,146.78,121.153,100.0,82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,
   17.7828,14.678,12.1153,10.0000,8.25404,6.81292,5.62341]

presize=len(pre_level)



rdif_ucmean=[];
rdif_ucmedian=[];
rdif_ucint=[]
rdif2_ucmean=[];
rdif2_ucmedian=[];
rdif2_ucint=[]

main_dif_ucmean=[];
main_dif_ucmean2=[];
main_rdif_ucmean=[];
main_rdif2_ucmean=[]
main_dif_ucint=[];
main_dif_ucint2=[];

main_rdif_org_ucint=[];
main_rdif_dqa_ucint=[]

# always 15,15, first date then pressure index

main_mean_rorg_ucint=np.zeros(presize);
main_mean_rdqa_ucint=np.zeros(presize);
main_mean_rtrc_ucint=np.zeros(presize);


main_std_rorg_ucint=np.zeros(presize);
main_std_rdqa_ucint=np.zeros(presize);
main_std_rtrc_ucint=np.zeros(presize);



print('first filling')


for j in range(len(pre_level)):
    print(j, pre_level[j])

    dfd[j]=df[df.PreLevel == pre_level[j]]
    dfd[j] = dfd[j].reset_index()

    dfd2[j] = df2[df2.PreLevel == pre_level[j]]
    dfd2[j] = dfd2[j].reset_index()
    
    dfd3[j] = df3[df3.PreLevel == pre_level[j]]
    dfd3[j] = dfd3[j].reset_index()

print('end of first filling')
## testing

for ld in range(presize):
    # for the all years
    main_std_rdqa_ucint[ld]=np.nanstd(dfd[ld]['RDif_UcIntLin'])
    main_std_rorg_ucint[ld]=np.nanstd(dfd2[ld]['RDif_UcIntLin'])
    main_std_rtrc_ucint[ld]=np.nanstd(dfd3[ld]['RDif_UcIntLin'])

    main_mean_rdqa_ucint[ld]=np.nanmedian(dfd[ld]['RDif_UcIntLin'])
    main_mean_rorg_ucint[ld]=np.nanmedian(dfd2[ld]['RDif_UcIntLin'])
    main_mean_rtrc_ucint[ld]=np.nanmedian(dfd3[ld]['RDif_UcIntLin'])

    # print(ld, ' main_mean_ucint[ld]',  main_mean_ucint2[ld])
    # print(ld, '  main_mean_rdqa_ucint[ld]',   main_mean_rdqa_ucint[ld])



# print(' V2  0th entry, pressure 216' , main_rdif_dqa_ucint[0], 'main_mean_rdqa_ucint ',   main_mean_rdqa_ucint)


print('two')

#
Y=[215.443,177.828,146.78,121.153,100.0,82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,
   17.7828,14.678,12.1153,10.0000,8.25404,6.81292,5.62341]
#




#
# plotyearly(mean_r2ucint,std_r2ucint,main_mean_rdqa_ucint,main_std_rdqa_ucint,Y,[-60,60],date_label,
#            f'MLS-{scname} {tag} [%]','Pressure [hPa]','RDif_MLS-Uccle_PerYear_usinginterpolation')

plottitle = f'{sccname} '
plotyearly(main_mean_rdqa_ucint,main_std_rdqa_ucint,main_mean_rorg_ucint,main_std_rorg_ucint,
           main_mean_rtrc_ucint,main_std_rtrc_ucint,
           Y,xlim,f'ECC - MLS [%]',f'Pressure [hPa]',plot_name, plottitle)

