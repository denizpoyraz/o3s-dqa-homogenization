import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime
import time

from functions.homogenization_functions import absorption_efficiency, stoichmetry_conversion, conversion_efficiency, \
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency, \
    return_phipcor, RS_pressurecorrection

from functions.df_filter import filter_data, filter_metadata


path = '/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/version2/'

## important adjusments
# if there was a change in the used background current or the location of the pump thermistor, please do the following

string_bkg_used = 'ib2'
# string_bkg_used = 'ib0'
string_pump_location = 'InternalPump'


k = 273.15

dfmeta = pd.read_hdf(path + 'All_metadata.hdf')
dfmeta = filter_metadata(dfmeta)

# part to calculate cph and its error
dfmeta = calculate_cph(dfmeta)
dfmeta['unc_cPH'] = dfmeta['cPH'].std()
dfmeta['unc_cPL'] = dfmeta['cPL'].std()
# print('cPH std', dfmeta['cPH'].std(), 'cpl std', dfmeta['cpl'].std())

allFiles = sorted(glob.glob(path + "Current/SO0504*rawcurrent.hdf"))
# mdFiles = sorted(glob.glob(path + "Metadata/*metadata.csv"))

size = len(allFiles)
datelist = [0] * size
j = 0

bool_rscorrection = True

for (filename) in (allFiles):
    print(filename)
    file = open(filename, 'r')

    date_tmp = filename.split('/')[-1].split('.')[0][2:8]
    fname = filename.split('/')[-1].split('.')[0][0:8]
    fullname = filename.split('/')[-1].split('.')[0]
    metaname = path + 'Metadata/' + fname + "_metadata.csv"
    if search("2nd", fullname): metaname = path + 'Metadata/' + fname + "_2nd_metadata.csv"

    date = datetime.strptime(date_tmp, '%y%m%d')
    datef = date.strftime('%Y%m%d')
    datestr = str(datef)

    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    # to deal with data that is not complete
    if (len(df) < 300): continue

    df['Date'] = datef
    df['Datedt'] = pd.to_datetime(df['Date'], format='%Y%m%d').dt.date

    #     IMPORTANT
    # if there was a change in the used background current or the location of the pump thermistor
    # (assuming you know the date when the change occurred), please do the following example
    # if datef > date_change: string_bkg_used = 'ib2'
    # if datef < date_change: string_bkg_used = 'ib0'
    # the string options for pump temperature can be seen in homogenisation_functions -> pumptemp_corr
    # see boxlocation strings

    # input variables for hom.
    df['Tpump'] = df['TboxK']
    df['Phip'] = 100 / dfm.at[dfm.first_valid_index(),'PF']
    df['Eta'] = 1

    df['dPhip'] = 0.02
    df['unc_Tpump'] = 1
    df['unc_cPH'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cPH']
    df['unc_cPL'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cPL']

    #      radiosonde RS80 correction   #
    try: rsmodel = dfm.at[dfm.first_valid_index(), 'RadiosondeModel']
    except KeyError: rsmodel = 'RS92'
    # print('rsmodel', rsmodel)
    if rsmodel == 'RS80': bool_rscorrection = True
    else: bool_rscorrection = False
    if bool_rscorrection:
        df['Crs'], df['unc_Crs'] = RS_pressurecorrection(df, 'Height', rsmodel)
        df['Pair'] = df['Pair'] - df['Crs']

    #      conversion efficiency        #
    df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair', dfm.at[dfm.first_valid_index(),'SolutionVolume'])
    df['stoich'], df['unc_stoich'] = stoichmetry_conversion(df, 'Pair', dfm.at[dfm.first_valid_index(), 'SensorType'],
                                                            dfm.at[dfm.first_valid_index(), 'SolutionConcentration'], 'ENSCI05')
    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    if string_bkg_used == 'ib2': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2')
    if string_bkg_used == 'ib0': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB0')

    #       pump temperature correction       #
    df['Tpump_cor'], df['unc_Tpump_cor'] = pumptemp_corr(df, string_pump_location, 'Tpump', 'unc_Tpump', 'Pair')

    #      pump flow corrections        #
    # ground correction
    df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'Pground', 'ULab',True)
    # efficiency correction
    pumpflowtable = ''
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': pumpflowtable = 'komhyr_86'
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': pumpflowtable = 'komhyr_95'
    df['Cpf'], df['unc_Cpf'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'table_interpolate')
    df['Phip_cor'], df['unc_Phip_cor'] = return_phipcor(df, 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf')

    # all corrections
    df['O3c'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor', False)

    # uncertainities
    df['dI'] = 0
    df.loc[df.I < 1, 'dI'] = 0.01
    df.loc[df.I >= 1, 'dI'] = 0.01 * df.loc[df.I > 1, 'I']
    df['dIall'] = (df['dI'] ** 2 + df['unc_iBc']**2) / (df['I'] - df['iBc'])**2
    df['dEta'] = (df['unc_eta_c'] / df['eta_c'])**2
    df['dPhi_cor'] = (df['unc_Phip_cor'] / df['Phip_cor'])**2
    df['dTpump_cor'] = (df['unc_Tpump_cor'] / df['Tpump_cor'])**2
    if bool_rscorrection: df['dPrs'] = (df['unc_Crs']/df['Crs'])**2
    # final uncertainity on O3
    df['dO3'] = np.sqrt(df['dIall'] + df['dEta'] + df['dPhi_cor'] + df['dTpump_cor'])

    md_clist = ['Phip', 'Eta', 'unc_Phip', 'unc_Tpump', 'unc_cPH', 'unc_cPL', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich',
              'eta_c', 'unc_eta', 'unc_eta_c', 'iBc', 'unc_iBc',  'unc_Tpump_cor', 'deltat', 'unc_deltat',  'unc_deltat_ppi',
              'x', 'psaturated', 'cPH', 'TLabK', 'cPL', 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf',
              'dEta', 'dTpump_cor']

    # merge all the metadata to md df and save it as a csv file
    for j in range(len(md_clist)):
        dfm[md_clist[j]] = df.at[df.first_valid_index(), md_clist[j]]

    dfm.to_csv(path + '/DQA/'+ datestr + "_o3smetadata.csv")

    df = df.drop(
        ['Datedt', 'Phip', 'Eta', 'unc_Phip', 'unc_Tpump', 'unc_cPH', 'TboxK',
     'unc_cPL', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta', 'unc_eta_c',
     'iBc', 'unc_iBc', 'unc_Tpump_cor', 'deltat', 'unc_deltat', 'deltat_ppi', 'unc_deltat_ppi', 'TLab',
     'ULab', 'Pground', 'x', 'psaturated', 'cPH', 'TLabK', 'cPL', 'Phip_ground', 'unc_Phip_ground',
     'dI'], axis=1)

    # data file that has data and uncertainties that depend on Pair or Height or Temperature
    df.to_hdf(path + '/DQA/' + datestr + "_all_hom.hdf", key = 'df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']
    df = df.drop(['TboxC', 'Tpump', 'Tpump_cor', 'Cpf', 'unc_Cpf', 'Phip_cor', 'unc_Phip_cor', 'O3c', 'dPhi_cor'], axis = 1)
    # df to be converted to WOUDC format together with the metadata
    df.to_hdf(path + '/DQA/' + datestr + "_o3sdqa.hdf", key = 'df')

