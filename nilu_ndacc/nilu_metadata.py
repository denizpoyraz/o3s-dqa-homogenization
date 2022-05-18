import pandas as pd
import glob
from datetime import datetime
from re import search

from nilu_ndacc.read_nilu_functions import organize_df
import matplotlib.pyplot as plt

def plot_ib2():
    dfm = pd.read_csv(filepath + "Metadata/All_metadata.csv")

    dfm = dfm[dfm.iB2 < 0.5]

    dfm['Date'] = dfm['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
    dfm['Date2'] = dfm['Date']

    print(dfm[['Date']][0:2])
    # print('dtypes', dfm.dtypes)

    # date = datetime.strptime(date_tmp, '%y%m%d')

    # print(dfm[['Date','Datenf']][0:5])
    dfm = dfm.set_index('Date').sort_index()

    dfm['iB0'] = dfm['iB0'].astype(float)
    dfm['iB2'] = dfm['iB2'].astype(float)
    dfm['iB1'] = dfm['iB1'].astype(float)

    # scoresbysund  '1993', '1995', '2017'

    dfm1 = dfm[dfm.index < '1993']
    dfm2 = dfm[(dfm.index > '1993') & (dfm.index < '1995')]
    dfm3 = dfm[(dfm.index > '1995') & (dfm.index < '2017')]
    dfm4 = dfm[dfm.index > '2017']

    dfm1 = dfm1.set_index('Date2').sort_index()
    dfm2 = dfm2.set_index('Date2').sort_index()

    min1 = dfm.index.min()
    min12 = datetime.strptime('1992-01-05 00:00:0', '%Y-%m-%d %H:%M:%S')

    min2 = datetime.strptime('1993-01-06 00:00:0', '%Y-%m-%d %H:%M:%S')

    min3 = datetime.strptime('1995-01-06 00:00:0', '%Y-%m-%d %H:%M:%S')
    min4 = datetime.strptime('2016-12-31 00:00:0', '%Y-%m-%d %H:%M:%S')
    min5 = dfm.index.max()

    path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/Plots/ndacc_metadata/'

    print(list(dfm))

    plt.close('all')
    fig, ax = plt.subplots()

    # plt.fill_between(dfm.index, dfm.iB2.mean()-2 * dfm.iB2.std(), dfm.iB2.mean()+ 2 *dfm.iB2.std(), facecolor='#1f77b4', alpha=.2, label = r"Mean$\pm$2sigma")
    # plt.plot(dfm.index, dfm.iB2,  label="iB2", linestyle = 'None', color = '#1f77b4',  marker="o", markersize = 3)
    # ax.axhline(y=dfm.iB2.mean() + dfm.iB2.std(), color='#1f77b4',linestyle='--', label = "Mean iB2 + 1sigma")
    # ax.axhline(y=dfm.iB2.mean(), color='#1f77b4', label = "Mean iB2")
    # ax.axhline(y=dfm.iB2.mean() - dfm.iB2.std(), color='#1f77b4',linestyle='--', label = "Mean iB2 - 1sigma")

    plt.fill_between(dfm1.index, dfm1.iB2.mean() - 2 * dfm1.iB2.std(), dfm1.iB2.mean() + 2 * dfm1.iB2.std(),
                     facecolor='#1f77b4', alpha=.2, label=r"Mean$\pm$2sigma")
    plt.plot(dfm1.index, dfm1.iB2, label="iB2", linestyle='None', color='#1f77b4', marker="o", markersize=3)
    ax.hlines(y=dfm1.iB2.mean(), xmin=min1, xmax=min12, label='Mean=' + str(round(dfm1.iB2.mean(), 2)), color='#1f77b4',
              linewidth=2.5)
    # plt.ylim([-0.1, 0.3])

    plt.fill_between(dfm2.index, dfm2.iB2.mean() - 2 * dfm2.iB2.std(), dfm2.iB2.mean() + 2 * dfm2.iB2.std(),
                     facecolor='#ff7f0e', alpha=.2)
    plt.plot(dfm2.index, dfm2.iB2, linestyle='None', color='#ff7f0e', marker="o", markersize=3)
    # ax.axhline(y=dfm2.iB2.mean(),xmin = min2, xmax = min3, color='#ff7f0e')
    ax.hlines(y=dfm2.iB2.mean(), xmin=min2, xmax=min3, color='#ff7f0e', linewidth=2.5,
              label='Mean=' + str(round(dfm2.iB2.mean(), 2)))

    plt.fill_between(dfm3.index, dfm3.iB2.mean() - 2 * dfm3.iB2.std(), dfm3.iB2.mean() + 2 * dfm3.iB2.std(),
                     facecolor='#2ca02c', alpha=.2)
    plt.plot(dfm3.index, dfm3.iB2, linestyle='None', color='#2ca02c', marker="o", markersize=3)
    ax.hlines(y=dfm3.iB2.mean(), xmin=min3, xmax=min4, color='#2ca02c', linewidth=2.5,
              label='Mean=' + str(round(dfm3.iB2.mean(), 2)))

    plt.fill_between(dfm4.index, dfm4.iB2.mean() - 2 * dfm4.iB2.std(), dfm4.iB2.mean() + 2 * dfm4.iB2.std(),
                     facecolor='#8c564b', alpha=.2)
    plt.plot(dfm4.index, dfm4.iB2, linestyle='None', color='#8c564b', marker="o", markersize=3)
    ax.hlines(y=dfm4.iB2.mean(), xmin=dfm4.index.min(), xmax=dfm4.index.max(), color='#8c564b', linewidth=2.5,
              label='Mean=' + str(round(dfm4.iB2.mean(), 2)))
    # plt.title('Madrid iB2 values for homogenization')
    plt.title('Scoresbysund iB2 time-series')

    # ax.legend(loc='lower right', frameon=True, fontsize='small')
    ax.legend(loc='best', frameon=True, fontsize='small')

    plotname = 'iB2_all'
    # #
    plt.savefig(path + plotname + '.pdf')
    plt.savefig(path + plotname + '.png')

    plt.show()



filepath = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'
station_name = 'scoresby'

# ##read datafiles
allFiles = sorted(glob.glob(filepath + "ndacc/*.hdf"))


list_metadata = []

for filename in (allFiles):
    # print('filename', filename)
    name = filename.split(".")[-2].split("/")[-1][2:8]
    fname = filename.split(".")[-2].split("/")[-1]
    # not to read metada files with _md extension
    if (search("md", fname)) or (search("metadata", fname)): continue
    # if (fname == 'so980827') | (fname == 'so990708'): continue #one problematic file in sodankyal

    metafile = filepath + 'ndacc/' + fname + "_md.csv"
    print(metafile)

    # extract the date from file name
    date = datetime.strptime(name, '%y%m%d')
    datef = date.strftime('%Y%m%d')

    dfd = pd.read_hdf(filename)
    # dfd = pd.read_csv(filename)
    # dfd = dfd[1:]

    for i in list(dfd):
        dfd[i] = dfd[i].astype('float')

    if (len(dfd) < 100): continue
    if len(dfd.columns) < 8: continue

    # read the metadata file
    try:
        dfm_tmp = pd.read_csv(metafile, index_col=0, names=['Parameter', 'Value'])
        if (len(dfm_tmp)) < 15:
            print('skip this dataset')
            continue
    except FileNotFoundError:
        continue

    dfm_tmp = dfm_tmp.T

    dfl = pd.DataFrame()
    dfm = pd.DataFrame()

    # using the data and metadata make a new dataframe from them
    dfl, dfm = organize_df(dfd, dfm_tmp)
    dfm['Date'] = datef

    list_metadata.append(dfm)


# save all the metada in one file, either in hdf format or csv format
dff = pd.concat(list_metadata, ignore_index=True)

hdfall = filepath + "Metadata/All_metadata_ndacc.hdf"
csvall = filepath + "Metadata/All_metadata_ndacc.csv"

dff.to_hdf(hdfall, key = 'df')
dff.to_csv(csvall)


dff['Date'] = dff['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
dff['Date2'] = dff['Date']

dff = dff.set_index('Date').sort_index()

dff['iB0'] = dff['iB0'].astype(float)
dff['iB2'] = dff['iB2'].astype(float)
dff['iB1'] = dff['iB1'].astype(float)

dff2 = dff[dff.iB2 < 0.5]


dfm1 = dff2[dff2.index < '1993']
dfm2 = dff2[(dff2.index > '1993') & (dff2.index < '1995')]
dfm3 = dff2[(dff2.index > '1995') & (dff2.index < '2017')]
dfm4 = dff2[dff2.index > '2017']


dff.loc[dff.index < '1993', 'ib2_mean'] = dfm1.iB2.mean()
dff.loc[dff.index < '1993', 'ib2_std'] = dfm1.iB2.std()

dff.loc[(dff.index > '1993') & (dff.index < '1995'), 'ib2_mean'] = dfm2.iB2.mean()
dff.loc[(dff.index > '1993') & (dff.index < '1995'), 'ib2_std'] = dfm2.iB2.std()

dff.loc[(dff.index > '1995') & (dff.index < '2017'), 'ib2_mean'] = dfm3.iB2.mean()
dff.loc[(dff.index > '1995') & (dff.index < '2017'), 'ib2_std'] = dfm3.iB2.std()

dff.loc[dff.index > '2017', 'ib2_mean'] = dfm4.iB2.mean()
dff.loc[dff.index > '2017', 'ib2_std'] = dfm4.iB2.std()

hdfall = filepath + "Metadata/All_metadata_ndacc_ib2.hdf"
csvall = filepath + "Metadata/All_metadata_ndacc_ib2.csv"

dff.to_hdf(hdfall, key = 'df')
dff.to_csv(csvall)

#################################################################################################
#
# dfm = pd.read_csv(filepath + "Metadata/All_metadata.csv" )
#
# dfm = dfm[dfm.iB2 < 0.5]
#
# dfm['Date'] = dfm['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
# dfm['Date2'] = dfm['Date']
#
# print(dfm[['Date']][0:2])
# # print('dtypes', dfm.dtypes)
#
#
#
# # date = datetime.strptime(date_tmp, '%y%m%d')
#
# # print(dfm[['Date','Datenf']][0:5])
# dfm = dfm.set_index('Date').sort_index()
#
# dfm['iB0'] = dfm['iB0'].astype(float)
# dfm['iB2'] = dfm['iB2'].astype(float)
# dfm['iB1'] = dfm['iB1'].astype(float)
#
# #scoresbysund  '1993', '1995', '2017'
#
# dfm1 = dfm[dfm.index < '1993']
# dfm2 = dfm[(dfm.index > '1993') & (dfm.index < '1995')]
# dfm3 = dfm[(dfm.index > '1995') & (dfm.index < '2017')]
# dfm4 = dfm[dfm.index > '2017']
#
# dfm1 = dfm1.set_index('Date2').sort_index()
# dfm2 = dfm2.set_index('Date2').sort_index()
#
# min1 = dfm.index.min()
# min12 = datetime.strptime('1992-01-05 00:00:0', '%Y-%m-%d %H:%M:%S')
#
# min2 = datetime.strptime('1993-01-06 00:00:0', '%Y-%m-%d %H:%M:%S')
#
# min3 = datetime.strptime('1995-01-06 00:00:0', '%Y-%m-%d %H:%M:%S')
# min4 = datetime.strptime('2016-12-31 00:00:0', '%Y-%m-%d %H:%M:%S')
# min5 = dfm.index.max()
#
# print('before 1993', dfm1.iB2.mean())
# print('1993 - 1995', dfm2.iB2.mean())
# print('1995 - 2017', dfm3.iB2.mean())
# print('2017 - ', dfm4.iB2.mean())
#
#
#
#
#
# # dfm['mean2'] = 0
#

# plot_ib2()