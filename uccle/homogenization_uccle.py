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

from functions.df_filter import filter_data



path = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/'

## important adjusments
# if there was a change in the used background current or the location of the pump thermistor, please do the following

# string_bkg_used = 'ib2'
string_bkg_used = 'ib0'
string_pump_location = 'InternalPump'


k = 273.15

dfmeta = pd.read_csv(path + 'Raw_upd/All_metadata.csv')
print(list(dfmeta))

allFiles = sorted(glob.glob(path + "/Raw_upd/*hdf"))


size = len(allFiles)
datelist = [0] * size
j = 0

bool_rscorrection = False

for (filename) in (allFiles):
    file = open(filename, 'r')
    print(filename)

    date_tmp = filename.split('/')[-1].split('.')[0][2:8]
    fname = filename.split('/')[-1].split('.')[0][0:8]
    fullname = filename.split('/')[-1].split('.')[0]
    metaname = path + 'Raw_upd/' + fname + "_md.csv"
    if search("2nd", fullname): metaname = path + 'Raw_upd/' + fname + "_2nd_md.csv"

    date = datetime.strptime(date_tmp, '%y%m%d')
    datef = date.strftime('%Y%m%d')
    datestr = str(datef)
    if datef < '19961001':continue #before this date it is BrewerMast
    if datef > '19970501':continue #already homogenized

    print(filename)

    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    df = filter_data(df)

    # to deal with data that is not complete
    if (len(df) < 50): continue

    df['Date'] = datef
    df['Datedt'] = pd.to_datetime(df['Date'], format='%Y%m%d').dt.date

    if len(dfm) == 0:
        print('No metadata', datef)
        continue

    # input variables for hom.
    df['Tpump'] = df['Tbox'] + k
    df['Phip'] = 100 / dfm.at[dfm.first_valid_index(),'PF']
    df['Eta'] = 1
    df['Pair'] = df['P']

    df['dPhip'] = 0.02
    df['unc_Tpump'] = 0.5
    # no lab ptu correction is needed for uccle
    # df['unc_cph'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cph']
    # df['unc_cpl'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cpl']

    #      radiosonde RS80 correction   #
    rsmodel = ''
    bool_rscorrection = ''
    if datef <= '20070901':
        rsmodel = 'RS80'
        bool_rscorrection = True
    if datef > '20070901':
        bool_rscorrection = False
    #
    if bool_rscorrection:
        df['Crs'], df['unc_Crs'] = RS_pressurecorrection(df, 'Height', rsmodel)
        df['Pair'] = df['Pair'] - df['Crs']

    #      conversion efficiency        #
    df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair',3)
    df['stoich'] = 1
    df['unc_stoich'] = 0
    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    if string_bkg_used == 'ib2': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2')
    if string_bkg_used == 'ib0': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB0')

    #       pump temperature correction       #
    if datef < '19981201':
        string_pump_location = 'case3'
    if datef > '19981201':
        string_pump_location = 'InternalPump'
    df['Tpump_cor'], df['unc_Tpump_cor'] = pumptemp_corr(df, string_pump_location, 'Tpump', 'unc_Tpump', 'Pair')

    #      pump flow corrections        #
    # ground correction
    dfm['TLab'] = 20
    df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'Pground', 'ULab', False)
    # efficiency correction
    # pumpflowtable = ''
    # if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': pumpflowtable = 'komhyr_86'
    # if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': pumpflowtable = 'komhyr_95'
    pumpflowtable = 'komhyr_95'
    df['Cpf'], df['unc_Cpf'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'polyfit')
    # df['Cpf'], df['unc_Cpf'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'table_interpolate')

    df['Phip_coreff'] = df['Phip']/df['Cpf']
    df['Phip_cor'], df['unc_Phip_cor'] = return_phipcor(df, 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf')

    df['iB0'] = dfm.at[dfm.first_valid_index(),'iB0']
    df['I'] = df['I'].astype('float')
    df['Tpump'] = df['Tpump'].astype('float')
    df['Tpump_cor'] = df['Tpump_cor'].astype('float')

    # all corrections
    df['O3_nc'] = currenttopo3(df, 'I', 'Tpump', 'iB0', 'Eta', 'Phip', False)
    df['O3c_phipeff'] = currenttopo3(df, 'I', 'Tpump', 'iB0', 'Eta', 'Phip_coreff', False)
    df['O3c_eta'] = currenttopo3(df, 'I', 'Tpump', 'iB0', 'eta_c', 'Phip', False)
    df['O3c_etabkg'] = currenttopo3(df, 'I', 'Tpump', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpump'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpumpphigr'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_ground', False)
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
    # if bool_rscorrection: df['dO3'] = np.sqrt(df['dIall'] + df['dEta'] + df['dPhi_cor'] + df['dTpump_cor'] + df['dPrs'])


    md_clist = ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
                'unc_eta_c','iB0', 'iBc', 'unc_iBc',  'TLab', 'deltat', 'unc_deltat',  'unc_deltat_ppi', 'dEta']

    # merge all the metadata to md df and save it as a csv file
    for j in range(len(md_clist)):
        dfm[md_clist[j]] = df.at[df.first_valid_index(), md_clist[j]]

    dfm.to_csv(path + '/DQA_upd/'+ datestr + "_o3smetadata_rs80.csv")


    df = df.drop(
        ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
         'unc_eta_c', 'iB0', 'iBc', 'unc_iBc','dEta','Phi'], axis=1)


    # data file that has data and uncertainties that depend on Pair or Height or Temperature
    df.to_hdf(path + '/DQA_upd/' + datestr + "_all_hom_rs80.hdf", key = 'df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']
    df['Phip'] = df['Phip_cor']

    df = df.drop(['Tboxcor', 'PO3_dqar',
    'dPO3_dqar',  'Tpump', 'Tpump_cor', 'deltat_ppi', 'TLab', 'TLabK', 'cPL', 'cPH', 'Phip_ground',
    'unc_Phip_ground', 'Cpf', 'unc_Cpf', 'Phip_cor', 'unc_Phip_cor', 'O3_nc','O3c', 'O3c_eta', 'O3c_etabkg','O3c_etabkgtpump',
    'O3c_etabkgtpumpphigr','dI', 'dIall', 'dPhi_cor', 'dTpump_cor', 'dPhip'], axis = 1)
    # , 'Crs', 'unc_Crs', 'dPrs'
    # df to be converted to WOUDC format together with the metadata

    # df.to_hdf(path + '/DQA_upd/' + datestr + "_o3sdqa_rs80.hdf", key = 'df')

