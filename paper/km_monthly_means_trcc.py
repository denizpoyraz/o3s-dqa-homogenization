import pandas as pd
import numpy as np
from datetime import datetime
import glob
from re import search
from scipy.interpolate import interp1d

pmain = [1000.000, 825.404, 681.292, 562.341, 464.159, 383.119, 316.228, 261.016, 215.443, 177.828, 146.780,
         121.153, 100.000,
         82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.6780, 12.1153, 10.0000,
         8.25404,
         6.81292, 5.62341]

## code to calculate data in each km and make monthly mean data
#actually you can use station binned data for pressure grids, now do the same for km binning

ozone = 'O3' #original
# sname = 'ny-aalesund'
# scname = 'Ny-Alesund'
sname = 'sodankyla'
scname='Sodankyla'
# sname = 'madrid'
# scname='Madrid'
# sname = 'uccle'
# scname='Uccle'


bool_trcc = True
if bool_trcc: nt = 'trc'
# else:nt = 'original'
name_out = f'{scname}_{nt}'
print((name_out))
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/DQA_trc/'

allFiles = sorted(glob.glob(path + "*all_trcc_hom.csv"))
print('len of files', len(allFiles))

listall_data = []
listall_datap = []

ymainh = np.arange(0.5,36.5,1)
ymaini = np.arange(0,36,1)


for (filename) in (allFiles):
    file = open(filename, 'r')
    if search('test', filename):continue
    # if search('upd', filename):continue

    # print(filename)

    if search('csv', filename):
        df = pd.read_csv(filename)
    if search('hdf', filename):df = pd.read_hdf(filename)
    # print(filename.split("nors80/")[1][0:10])
    # date_tmp = int(filename.split("nors80/")[1][0:10])
    # try:df['date'] = df['Date']
    # except KeyError:
    #     df['Date'] = date_tmp
    df['date'] = df['Date']
    # if date_tmp == 20070131:continue
    datestr = df.at[df.first_valid_index(), 'date']



    df = df[df.O3.isnull()==False]

    df = df[df.Pair != -9999]
    df = df[df.I > -99]
    df = df[df.I < 99]
    df = df[df.O3 > 0]
    df = df[df.O3 < 99]
    if bool_trcc:
        df = df[df.O3_trcc > 0]
        df = df[df.O3_trcc < 99]

    if len(df) < 100:
        print('EMPTY DF', filename)
        continue



    dfn = df[df.Height > 0]
    if len(dfn) == 0:
        print('Problematic files', filename)
        continue
    maxh = dfn.Height.max()
    index = dfn[dfn["Height"] == maxh].index[0]
    descent_list = dfn[dfn.index > index].index.tolist()
    dfa = dfn.drop(descent_list)
     ##for the frozen solutions
    dfa = dfa.drop(dfa[(dfa[ozone] <= 2) & (dfa.Pair <= 10)].index)
    dfa['Height'] = dfa['Height']/1000

    dfl = pd.DataFrame()
    dfp = pd.DataFrame()

    xstation = np.array(dfa[ozone].tolist())
    ystation = np.array(dfa['Height'].tolist())
    pstation = np.array(dfa['Pair'].tolist())

    if bool_trcc:
        dfa = dfa[dfa.O3_trcc > 0]
        dfa = dfa[dfa.O3_trcc < 99]
        xstation = np.array(dfa[f'O3_{nt}'].tolist())

    fl = interp1d(ystation, xstation)
    flp = interp1d(pstation, xstation)

    xinter_linearh = [0] * len(ymainh)
    xinter_lineari = [0] * len(ymaini)
    xinter_linearp = [0] * len(pmain)

    for ih in range(len(ymainh)):
        try:
            xinter_linearh[ih] = fl(ymainh[ih])
        except ValueError:
            xinter_linearh[ih] = np.nan
    for i in range(len(ymaini)):
        try:
            xinter_lineari[i] = fl(ymaini[i])
        except ValueError:
            xinter_lineari[i] = np.nan
        dfl.at[0, f'{i}km'] = xinter_linearh[i]

    for p in range(len(pmain)):
        try:
            xinter_linearp[p] = flp(pmain[p])
        except ValueError:
            xinter_linearp[p] = np.nan
        pv = int(pmain[p])
        dfp.at[0, f'{pv}hPa'] = xinter_linearp[p]

    header_date = df.at[df.first_valid_index(), 'Date']
    ddate = df.at[df.first_valid_index(), 'Date']


    dfl['Date'] = ddate
    try:dfl['DateTime'] = pd.to_datetime(dfl['Date'], format='%Y%m%d')
    except ValueError:dfl['DateTime'] = pd.to_datetime(dfl['Date'], format='%Y-%m-%d')

    dfp['Date'] = ddate
    try:dfp['DateTime'] = pd.to_datetime(dfp['Date'], format='%Y%m%d')
    except ValueError: dfp['DateTime'] = pd.to_datetime(dfp['Date'], format='%Y-%m-%d')

    listall_data.append(dfl)
    listall_datap.append(dfp)


dfall = pd.concat(listall_data, ignore_index=True)
dfall = dfall.drop_duplicates(['Date'])
dfall.to_csv(path + "/Binned/" + name_out + '_km.csv')

dfallp = pd.concat(listall_datap, ignore_index=True)
dfallp = dfallp.drop_duplicates(['Date'])
dfallp.to_csv(path + "/Binned/" + name_out + '_plev.csv')

cnames = ['0km', '1km', '2km', '3km', '4km', '5km', '6km', '7km', '8km', '9km', '10km', '11km', '12km', '13km', '14km',
          '15km', '16km', '17km', '18km', '19km', '20km', '21km', '22km', '23km', '24km', '25km', '26km', '27km', '28km',
          '29km', '30km', '31km', '32km', '33km', '34km', '35km']

pnames = ['1000hPa', '825hPa', '681hPa', '562hPa', '464hPa', '383hPa', '316hPa', '261hPa', '215hPa', '177hPa', '146hPa',
          '121hPa', '100hPa', '82hPa', '68hPa', '56hPa', '46hPa', '38hPa', '31hPa', '26hPa', '21hPa', '17hPa', '14hPa',
          '12hPa', '10hPa', '8hPa', '6hPa', '5hPa']


dfm = dfall.groupby(pd.PeriodIndex(dfall['DateTime'], freq="M"))[cnames].mean()
dfm.to_csv(path + "/Binned/monthly_mean_" + name_out + "_km.csv")

dfpm = dfallp.groupby(pd.PeriodIndex(dfallp['DateTime'], freq="M"))[pnames].mean()
dfpm.to_csv(path + "/Binned/monthly_mean_" + name_out + "_plev.csv")

