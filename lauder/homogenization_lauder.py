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



dfmeta.loc[dfmeta.TLab > k, 'TLab'] = dfmeta.loc[dfmeta.TLab > k, 'TLab'] - k
dfmeta['PF'] = dfmeta['Phip']

series = dfmeta[['Date','TLab','ULab','PF']]
series['Date'] = pd.to_datetime(series['Date'], format='%Y-%m-%d')

# df['DataFrame Column'] = pd.to_datetime(df['DataFrame Column'], format=specify your format)
series = series.set_index('Date')
series = series[series.TLab < 500]
upsampled = series.resample('1M').mean()

# plab = [0] * 12
tlab = [0] * 12
ulab = [0] * 12
pf = [0] * 12

for i in range(1,13):
    j = i-1
    tlab[j] = upsampled[upsampled.index.month == i].median()[0]
    ulab[j] = upsampled[upsampled.index.month == i].median()[1]
    pf[j] = upsampled[upsampled.index.month == i].median()[2]

print('TLab', np.mean(tlab))
print('ULab', np.mean(ulab))
print("PF", pf)

dfmeta['PLab'] = 970.2
dfmeta['Pground'] = 970.2

dfmeta.loc[dfmeta.Date < '2014-02-05', 'TLab'] = np.mean(tlab)
dfmeta.loc[dfmeta.Date < '2014-02-05', 'ULab'] = np.mean(ulab)

#clean some outliers
dfmeta.loc[dfmeta.ULab > 100, 'ULab'] = np.mean(ulab)
dfmeta.loc[dfmeta.TLab > 50, 'TLab'] = np.mean(tlab)


dfmeta = calculate_cph(dfmeta)

print('come on', dfmeta['cPH'].mean(),  dfmeta['cPH'].median(), dfmeta['cPH'].max(), dfmeta['cPH'].min() ,dfmeta['cPH'].std())

dfmeta['unc_cPH'] = dfmeta['cPH'].std()
dfmeta['unc_cPL'] = dfmeta['cPL'].std()


dfmt = dfmeta[['Date', 'cPH', 'unc_cPH', 'PLab', 'Pground', 'TLab', 'ULab', 'x', 'psaturated']]

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


allFiles = sorted(glob.glob(path + "CSV/*hdf"))


size = len(allFiles)
datelist = [0] * size
j = 0

bool_rscorrection = False

for (filename) in (allFiles):
    file = open(filename, 'r')

    date_tmp = filename.split('/')[-1].split('.')[0][0:8]
    fname = date_tmp
    metaname = path + 'metadata/' + fname + "_md.csv"

    date = datetime.strptime(date_tmp, '%Y%m%d')
    datef = date.strftime('%Y%m%d')
    date2 = date.strftime('%Y-%m-%d')

    datestr = str(datef)
    # if datef < '19961001':continue #before this date it is BrewerMast
    # if datef < '2009':continue #already homogenized
    # if datef > '2017':continue #already homogenized

    if datef == '20020725': continue
    if datef == '20050124': continue
    # if datef == '20190524': continue
    if datef == '20191216': continue

    print('one', filename)


    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    # get rid of the commas
    df = df.replace(",", " ", regex=True)

    try: dfm['SensorType'] = dfm['SondeType']
    except KeyError: continue # for some sondes that have N serial number
    dfm['Date'] = pd.to_datetime(dfm['Date'], format='%Y-%m-%d')
    dfm['Date'] = dfm['Date'].dt.date
    dfm['DateTime'] = pd.to_datetime(dfm['Date'], format='%Y-%m-%d')
    df_tmp = dfmeta[dfmeta.Date == date2]
    df_tmp = df_tmp.reset_index()
    dfm['ROC'] = df_tmp['ROC']

    # df = filter_data(df)
    # df = df.reset_index()
    # print(list(dfm))
    # print(list(dfmeta))

    df['Date'] = datef


    # missing TLab, PLAb, ULab values
    if datef < '2014-02-05':
        dfm.at[0, 'TLab'] = tlab[date.month - 1]
        dfm.at[0, 'ULab'] = ulab[date.month - 1]


    # #for some of the dates TLab is measured in K, to fix it:
    # if (dfm.at[0, 'TLab'] < 320) & (dfm.at[0, 'TLab'] > 50):
    #     dfm.at[0, 'TLab'] = dfm.at[0, 'TLab'] - k

    dfm.at[0, 'Pground'] = 970.2
    dfm.at[0, 'PLab'] = 970.2


    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d').dt.date
    #convert df (which is a str) to float
    df[['Time', 'Press', 'Alt', 'Temp', 'RH', 'PO3', 'TPump', 'O3CellI', 'EvapCath', 'WindSp', 'WindDir', 'Lat', 'Lon',
         'RH1', 'RH2', 'GPSPres', 'GPSAlt', 'GPSTraw', 'GPSTcor', 'GPSRH']] = df[['Time', 'Press', 'Alt', 'Temp', 'RH', 'PO3', 'TPump', 'O3CellI', 'EvapCath', 'WindSp', 'WindDir', 'Lat', 'Lon',
         'RH1', 'RH2', 'GPSPres', 'GPSAlt', 'GPSTraw', 'GPSTcor', 'GPSRH']].astype(float)

    df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')


    if len(dfm) == 0:
        print('No metadata', datef)
        continue



    # for O3 use PO3 from DQA processed by station
    df['O3'] = df['PO3']
    # input variables for hom.
    df['Tpump'] = df['TPump'].astype(float) + k
    df['Phip'] = 100 / dfm.at[dfm.first_valid_index(),'Phip']
    df['Eta'] = 1
    df['Pair'] = df['Press']


    df['dPhip'] = 0.02
    df['unc_Tpump'] = 0.5
    df['unc_cPH'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cPH']
    df['unc_cPL'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cPL']


    # print(dfm.at[0, 'SensorType'], dfm.at[0, 'SolutionConcentration'] )
    #      conversion efficiency        #
    df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair',3)
    df['stoich'], df['unc_stoich'] = stoichmetry_conversion(df, 'Pair', dfm.at[0, 'SensorType'],
                                                            dfm.at[0, 'SolutionConcentration'], 'ENSCI05')

    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    if string_bkg_used == 'ib2': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2','1996')

    #       pump temperature correction       #
    if dfm.at[dfm.first_valid_index(), 'Pump_loc'] == '4A': string_pump_location = 'case1'
    if dfm.at[dfm.first_valid_index(), 'Pump_loc'] == '5A': string_pump_location = 'case3'
    if dfm.at[dfm.first_valid_index(), 'Pump_loc'] == '6A': string_pump_location = 'case5'
    if dfm.at[dfm.first_valid_index(), 'Pump_loc'] == 'Z': string_pump_location = 'case5'
    df['Tpump_cor'], df['unc_Tpump_cor'] = pumptemp_corr(df, string_pump_location, 'Tpump', 'unc_Tpump', 'Pair')


    #      pump flow corrections        #
    # ground correction
    df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'Pground', 'ULab', True)
    # efficiency correction
    # pumpflowtable = ''
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': pumpflowtable = 'komhyr_86'
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': pumpflowtable = 'komhyr_95'

    df['Cpf'], df['unc_Cpf'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'table_interpolate')

    # df['Phip_coreff'] = df['Phip']/df['Cpf']
    df['Phip_cor'], df['unc_Phip_cor'] = return_phipcor(df, 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf')


    df['iB2'] = dfm.at[dfm.first_valid_index(),'iB2']
    df['I'] = df['O3CellI']
    df['Tpump'] = df['Tpump'].astype('float')
    df['Tpump_cor'] = df['Tpump_cor'].astype('float')


    # all corrections
    df['O3_nc'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'Eta', 'Phip', False)
    df['O3c_eta'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'eta_c', 'Phip', False)
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
    # df['dTpump_cor'] = (df['unc_Tpump_cor'] / df['Tpump_cor'])**2
    df['dTpump_cor'] = df['unc_Tpump_cor']

    # final uncertainity on O3
    df['dO3'] = np.sqrt(df['dIall'] + df['dEta'] + df['dPhi_cor'] + df['dTpump_cor'])

    dfm['O3Sonde_burst'] = o3_integrate(df, 'O3')
    dfm['burst'] = df.Pair.min()

    if df.Pair.min() <= 10:
        # print('and now how to calculate TON', df.Pair.min())
        dft = df[df.Pair >= 10]

        # for woudc O3 values
        dfm['O3Sonde'] = o3_integrate(dft, 'O3')
        dfm['O3SondeTotal'] = dfm['O3Sonde'] + dfm['ROC']
        # if there is no Dobson values, assign the ratio to 9999
        try:
            dfm['O3ratio'] = dfm['Dobson'] / dfm['O3SondeTotal']
        except KeyError:
            dfm['Dobson'] = 9999
            dfm['O3ratio'] = 9999

        # the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = o3_integrate(dft, 'O3c')
        dfm['O3SondeTotal_hom'] = dfm['O3Sonde_hom'] + dfm['ROC']
        # if there is no Dobson values, assign the ratio to 9999
        try:
            dfm['O3ratio_hom'] = dfm['Dobson'] / dfm['O3SondeTotal_hom']
        except KeyError:
            dfm['Dobson'] = 9999
            dfm['O3ratio'] = 9999
        # the same for raw no corrected o3 values
        dfm['O3Sonde_raw'] = o3_integrate(dft, 'O3_nc')
        dfm['O3SondeTotal_raw'] = dfm['O3Sonde_raw'] + dfm['ROC']
        try:
            dfm['O3ratio_raw'] = dfm['Dobson'] / dfm['O3SondeTotal_raw']
        except KeyError:
            dfm['Dobson'] = 9999
            dfm['O3ratio'] = 9999

        dfm['O3Sonde_10hpa'] = o3_integrate(dft, 'O3')
        dfm['O3Sonde_10hpa_raw'] = o3_integrate(dft, 'O3_nc')
        dfm['O3Sonde_10hpa_hom'] = o3_integrate(dft, 'O3c')


        if dfm.at[0, 'Dobson'] > 999:
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
                'unc_eta_c','iB2', 'iBc', 'unc_iBc',  'TLab', 'deltat', 'unc_deltat',  'unc_deltat_ppi', 'dEta']

    # merge all the metadata to md df and save it as a csv file
    for j in range(len(md_clist)):
        dfm[md_clist[j]] = df.at[df.first_valid_index(), md_clist[j]]

    dfm.to_csv(path + '/DQA_nors80/'+ datestr + "_o3smetadata_nors80.csv")


    # df = df.drop(
    #     ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
    #      'unc_eta_c', 'iB2', 'iBc', 'unc_iBc','dEta'], axis=1)


    # data file that has data and uncertainties that depend on Pair or Height or Temperature
    df.to_hdf(path + '/DQA_nors80/' + datestr + "_all_hom_nors80.hdf", key = 'df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']
    df['Phip'] = df['Phip_cor']


    df = df.drop(['dPhip','Tpump', 'Tpump_cor', 'deltat_ppi', 'TLab', 'TLabK', 'cPL', 'cPH', 'Phip_ground', 'deltat', 'unc_deltat',
                  'deltat_ppi', 'unc_deltat_ppi', 'TLab', 'TLabK', 'cPL', 'cPH', 'Phip_ground', 'unc_Phip_ground',
     'Cpf', 'unc_Cpf', 'Phip_cor', 'unc_Phip_cor', 'O3_nc','O3c', 'O3c_eta', 'O3c_etabkg','O3c_etabkgtpump',
                  'O3c_etabkgtpumpphigr','dI', 'dIall', 'dPhi_cor', 'dTpump_cor', 'dPhip'], axis = 1)
    # , 'Crs', 'unc_Crs', 'dPrs'
    # df to be converted to WOUDC format together with the metadata

    df.to_hdf(path + '/DQA_nors80/' + datestr + "_o3sdqa_nors80.hdf", key = 'df')

