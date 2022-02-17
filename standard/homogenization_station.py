import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime
import time
import math
from scipy.interpolate import interp1d

from functions.homogenization_functions import absorption_efficiency, stoichmetry_conversion, conversion_efficiency, \
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency, \
    return_phipcor, o3_integrate, roc_values, RS_pressurecorrection

from functions.functions_perstation import organize_sodankyla


# homogenization code to be used by all stations
### all corrections recommended by the DQA:
## Conversion Efficiency:
#  absorption and stoichiometry->
#  variables:solution volume,
#  sonde type and solution concentration
## Background Current:
#  df of all metadata is needed to calculate the mean and std of bkg.
#  most of the time 2 different periods are needed
#  which has a parameter IBGsplit the year in which
#  bkg values has changed from high to low
#  which bkg is used important, mostly iB2
#  but this can be station specific
## Pump Temp. Measurement (location):
#  pump location. if a change in the type of the sonde was made
#  this would effect this variable
## Pump Flow Rate (moistening effect)
#
## Pump flow efficiency at low pressures
# TON not to be applied but to be kept in the database
# Radiosonde correction (not to be applied)

k = 273.15

#           parts to be changed by hand!!!!         #

path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
dfmeta = pd.read_hdf(path + 'Metadata/All_metadata.hdf')
allFiles = sorted(glob.glob(path + "Current/*961211*rawcurrent.hdf"))
roc_table_file = ('/home/poyraden/Analysis/Homogenization_public/Files/sonde_sodankyla_roc.txt')
roc_plevel = 10 # pressure value to obtain roc

# the date when the homogenization starts, there is a continue statement
# in the main loop for the dates before this date, "may not be needed always"
date_start_hom = '19941012'
# the date where there was a change from rs80
date_rs80 = '20051124'

# the date if there is a lower/higher bkg value region
IBGsplit = '2005'

humidity_correction = True
bool_rscorrection = False

if humidity_correction:
    dfmeta = calculate_cph(dfmeta)
    dfmeta['unc_cPH'] = dfmeta['cPH'].std()
    dfmeta['unc_cPL'] = dfmeta['cPL'].std()

dfmeta = organize_sodankyla(dfmeta)

#           end of the parts to be changed by hand!!!!          #

#check if dfmeta has "Date" variable, otherwise create it
clms = [i for i in range(1,13)]
table = pd.read_csv(roc_table_file,  skiprows=1, sep="\s *", names = clms,  header=None)
dfmeta = roc_values(dfmeta,table, roc_plevel)
PFmean = np.nanmean(dfmeta[(dfmeta.PF > 0) & (dfmeta.PF < 99)].PF)



#read over all files to do the homogenization

for (filename) in (allFiles):
    file = open(filename, 'r')

    date_tmp = filename.split('/')[-1].split('.')[0][2:8]
    fname = filename.split('/')[-1].split('.')[0][0:8]
    fullname = filename.split('/')[-1].split('.')[0]

    date = datetime.strptime(date_tmp, '%y%m%d')
    datestr = date.strftime('%Y%m%d')

    print(filename)

    df = pd.read_hdf(filename)
    dfm = dfmeta[dfmeta.Date == datestr]
    dfm = dfm.reset_index()
    if len(dfm) == 1:
        dfm = dfmeta[dfmeta.Date == datestr][0:1]
    if (len(dfm) == 2) and search("2nd", fullname):
        dfm = dfmeta[dfmeta.Date == datestr][1:2]
    dfm = dfm.reset_index()

    if datestr < date_start_hom: continue # no bkg values
    if (len(df) < 200): continue

    # input variables for hom.
    df['Tpump'] = df['TboxK']
    df['Phip'] = 100 / dfm.at[dfm.first_valid_index(), 'PF']
    df['Eta'] = 1

    df['dPhip'] = 0.02
    df['unc_cPH'] = dfm.at[dfm.first_valid_index(), 'unc_cPH']
    df['unc_cPL'] = dfm.at[dfm.first_valid_index(), 'unc_cPL']

    df['unc_Tpump'] = 0.5  # case II-V

    # #      radiosonde RS80 correction   #
    # # Electronic o3 sonde interface  was replaced with the transfer from RS80 to RS92  in 24 Nov 2005.
    # rsmodel = ''
    # bool_rscorrection = ''
    # if datestr <= date_rs80:
    #     bool_rscorrection = True
    # if datestr > date_rs80:
    #     bool_rscorrection = False
    # #
    #
    # if bool_rscorrection:
    #     df['Crs'], df['unc_Crs'] = RS_pressurecorrection(df, 'Height', rsmodel)
    #     df['Pair'] = df['Pair'] - df['Crs']

    # DQA corrections
    #      conversion efficiency        #
    df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair', dfm.at[0,'SolutionVolume'])
    df['stoich'], df['unc_stoich'] = stoichmetry_conversion(df, 'Pair', dfm.at[0, 'SensorType'],
                                                            dfm.at[0, 'SolutionConcentration'], 'ENSCI05')
    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    if dfm.at[0, 'string_bkg_used'] == 'ib2': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2', IBGsplit)
    if dfm.at[0, 'string_bkg_used']  == 'ib0': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB0', IBGsplit)

    #       pump temperature correction       #
    df['Tpump_cor'], df['unc_Tpump_cor'] = pumptemp_corr(df, dfm.loc[0,'string_pump_location'], 'Tpump', 'unc_Tpump', 'Pair')

    #      pump flow corrections        #
    # ground correction, humidity correction PTU
    if humidity_correction:
        df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'PLab', 'ULab', True)
    if not humidity_correction:
        df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'PLab', 'ULab', False)
    # efficiency correction
    pumpflowtable = '999 '
    if dfm.at[0, 'SensorType'] == 'SPC': pumpflowtable = 'komhyr_86'
    if dfm.at[0, 'SensorType'] == 'DMT-Z': pumpflowtable = 'komhyr_95'
    df['Cpf'], df['unc_Cpf'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'table_interpolate')
    df['Phip_cor'], df['unc_Phip_cor'] = return_phipcor(df, 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf')

    # all corrections
    df['O3_nc'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'Eta', 'Phip', False)
    df['O3c_eta'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'eta_c', 'Phip', False)
    df['O3c_etabkg'] = currenttopo3(df, 'I', 'Tpump', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpump'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpumpphigr'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_ground', False)
    df['O3c_etabkgtpumpphigref'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor', False)
    df['O3c'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor', False)

    # uncertainities
    df['dI'] = 0
    df.loc[df.I < 1, 'dI'] = 0.01
    df.loc[df.I >= 1, 'dI'] = 0.01 * df.loc[df.I > 1, 'I']
    df['dIall'] = (df['dI'] ** 2 + df['unc_iBc'] ** 2) / (df['I'] - df['iBc']) ** 2
    df['dEta'] = (df['unc_eta_c'] / df['eta_c']) ** 2
    df['dPhi_cor'] = (df['unc_Phip_cor'] / df['Phip_cor']) ** 2
    df['dTpump_cor'] = df['unc_Tpump_cor']
    # final uncertainity on O3
    df['dO3'] = np.sqrt(df['dIall'] + df['dEta'] + df['dPhi_cor'] + df['dTpump_cor'])

    # # check all the variables if they are in accepted value range
    # if (len(df[df['O3c'] < 0]) > 0) | (len(df[df['O3c'] > 30]) > 0):
    #     print('     BREAK       1', filename)
    # if (len(df[df['I'] < 0]) > 0) | (len(df[df['I'] > 10]) > 0):
    #     print('     BREAK       2', filename)
    # if (len(df[df['Tpump_cor'] < 0]) > 0) | (len(df[df['Tpump_cor'] > 325]) > 0):
    #     print('     BREAK       3', filename)
    # if (len(df[df['iBc'] > 0.5]) > 0):
    #     print('     BREAK       4', filename)

    # TON calculations
    dfm['O3Sonde_burst'] = o3_integrate(df, 'O3')
    dfm['O3Sonde_burst_raw'] = o3_integrate(df, 'O3_nc')
    dfm['O3Sonde_burst_hom'] = o3_integrate(df, 'O3c')

    if df.Pair.min() <= 10:
        # print('and now how to calculate TON', df.Pair.min())
        dft = df[df.Pair >= 10]

        # for woudc O3 values
        dfm['O3Sonde'] = o3_integrate(dft, 'O3')
        dfm['O3SondeTotal'] = dfm['O3Sonde'] + dfm['ROC']
        # the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = o3_integrate(dft, 'O3c')
        dfm['O3SondeTotal_hom'] = dfm['O3Sonde_hom'] + dfm['ROC']

        # the same for raw no corrected o3 values
        dfm['O3Sonde_raw'] = o3_integrate(dft, 'O3_nc')
        dfm['O3SondeTotal_raw'] = dfm['O3Sonde_raw'] + dfm['ROC']
        try:
            dfm['O3ratio'] = dfm['TotalO3_Col2A'] / dfm['O3SondeTotal']
            dfm['O3ratio_hom'] = dfm['TotalO3_Col2A'] / dfm['O3SondeTotal_hom']
            dfm['O3ratio_raw'] = dfm['TotalO3_Col2A'] / dfm['O3SondeTotal_raw']
            if dfm.at[0, 'TotalO3_Col2A'] > 999:
                dfm['O3ratio'] = 9999
                dfm['O3ratio_hom'] = 9999
                dfm['O3ratio_raw'] = 9999
        except KeyError:
            dfm['O3ratio'] = 9999
            dfm['O3ratio_hom'] = 9999
            dfm['O3ratio_raw'] = 9999

        dfm['O3Sonde_10hpa'] = o3_integrate(dft, 'O3')
        dfm['O3Sonde_10hpa_raw'] = o3_integrate(dft, 'O3_nc')
        dfm['O3Sonde_10hpa_hom'] = o3_integrate(dft, 'O3c')

    if df.Pair.min() > 10:
        dfm['O3Sonde'] = 9999
        dfm['O3SondeTotal'] = 9999
        dfm['O3ratio'] = 9999
        # the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = 9999
        dfm['O3SondeTotal_hom'] = 9999
        dfm['O3ratio_hom'] = 9999
        dfm['O3Sonde_raw'] = 9999
        dfm['O3SondeTotal_raw'] = 9999
        dfm['O3ratio_raw'] = 9999


    #
    md_clist = ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
                'unc_eta_c', 'iB2', 'iBc', 'unc_iBc', 'TLab', 'deltat', 'unc_deltat', 'unc_deltat_ppi', 'dEta']

    # merge all the metadata to md df and save it as a csv file
    for j in range(len(md_clist)):
        dfm[md_clist[j]] = df.at[df.first_valid_index(), md_clist[j]]

    dfm.to_csv(path + '/DQA_nors80/' + datestr + "_o3smetadata_nors80.csv")

    df = df.drop(
        ['Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'unc_eta',
         'unc_eta_c', 'dEta'], axis=1)

    # df = df.drop(
    #     ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
    #      'unc_eta_c', 'iB2', 'iBc', 'unc_iBc', 'dEta'], axis=1)

    # data file that has data and uncertainties that depend on Pair or Height or Temperature
    df.to_hdf(path + '/DQA_nors80/' + datestr + "_all_hom_nors80.hdf", key='df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']
    df = df.drop(['TboxC', 'Tpump', 'Tpump_cor', 'Cpf', 'unc_Cpf', 'Phip_cor', 'unc_Phip_cor', 'O3c', 'dPhi_cor'],
                 axis=1)
    # df to be converted to WOUDC format together with the metadata
    df.to_hdf(path + '/DQA_nors80/' + datestr + "_o3sdqa_nors80.hdf", key='df')



