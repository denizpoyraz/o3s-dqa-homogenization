import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime
import time

from functions.homogenization_functions import absorption_efficiency, stoichmetry_conversion, conversion_efficiency, \
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency,return_phipcor, RS_pressurecorrection

from functions.df_filter import filter_data, filter_metadata
from functions_copy import o3tocurrent


k = 273.15


path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'

dfmeta = pd.read_csv(path + 'Madrid_Metadata.csv')
dfmeta = dfmeta[dfmeta.DateTime > '1994-01-01'] # start from 1994, because before there are no background values
dfmeta = dfmeta.reset_index()
dfmeta['Date'] = dfmeta['DateTime'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
dfmeta['Date2'] = dfmeta['Date'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))

dfmeta = calculate_cph(dfmeta)
dfmeta['unc_cPH'] = dfmeta['cPH'].std()
dfmeta['unc_cPL'] = dfmeta['cPL'].std()

print(dfmeta['unc_cPH'][0:2])

## part related with TON

# to fix some non-float characters
for i in range(len(dfmeta)):
    try:dfmeta.at[i, 'BrewO3'] = float(dfmeta.at[i, 'BrewO3'])
    except ValueError:dfmeta.at[i, 'BrewO3'] = 0
# to get ROC from the corresponding station roc table
clms = [i for i in range(1,13)]
table = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/sonde_madrid_roc.txt',  skiprows=1, sep="\s *", names = clms,  header=None)
# take roc at 10hpa values
table = table[table.index ==10]
# assign ROC values to dfmeta
dfmeta['datetmp'] = dfmeta['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
dfmeta['ROC'] = 0
for i in range(1,13):
    dfmeta.loc[dfmeta.datetmp.dt.month == i, 'ROC'] = table[i].tolist()[0]




# dfmeta = filter_metadata(dfmeta)

series = dfmeta[['DateTime', 'PLab', 'TLab','ULab','PF']]
series['Date'] = series['DateTime'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
series = series.set_index('Date')
upsampled = series.resample('1M').mean()

plab = [0] * 12
tlab = [0] * 12
ulab = [0] * 12
pf = [0] * 12

for i in range(1,13):
    j = i-1
    plab[j] = upsampled[upsampled.index.month == i].mean()[0]
    tlab[j] = upsampled[upsampled.index.month == i].mean()[1]
    # ulab[j] = upsampled[upsampled.index.month == i].mean()[2]
    ulab[j] = upsampled.mean()[2]

    pf[j] = upsampled[upsampled.index.month == i].mean()[3]

print('tlab', tlab)
print('plab', plab)
print('ulab', ulab)


# allFiles = sorted(glob.glob(path + "CSV/out/19950111*.hdf"))

allFiles = sorted(glob.glob(path + "CSV/out/*.hdf"))

metadata = []


for (filename) in (allFiles):
    file = open(filename, 'r')

    df = pd.read_hdf(filename)

    # if df.at[df.first_valid_index(),'Date'] < '2021-04-21': continue
    if df.at[df.first_valid_index(),'Date'] == '2011-04-06': continue
    # if df.at[df.first_valid_index(),'Date'] == '2021-04-28': continue

    print(filename)

    # print('df', df.dtypes, df['Date'][0:3])
    date = datetime.strptime(df.at[df.first_valid_index(),'Date'], '%Y-%m-%d')
    date2 = datetime.strftime(date, '%Y-%m-%d')
    date_out = datetime.strftime(date, '%Y%m%d')

    dfm = dfmeta[dfmeta.Date2 == date2]
    dfm = dfm.reset_index()


    df['Pair'] = df['Pressure']
    df['O3'] = df['O3PartialPressure']
    df['TboxK'] = df['SampleTemperature'] + k


    if df.at[df.first_valid_index(),'Date'] < '2006-02-26':
        dfm.at[0,'TLab'] = tlab[date.month-1]
        dfm.at[0,'Pground'] = plab[date.month-1]
        dfm.at[0,'PLab'] = plab[date.month-1]


    if df.at[df.first_valid_index(),'Date'] < '2020-11-18':
        dfm.at[0, 'ULab'] = ulab[date.month-1]

    if df.at[df.first_valid_index(),'Date'] < '1994-01-01': continue # no bkg values

    # to deal with data that is not complete
    if (len(df) < 100): continue

    df = o3tocurrent(df, dfm)

    # input variables for hom.
    df['Tpump'] = df['SampleTemperature'] + k
    df['Phip'] = 100 / dfm.at[dfm.first_valid_index(), 'PF']
    df['Eta'] = 1

    df['dPhip'] = 0.02
    df['unc_cPH'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cPH']
    df['unc_cPL'] = dfmeta.at[dfmeta.first_valid_index(), 'unc_cPL']

    # different pump temperature corrections
    df['unc_Tpump'] = 0.5  # case II-V
    # serial_ecc = dfm.at[dfm.first_valid_index(), 'SerialECC']
    # infor from station pi
    if date2 < '1998-12-02':
        string_pump_location = 'case3'
    if date2 >= '1998-12-02':
        string_pump_location = 'InternalPump'

        #      radiosonde RS80 correction   #
        # Electronic o3 sonde interface  was replaced with the transfer from RS80 to RS92  in 24 Nov 2005.
    bool_rscorrection = False
    rsmodel = ''
    bool_rscorrection = ''
    if date2 <= '2006-03-01':
        # rsmodel = 'RS80'
        bool_rscorrection = True
    if date2 >= '2006-03-08 ':
        bool_rscorrection = False

    if bool_rscorrection:
        df['Crs'], df['unc_Crs'] = RS_pressurecorrection(df, 'GPHeight', rsmodel)
        df['Pair'] = df['Pair'] - df['Crs']

    df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair', 3.0)
    # correction to the metadata from the station PI:
    # All z-sondes before so06020112 were flown with 1 %KI
    dfm['SolutionConcentration'] = 10
    dfm['SensorType'] = 'SPC'
    df['stoich'], df['unc_stoich'] = stoichmetry_conversion(df, 'Pair', dfm.at[dfm.first_valid_index(), 'SensorType'],
                                                            dfm.at[dfm.first_valid_index(), 'SolutionConcentration'],
                                                            'ENSCI05')
    # print('stoich', df.at[df.first_valid_index(),'stoich'])
    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2')
    df['iB2'] = dfm.at[dfm.first_valid_index(), 'iB2']

    #       pump temperature correction       #
    df['Tpump_cor'], df['unc_Tpump_cor'] = pumptemp_corr(df, string_pump_location, 'Tpump', 'unc_Tpump', 'Pair')

    #      pump flow corrections        #
    # ground correction
    df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'PLab',
                                                                   'ULab', True)

    # efficiency correction
    pumpflowtable = ''
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': pumpflowtable = 'komhyr_86'
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': pumpflowtable = 'komhyr_95'
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

    if len(df[df['O3c'] < 0]) > 0: print('why', filename)

    # uncertainities
    df['dI'] = 0
    df.loc[df.I < 1, 'dI'] = 0.01
    df.loc[df.I >= 1, 'dI'] = 0.01 * df.loc[df.I > 1, 'I']
    df['dIall'] = (df['dI'] ** 2 + df['unc_iBc'] ** 2) / (df['I'] - df['iBc']) ** 2
    df['dEta'] = (df['unc_eta_c'] / df['eta_c']) ** 2
    df['dPhi_cor'] = (df['unc_Phip_cor'] / df['Phip_cor']) ** 2
    df['dTpump_cor'] = (df['unc_Tpump_cor'] / df['Tpump_cor']) ** 2
    dp1 = 0.05 ; dp2 = 0.1 ; dp3 = 0.5
    if bool_rscorrection:
        df['eps1'] = (df[df.Pair == df.Pair + dp1]['O3'] - df[df.Pair == df.Pair - dp1]['O3'] )/\
                     (df[df.Pair == df.Pair + dp1]['O3'] + df[df.Pair == df.Pair - dp1]['O3'])
        df['eps2'] = (df[df.Pair == df.Pair + dp2]['O3'] - df[df.Pair == df.Pair - dp2]['O3']) / \
                     (df[df.Pair == df.Pair + dp2]['O3'] + df[df.Pair == df.Pair - dp2]['O3'])
        df['eps3'] = (df[df.Pair == df.Pair + dp3]['O3'] - df[df.Pair == df.Pair - dp3]['O3']) / \
                     (df[df.Pair == df.Pair + dp3]['O3'] + df[df.Pair == df.Pair - dp3]['O3'])

    # final uncertainity on O3
    df['dO3'] = np.sqrt(df['dIall'] + df['dEta'] + df['dPhi_cor'] + df['dTpump_cor'])

    #part for TON
    # print('min Pair', df.Pair.min())

    if df.Pair.min () <= 10:
        # print('and now how to calculate TON', df.Pair.min())
        dft = df[df.Pair >= 10]

        #for woudc O3 values
        dfm['O3Sonde'] = (3.9449 * (dft.O3.shift() + dft.O3) * np.log(dft.Pair.shift() / dft.Pair)).sum()
        dfm['O3SondeTotal'] = dfm['O3Sonde'] + dfm['ROC']
        dfm['O3ratio'] = dfm['BrewO3'] / dfm['O3SondeTotal']
        #the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = (3.9449 * (dft.O3c.shift() + dft.O3c) * np.log(dft.Pair.shift() / dft.Pair)).sum()
        dfm['O3SondeTotal_hom'] = dfm['O3Sonde_hom'] + dfm['ROC']
        dfm['O3ratio_hom'] = dfm['BrewO3'] / dfm['O3SondeTotal_hom']
        # the same for raw no corrected o3 values
        dfm['O3Sonde_raw'] = (3.9449 * (dft.O3_nc.shift() + dft.O3_nc) * np.log(dft.Pair.shift() / dft.Pair)).sum()
        dfm['O3SondeTotal_raw'] = dfm['O3Sonde_raw'] + dfm['ROC']
        dfm['O3ratio_raw'] = dfm['BrewO3'] / dfm['O3SondeTotal_raw']

        # print('o3sonde', dfm[['O3Sonde', 'O3Sonde_hom']])


    if df.Pair.min () > 10:
        dfm['O3Sonde'] = 9999
        dfm['O3SondeTotal'] = 9999
        dfm['O3ratio'] = 9999
        # the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = 9999
        dfm['O3SondeTotal_hom'] = 9999
        dfm['O3ratio_hom'] = 9999

        # print('o3sonde', dfm[['O3Sonde', 'O3Sonde_hom']])



    dfm['iBc'] = df.at[df.first_valid_index(), 'iBc']

    dfm.to_csv(path + '/DQA/'+ date_out + "_o3smetadata_rs80.csv")

    metadata.append(dfm)


    df.to_hdf(path + '/DQA/' + date_out + "_all_hom_rs80.hdf", key = 'df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']

    if bool_rscorrection:

        df = df.drop(['TboxK', 'SensorType', 'SolutionVolume', 'Cef', 'ibg', 'iB2', 'Tpump', 'Phip', 'Eta', 'dPhip',
                      'unc_cPH', 'unc_cPL', 'unc_Tpump', 'Crs', 'unc_Crs', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich',
                      'eta_c', 'unc_eta', 'unc_eta_c', 'iBc', 'unc_iBc', 'Tpump_cor', 'unc_Tpump_cor', 'deltat', 'unc_deltat', 'deltat_ppi',
                      'unc_deltat_ppi', 'TLab', 'ULab', 'Pground', 'x', 'psaturated', 'cPH', 'TLabK', 'cPL', 'Phip_ground',
                      'unc_Phip_ground', 'Cpf', 'unc_Cpf', 'Phip_cor', 'unc_Phip_cor', 'O3c', 'O3_nc', 'O3c_eta', 'O3c_etabkg',
                      'O3c_etabkgtpump', 'O3c_etabkgtpumpphigr', 'O3c_etabkgtpumpphigref', 'dI', 'dIall', 'dEta', 'dPhi_cor', 'dTpump_cor', 'dO3'],axis=1)

    if not bool_rscorrection:
        df = df.drop(['TboxK', 'SensorType', 'SolutionVolume', 'Cef', 'ibg', 'iB2', 'Tpump', 'Phip', 'Eta', 'dPhip',
                      'unc_cPH', 'unc_cPL', 'unc_Tpump',  'unc_alpha_o3', 'alpha_o3', 'stoich',
                      'unc_stoich',
                      'eta_c', 'unc_eta', 'unc_eta_c', 'iBc', 'unc_iBc', 'Tpump_cor', 'unc_Tpump_cor', 'deltat',
                      'unc_deltat', 'deltat_ppi',
                      'unc_deltat_ppi', 'TLab', 'ULab', 'Pground', 'x', 'psaturated', 'cPH', 'TLabK', 'cPL',
                      'Phip_ground',
                      'unc_Phip_ground', 'Cpf', 'unc_Cpf', 'Phip_cor', 'unc_Phip_cor', 'O3c', 'O3_nc', 'O3c_eta',
                      'O3c_etabkg',
                      'O3c_etabkgtpump', 'O3c_etabkgtpumpphigr', 'O3c_etabkgtpumpphigref', 'dI', 'dIall', 'dEta',
                      'dPhi_cor', 'dTpump_cor', 'dO3'], axis=1)


    df.to_hdf(path + '/DQA/' + date_out + "_o3sdqa_rs80.hdf", key = 'df')

dfall = pd.concat(metadata, ignore_index=True)

name_out = 'Madrid_Metada_DQA_rs80'

dfall.to_csv(path + "DQA/" + name_out + ".csv")
dfall.to_hdf(path + "DQA/" + name_out + ".h5", key = 'df')