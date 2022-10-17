import pandas as pd
import numpy as np
import math
from math import log
from scipy.interpolate import interp1d
import glob
from re import search
from datetime import datetime
from functions.df_filter import filter_data

# ozone = 'O3_nc' # raw, no correction applied
# ozone = 'O3c_eta' # etac correction applied
# ozone = 'O3c_etabkg' # eta bkg correction applied
# ozone = 'O3c_etabkgtpump' # only phip correction applied
# ozone = 'O3c_etabkgtpumpphigr' # only tpump applied
# ozone = 'O3c_bkgphip'
ozone = 'O3' #woudc
# ozone = 'PO3_dqar'


# name_out = 'SodankylaInterpolated_dqa_nors80'
name_out = 'UccleInterpolated_dqa_nors80'
# name_out = 'LauderInterpolated_dqa_nors80'
# name_out = 'LauderInterpolated_dqa_nors80'
# name_out = 'scoresbyInterpolated_dqa_nors80'
# name_out = 'MadridInterpolated_dqa_nors80'



# path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/DQA_nors80/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/DQA_nors80/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/DQA_nors80/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/'

allFiles = sorted(glob.glob(path + "*_all_hom_nors80.hdf"))
print('len of files', len(allFiles))

# list_data = []
listall_data = []

# file_test = matcheddates[300:800]

for (filename) in (allFiles):
    file = open(filename, 'r')

    print(filename)

    df = pd.read_hdf(filename)
    # df['date'] = df['Date'].dt.strftime("%Y%m%d")
    df['date'] = df['Date']
    # df['date'] = df['DateTime'].dt.strftime("%Y%m%d")

    datestr = df.at[df.first_valid_index(), 'date']
    # print(datestr)


    # date_tmp = filename.split('/')[-1].split('.')[0][2:8]
    # fname = filename.split('/')[-1].split('.')[0][0:8]
    # fullname = filename.split('/')[-1].split('.')[0]
    # metaname = path  + fname + "_o3smetadata_nors80.csv"
    # metaname = path  + datestr + "_o3smetadata_nors80.csv"
    # print(metaname)


    # if search("2nd", fullname): metaname = path +  fname + "_2nd_metadata.csv"

    # date = datetime.strptime(date_tmp, '%y%m%d')
    # # print(date)
    # datef = date.strftime('%Y%m%d')
    # datestr = str(datef)

    # if datestr >= '20210421':continue
    # if datestr > '20061231': continue # no bkg values

    # print(filename)


    # print(filename)
    df = pd.read_hdf(filename)

    # print(list(df))
    # #lauder
    # df['Height'] = df['GPHeight']
    # df['TboxC'] = df['SampleTemperature']

    # df = filter_data(df)
    df = df[df.Pair != -9999]
    df = df[df.I > -99 ]
    # df = [df.O3 > 0]
    # df = df[df.Pair >= 5.62341]
    if len(df) < 10:
        print(filename, 'PROBLEM why', len(df))
        continue

    #for lauder
    # df['Height'] = df['GPHeight']
    # df['Height'] = df['Alt']

 # now downsample the lauder data remove descent list
    try: dfn = df[df.Height > 0]
    except TypeError:
        df['Height'] = df['Height'].astype(int)
        dfn = df[df.Height > 0]
    maxh = dfn.Height.max()

    if len(dfn) < 10:
        print('height problem', datestr)
        continue

    index = dfn[dfn["Height"] == maxh].index[0]


    descent_list = dfn[dfn.index > index].index.tolist()
    dfa = dfn.drop(descent_list)

     ##for the frozen solutions
    dfa = dfa.drop(dfa[(dfa[ozone] <= 2) & (dfa.Pair <= 10)].index)


    # yref = [1000.000, 825.404, 681.292, 562.341, 464.159, 383.119, 316.228, 261.016, 215.443, 177.828, 146.780,
    #          121.153, 100.000,
    #          82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.6780, 12.1153, 10.0000,
    #          8.25404,
    #          6.81292, 5.62341]
    #
    #

    # ymain_tmp = []
    # for j in range(len(yref)):
    #     if yref[j] <= np.max(ystation):
    #         ymain_tmp.append(yref[j])
    #
    # ymain = []
    # for j in range(len(ymain_tmp)):
    #     if ymain_tmp[j] >= np.min(ystation):
    #         ymain.append(ymain_tmp[j])

    xstation = np.array(dfa[ozone].tolist())
    ystation = np.array(dfa['Pair'].tolist())
    #

    ymain = [1000.000, 825.404, 681.292, 562.341, 464.159, 383.119, 316.228, 261.016, 215.443, 177.828, 146.780,
             121.153, 100.000,
             82.5404, 68.1292, 56.2341, 46.4159, 38.3119, 31.6228, 26.1016, 21.5443, 17.7828, 14.6780, 12.1153, 10.0000,
             8.25404,
             6.81292, 5.62341]

    dfa['MR_dqa'] = dfa['O3c'] / (dfa['Pair'] * 100000)


    xstation_nc = np.array(dfa['O3_nc'].tolist())
    xstation_eta = np.array(dfa['O3c_eta'].tolist())
    xstation_etabkg = np.array(dfa['O3c_etabkg'].tolist())
    xstation_etabkgtpump = np.array(dfa['O3c_etabkgtpump'].tolist())
    xstation_etabkgtpumpphigr = np.array(dfa['O3c_etabkgtpumpphigr'].tolist())
    xstation_dqa = np.array(dfa['O3c'].tolist())
    xstation_dqa_mr = np.array(dfa['MR_dqa'].tolist())




    if ((len(xstation) < 15) | (len(xstation) == 0)):
        print('Problem here ? ', header_date)
        continue


    if ((len(xstation) < 10) | (len(xstation) == 0)):
        print('here one')
        continue

    # print(len(ystation), len(xstation_nc))

    fl = interp1d(ystation, xstation)
    fl_nc = interp1d(ystation, xstation_nc)
    fl_eta = interp1d(ystation, xstation_eta)
    fl_etabkg = interp1d(ystation, xstation_etabkg)
    fl_etabkgtpump = interp1d(ystation, xstation_etabkgtpump)
    fl_etabkgtpumpphigr = interp1d(ystation, xstation_etabkgtpumpphigr)
    fl_dqa = interp1d(ystation, xstation_dqa)
    fl_dqa_mr = interp1d(ystation, xstation_dqa_mr)


    ## try except part
    xinter_linear = [0] * len(ymain);
    xinter_linear_nc = [0] * len(ymain);
    xinter_linear_eta = [0] * len(ymain);
    xinter_linear_etabkg = [0] * len(ymain);
    xinter_linear_etabkgtpump = [0] * len(ymain);
    xinter_linear_etabkgtpumpphigr = [0] * len(ymain);
    xinter_linear_dqa = [0] * len(ymain);
    xinter_linear_dqa_mr = [0] * len(ymain);

    # xinter_linear_woudc = [0] * len(ymain);
    # xinter_linear_woudc_v2 = [0] * len(ymain);

    for ix in range(len(ymain)):

        try:
            xinter_linear[ix] = fl(ymain[ix])
            xinter_linear_nc[ix] = fl_nc(ymain[ix])
            xinter_linear_eta[ix] = fl_eta(ymain[ix])
            xinter_linear_etabkg[ix] = fl_etabkg(ymain[ix])
            xinter_linear_etabkgtpump[ix] = fl_etabkgtpump(ymain[ix])
            xinter_linear_etabkgtpumpphigr[ix] = fl_etabkgtpumpphigr(ymain[ix])
            xinter_linear_dqa[ix] = fl_dqa(ymain[ix])
            xinter_linear_dqa_mr[ix] = fl_dqa_mr(ymain[ix])

        except ValueError:
            xinter_linear[ix] = np.nan
            xinter_linear_nc[ix] = np.nan
            xinter_linear_eta[ix] = np.nan
            xinter_linear_etabkg[ix] = np.nan
            xinter_linear_etabkgtpump[ix] = np.nan
            xinter_linear_etabkgtpumpphigr[ix] = np.nan
            xinter_linear_dqa[ix] = np.nan
            xinter_linear_dqa_mr[ix] = np.nan




    for ir in range(len(xinter_linear)):
        if (xinter_linear[ir] <= 0):
            # print(ymain[ir], xinter_linear[ir])
            xinter_linear[ir] = np.nan
            xinter_linear_nc[ir] = np.nan
            xinter_linear_eta[ir] = np.nan
            xinter_linear_etabkg[ir] = np.nan
            xinter_linear_etabkgtpump[ir] = np.nan
            xinter_linear_etabkgtpumpphigr[ir] = np.nan
            xinter_linear_dqa[ir] = np.nan
            xinter_linear_dqa_mr[ir] = np.nan



    header_date = df.at[df.first_valid_index(), 'Date']
    ddate = [df.at[df.first_valid_index(), 'Date']] * len(ymain)

    # dfl = pd.DataFrame(
    #     columns=['Date', 'PreLevel', 'PO3_UcIntLin'])

    dfl = pd.DataFrame()


    dfl['Date'] = ddate
    dfl['PreLevel'] = np.asarray(ymain)
    # dfl['PO3_UcMean'] = xmean
    # dfl['PO3_UcMedian'] = xmedian
    dfl['PO3_UcIntLin'] = xinter_linear
    dfl['PO3_UcIntLin_nc'] = xinter_linear_nc
    dfl['PO3_UcIntLin_eta'] = xinter_linear_eta
    dfl['PO3_UcIntLin_etabkg'] = xinter_linear_etabkg
    dfl['PO3_UcIntLin_etabkgtpump'] = xinter_linear_etabkgtpump
    dfl['PO3_UcIntLin_etabkgtpumpphigr'] = xinter_linear_etabkgtpumpphigr
    dfl['PO3_UcIntLin_dqa'] = xinter_linear_dqa
    dfl['MR_UcIntLin_dqa'] = xinter_linear_dqa_mr


    # dfl['PO3_UcIntLin_woudc'] = xinter_linear_woudc
    # dfl['PO3_UcIntLin_woudc_v2'] = xinter_linear_woudc_v2


    listall_data.append(dfl)

# Merging all the data files to df

# df = pd.concat(list_data, ignore_index=True)
dfall = pd.concat(listall_data, ignore_index=True)
#
dfall.to_csv(path + "/Binned/" + name_out + ".csv")
dfall.to_hdf(path + "/Binned/" + name_out + ".h5", key = 'df')


###########################################################################################################################33

# ymain = [825.404,681.292,562.341,464.159,383.119,316.228,261.016,215.443,177.828,146.780,121.153,100.000,
#          82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,17.7828,14.6780,12.1153,10.0000,8.25404,
#          6.81292,  5.62341]

# linear interpolations
# try:
#     fl = interp1d(ystation, xstation)
#     fl_nc = interp1d(ystation, xstation_nc)
#     fl_eta = interp1d(ystation, xstation_eta)
#     fl_etabkg = interp1d(ystation, xstation_etabkg)
#     fl_etabkgtpump = interp1d(ystation, xstation_etabkgtpump)
#     fl_etabkgtpumpphigr = interp1d(ystation, xstation_etabkgtpumpphigr)
#     fl_dqa = interp1d(ystation, xstation_dqa)
#     # fl_woudc = interp1d(ystation, xstation_woudc)
#     # fl_woudc_v2 = interp1d(ystation, xstation_woudc_v2)
#
# except ValueError:
#     print('Value Error: ', datef)
#     continue

# print('ystation', np.array(ystation))
# print('xstation', xstation)

# print(len(ystation), len(xstation))
# print(len(ystation), len(xstation_nc))

# if(datef == '20140926'):continue
# if (datef == '20150423'): continue
# print(len(xstation), xstation)
# print(len(xstation_nc), xstation_nc)
