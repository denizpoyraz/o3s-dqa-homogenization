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


name_out = 'SodankylaInterpolated_dqa_nors80'
# name_out = 'UccleInterpolated_dqa_nors80'


path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
# path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/'
allFiles = sorted(glob.glob(path + "DQA_nors80/*_all_hom_nors80.hdf"))
print('len of files', len(allFiles))

# list_data = []
listall_data = []

# file_test = matcheddates[300:800]

for (filename) in (allFiles):
    file = open(filename, 'r')

    date_tmp = filename.split('/')[-1].split('.')[0][2:8]
    fname = filename.split('/')[-1].split('.')[0][0:8]
    fullname = filename.split('/')[-1].split('.')[0]
    metaname = path  + fname + "_o3smetadata_nors80.csv"
    if search("2nd", fullname): metaname = path +  fname + "_2nd_metadata.csv"

    date = datetime.strptime(date_tmp, '%y%m%d')
    # print(date)
    datef = date.strftime('%Y%m%d')
    datestr = str(datef)

    # if datef < '19970401':continue
    # if datef < '19941012': continue # no bkg values


    # if (datef > '20210428') : continue #already homogenized

    print(datef)


    # print(filename)
    df = pd.read_hdf(filename)

    # print(list(df))
    # #madrid
    # df['Height'] = df['GPHeight']
    # df['TboxC'] = df['SampleTemperature']

    # df = filter_data(df)
    df = df[df.Pair != -9999]
    df = df[df.I != -9999 ]
    if len(df) < 10:
        print(date, len(df))
        continue


 # now downsample the madrid data remove descent list
    dfn = df[df.Height > 0]
    maxh = dfn.Height.max()

    if len(dfn) < 10:
        print('height problem', date)
        continue

    index = dfn[dfn["Height"] == maxh].index[0]
    descent_list = dfn[dfn.index > index].index.tolist()
    dfa = dfn.drop(descent_list)

     ##for the frozen solutions
    dfa = dfa.drop(dfa[(dfa[ozone] <= 2) & (dfa.Pair <= 10)].index)



    # previous
    yref = [1000.000, 825.404,681.292,562.341,464.159,383.119,316.228,261.016,215.443,177.828,146.780,121.153,100.000,
             82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,17.7828,14.6780,12.1153,10.0000,8.25404,
             6.81292,  5.62341]
    uybin = []

    for y in range(len(yref) - 1):
        tmp = (log(yref[y]) + log(yref[y + 1])) / 2
        uybin.append(math.exp(tmp))
        # means will be calculated between uybin[i] and uybin[i+1]

    size = len(uybin) - 1
    xmean = [0] * size;
    xmedian = [0] * size

    for xb in range(size):
        tmp = dfa[(dfa.Pair < uybin[xb]) & (dfa.Pair >= uybin[xb + 1])][ozone].tolist()

        if (len(tmp) < 10):
            continue

        if ((np.mean(tmp) > 0)):
            # print(xb, 'posifitf tmp',tmp)

            xmean[xb] = np.mean(tmp)
            xmedian[xb] = np.median(tmp)

            if (xmean[xb] == 0): print('one here ?')

        if ((np.mean(tmp) < 0)):
            tmp = np.array(tmp)
            ind = np.where(tmp < .0)[0]
            new = np.delete(tmp, ind)

            if (int(len(tmp) / len(ind)) < 3):
                continue
            if (len(new) < 10):
                continue

            xmean[xb] = np.mean(new)
            xmedian[xb] = np.median(new)
            if (xmean[xb] == 0): print('two here ?')

        if ((np.mean(tmp) == 0)):
            xmean[xb] = np.nan

    for aa in range(size):
        if (xmean[aa] == 0):
            # print(dfas.iloc[0]['Header_Date'],uybin[aa], aa, xmean[aa])
            xmean[aa] = np.nan

    xmadrid = np.array(dfa[ozone].tolist())
    ymadrid = np.array(dfa['Pair'].tolist())

    xmadrid_nc = np.array(dfa['O3_nc'].tolist())
    xmadrid_eta = np.array(dfa['O3c_eta'].tolist())
    xmadrid_etabkg = np.array(dfa['O3c_etabkg'].tolist())
    xmadrid_etabkgtpump = np.array(dfa['O3c_etabkgtpump'].tolist())
    xmadrid_etabkgtpumpphigr = np.array(dfa['O3c_etabkgtpumpphigr'].tolist())
    xmadrid_dqa = np.array(dfa['O3c'].tolist())
    # xmadrid_woudc = np.array(dfa['O3c_woudc'].tolist())
    # xmadrid_woudc_v2 = np.array(dfa['O3c_woudc_v2'].tolist())


    if ((len(xmadrid) < 15) | (len(xmadrid) == 0)):
        print('Problem here ? ', header_date)
        continue

    indu = np.where(xmadrid < 0)[0]

    xmadrid = np.delete(xmadrid, indu)
    ymadrid = np.delete(ymadrid, indu)
    if ((len(xmadrid) < 10) | (len(xmadrid) == 0)):
        print('here one')
        continue

    ymain = [1000.000, 825.404,681.292,562.341,464.159,383.119,316.228,261.016,215.443,177.828,146.780,121.153,100.000,
             82.5404,68.1292,56.2341,46.4159,38.3119,31.6228,26.1016,21.5443,17.7828,14.6780,12.1153,10.0000,8.25404,
             6.81292,  5.62341]

    # linear interpolations
    try:
        fl = interp1d(ymadrid, xmadrid)
        fl_nc = interp1d(ymadrid, xmadrid_nc)
        fl_eta = interp1d(ymadrid, xmadrid_eta)
        fl_etabkg = interp1d(ymadrid, xmadrid_etabkg)
        fl_etabkgtpump = interp1d(ymadrid, xmadrid_etabkgtpump)
        fl_etabkgtpumpphigr = interp1d(ymadrid, xmadrid_etabkgtpumpphigr)
        fl_dqa = interp1d(ymadrid, xmadrid_dqa)
        # fl_woudc = interp1d(ymadrid, xmadrid_woudc)
        # fl_woudc_v2 = interp1d(ymadrid, xmadrid_woudc_v2)

    except ValueError:
        print('Value Error: ', datef)
        continue


    ## try except part
    xinter_linear = [0] * len(ymain);
    xinter_linear_nc = [0] * len(ymain);
    xinter_linear_eta = [0] * len(ymain);
    xinter_linear_etabkg = [0] * len(ymain);
    xinter_linear_etabkgtpump = [0] * len(ymain);
    xinter_linear_etabkgtpumpphigr = [0] * len(ymain);
    xinter_linear_dqa = [0] * len(ymain);
    # xinter_linear_woudc = [0] * len(ymain);
    # xinter_linear_woudc_v2 = [0] * len(ymain);


    for ix in range(len(ymain)):
        # xinter_linear[ix] = fl(ymain[ix])
        # print('one',date,  ymain[ix], xinter_linear[ix])
        try:
            xinter_linear[ix] = fl(ymain[ix])
            xinter_linear_nc[ix] = fl_nc(ymain[ix])
            xinter_linear_eta[ix] = fl_eta(ymain[ix])
            xinter_linear_etabkg[ix] = fl_etabkg(ymain[ix])
            xinter_linear_etabkgtpump[ix] = fl_etabkgtpump(ymain[ix])
            xinter_linear_etabkgtpumpphigr[ix] = fl_etabkgtpumpphigr(ymain[ix])
            xinter_linear_dqa[ix] = fl_dqa(ymain[ix])
            # xinter_linear_woudc[ix] = fl_woudc(ymain[ix])
            # xinter_linear_woudc_v2[ix] = fl_woudc_v2(ymain[ix])


            # if ymain[ix] > 215:
            #     print(date, 'one',  ymain[ix], xinter_linear[ix])
        except ValueError:
            xinter_linear[ix] = np.nan
            xinter_linear_nc[ix] = np.nan
            xinter_linear_eta[ix] = np.nan
            xinter_linear_etabkg[ix] = np.nan
            xinter_linear_etabkgtpump[ix] = np.nan
            xinter_linear_etabkgtpumpphigr[ix] = np.nan
            xinter_linear_dqa[ix] = np.nan
            # xinter_linear_woudc[ix] = np.nan
            # xinter_linear_woudc_v2[ix] = np.nan


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
            # xinter_linear_woudc[ix] = np.nan
            # xinter_linear_woudc_v2[ix] = np.nan


    header_date = df.at[df.first_valid_index(), 'Date']
    ddate = [df.at[df.first_valid_index(), 'Date']] * len(ymain)

    dfl = pd.DataFrame(
        columns=['Date', 'PreLevel', 'PO3_UcIntLin'])

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
    # dfl['PO3_UcIntLin_woudc'] = xinter_linear_woudc
    # dfl['PO3_UcIntLin_woudc_v2'] = xinter_linear_woudc_v2


    listall_data.append(dfl)

# Merging all the data files to df

# df = pd.concat(list_data, ignore_index=True)
dfall = pd.concat(listall_data, ignore_index=True)
#
dfall.to_csv(path + "DQA_nors80/Binned/" + name_out + ".csv")
dfall.to_hdf(path + "DQA_nors80/Binned/" + name_out + ".h5", key = 'df')



