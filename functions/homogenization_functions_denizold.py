import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from nilu_ndacc.read_nilu_functions import ComputeIBG

# the version that has some bugs, saved here just in case
# fixed during deniz's maternity leave

## General guidelines for Homogenisation of O3S-Data
# P03 = 0.043085 T_pump ( I_M - I_B) / (eta_c * Phi_p)
# T_pump " pump temperature in Kelvin
# I_M: ECC current in microA
# I_B background current
# eta_c: conersion efficiency
# Phi_p: gas volume flow rate in cm3^3/s

pval = np.array([1100, 200, 100, 50, 30, 20, 10, 7, 5, 3])

pvallog = [np.log10(i) for i in pval]
print(pvallog)

pval_sod = np.array([1100, 150, 100, 70, 60, 50, 40, 30, 20, 15, 10, 8, 5])
corr_sod = np.array([1,1,1.010, 1.022, 1.025, 1.035, 1.047, 1.065, 1.092, 1.120, 1.170, 1.206, 1.300])
corr_sod_unc = np.array([0 ,0 ,0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])


komhyr_86 = np.array([1, 1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092, 1.124])  # SP Komhyr
komhyr_95 = np.array([1,1,  1.007, 1.018, 1.029, 1.041, 1.066, 1.087, 1.124, 1.241])  # ENSCI Komhyr
john_02 = np.array([1, 1.035, 1.052, 1.072, 1.088, 1.145, 1.200, 1.1260, 1])  # ECC Johnson
sbrecht_98 = np.array([1, 1.027, 1.075, 1.108, 1.150, 1.280, 1.5, 1.8, 1])  # BM Steinbrecht
kob_66 = np.array([1, 1.02, 1.04, 1.07, 1.11, 1.25, 1.4, 1.66, 1])  # Kobayashi

# SensorType = 'SPC-6A'
VecP_ECC6A =    [    0,     2,     3,      5,    10,    20,    30,    50,   100,   200,   300,   500, 1000, 1100]
VecC_ECC6A_25 = [ 1.16,  1.16, 1.124,  1.087, 1.054, 1.033, 1.024, 1.015, 1.010, 1.007, 1.005, 1.002,    1,    1]
VecC_ECC6A_30 = [ 1.171, 1.171, 1.131, 1.092, 1.055, 1.032, 1.022, 1.015, 1.011, 1.008, 1.006, 1.004,    1,    1]

# SensorType = 'DMT-Z'
VecP_ECCZ = [0, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 1100]
VecC_ECCZ = [1.24, 1.24, 1.124, 1.087, 1.066, 1.048, 1.041, 1.029, 1.018, 1.013, 1.007, 1.002, 1, 1]

komhyr_86_unc = np.array([0,0, 0.005, 0.006, 0.008, 0.009, 0.010, 0.012, 0.014, 0.025])  # SP Komhyr
komhyr_95_unc = np.array([0,0, 0.005, 0.005, 0.008, 0.012, 0.023, 0.024, 0.024, 0.043])  # ECC Komhyr
john_02_unc = np.array([0, 0.011, 0.012, 0.015, 0.018, 0.020, 0.025, 0.030, 0.0])  # ECC Johnson
sbrecht_98_unc = np.array([0, 0.004, 0.006, 0.007, 0.011, 0.020, 0.1, 0.2, 0.0])  # BM Steinbrecht
kob_66_unc = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])  # Kobayashi

RS41_cor = np.array([1.171, 1.131, 1.092, 1.055, 1.032, 1.022, 1.015, 1.011, 1.008, 1.006, 1.004, 1.000])
RS41_pval = np.array([2.0, 3.0, 5.0, 10.0, 20.0, 30.0, 50.0, 100.0, 200.0, 300.0, 500.0, 1000.0])

RS41_cor = np.flipud(RS41_cor)
RS41_pval = np.flipud(RS41_pval)

RS80_cor = np.array([0, -0.34, 0.05, -0.17, -0.47, -0.61, -0.70, -0.83, -0.85, -0.91, -0.94, -0.97, -0.98, -1.02, -1.02, -1.01, -0.94, -0.94,
-1.01, -0.95,-1.00, -0.96, -0.98, -0.99, -1.00, -0.99, -1.01, -1.00, -1.06, -1.01, -1.04])
RS80_cor_err = np.array([0, 1.57, 1.56, 1.46, 1.43, 1.33, 1.26, 1.26, 1.21, 1.17, 1.14, 1.15, 1.16, 1.16, 1.17, 1.29, 1.28, 1.20, 1.29, 1.41,
1.36, 1.23, 1.31, 1.30, 1.39, 1.33, 1.35, 1.38, 1.40, 1.44, 1.60])
RS_alt = np.array([0, 1,2,3,4,5,6,7,8,9,10,11,12,13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])


# RS92_cor = np.array([0, 1.11, 0.56, 0.35, 0.23, 0.07, -0.03, -0.11, -0.16, -0.21, -0.26, -0.27, -0.27, -0.24, -0.28, -0.27,
# -0.25, -0.24, -0.22, -0.20, -0.19, -0.17, -0.15, -0.14, -0.14, -0.13, -0.12, -0.12, -0.12, -0.11, -0.11])
# RS92_cor_err = np.array([0, 1.42, 1.41, 1.17, 1.03, 0.92, 0.85, 0.78, 0.75, 0.70, 0.65, 0.62, 0.58, 0.75, 0.50, 0.47, 0.45,
# 0.42, 0.40, 0.35, 0.34, 0.31, 0.30, 0.28, 0.27, 0.27, 0.27, 0.27, 0.26, 0.26, 0.25])
# # RS_alt = [i * 1000 for i in RS_alt]

k = 273.15


def calculate_cph(dfmeta):
    '''
    O3S-DQA Section 8.4
    '''

    dfmeta['x'] = ((7.5 * dfmeta['TLab'].astype('float')) / (dfmeta['TLab'].astype('float') + 237.3)) + 0.7858
    dfmeta['psaturated'] = 10 ** (dfmeta['x'])
    # Eq.17
    dfmeta['cPH'] = (1 - dfmeta['ULab'].astype('float')/100) * dfmeta['psaturated']/dfmeta['Pground'].astype('float')
    #madrid
    # dfmeta['cPH'] = (1 - dfmeta['ULab'].astype('float')/100) * dfmeta['psaturated']/dfmeta['PLab'].astype('float')

    # Eq.16
    dfmeta['cPL'] = 2/(dfmeta['TLab'].astype('float') + k)

    return dfmeta


def pf_groundcorrection(df, dfm, phim, dphim, tlab, plab, rhlab, boolrh):
    """
    O3S-DQA 8.4
    :param df:
    :param dfm:  metadata df
    :param phim:
    :param unc_phip:
    :param tlab:
    :param plab:
    :param rhlab:
    :return:
    """
    df['TLab'] = dfm.at[dfm.first_valid_index(),tlab].astype('float')

    if boolrh == True:
        df['ULab'] = dfm.at[dfm.first_valid_index(), rhlab].astype('float')
        df['Pground'] = dfm.at[dfm.first_valid_index(), plab].astype('float')
        df['x'] = ((7.5 * df['TLab']) / (df['TLab'] + 237.3)) + 0.7858
        df['psaturated'] = 10 ** (df['x'])
        df['cPH'] = (1 - df['ULab']/ 100) * df['psaturated'] / df['Pground'] #Eq. 17
        unc_cPH = df.at[df.first_valid_index(), 'unc_cPH']
        df['TLabK'] = df[tlab] + k
        df['cPL'] = 2 / df['TLabK']  # Eq. 16
        unc_cPL = df.at[df.first_valid_index(), 'unc_cPL']
        
    if boolrh == False:

        df['TLabK'] = df[tlab] + k
        df['cPL'] = 2/df['TLabK'] #Eq. 16
        unc_cPL = 0
        df['cPH'] = 0
        unc_cPH = 0

    df['Phip_ground'] = (1 + df['cPL'] - df['cPH']) * df[phim]  # Eq. 15
    df['unc_Phip_ground'] = df['Phip_ground'] * np.sqrt(
        (df[dphim]) ** 2 + (unc_cPL) ** 2 + (unc_cPH) ** 2)  # Eq. 21

    return df['Phip_ground'], df['unc_Phip_ground']

def VecInterpolate_linear(XValues, YValues, unc_YValues, dft, Pair):

    dft = dft.reset_index()

    for k in range(len(dft)):

        for i in range(len(XValues)-1):
            # check that value is in between xvalues
            if (XValues[i] >= dft.at[k, Pair] >= XValues[i + 1]):
                x1 = float(XValues[i])
                x2 = float(XValues[i+1])
                y1 = float(YValues[i])
                y2 = float(YValues[i+1])
                unc_y1 = float(unc_YValues[i])
                unc_y2 = float(unc_YValues[i + 1])
                dft.at[k,'Cpf'] = y1 + (dft.at[k,Pair] - x1) * (y2 - y1) / (x2 - x1)
                dft.at[k,'unc_Cpf'] = unc_y1 + (dft.at[k,Pair] - x1) * (unc_y2 - unc_y1) / (x2 - x1)

    return dft['Cpf'], dft['unc_Cpf']


def VecInterpolate_log(XValues, YValues, unc_YValues, dft, Pair):

    dft = dft.reset_index()


    dft['plog'] = np.log10(dft[Pair])

    for k in range(len(dft)):
        # dft.at[k, 'Cpf'] = 1

        for i in range(len(XValues)-1):
            # check that value is in between xvalues
            if (XValues[i] >= dft.at[k, 'plog'] >= XValues[i + 1]):

                x1 = float(XValues[i])
                x2 = float(XValues[i+1])
                y1 = float(YValues[i])
                y2 = float(YValues[i+1])
                unc_y1 = float(unc_YValues[i])
                unc_y2 = float(unc_YValues[i + 1])
                dft.loc[k,'Cpf'] = y1 + (dft.at[k,'plog'] - x1) * (y2 - y1) / (x2 - x1)
                dft.loc[k,'unc_Cpf'] = unc_y1 + (dft.at[k,'plog'] - x1) * (unc_y2 - unc_y1) / (x2 - x1)



    return dft['Cpf'], dft['unc_Cpf']
    # return dft

def pumpflow_efficiency(df, pair,  pumpcorrectiontag, effmethod ):
    '''
    O3S-DQA 8.5 based on Table 6
    :param df:
    :param pair:
    :param pumpcorrectiontag:
    :param effmethod:
    :return:
    '''

    df['Cpf'] = 1
    df['unc_Cpf'] =1

    if effmethod == 'polyfit':

        if pumpcorrectiontag == 'komhyr_95':
            df['Cpf'] = 2.17322861 - 3.686021555 * np.log10(df[pair]) + 5.105113826 * (
                np.log10(df[pair])) ** 2 - 3.741595297 * (np.log10(df[pair])) ** 3 + 1.496863681 * (
                            np.log10(df[pair])) ** 4 - \
                        0.3086952232 * (np.log10(df[pair])) ** 5 + 0.02569158956 * (np.log10(df[pair])) ** 6
            df['unc_Cpf'] = 0.07403603165 - 0.08532895578 * np.log10(df[pair]) + 0.03463984997 * (
                np.log10(df[pair])) ** 2 - 0.00462582698 * (np.log10(df[pair])) ** 3


    if effmethod == 'table_interpolate':

        if pumpcorrectiontag == 'komhyr_86':
            # df['Cpf'], df['unc_Cpf'] = VecInterpolate_linear(pval, komhyr_86, komhyr_86_unc,  df, pair)
            df['Cpf'], df['unc_Cpf'] = VecInterpolate_log(pvallog, komhyr_86, komhyr_86_unc,  df, pair)
            # df = VecInterpolate_log(pvallog, komhyr_86, komhyr_86_unc,  df, pair)

        if pumpcorrectiontag == 'komhyr_95':
            # df['Cpf'], df['unc_Cpf'] = VecInterpolate_linear(pval, komhyr_95, komhyr_95_unc,  df, pair)
            df['Cpf'], df['unc_Cpf'] = VecInterpolate_log(pvallog, komhyr_95, komhyr_95_unc,  df, pair)

        # if pumpcorrectiontag == 'sodankayl':
        #     df['Cpf'], df['unc_Cpf'] = VecInterpolate(pval_sod, corr_sod, corr_sod_unc,  df, pair, 1)

    # return df
    return df['Cpf'], df['unc_Cpf']

def return_phipcor(df,phip_grd, unc_phip_grd, cpf, unc_cpf):
    #O3S-DQA 8.5

    df['Phip_cor'] = df[phip_grd]/df[cpf] #Eq. 22
    df['unc_Phip_cor'] = df['Phip_cor'] * np.sqrt( df[unc_phip_grd]**2/df[phip_grd]**2 + df[unc_cpf]**2/df[cpf]**2 ) #Eq. 23

    return df['Phip_cor'], df['unc_Phip_cor']

def background_correction(df, dfmeta, dfm, ib,):
    """
    O3S-DQA 8.2
    :param df: data df
    :param dfmeta: all metadata df
    :param dfm: corresponding metadata of df
    :param ib2:
    :return: df[ib]
    """

    df['iBc'] = 0
    df['unc_iBc'] = 0

    # #generaly for all stations
    # mean = np.mean(dfmeta[dfmeta[ib] < 0.1][ib])
    # std = np.std(dfmeta[dfmeta[ib] < 0.1][ib])
    #
    # if (dfm.at[dfm.first_valid_index(),ib] > mean + 2 * std):
    #     df['iBc'] = mean
    #     df['unc_iBc'] = 2 * std
    # if (dfm.at[dfm.first_valid_index(),ib] <= mean + 2 * std):
    #     df['iBc'] = dfm.at[dfm.first_valid_index(),ib]
    #     df['unc_iBc'] = std

    #special section for stations that have different bkg means in different periods
    # due to th efact that older ECC's had a larger bkg, also confirmed by JOSIE campaigns
    dfm['Date'] = dfm['Date'].astype(str)
    dfmeta['Date'] = dfmeta['Date'].astype(str)
    df['Date'] = df['Date'].astype(str)

    year = '2004' #uccle
    # year = '2005' #sodankyla
    # year = '1998' #lauder
    mean1 = np.nanmean(dfmeta[dfmeta.Date < year][ib])
    std1 = np.nanstd(dfmeta[dfmeta.Date < year][ib])
    mean2 = np.nanmean(dfmeta[dfmeta.Date >= year][ib])
    std2 = np.nanstd(dfmeta[dfmeta.Date >= year][ib])

    print('values', mean1, std1, mean2, std2)


    if (dfm.at[dfm.first_valid_index(), ib] > mean1 + 2 * std1) & (dfm.at[dfm.first_valid_index(), 'Date'] < year):
        df.loc[df.Date < year, 'iBc'] = mean1
        df.loc[df.Date < year, 'unc_iBc'] = 2 * std1

        # print('bkg correction before 2004 ', mean1)
        # df['iBc'] = mean1
        # df['unc_iBc'] = 2 * std1
    if (dfm.at[dfm.first_valid_index(), ib] <= mean1 + 2 * std1) & (dfm.at[dfm.first_valid_index(), 'Date'] < year):
        df.loc[df.Date < year, 'iBc'] = dfm.at[dfm.first_valid_index(), ib]
        df.loc[df.Date < year, 'unc_iBc'] = std1
        # print('before 2004', dfm.at[dfm.first_valid_index(), ib])

        # df['iBc'] = dfm.at[dfm.first_valid_index(), ib]
        # df['unc_iBc'] = std1

    if (dfm.at[dfm.first_valid_index(), ib] > mean2 + 2 * std2) & (dfm.at[dfm.first_valid_index(), 'Date'] >= year):
        df.loc[df.Date >= year, 'iBc'] = mean2
        df.loc[df.Date >= year, 'unc_iBc'] = 2 * std2
        # print('after 2004 bkg correction', mean1)


    if (dfm.at[dfm.first_valid_index(), ib] <= mean2 + 2 * std2) & (dfm.at[dfm.first_valid_index(), 'Date'] >= year):
        df.loc[df.Date >= year, 'iBc'] = dfm.at[dfm.first_valid_index(), ib]
        df.loc[df.Date >= year, 'unc_iBc'] = std2
        # print('after 2004', dfm.at[dfm.first_valid_index(), ib])


    if (df.at[df.first_valid_index(), 'iBc'] == 0) & (df.at[df.first_valid_index(),'Date'] < year):
        df.loc[df.Date < year, 'iBc'] = mean1
        df.loc[df.Date < year, 'unc_iBc'] = 2 * std1
        # print('before 2004 no bkg', mean1)
    if (df.at[df.first_valid_index(), 'iBc'] == 0) & (df.at[df.first_valid_index(),'Date'] >= year):
        df.loc[df.Date >= year, 'iBc'] = mean2
        df.loc[df.Date >= year, 'unc_iBc'] = 2 * std2
        # print('after 2004 no bkg', mean2)


    # print('end of function', df.at[df.first_valid_index(), 'iBc'])
    return df['iBc'], df['unc_iBc']


def po3tocurrent(df, po3, tpump, ib, etac, phip, boolcorrection, out):
    '''
    :param df: dataframe
    :param po3: partial ozone pressure of the sonde
    :param tpump: pump temperature
    :param ib: background current, question: which one?
    :param etac: conversion efficiency
    :param phip: gas volume flow rate in cm3^3/s
    :param boolcorrection: a boolean for if any other correction is applied
    :return: Current obtained from PO3
    '''

    if (boolcorrection == False):
        df.loc[(df[po3] == 0), out] = 0
        df[out] = (df[po3] * df[etac] * df[phip]) / (df[tpump] * 0.043085) + df[ib]

    return df[out]


def currenttopo3(df, im, tpump, ib, etac, phip, boolcorrection):
    '''
    :param df: dataframe
    :param po3: partial ozone pressure of the sonde
    :param pair:pressure of the air
    :param tpump: pump temperature
    :param ib: background current, question: which one?
    :param etac: conversion efficiency
    :param phip: gas volume flow rate in cm3^3/s
    :param boolcorrection: a boolean for if any other correction is applied
    :return: Current obtained from PO3
    '''

    if (boolcorrection == False):
        df.loc[(df[im] == 0), 'O3c'] = 0
        df['O3c'] = 0.043085 * df[tpump] * (df[im] - df[ib]) / (df[etac] * df[phip])

    return df['O3c']


def pumptemp_corr(df, boxlocation, temp, unc_temp, pair):
    '''
    O3S-DQA 8.3
    :param df: dataframe
    :param boxlocation: location of the temperature measurement
    :param temp: temp. of the pump that was measured at boxlocation
    :param pressure: pressure of the air
    :return: the corrected base temperature of the pump
    '''
    df['Tpump_cor'] = 0
    df['unc_Tpump_cor'] = 0

    if (boxlocation == 'Box') | (boxlocation == 'case1'):  # case I in O3S-DQA guide
        df.loc[(df[pair] >= 40), 'deltat'] = 7.43 - 0.393 * np.log10(df.loc[(df[pair] >= 40), pair])
        df.loc[(df[pair] < 40) & (df[pair] > 6), 'deltat'] = 2.7 + 2.6 * np.log10(
            df.loc[(df[pair] < 40) & (df[pair] > 6), pair])
        df.loc[(df[pair] <= 6), 'deltat'] = 4.5
        df['unc_deltat'] = 1  # units in K

    if (boxlocation == 'ExternalPumpTaped') | (boxlocation == 'case2') | (boxlocation == 'case3'):  # case III in O3S-DQA guide
        df.loc[(df[pair] > 70), 'deltat'] = 20.6 - 6.7 * np.log10(df.loc[(df[pair] > 70), pair])
        df.loc[(df[pair] > 70), 'unc_deltat'] = 3.9 - 1.13 * np.log10(df.loc[(df[pair] > 70), pair])
        df.loc[(df[pair] <= 70) & (df[pair] >= 15), 'deltat'] = 8.25
        # updated formula, 17/06/2021 not 3.25 - 4.25 ... but 3.25 + 4.25
        df.loc[(df[pair] < 15) & (df[pair] >= 5), 'deltat'] = 3.25 + 4.25 * np.log10(
            df.loc[(df[pair] < 15) & (df[pair] >= 5), pair])
        df.loc[(df[pair] <= 70), 'unc_deltat'] = 0.3 + 1.13 * np.log10(df.loc[(df[pair] <= 70), pair])

    if (boxlocation == 'ExternalPumpGlued') | (boxlocation == 'case4'):  # case IV in O3S-DQA guide
        df.loc[(df[pair] > 40), 'deltat'] = 6.4 - 2.14 * np.log10(df.loc[(df[pair] > 40), pair])
        df.loc[(df[pair] <= 40) & (df[pair] >= 3), 'deltat'] = 3.0
        df['unc_deltat'] = 0.5  # units in K

    filt = df[pair] > 3

    if (boxlocation == 'InternalPump') | (boxlocation == 'case5'):  # case V in O3S-DQA guide
        df.loc[filt,'deltat'] = 0  # units in K
        df.loc[filt,'unc_deltat'] = 0  # units in K

    df.loc[(df[pair] > 3), 'deltat_ppi'] = 3.9 - 0.8 * np.log10(df.loc[(df[pair] > 3), pair]) #Eq. 12
    df.loc[(df[pair] > 3), 'unc_deltat_ppi'] = 0.5

    df.loc[filt, 'Tpump_cor'] = df.loc[filt, temp] + df.loc[filt, 'deltat'] + df.loc[filt, 'deltat_ppi'] #Eq. 13
    df.loc[filt, 'unc_Tpump_cor'] = (df.loc[filt, unc_temp] ** 2 / df.loc[filt, temp] ** 2) + \
                            (df.loc[filt, 'unc_deltat'] ** 2 / df.loc[filt, temp] ** 2)+ (df.loc[filt, 'unc_deltat_ppi'] ** 2 / df.loc[filt, temp] ** 2) #Eq. 14

    # df = df.drop(['deltat', 'unc_deltat', 'deltat_ppi', 'unc_deltat_ppi'], axis=1)

    return df.loc[filt,'Tpump_cor'], df.loc[filt,'unc_Tpump_cor']


def absorption_efficiency (df, pair, solvolume):
    '''
    O3S-DQA 8.1.1
    :param df: dataframe
    :param pair: air pressure column
    :param solvolume: volume of the cathode solution in mls
    :return: absorption efficeincy and its uncertainity
    '''
    df['unc_alpha_o3'] = 0.01
    df['alpha_o3'] = 1
    # Eq. 6A-6B
    if solvolume == 2.5:
        df.loc[(df[pair] > 100) & (df[pair] < 1050), 'alpha_o3'] = 1.0044 - 4.4 * 10 ** -5 * df.loc[(df[pair] > 100) & (df[pair] < 1050), pair]
        df.loc[(df[pair] <= 100), 'alpha_o3'] = 1.0
    # Eq. 6C
    if solvolume == 3.0:
        df.loc[(df[pair] <= 1050), 'alpha_o3'] = 1.0

    return df['alpha_o3'], df['unc_alpha_o3']


def stoichmetry_conversion(df, pair, sensortype, solutionconcentration, reference):
    '''
    O3S-DQA 8.1.2
    :param pair: Pressure of the air
    :param sondesstone: an array of the Sonde type and SST i.e: ['SPC', '0.5'] that was in use
    :param sondessttwo: an array of the Sonde type and SST to be changed to i.e: ['SP', '1.0']
    :return: r and uncertainity on r which are transfer functions and taken from Table 3 from the guideline
    '''

    # print('in the function', sensortype)

    df['stoich'] = 1
    df['unc_stoich'] = 0.05
    solutionconcentration = float(solutionconcentration)

    if (reference == 'ENSCI05') & (sensortype == 'DMT-Z') & (solutionconcentration == 10):
        df.loc[df[pair] >= 30, 'stoich'] = 0.96 #Eq 7A
        df.loc[df[pair] < 30, 'stoich'] = 0.90 + 0.041 * np.log10(df[df[pair] < 30][pair]) #Eq 7B

    if (reference == 'ENSCI05') & (sensortype == 'DMT-Z') & (solutionconcentration == 5.0):
        df['stoich'] = 1
        df['unc_stoich'] = 0.03

    if (reference == 'ENSCI05') & (sensortype == 'SPC') & (solutionconcentration == 10):
        df['stoich'] = 1
        df['unc_stoich'] = 0.03

    if (reference == 'SPC10') & (sensortype == 'SPC') & (solutionconcentration == 10):
        df['stoich'] = 1
        df['unc_stoich'] = 0.03

    if (reference == 'SPC10') & (sensortype == 'DMT-Z') & (solutionconcentration == 10):
        df.loc[df[pair] >= 30, 'stoich'] = 0.96 #Eq 7C
        df.loc[df[pair] < 30, 'stoich'] = 0.764 + 0.133 * np.log10(df[df[pair] < 30]) #Eq 7D

    if (reference == 'SPC10') & (sensortype == 'SPC') & (solutionconcentration == 5):
        df.loc[df[pair] >= 30, 'stoich'] = 1/0.96 #inverse of Eq. 7A
        df.loc[df[pair] < 30, 'stoich'] = 1/(0.90 + 0.041 * np.log10(df[df[pair] < 30][pair])) #inverse of Eq. 7B

    return df['stoich'], df['unc_stoich']


def conversion_efficiency(df, alpha_o3, alpha_unc_o3, stoich, stoich_unc):
    '''
    O3S-DQA 8.1
    :param alpha: absorption efficiency obtained by conversion_absorption
    :param alpha_unc: absorption efficiency unc. obtained by conversion_alpha
    :param rstoich: transfer functions obtained by conversion_stoichemtry
    :param rstoich_err: transfer functions unc. obtained by conversion_stoichemtry
    :return: total efficiency of the conversion etac_c and its uncertainity Eq. 4 from the guideline
    here Eq.4 in the guideline the stoichmetry factor should be multiplied with the partial pressure, thats why
    it is in the denominator in eta_C equation
    '''

    df['eta_c'] = df[alpha_o3] / df[stoich]
    df['unc_eta'] = df['eta_c'] * np.sqrt((df[alpha_unc_o3] / df[alpha_o3]) ** 2 + (df[stoich_unc] / df[stoich]) ** 2)

    return df['eta_c'], df['unc_eta']



def o3_integrate(df, po3):

    int =  (3.9449 * (df[po3].shift() + df[po3]) * np.log(df.Pair.shift() / df.Pair)).sum()

    return int



def RS_pressurecorrection(dft, height, radiosondetype):
    '''
    correction of "Propagation of radiosonde pressure sensor errors to ozonesonde measurements" https://doi.org/10.5194/amt-7-65-2014
    :param dft:
    :param height:
    :param radiosondetype:
    :return: correction factors and their uncertainties
    '''

    dft = dft.reset_index()

    dft['height_km'] = dft[height]/1000

    dft['Crs'] = 0.0
    dft['unc_Crs'] = 0.0

    RS_cor = RS80_cor
    RS_cor_err = RS80_cor_err

    for k in range(len(dft)):

        for i in range(len(RS_alt) - 1):
            # just check that value is in between xvalues
            if (RS_alt[i] <= dft.at[k, 'height_km'] < RS_alt[i + 1]):
                # x1 = float(RS_alt[i])
                # x2 = float(RS_alt[i + 1])
                # y1 = float(RS_cor[i])
                # y2 = float(RS_cor[i + 1])
                # unc_y1 = float(RS_cor_err[i])
                # unc_y2 = float(RS_cor_err[i + 1])
                # dft.at[k, 'Crs'] = float(y1 + (dft.at[k, 'height_km'] - x1) * (y2 - y1) / (x2 - x1))
                # dft.at[k, 'unc_Crs'] = float(unc_y1 + (dft.at[k, 'height_km'] - x1) * (unc_y2 - unc_y1) / (x2 - x1))
                dft.at[k, 'Crs'] = RS_cor[i+1]
                dft.at[k, 'unc_Crs'] = RS_cor_err[i+1]

        if (dft.at[k, 'height_km'] > 30):
            dft.at[k, 'Crs'] = -1.02
            dft.at[k, 'unc_Crs'] = -1.43

        # print('rs80',k, dft.at[k, 'height_km'], dft.at[k, 'Crs'])

    return dft['Crs'], dft['unc_Crs']



## below functions copied from read_nilu_functions.py to convert PO3 to current, to calculate current from partial pressure


def o3tocurrent(dft, dfm):
    '''

    :param dft: data df
    :param dfm: metadata df
    :return: dft
    '''
    # o3(mPa) = 4.3087 * 10e-4 * (i - ibg) * tp * t * cef * cref
    # tp: pump temp. in K, t: pumping time for 100 ml of air in seconds, cef: correction due to reduced ambient pressure for pump
    # cref: additional correction factor
    # i = o3 / (4.3087 * 10e-4 * tp * t * cef * cref ) + ibg

    dft['SensorType'] = 'SPC'
    dfm['SensorType'] = 'SPC'

    dft['SolutionVolume'] = 3
    dfm['SolutionVolume'] = 3

    dft['Cef'] = ComputeCef(dft)

    cref = 1
    dft['ibg'] = 0
    dft['iB2'] = dfm.at[dfm.first_valid_index(), 'iB2']

    # check PF values
    if (dfm.at[dfm.first_valid_index(), 'PF'] > 40) | (dfm.at[dfm.first_valid_index(), 'PF'] < 20): dfm.at[dfm.first_valid_index(), 'PF'] = 28

    # # by default uses iB2 as background current
    # dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB2']
    # if it was mentioned that BkgUsed is Ibg1, then iB0 is used
    # if (dfm.at[dfm.first_valid_index(), 'BkgUsed'] == 'Ibg1') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z'):
    #     dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB0']
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': dft['ibg'] = ComputeIBG(dft, 'iB2')
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB2']

    dft['I'] = dft['O3'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dfm.at[dfm.first_valid_index(), 'PF'] * dft['Cef'] * cref) + dft['ibg']


    return dft


def ComputeCef(dft):
    """ Computes pump efficiency correction factor based on pressure

        Arguments:
        Pressure -- air pressure [hPa]
    """

    # dft['SensorType'] = 'DMT-Z'
    # dft['SolutionVolume'] = 3.0
    #
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'SPC') and (
            dft.at[dft.first_valid_index(), 'SolutionVolume'] > 2.75):
        dft['Cef'] = VecInterpolate(VecP_ECC6A, VecC_ECC6A_30, dft, 0)
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'SPC') and (
            dft.at[dft.first_valid_index(), 'SolutionVolume'] < 2.75):
        dft['Cef'] = VecInterpolate(VecP_ECC6A, VecC_ECC6A_25, dft, 0)
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'DMT-Z'):
        dft['Cef'] = VecInterpolate(VecP_ECCZ, VecC_ECCZ, dft, 0)

    return dft['Cef']


def VecInterpolate(XValues, YValues, dft, LOG):
    dft['Cef'] = 0.0

    i = 1
    ilast = len(XValues) - 1
    # return last value if xval out of xvalues range
    y = float(YValues[ilast])

    dft = dft.reset_index()

    for k in range(len(dft)):
        for i in range(len(XValues) - 1):
            # just check that value is in between xvalues
            if (XValues[i] <= dft.at[k, 'Pair'] <= XValues[i + 1]):

                x1 = float(XValues[i])
                x2 = float(XValues[i + 1])
                if LOG == 1:
                    x = math.log(x)
                    x1 = math.log(x1)
                    x2 = math.log(x2)
                y1 = float(YValues[i])
                y2 = float(YValues[i + 1])

                dft.at[k, 'Cef'] = y1 + (dft.at[k, 'Pair'] - x1) * (y2 - y1) / (x2 - x1)

    return dft['Cef']
