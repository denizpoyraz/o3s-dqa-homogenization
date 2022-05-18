import pandas as pd
import numpy as np
import math
from math import log
from scipy.interpolate import interp1d
import glob

from functions.df_filter import filter_data


# 3rd code of MLS analysis
# write the Sodankyla data to a df that matches with MLS

problem = open("DQA_ProblematicFiles.txt", "a")


# path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/'
path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'

# ozone = 'O3_nc' # raw, no correction applied
# ozone = 'O3c_eta' # etac correction applied
# ozone = 'O3c_etabkg' # eta bkg correction applied
# ozone = 'O3c_etabkgtpump' # only phip correction applied
# ozone = 'O3c_etabkgtpumpphigr' # only tpump applied
# ozone = 'O3c_bkgphip'
ozone = 'O3c'
# ozone = 'PO3_dqar'

# name_out = 'MLS_SodankylaInterpolated_raw_rs80_v04'
# name_out = 'MLS_LauderInterpolated_previousversion_rs80_v04'
# name_out = 'MLS_MadridInterpolated_rs80_v04_dqa'
# name_out = 'MLS_LauderInterpolated_rs80_v04_dqa'
name_out = 'MLS_ScoresbyInterpolated_nors80_v04_dqa'


# mls data frame to read
# dfm = pd.read_csv(path + 'AURA_MLSData_MatchedMadrid_DQA_v04.csv')
# dfm = pd.read_csv(path + 'AURA_MLSData_MatchedSodankyla_DQA_v04.csv')
# dfm = pd.read_csv(path + 'AURA_MLSData_MatchedLauder_DQA_v04.csv')
dfm = pd.read_csv(path + 'AURA_MLSData_MatchedScoresby_DQA_v04.csv')


# dfm = dfm[dfm.Date < 20080612]
date_list = dfm.drop_duplicates(['Date']).Date.tolist()
print(len(date_list), date_list)

# list_data = []
listall_data = []

# file_test = matcheddates[300:800]

for date in date_list:
    # print(date, type(date))
    # if (date == 20190605) | (date == 20191010) | (date == 20200902) | (date == 20210414): continue
    # if date == 20190605:
    #     continue
    try: df = pd.read_hdf(path + "DQA_nors80/" + str(date) + "_all_hom_nors80.hdf")
    except FileNotFoundError:
        print('FileNotFoundError', date)
        continue

    # df = filter_data(df)
    if len(df) < 10:
        print(date, len(df))
        continue

    # df['Height'] = df['Alt']

    print(date)

    # df['Height'] = df['GPHeight']
 # now downsample the uccle data remove descent list
    dfn = df[df.Height > 0]
    maxh = dfn.Height.max()

    if len(dfn) < 10:
        print('height problem', date)
        continue

    index = dfn[dfn["Height"] == maxh].index[0]
    descent_list = dfn[dfn.index > index].index.tolist()
    dfa = dfn.drop(descent_list)


    ##for the frzoen solutions
    dfa = dfa.drop(dfa[(dfa[ozone] <= 2) & (dfa.Pair <= 10)].index)

    # skimming for the mls data
    dfas = dfa[(dfa.Pair >= 3) & (dfa.Pair <= 400)]
    # dfas = dfa[(dfa.Pair >= 10) & (dfa.Pair < 422 )]

    # string to get pressure values of the mls
    st = [''] * 55
    for p in range(55):
        st[p] = 'Pressure_' + str(p + 1)

    # previous
    yref = [383.119, 316.228, 261.016, 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159,
            38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.678, 12.1153, 10.0000, 8.25404, 6.81292, 5.62341, 4.64159]


    xuccle = dfas[ozone].tolist()
    yuccle = dfas['Pair'].tolist()

    xuccle = np.array(xuccle)
    yuccle = np.array(yuccle)
    if ((len(xuccle) < 15) | (len(xuccle) == 0)):
        # print('Problem here ? ', header_date)/
        problem.write(str(df.at[df.first_valid_index(), 'Date']) + '\n')
        continue

    # indu = np.where(xuccle < 0)[0]
    #
    # xuccle = np.delete(xuccle, indu)
    # yuccle = np.delete(yuccle, indu)
    # if ((len(xuccle) < 10) | (len(xuccle) == 0)):
    #     continue

    ymain = [316.228, 261.016, 215.443, 177.828, 146.78, 121.153, 100.0, 82.5404, 68.1292, 56.2341, 46.4159, 38.3119,
             31.6228, 26.1016, 21.5443, 17.7828, 14.678, 12.1153, 10.0000, 8.25404, 6.81292, 5.62341]

    if (max(yuccle) < max(ymain)): continue
    # if(min(yuccle) > min(ymain)):continue

    # 5 different linear interpolations
    fl = interp1d(yuccle, xuccle)
    # fn = interp1d(yuccle, xuccle, kind='nearest')
    # fp = interp1d(yuccle, xuccle, kind='previous')
    # fne = interp1d(yuccle, xuccle, kind='next')

    ## try except part
    xinter_linear = [0] * len(ymain);
    # xinter_nearest = [0] * len(ymain)
    # xinter_previous = [0] * len(ymain)
    # xinter_next = [0] * len(ymain)

    for ix in range(len(ymain)):
        try:
            xinter_linear[ix] = fl(ymain[ix])
        except ValueError:
            xinter_linear[ix] = np.nan


    for ir in range(len(xinter_linear)):
        if (xinter_linear[ir] <= 0):
            # print(ymain[ir], xinter_linear[ir])
            xinter_linear[ir] = np.nan


    df['Date'] = df['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
    df['Date'] = df["Date"].dt.strftime('%Y%m%d')

    header_date = df.at[df.first_valid_index(), 'Date']
    ddate = [df.at[df.first_valid_index(), 'Date']] * len(ymain)
    # im = 23
    im = 28
    ##ib = 8
    ib = 6

    dl = dfm.index[dfm.Date == int(header_date)].tolist()
    # print('dl', dl)
    mlspo3 = list(dfm.loc[dl[0], st[ib:im]])
    tim = dfm.loc[dl[0], 'Time']
    mlstime = [tim] * len(ymain)
    # print(header_date,'and', mlstime)
    dis = dfm.loc[dl[0], 'Dis']
    mlsdis = [dis] * len(ymain)
    if (len(dl) == 2):
        mlspo3_two = list(dfm.loc[dl[1], st[ib:im]])
        tim2 = dfm.loc[dl[1], 'Time']

        mlstime_two = [tim2] * len(ymain)
        dis2 = dfm.loc[dl[1], 'Dis']
        mlsdis_two = [dis2] * len(ymain)

    for il in range(len(mlspo3)):
        if (mlspo3[il] < 0):
            mlspo3[il] = np.nan
            xinter_linear[il] = np.nan
        if (len(dl) == 2):
            if ((mlspo3_two[il] < 0)):
                mlspo3_two[il] = np.nan
                xinter_linear[il] = np.nan


    dfl = pd.DataFrame(
        columns=['Date', 'Time', 'Dis', 'PreLevel', 'PO3_MLS', 'PO3_UcIntLin'])

    if (len(dl) == 1):
        dfl['Date'] = ddate
        dfl['Time'] = np.asarray(mlstime)
        dfl['Dis'] = np.asarray(mlsdis)
        dfl['PreLevel'] = np.asarray(ymain)
        dfl['PO3_MLS'] = mlspo3
        dfl['PO3_UcIntLin'] = xinter_linear

    if (len(dl) == 2):
        dfl['Date'] = np.concatenate((ddate, ddate))
        dfl['Time'] = np.concatenate((mlstime, mlstime_two))
        dfl['Dis'] = np.concatenate((mlsdis, mlsdis_two))
        dfl['PreLevel'] = np.concatenate((ymain, ymain))
        dfl['PO3_MLS'] = np.concatenate((mlspo3, mlspo3_two))
        dfl['PO3_UcIntLin'] = np.concatenate((xinter_linear, xinter_linear))


    listall_data.append(dfl)

# Merging all the data files to df

# df = pd.concat(list_data, ignore_index=True)
dfall = pd.concat(listall_data, ignore_index=True)

dfall.to_csv(path + "MLS/" + name_out + ".csv")
dfall.to_hdf(path + "MLS/" + name_out + ".h5", key = 'df')




