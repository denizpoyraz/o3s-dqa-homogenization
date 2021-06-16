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


path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'

dfmeta = pd.read_hdf(path + 'Metadata/All_metadata.hdf')
# dfmeta = filter_metadata(dfmeta)

## use climatological means for missing PLab, TLab, ULab values
series = dfmeta[['Date', 'Pground', 'TLab','ULab','PF']]
series['Date'] = series['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
series = series.set_index('Date')
upsampled = series.resample('1M').mean()

series04 = dfmeta[dfmeta.Date < '20040101'][['Date', 'Pground', 'TLab','ULab','PF']]
series04['Date']  = series04['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
series04 = series04.set_index('Date')
upsampled04 = series04.resample('1M').mean()

plab = [0] * 12
tlab = [0] * 12
ulab = [0] * 12
pf = [0] * 12

for i in range(1,13):
    j = i-1
    plab[j] = upsampled[upsampled.index.month == i].mean()[0]
    tlab[j] = upsampled[upsampled.index.month == i].mean()[1]
    ulab[j] = upsampled[upsampled.index.month == i].mean()[2]
    pf[j] = upsampled04[upsampled04.index.month == i].mean()[3]

print(pf)
# print(tlab)

## important adjusments
# if there was a change in the used background current or the location of the pump thermistor, please do the following

string_bkg_used = 'ib2'
# string_bkg_used = 'ib0'
string_pump_location = 'InternalPump'

k = 273.15

# part to calculate cph and its error
dfmeta = calculate_cph(dfmeta)
dfmeta['unc_cPH'] = dfmeta['cPH'].std()
dfmeta['unc_cPL'] = dfmeta['cPL'].std()

allFiles = sorted(glob.glob(path + "Current/*rawcurrent.hdf"))

size = len(allFiles)
datelist = [0] * size
j = 0

bool_rscorrection = True

for (filename) in (allFiles):
    file = open(filename, 'r')

    date_tmp = filename.split('/')[-1].split('.')[0][2:8]
    fname = filename.split('/')[-1].split('.')[0][0:8]
    fullname = filename.split('/')[-1].split('.')[0]
    metaname = path + 'Metadata/' + fname + "_metadata.csv"
    if search("2nd", fullname): metaname = path + 'Metadata/' + fname + "_2nd_metadata.csv"

    date = datetime.strptime(date_tmp, '%y%m%d')
    datef = date.strftime('%Y%m%d')
    datestr = str(datef)

    print(filename)

    if (datef == '20050222') | (datef == '20050301') | (datef == '20050322') | (datef == '20050412'): continue


    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    ## missing PTU lab and PF values for values before 1999 and 1997
    if datef < '19970107':
        dfm['PF'] = pf[date.month-1]
        dfm['Pground'] = plab[date.month-1]
    if datef < '19981111':
        dfm['TLab'] = tlab[date.month-1]
        dfm['ULab'] = ulab[date.month-1]

    if datef < '19941012': continue # no bkg values
    # if datef > '20000105': continue #already hom.


    # to deal with data that is not complete
    if (len(df) < 100): continue

    df['Date'] = datef
    df['Datedt'] = pd.to_datetime(df['Date'], format='%Y%m%d').dt.date

    # input variables for hom.
    df['Tpump'] = df['TboxK']
    df['Phip'] = 100 / dfm.at[dfm.first_valid_index(),'PF']
    df['Eta'] = 1

    df['dPhip'] = 0.02
    df['unc_cPH'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cPH']
    df['unc_cPL'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cPL']

    # different pump temperature corrections
    df['unc_Tpump'] = 0.5  # case II-V
    serial_ecc = dfm.at[dfm.first_valid_index(), 'SerialECC']
    # infor from station pi
    if datef <= '20001101':
        string_pump_location = 'case3'
    if datef > '20001101':
        string_pump_location = 'InternalPump'

    #      radiosonde RS80 correction   #
    # Electronic o3 sonde interface  was replaced with the transfer from RS80 to RS92  in 24 Nov 2005.
    rsmodel = ''
    # bool_rscorrection = ''
    if datef <= '20051124':
        # rsmodel = 'RS80'
        bool_rscorrection = True
    if datef > '20051124':
        bool_rscorrection = False
    #
    # bool_rscorrection = False

    if bool_rscorrection:
        df['Crs'], df['unc_Crs'] = RS_pressurecorrection(df, 'Height', rsmodel)
        df['Pair'] = df['Pair'] - df['Crs']


    #      conversion efficiency        #
    try: df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair', 3.0)
    except KeyError: df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair', 3.0)
    #correction to the metadata from the station PI:
    # All z-sondes before so06020112 were flown with 1 %KI
    if (datef < '20060201') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z' ): dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] = 10
    if (datef >= '20060201') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z' ): dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] = 5
    if (datef < '20060201') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC' ): dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] = 10


    df['stoich'], df['unc_stoich'] = stoichmetry_conversion(df, 'Pair', dfm.at[dfm.first_valid_index(), 'SensorType'],
                                                            dfm.at[dfm.first_valid_index(), 'SolutionConcentration'], 'ENSCI05')
    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    if string_bkg_used == 'ib2': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2')
    if string_bkg_used == 'ib0': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB0')
    df['iB2'] = dfm.at[dfm.first_valid_index(), 'iB2']

    #       pump temperature correction       #
    df['Tpump_cor'], df['unc_Tpump_cor'] = pumptemp_corr(df, string_pump_location, 'Tpump', 'unc_Tpump', 'Pair')

    #      pump flow corrections        #
    # ground correction
    df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'Pground',
                                                                   'ULab', True)
    # efficiency correction
    pumpflowtable = ''
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': pumpflowtable = 'komhyr_86'
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': pumpflowtable = 'komhyr_95'
    df['Cpf'], df['unc_Cpf'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'table_interpolate')
    df['Phip_cor'], df['unc_Phip_cor'] = return_phipcor(df, 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf')

    # all corrections
    # all corrections
    df['O3_nc'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'Eta', 'Phip', False)
    df['O3c_eta'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'eta_c', 'Phip', False)
    df['O3c_etabkg'] = currenttopo3(df, 'I', 'Tpump', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpump'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpumpphigr'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_ground', False)
    df['O3c_etabkgtpumpphigref'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor', False)
    df['O3c'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor', False)

    if len(df[df['O3c']< 0]) > 0: print('why',filename)

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

    md_clist = ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
                'unc_eta_c', 'iB2', 'iBc', 'unc_iBc', 'TLab', 'deltat', 'unc_deltat', 'unc_deltat_ppi', 'dEta']

    # merge all the metadata to md df and save it as a csv file
    for j in range(len(md_clist)):
        dfm[md_clist[j]] = df.at[df.first_valid_index(), md_clist[j]]

    # dfm.to_csv(path + '/DQA_upd/'+ datestr + "_o3smetadata_rs80.csv")

    df = df.drop(
        ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
         'unc_eta_c', 'iB2', 'iBc', 'unc_iBc', 'dEta'], axis=1)
    
     # data file that has data and uncertainties that depend on Pair or Height or Temperature
    # df.to_hdf(path + '/DQA_upd/' + datestr + "_all_hom_rs80.hdf", key = 'df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']
    df = df.drop(['TboxC', 'Tpump', 'Tpump_cor', 'Cpf', 'unc_Cpf', 'Phip_cor', 'unc_Phip_cor', 'O3c', 'dPhi_cor'], axis = 1)
    # df to be converted to WOUDC format together with the metadata
    # df.to_hdf(path + '/DQA_upd/' + datestr + "_o3sdqa_rs80.hdf", key = 'df')

################################################################################################################################

 ##exceptions for sodankyla
    # try:
    #     if dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 3:
    #         if (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC') & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 3):
    #             dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] = 10
    #         if (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z') & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 3):
    #             dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] = 5
    # except KeyError:
    #     if (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC'): dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] = 10
    #     if (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z'): dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] = 5
    #
    # if (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z') & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 5)\
    #         & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 10) & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 3):
    #     dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] = 5
    # if (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC') & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 5)\
    #         & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 10) & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 3):
    #     dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] = 10
