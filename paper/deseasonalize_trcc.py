import pandas as pd
import numpy as np
from datetime import datetime
import statistics
import sys

# sname = 'uccle'
# scname = 'Uccle'
sname = 'sodankyla'
scname='Sodankyla'
bool_trcc = True
bool_km = True
if bool_trcc: nt = 'trc'
else:nt = 'original'
if bool_km: en = 'km'
else: en = 'plev'
fname = f'monthly_mean_{scname}_{nt}_{en}'
print(fname)
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{sname}/DQA_trc/Binned/'

dfi = pd.read_csv(path+f'{fname}.csv')

# dfi = dfi.drop(['Unnamed: 0'], axis=1)
dfi['DateTime'] = pd.to_datetime(dfi['DateTime'], format='%Y-%m')
dfi.set_index('DateTime', inplace=True)

plev = ['1000hPa', '825hPa', '681hPa', '562hPa', '464hPa', '383hPa', '316hPa', '261hPa', '215hPa', '177hPa','121hPa',
        '100hPa', '82hPa', '68hPa', '56hPa', '46hPa', '38hPa', '31hPa', '26hPa', '21hPa', '17hPa','12hPa', '10hPa', '8hPa', '6hPa', '5hPa']

if bool_km:
    plev = ['0km', '1km', '2km', '3km', '4km', '5km', '6km', '7km', '8km', '9km', '10km', '11km', '12km', '13km', '14km',
          '15km', '16km', '17km', '18km', '19km', '20km', '21km', '22km', '23km', '24km', '25km', '26km', '27km', '28km',
          '29km', '30km', '31km', '32km', '33km', '34km', '35km']

plen = len(plev)
dlen = len(dfi)

uc = {}
uct = {}
uct2 = {}

alt = [''] * plen

jan = [[0] * dlen] * plen;
feb = [[0] * dlen] * plen;
mar = [[0] * dlen] * plen;
apr = [[0] * dlen] * plen;
may = [[0] * dlen] * plen;
jun = [[0] * dlen] * plen;
jul = [[0] * dlen] * plen;
aug = [[0] * dlen] * plen;
sep = [[0] * dlen] * plen;
oct = [[0] * dlen] * plen;
nov = [[0] * dlen] * plen;
dec = [[0] * dlen] * plen

jan_mean = [0] * plen;
feb_mean = [0] * plen;
mar_mean = [0] * plen;
apr_mean = [0] * plen;
may_mean = [0] * plen;
jun_mean = [0] * plen;
jul_mean = [0] * plen;
aug_mean = [0] * plen;
sep_mean = [0] * plen;
oct_mean = [0] * plen;
nov_mean = [0] * plen;
dec_mean = [[0] * dlen] * plen

for ir in range(plen):  # per each km
    uct[ir] = dfi[dfi[plev[ir]] > 0]
    # uct[ir] = uc[ir]
    print(ir, plev[ir])

    jan[ir].clear();
    feb[ir].clear();
    mar[ir].clear();
    apr[ir].clear();
    may[ir].clear();
    jun[ir].clear()
    jul[ir].clear();
    aug[ir].clear();
    sep[ir].clear();
    oct[ir].clear();
    nov[ir].clear();
    dec[ir].clear()

    for i in (uct[ir][plev[ir]].index):

        if (pd.Timestamp(i).month == 1):
            # print('hey',plev[ir],  i, (uct[ir][plev[ir]].loc[pd.Timestamp(i)]))
            jan[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            jan[ir] = list(filter(lambda a: a != 0, jan[ir]))
        if (pd.Timestamp(i).month == 2):
            feb[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            feb[ir] = list(filter(lambda a: a != 0, feb[ir]))
        if (pd.Timestamp(i).month == 3):
            mar[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            mar[ir] = list(filter(lambda a: a != 0, mar[ir]))
        if (pd.Timestamp(i).month == 4):
            apr[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            apr[ir] = list(filter(lambda a: a != 0, apr[ir]))
        if (pd.Timestamp(i).month == 5):
            may[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            may[ir] = list(filter(lambda a: a != 0, may[ir]))
        if (pd.Timestamp(i).month == 6):
            jun[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            jun[ir] = list(filter(lambda a: a != 0, jun[ir]))
        if (pd.Timestamp(i).month == 7):
            jul[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            jul[ir] = list(filter(lambda a: a != 0, jul[ir]))
        if (pd.Timestamp(i).month == 8):
            aug[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            aug[ir] = list(filter(lambda a: a != 0, aug[ir]))
        if (pd.Timestamp(i).month == 9):
            sep[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            sep[ir] = list(filter(lambda a: a != 0, sep[ir]))
        if (pd.Timestamp(i).month == 10):
            oct[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            oct[ir] = list(filter(lambda a: a != 0, oct[ir]))
        if (pd.Timestamp(i).month == 11):
            nov[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            nov[ir] = list(filter(lambda a: a != 0, nov[ir]))
        if (pd.Timestamp(i).month == 12):
            dec[ir].append(uct[ir][plev[ir]].loc[pd.Timestamp(i)])
            dec[ir] = list(filter(lambda a: a != 0, dec[ir]))

        jan_mean[ir] = np.nanmean(jan[ir])
        feb_mean[ir] = np.nanmean(feb[ir])
        mar_mean[ir] = np.nanmean(mar[ir])
        apr_mean[ir] = np.nanmean(apr[ir])
        may_mean[ir] = np.nanmean(may[ir])
        jun_mean[ir] = np.nanmean(jun[ir])
        jul_mean[ir] = np.nanmean(jul[ir])
        aug_mean[ir] = np.nanmean(aug[ir])
        sep_mean[ir] = np.nanmean(sep[ir])
        oct_mean[ir] = np.nanmean(oct[ir])
        nov_mean[ir] = np.nanmean(nov[ir])
        dec_mean[ir] = np.nanmean(dec[ir])

print(jan_mean[0])
print(jan_mean[1])

dfde = pd.DataFrame()
alt2 = [''] * plen

# now subtract the monthly means from each year and the corresponding month

for ir2 in range(plen):  # per each km
    alt2[ir2] = plev[ir2] + '_ds'
    print(ir2, plev[ir2])
    uct2[ir2] = dfi[dfi[plev[ir2]] > 0]
    # or uct[ir] = uc[ir].loc['1987-02-01':'2017-06-01']
    # uct[ir] = uc[ir]
    for i2 in (uct2[ir2][plev[ir2]].index):
        #
        # if (pd.Timestamp(i2).month == 1):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - jan_mean[ir2]
        # if (pd.Timestamp(i2).month == 2):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - feb_mean[ir2]
        # if (pd.Timestamp(i2).month == 3):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - mar_mean[ir2]
        # if (pd.Timestamp(i2).month == 4):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - apr_mean[ir2]
        # if (pd.Timestamp(i2).month == 5):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - may_mean[ir2]
        # if (pd.Timestamp(i2).month == 6):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - jun_mean[ir2]
        # if (pd.Timestamp(i2).month == 7):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - jul_mean[ir2]
        # if (pd.Timestamp(i2).month == 8):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - aug_mean[ir2]
        # if (pd.Timestamp(i2).month == 9):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - sep_mean[ir2]
        # if (pd.Timestamp(i2).month == 10):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - oct_mean[ir2]
        # if (pd.Timestamp(i2).month == 11):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - nov_mean[ir2]
        # if (pd.Timestamp(i2).month == 12):
        #     uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - dec_mean[ir2]
        if (pd.Timestamp(i2).month == 1):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - jan_mean[ir2])/jan_mean[ir2]
        if (pd.Timestamp(i2).month == 2):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - feb_mean[ir2])/feb_mean[ir2]
        if (pd.Timestamp(i2).month == 3):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - mar_mean[ir2])/mar_mean[ir2]
        if (pd.Timestamp(i2).month == 4):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - apr_mean[ir2])/apr_mean[ir2]
        if (pd.Timestamp(i2).month == 5):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - may_mean[ir2])/may_mean[ir2]
        if (pd.Timestamp(i2).month == 6):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - jun_mean[ir2])/jun_mean[ir2]
        if (pd.Timestamp(i2).month == 7):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - jul_mean[ir2])/jul_mean[ir2]
        if (pd.Timestamp(i2).month == 8):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - aug_mean[ir2])/aug_mean[ir2]
        if (pd.Timestamp(i2).month == 9):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - sep_mean[ir2])/sep_mean[ir2]
        if (pd.Timestamp(i2).month == 10):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - oct_mean[ir2])/oct_mean[ir2]
        if (pd.Timestamp(i2).month == 11):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - nov_mean[ir2])/nov_mean[ir2]
        if (pd.Timestamp(i2).month == 12):
            uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] = (uct2[ir2][plev[ir2]].loc[pd.Timestamp(i2)] - dec_mean[ir2])/dec_mean[ir2]

    dfde[alt2[ir2]] = uct2[ir2][plev[ir2]]

all = pd.concat([dfi, dfde], axis=1, sort=False)
#all.to_csv('/Volumes/HD3/KMI//MLR_Uccle/Files/1km_monthlymean_all.csv')

all.to_csv(path + fname + f'_deseas.csv')
