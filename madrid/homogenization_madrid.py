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
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency,return_phipcor, \
    RS_pressurecorrection, o3_integrate, o3tocurrent, ComputeCef

from functions.df_filter import filter_data, filter_metadata


k = 273.15

# to calculate climatalogical means
path = '/mnt/HDS_OZONESONDES/DQA_Homogenization_Files/madrid/'
#
allFiles = sorted(glob.glob(path + "CSV/out/*.hdf"))
#
# listall = []
#
# for (filename) in (allFiles):
#     df = pd.read_hdf(filename)
#     print(filename)
#
#     listall.append(df)
#
# name_out = 'Madrid_AllData_woudc'
# dfall = pd.concat(listall, ignore_index=True)
#
# dfall.to_hdf(path + "DQA_nors80/" + name_out + ".hdf", key = 'df')

dfmain = pd.read_hdf("/mnt/HDS_OZONESONDES/DQA_Homogenization_Files/madrid/Madrid_AllData_woudc.hdf")

df = dfmain[['Date', 'Pressure', 'SampleTemperature']]
df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df = df[df.DateTime < '2007']

dfmean = {}
for i in range(1,13):
    dfmean[i-1] = df[df.DateTime.dt.month == i]
    dfmean[i-1] = dfmean[i-1].groupby(['Pressure']).mean()


dfmeta = pd.read_csv("/home/roeland/group/DQA_Homogenization/Files/madrid/Madrid_Metadata.csv")
# dfmeta = dfmeta[dfmeta.DateTime > '1994-01-01'] # start from 1994, because before there are no background values
dfmeta = dfmeta.reset_index()
dfmeta['Date'] = dfmeta['DateTime'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
dfmeta['Date2'] = dfmeta['Date'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))

dfmeta['Pground'] = dfmeta['PLab']
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
table = pd.read_csv('/home/roeland/group/DQA_Homogenization/Files/sonde_madrid_roc.txt',  skiprows=1, sep="\s *", names = clms,  header=None)
# take roc at 10hpa values
table = table[table.index ==10]
# assign ROC values to dfmeta
dfmeta['datetmp'] = dfmeta['DateTime'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
dfmeta['ROC'] = 0
for i in range(1,13):
    dfmeta.loc[dfmeta.datetmp.dt.month == i, 'ROC'] = table[i].tolist()[0]




# dfmeta = filter_metadata(dfmeta)

series = dfmeta[['DateTime', 'PLab', 'TLab','ULab','PF']]
# series['Date'] = series['DateTime'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
series['Date'] = pd.to_datetime(series['DateTime'], format='%Y-%m-%d %H:%M:%S')

# df['DataFrame Column'] = pd.to_datetime(df['DataFrame Column'], format=specify your format)
series = series.set_index('Date')
upsampled = series.resample('1M').mean()

plab = [0] * 12
tlab = [0] * 12
ulab = [0] * 12
pf = [0] * 12

dates_missingtpump = ['']

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
print('pf', np.nanmean(dfmeta.PF))
PFmean = np.nanmean(dfmeta.PF)

# allFiles = sorted(glob.glob(path + "CSV/out/19950111*.hdf"))

allFiles = sorted(glob.glob("/mnt/HDS_OZONESONDES/DQA_Homogenization_Files/madrid/CSV/out/*.hdf"))

metadata = []


for (filename) in (allFiles):
    file = open(filename, 'r')

    print(filename)


    df = pd.read_hdf(filename)

    # if df.at[df.first_valid_index(),'Date'] < '1998-03-01': continue
    if df.at[df.first_valid_index(),'Date'] == '2011-04-06': continue
    if df.at[df.first_valid_index(),'Date'] == '2014-06-04': continue
    if df.at[df.first_valid_index(),'Date'] == '2014-04-02': continue

    # if df.at[df.first_valid_index(),'Date'] == '2021-04-28': continue


    # print('df', df.dtypes, df['Date'][0:3])
    date = datetime.strptime(df.at[df.first_valid_index(),'Date'], '%Y-%m-%d')
    date2 = datetime.strftime(date, '%Y-%m-%d')
    date_out = datetime.strftime(date, '%Y%m%d')

    dfm = dfmeta[dfmeta.Date2 == date2]
    dfm = dfm.reset_index()

    # print(dfm.dtypes)

    # if df.at[df.first_valid_index(),'Date'] > '2006-01-01': continue # no bkg values

    df['Pair'] = df['Pressure']
    df['O3'] = df['O3PartialPressure']
    df['SampleTemperature_gen'] = 0

    # if the pump temp is missing use the interpolated climatological mean:
    df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    df.loc[df['SampleTemperature'].isnull(), 'value_is_NaN'] = 1
    df.loc[df['SampleTemperature'].notnull(), 'value_is_NaN'] = 0

    # print(df[df.value_is_NaN == 'Yes'][['Pressure','Date', 'I', 'SampleTemperature']])
    pair_missing = df[df.value_is_NaN == 1].Pressure.tolist()

    # print('missing temp len' , len(pair_missing))
    if len(pair_missing) > 1000:
        month_index = df['DateTime'].dt.month.tolist()[0]
        # print('no sample temperature', month_index, len(pair_missing), len(df))
        x = dfmean[month_index - 1]['SampleTemperature'].tolist()
        y = dfmean[month_index - 1].index.tolist()
        fb = interp1d(y, x)
        df_pair = df[df.value_is_NaN == 1].Pressure.tolist()
        if min(df_pair) < min(y):
            df_pair = df[(df.value_is_NaN == 1) & df.Pressure >= min(y)].Pressure.tolist()
            df_samptemp = fb(df_pair)
            df.loc[(df.value_is_NaN == 1) & df.Pressure >= min(y), 'SampleTemperature'] = df_samptemp

        elif max(df_pair) > max(y):
            df_pair = df[(df.value_is_NaN == 1) & (df.Pressure < max(y))].Pressure.tolist()
            df_samptemp = fb(df_pair)
            df.loc[(df.value_is_NaN == 1) & (df.Pressure < max(y)), 'SampleTemperature'] = df_samptemp

        else:
            df_pair = df[(df.value_is_NaN == 1)].Pressure.tolist()
            fb = interp1d(y, x)
            df_samptemp = fb(df_pair)
            df.loc[df.value_is_NaN == 1, 'SampleTemperature'] = df_samptemp
            df.loc[df.value_is_NaN == 1, 'SampleTemperature_gen'] = df_samptemp
        #
    if (len(pair_missing) < 1000) & (len(pair_missing) > 50):
        print('no sample temperature', len(pair_missing), len(df))

        x = df[df.value_is_NaN == 0]['SampleTemperature'].tolist()
        y = df[df.value_is_NaN == 0]['Pressure'].tolist()
        fb = interp1d(y, x)
        df_pair = df[df.value_is_NaN == 1].Pressure.tolist()

        if min(df_pair) < min(y):
            df_pair = df[(df.value_is_NaN == 1) & (df.Pressure >= min(y))].Pressure.tolist()
            df_samptemp = fb(df_pair)
            df.loc[(df.value_is_NaN == 1) & (df.Pressure >= min(y)), 'SampleTemperature'] = df_samptemp

        elif max(df_pair) > max(y):
            df_pair = df[(df.value_is_NaN == 1) & (df.Pressure < max(y))].Pressure.tolist()
            df_samptemp = fb(df_pair)
            df.loc[(df.value_is_NaN == 1) & (df.Pressure < max(y)), 'SampleTemperature'] = df_samptemp

        else:
            df_pair = df[(df.value_is_NaN == 1)].Pressure.tolist()
            fb = interp1d(y, x)
            df_samptemp = fb(df_pair)

            df.loc[df.value_is_NaN == 1, 'SampleTemperature'] = df_samptemp
            df.loc[df.value_is_NaN == 1, 'SampleTemperature_gen'] = df_samptemp


    df['TboxK'] = df['SampleTemperature'] + k


    if df.at[df.first_valid_index(),'Date'] < '2006-02-26':
        dfm.at[0,'TLab'] = tlab[date.month-1]
        dfm.at[0,'Pground'] = plab[date.month-1]
        dfm.at[0,'PLab'] = plab[date.month-1]


    if df.at[df.first_valid_index(),'Date'] < '2020-11-18':
        dfm.at[0, 'ULab'] = ulab[date.month-1]

    # if df.at[df.first_valid_index(),'Date'] < '2019-01-01': continue # no bkg values



    # to deal with data that is not complete
    # if PF is missing use the mean value of PF
    if (len(df) < 100): continue
    if (math.isnan(dfm.at[dfm.first_valid_index(), 'PF'])):
        dfm.at[dfm.first_valid_index(), 'PF'] = PFmean

    #calculate current from PO3
    dfm['SolutionConcentration'] = 10
    df['SensorType'] = 'SPC'
    df['SolutionVolume'] = 3.0
    dfm['SensorType'] = 'SPC'
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
    if len(pair_missing) > 1000:
        df['unc_Tpump'] = 1

    # serial_ecc = dfm.at[dfm.first_valid_index(), 'SerialECC']
    # string_pump_location = str(dfmeta.at[dfmeta.first_valid_index(), 'PumpTempLoc'])
    # infor from station pi
    if date2 < '1998-12-02':
        string_pump_location = 'case3'
    if date2 >= '1998-12-02':
        string_pump_location = 'InternalPump'

        #      radiosonde RS80 correction   #
    bool_rscorrection = False
    # rsmodel = ''
    # bool_rscorrection = ''
    # if date2 <= '2006-03-01':
    #     # rsmodel = 'RS80'
    #     bool_rscorrection = True
    # if date2 >= '2006-03-08 ':
    #     bool_rscorrection = False
    #
    # if bool_rscorrection:
    #     df['Crs'], df['unc_Crs'] = RS_pressurecorrection(df, 'GPHeight', rsmodel)
    #     df['Pair'] = df['Pair'] - df['Crs']

    df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair', 3.0)
    # correction to the metadata from the station PI:
    # All z-sondes before so06020112 were flown with 1 %KI
    dfm['SolutionConcentration'] = 10
    df['SensorType'] = 'SPC'
    df['SolutionVolume'] = 3.0
    dfm['SensorType'] = 'SPC'

    df['stoich'], df['unc_stoich'] = stoichmetry_conversion(df, 'Pair', dfm.at[dfm.first_valid_index(), 'SensorType'],
                                                            dfm.at[dfm.first_valid_index(), 'SolutionConcentration'],
                                                            'SPC10')
    # print('stoich', df.at[df.first_valid_index(),'stoich'])
    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    IBGsplit = '2004'
    df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2', IBGsplit)
    df['iB2'] = dfm.at[dfm.first_valid_index(), 'iB2']
    # print('corrected ibc', df.at[df.first_valid_index(), 'iBc'] )

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
    df['Cef'] = ComputeCef(df, dfm)
    df['Phip_eff'], df['unc_Phip_eff'] = return_phipcor(df, 'Phip', 'dPhip', 'Cef', 'unc_Cpf')

    # all corrections
    df['O3_nc'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'Eta', 'Phip', False)
    df['O3c_eta'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'eta_c', 'Phip', False)
    df['O3c_etabkg'] = currenttopo3(df, 'I', 'Tpump', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpump'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip', False)
    df['O3c_etabkgtpumpphigr'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_ground', False)
    df['O3c_etabkgtpumpphigref'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor', False)
    df['O3c'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor', False)
    df['O3c_woudc'] = currenttopo3(df, 'I', 'Tpump', 'ibg', 'Eta', 'Phip_eff', False)
    df['O3c_woudc_v2'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'Eta', 'Phip_eff', False)

    if len(df[df['O3c'] < 0]) > 0: print('why', filename)

    # uncertainities
    df['dI'] = 0
    df.loc[df.I < 1, 'dI'] = 0.01
    df.loc[df.I >= 1, 'dI'] = 0.01 * df.loc[df.I > 1, 'I']
    df['dIall'] = (df['dI'] ** 2 + df['unc_iBc'] ** 2) / (df['I'] - df['iBc']) ** 2
    df['dEta'] = (df['unc_eta_c'] / df['eta_c']) ** 2
    df['dPhi_cor'] = (df['unc_Phip_cor'] / df['Phip_cor']) ** 2
    #df['dTpump_cor'] = (df['unc_Tpump_cor'] / df['Tpump_cor']) ** 2

    # final uncertainity on O3
    df['dO3'] = np.sqrt(df['dIall'] + df['dEta'] + df['dPhi_cor'] + df['unc_Tpump_cor'])

    #part for TON
    # print('min Pair', df.Pair.min())

    dfm['O3Sonde_burst'] = o3_integrate(df, 'O3')
    dfm['O3Sonde_burst_raw'] = o3_integrate(df, 'O3_nc')

    dfm['O3Sonde_hom_burst'] = o3_integrate(df, 'O3c')
    dfm['O3Sonde_burst_eta'] = o3_integrate(df, 'O3c_eta')

    dfm['O3Sonde_burst_etabkg'] = o3_integrate(df, 'O3c_etabkg')
    dfm['O3Sonde_burst_etabkgtpump'] = o3_integrate(df, 'O3c_etabkgtpump')
    dfm['O3Sonde_burst_etabkgtpumpphigr'] = o3_integrate(df, 'O3c_etabkgtpumpphigr')
    dfm['O3Sonde_burst_etabkgtpumpphigref'] = o3_integrate(df, 'O3c_etabkgtpumpphigref')

    dfm['burst'] = df.Pair.min()

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

        dfm['O3Sonde_10hpa'] = o3_integrate(dft, 'O3')
        dfm['O3Sonde_10hpa_raw'] = o3_integrate(dft, 'O3_nc')

        dfm['O3Sonde_hom_10hpa'] = o3_integrate(dft, 'O3c')
        dfm['O3Sonde_10hpa_eta'] = o3_integrate(dft, 'O3c_eta')
        dfm['O3Sonde_10hpa_etabkg'] = o3_integrate(dft, 'O3c_etabkg')
        dfm['O3Sonde_10hpa_etabkgtpump'] = o3_integrate(dft, 'O3c_etabkgtpump')
        dfm['O3Sonde_10hpa_etabkgtpumpphigr'] = o3_integrate(dft, 'O3c_etabkgtpumpphigr')
        dfm['O3Sonde_10hpa_etabkgtpumpphigref'] = o3_integrate(dft, 'O3c_etabkgtpumpphigref')

        # print('o3sonde', dfm[['O3Sonde', 'O3Sonde_hom']])


    if df.Pair.min () > 10:
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

        # print('o3sonde', dfm[['O3Sonde', 'O3Sonde_hom']])



    dfm['iBc'] = df.at[df.first_valid_index(), 'iBc']

    dfm.to_csv(path + '/DQA_nors80/'+ date_out + "_o3smetadata_nors80.csv")

    metadata.append(dfm)


    df.to_hdf(path + '/DQA_nors80/' + date_out + "_all_hom_nors80.hdf", key = 'df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']

    if bool_rscorrection:

        df = df.drop(['TboxK', 'SensorType', 'SolutionVolume', 'Cef', 'ibg', 'iB2', 'Tpump', 'Phip', 'Eta', 'dPhip',
                      'unc_cPH', 'unc_cPL', 'unc_Tpump', 'Crs', 'unc_Crs', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich',
                      'eta_c', 'unc_eta', 'unc_eta_c', 'iBc', 'unc_iBc', 'Tpump_cor', 'unc_Tpump_cor', 'deltat', 'unc_deltat', 'deltat_ppi',
                      'unc_deltat_ppi', 'TLab', 'ULab', 'Pground', 'x', 'psaturated', 'cPH', 'TLabK', 'cPL', 'Phip_ground',
                      'unc_Phip_ground', 'Cpf', 'unc_Cpf', 'Phip_cor', 'unc_Phip_cor', 'O3c', 'O3_nc', 'O3c_eta', 'O3c_etabkg',
                      'O3c_etabkgtpump', 'O3c_etabkgtpumpphigr', 'O3c_etabkgtpumpphigref', 'dI', 'dIall', 'dEta', 'dPhi_cor', 'Un_Tpump_cor'],axis=1)

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
                      'dPhi_cor', 'unc_Tpump_cor'], axis=1)


    df.to_hdf(path + '/DQA_nors80/' + date_out + "_o3sdqa_nors80.hdf", key = 'df')

# dfall = pd.concat(metadata, ignore_index=True)
#
# name_out = 'Madrid_Metada_DQA_nors80_nors80'
#
# dfall.to_csv(path + "DQA_nors80/" + name_out + ".csv")
# dfall.to_hdf(path + "DQA_nors80/" + name_out + ".h5", key = 'df')
#
# print('missing tpump dates', dates_missingtpump)