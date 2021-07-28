import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime
import time

## for ib) values that are equal to -1.0 -> assign them to 0

from functions.homogenization_functions import absorption_efficiency, stoichmetry_conversion, conversion_efficiency, \
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency, \
    return_phipcor, RS_pressurecorrection, o3_integrate

from functions.df_filter import filter_data


k = 273.15

path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/'
dfmeta = pd.read_csv(path + 'metadata/Lauder_MetadaAll.csv')
dfmeta = dfmeta[dfmeta.TLab < 500]
dfmeta.loc[dfmeta.TLab > k, 'TLab'] = dfmeta.loc[dfmeta.TLab > k, 'TLab'] - k
dfmeta['PF'] = dfmeta['Phip']

# dfmeta = calculate_cph(dfmeta)
# dfmeta['unc_cPH'] = dfmeta['cPH'].std()
# dfmeta['unc_cPL'] = dfmeta['cPL'].std()

series = dfmeta[['Date','TLab','ULab','PF']]
series['Date'] = pd.to_datetime(series['Date'], format='%Y-%m-%d')

# df['DataFrame Column'] = pd.to_datetime(df['DataFrame Column'], format=specify your format)
series = series.set_index('Date')
upsampled = series.resample('1M').mean()

# plab = [0] * 12
tlab = [0] * 12
ulab = [0] * 12
pf = [0] * 12

for i in range(1,13):
    j = i-1
    tlab[j] = upsampled[upsampled.index.month == i].mean()[0]
    ulab[j] = upsampled[upsampled.index.month == i].mean()[1]
    pf[j] = upsampled[upsampled.index.month == i].mean()[2]

print('TLab', tlab)
print('ULab', ulab)
print("PF", pf)


## important adjusments
# if there was a change in the used background current or the location of the pump thermistor, please do the following

string_bkg_used = 'ib2'


# to get ROC from the corresponding station roc table
clms = [i for i in range(1,13)]
table = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/sonde_lauder_roc.txt',  skiprows=1, sep="\s *", names = clms,  header=None)
# take roc at 10hpa values
table = table[table.index ==10]
# assign ROC values to dfmeta
dfmeta['Date'] =  pd.to_datetime(dfmeta['Date'], format='%Y-%m-%d')
dfmeta['Date'] =  dfmeta['Date'].dt.date
dfmeta['DateTime'] =  pd.to_datetime(dfmeta['Date'], format='%Y-%m-%d')
dfmeta['ROC'] = 0
for i in range(1,13):
    dfmeta.loc[dfmeta.DateTime.dt.month == i, 'ROC'] = table[i].tolist()[0]

dfmeta['Date'] = dfmeta['DateTime'].dt.strftime('%Y-%m-%d')


allFiles = sorted(glob.glob(path + "csv/*hdf"))


size = len(allFiles)
datelist = [0] * size
j = 0

bool_rscorrection = False

for (filename) in (allFiles):
    file = open(filename, 'r')

    print(filename)

    date_tmp = filename.split('/')[-1].split('.')[0][0:8]
    print(date_tmp)
    fname = date_tmp
    # fullname = filename.split('/')[-1].split('.')[0]
    metaname = path + 'metadata/' + fname + "_md.csv"

    date = datetime.strptime(date_tmp, '%Y%m%d')
    datef = date.strftime('%Y%m%d')
    date2 = date.strftime('%Y-%m-%d')

    datestr = str(datef)
    # if datef < '19961001':continue #before this date it is BrewerMast
    # if datef < '19970301':continue #already homogenized

    print(filename)

    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    dfm['Date'] = pd.to_datetime(dfm['Date'], format='%Y-%m-%d')
    dfm['Date'] = dfm['Date'].dt.date
    dfm['DateTime'] = pd.to_datetime(dfm['Date'], format='%Y-%m-%d')
    df_tmp = dfmeta[dfmeta.Date == date2]
    df_tmp = df_tmp.reset_index()
    dfm['ROC'] = df_tmp['ROC']

    # df = filter_data(df)
    # df = df.reset_index()

    # to deal with data that is not complete
    if (len(df) < 200): continue

    df['Date'] = datef
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d').dt.date
    df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    if len(dfm) == 0:
        print('No metadata', datef)
        continue

    # for O3 use PO3 from DQA processed by station
    df['O3'] = df['PO3']
    # input variables for hom.
    df['Tpump'] = df['TPump'] + k
    df['Phip'] = 100 / dfm.at[dfm.first_valid_index(),'Phip']
    df['Eta'] = 1
    df['Pair'] = df['Press']
    # df['Cpf'] = 1
    # df['unc_Cpf'] = 1


    df['dPhip'] = 0.02
    df['unc_Tpump'] = 0.5
    # df['unc_cph'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cph']
    # df['unc_cpl'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cpl']


    #      conversion efficiency        #
    df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair',3)
    df['stoich'], df['unc_stoich'] = stoichmetry_conversion(df, 'Pair', dfm.at[0, 'SensorType'],
                                                            dfm.at[0, 'SolutionConcentration'], 'ENSCI05')

    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    # if string_bkg_used == 'ib2': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2')
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
    df['Cpoly'], df['unc_Coly'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'polyfit')

    df['Cpf'], df['unc_Cpf'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'table_interpolate')

    # df = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'table_interpolate')

    df['Phip_coreff'] = df['Phip']/df['Cpf']
    df['Phip_corpoly'], df['unc_Phip_corpoly'] = return_phipcor(df, 'Phip_ground', 'unc_Phip_ground', 'Cpoly', 'unc_Coly')
    df['Phip_cor'], df['unc_Phip_cor'] = return_phipcor(df, 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf')


    df['iB0'] = dfm.at[dfm.first_valid_index(),'iB0']
    df['I'] = df['I'].astype('float')
    df['Tpump'] = df['Tpump'].astype('float')
    df['Tpump_cor'] = df['Tpump_cor'].astype('float')


    # all corrections
    df['O3_nc'] = currenttopo3(df, 'I', 'Tpump', 'iB0', 'Eta', 'Phip', False)
    df['O3c_eta'] = currenttopo3(df, 'I', 'Tpump', 'iB0', 'eta_c', 'Phip', False)
    df['O3c_etabkg'] = currenttopo3(df, 'I', 'Tpump', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpump'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpumpphigr'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_ground', False)
    df['O3cpoly'] = currenttopo3(df, 'I', 'Tpump_cor', 'iB0', 'eta_c', 'Phip_corpoly', False)
    df['O3c'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor', False)

    dftest = df[['Time','P', 'I', 'Cpf','Cpoly','O3', 'O3c','O3cpoly', 'Phip_cor', 'Phip_corpoly']]


    # uncertainities
    df['dI'] = 0
    df.loc[df.I < 1, 'dI'] = 0.01
    df.loc[df.I >= 1, 'dI'] = 0.01 * df.loc[df.I > 1, 'I']
    df['dIall'] = (df['dI'] ** 2 + df['unc_iBc']**2) / (df['I'] - df['iBc'])**2
    df['dEta'] = (df['unc_eta_c'] / df['eta_c'])**2
    df['dPhi_cor'] = (df['unc_Phip_cor'] / df['Phip_cor'])**2
    df['dTpump_cor'] = (df['unc_Tpump_cor'] / df['Tpump_cor'])**2
    # final uncertainity on O3
    df['dO3'] = np.sqrt(df['dIall'] + df['dEta'] + df['dPhi_cor'] + df['dTpump_cor'])

    dfm['O3Sonde_burst'] = o3_integrate(df, 'O3')
    dfm['O3Sonde_burst_raw'] = o3_integrate(df, 'O3_nc')

    dfm['O3Sonde_burst_hom'] = o3_integrate(df, 'O3c')
    dfm['O3Sonde_burst_eta'] = o3_integrate(df, 'O3c_eta')
    dfm['O3Sonde_burst_etabkg'] = o3_integrate(df, 'O3c_etabkg')
    dfm['O3Sonde_burst_etabkgtpump'] = o3_integrate(df, 'O3c_etabkgtpump')
    dfm['O3Sonde_burst_etabkgtpumpphigr'] = o3_integrate(df, 'O3c_etabkgtpumpphigr')

    dfm['burst'] = df.Pair.min()

    if df.Pair.min() <= 10:
        # print('and now how to calculate TON', df.Pair.min())
        dft = df[df.Pair >= 10]

        # for woudc O3 values
        dfm['O3Sonde'] = o3_integrate(dft, 'O3')
        dfm['O3SondeTotal'] = dfm['O3Sonde'] + dfm['ROC']
        dfm['O3ratio'] = dfm['TO_Brewer'] / dfm['O3SondeTotal']
        # the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = o3_integrate(dft, 'O3c')
        dfm['O3SondeTotal_hom'] = dfm['O3Sonde_hom'] + dfm['ROC']
        dfm['O3ratio_hom'] = dfm['TO_Brewer'] / dfm['O3SondeTotal_hom']
        # the same for raw no corrected o3 values
        dfm['O3Sonde_raw'] = o3_integrate(dft, 'O3_nc')
        dfm['O3SondeTotal_raw'] = dfm['O3Sonde_raw'] + dfm['ROC']
        dfm['O3ratio_raw'] = dfm['TO_Brewer'] / dfm['O3SondeTotal_raw']

        dfm['O3Sonde_10hpa'] = o3_integrate(dft, 'O3')
        dfm['O3Sonde_10hpa_raw'] = o3_integrate(dft, 'O3_nc')
        dfm['O3Sonde_10hpa_hom'] = o3_integrate(dft, 'O3c')
        dfm['O3Sonde_10hpa_eta'] = o3_integrate(dft, 'O3c_eta')
        dfm['O3Sonde_10hpa_etabkg'] = o3_integrate(dft, 'O3c_etabkg')
        dfm['O3Sonde_10hpa_etabkgtpump'] = o3_integrate(dft, 'O3c_etabkgtpump')
        dfm['O3Sonde_10hpa_etabkgtpumpphigr'] = o3_integrate(dft, 'O3c_etabkgtpumpphigr')

        if dfm.at[0, 'TO_Brewer'] > 999:
            dfm['O3ratio'] = 9999
            dfm['O3ratio_hom'] = 9999
            dfm['O3ratio_raw'] = 9999

        # print('o3sonde', dfm[['O3Sonde', 'O3Sonde_hom']])

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

    #TON related
    # 'TO_Brewer', 'RO_aboveburst', 'TON', 'SondeO3', 'IntegratedO3'


    md_clist = ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
                'unc_eta_c','iB0', 'iBc', 'unc_iBc',  'TLab', 'deltat', 'unc_deltat',  'unc_deltat_ppi', 'dEta']

    # merge all the metadata to md df and save it as a csv file
    for j in range(len(md_clist)):
        dfm[md_clist[j]] = df.at[df.first_valid_index(), md_clist[j]]

    dfm.to_csv(path + '/DQA_nors80/'+ datestr + "_o3smetadata_nors80.csv")


    df = df.drop(
        ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
         'unc_eta_c', 'iB0', 'iBc', 'unc_iBc','dEta','Phi'], axis=1)


    # data file that has data and uncertainties that depend on Pair or Height or Temperature
    df.to_hdf(path + '/DQA_nors80/' + datestr + "_all_hom_nors80.hdf", key = 'df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']
    df['Phip'] = df['Phip_cor']

    # print(list(df))

    df = df.drop(['Tboxcor', 'PO3_dqar', 'dPhip',
    'dPO3_dqar',  'Tpump', 'Tpump_cor', 'deltat_ppi', 'TLab', 'TLabK', 'cPL', 'cPH', 'Phip_ground', 'deltat', 'unc_deltat',
                  'deltat_ppi', 'unc_deltat_ppi', 'TLab', 'TLabK', 'cPL', 'cPH', 'Phip_ground', 'unc_Phip_ground',
     'Cpf', 'unc_Cpf', 'Phip_cor', 'unc_Phip_cor', 'O3_nc','O3c', 'O3c_eta', 'O3c_etabkg','O3c_etabkgtpump',
                  'O3c_etabkgtpumpphigr','dI', 'dIall', 'dPhi_cor', 'dTpump_cor', 'dPhip'], axis = 1)
    # , 'Crs', 'unc_Crs', 'dPrs'
    # df to be converted to WOUDC format together with the metadata

    df.to_hdf(path + '/DQA_nors80/' + datestr + "_o3sdqa_nors80.hdf", key = 'df')

