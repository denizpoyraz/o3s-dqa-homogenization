import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from re import search
from scipy.interpolate import interp1d

from functions.homogenization_functions import absorption_efficiency, stoichmetry_conversion, conversion_efficiency, \
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency, \
    return_phipcor, o3_integrate, roc_values, missing_station_values, assign_missing_ptupf, make_1m_upsamle
import glob

K = 273.15
k = 273.15

def make_madrid_maindl(path):

    # path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'

    allFiles = sorted(glob.glob(path + "CSV/out/*.hdf"))

    #
    listall = []

    for (filename) in (allFiles):
        df = pd.read_hdf(filename)
        print(filename)

        listall.append(df)

    name_out = 'Madrid_AllData_woudc'
    dfall = pd.concat(listall, ignore_index=True)

    dfall.to_hdf(path + "DQA_nors80/" + name_out + ".hdf", key = 'df')


def madrid_missing_tpump(dfmainf):

    #use it for one time only
    # make_madrid_maindf

    # dfmain = pd.read_hdf(
    #     "/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Madrid_AllData_woudc.hdf")

    dft = dfmainf[['Date', 'Pressure', 'SampleTemperature']].copy()
    dft = dft[dft.SampleTemperature.isnull() == 0]
    dft['DateTime'] = pd.to_datetime(dft['Date'], format='%Y-%m-%d')
    dft = dft[dft.DateTime < '2007']

    dfmean = {}
    for i in range(1, 13):
        dfmean[i - 1] = dft[dft.DateTime.dt.month == i]
        dfmean[i - 1] = dfmean[i - 1].groupby(['Pressure']).median()


    return dfmean

def organize_madrid(dmm):
    # path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
    # #
    # allFiles = sorted(glob.glob(path + "CSV/out/*MD2*.hdf"))
    # print('All Files:', len(allFiles))
    # dfl = pd.read_csv(path + 'Madrid_Metadata.csv')
    # roc_table_file = ('/home/poyraden/Analysis/Homogenization_public/Files/sonde_madrid_roc.txt')
    # IBGsplit = '2004'
    # sonde_tbc = 'SPC10'
    #
    # humidity_correction = True
    # # if there are missing variables in df like tpump in madrid
    # df_missing_tpump = True
    # if df_missing_tpump:
    #     dfmain = pd.read_hdf(
    #         "/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Madrid_AllData_woudc.hdf")
    #     dfmean = madrid_missing_tpump(dfmain)
    # # rename variables if needed
    # df_rename = True
    # # if current is not known and not in df
    # calculate_current = True
    #
    # if datestr == '20140604': continue
    # if datestr == '20140402': continue
    # if datestr == '20210428': continue


    for i in range(len(dmm)):
        try:
            dmm.at[i, 'BrewO3'] = float(dmm.at[i, 'BrewO3'])
        except ValueError:
            dmm.at[i, 'BrewO3'] = 0

    dmm['Date'] = dmm['DateTime'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
    dmm['Date'] = dmm['Date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))

    #specific for ulab, since there is not enough data the overall mean is used, not monthly
    ulab = [0] * 12
    updmm = make_1m_upsamle(dmm, 'ULab', False, 'nan')
    for i in range(1, 13):
        j = i - 1
        ulab[j] = updmm.mean()[0]

    PFmean = np.nanmean(dmm.PF)
    print('PFmean', PFmean)
    # dmm['PFmean'] = PFmean

    #part related with missing ptupf
    date_missing = '2006-02-26'
    date_missing_u = '2020-11-18'

    plab = missing_station_values(dmm, 'PLab', False, 'nan')
    tlab = missing_station_values(dmm, 'TLab', False, 'nan')
    pflab = missing_station_values(dmm, 'PF', False, 'nan')  # PF values are


    dmm = assign_missing_ptupf(dmm, True, True, False, False, date_missing, date_missing, date_missing_u,
                                  date_missing, plab, tlab, ulab, pflab)

    dmm['Date2'] = pd.to_datetime(dmm['Date'], format='%Y-%m-%d')
    dmm['Date2'] = dmm['Date2'].dt.date
    dmm['DateTime2'] = pd.to_datetime(dmm['Date2'], format='%Y-%m-%d')

    dmm.loc[dmm.DateTime <= '2020-11-18', 'ULab'] = \
        dmm.loc[dmm.DateTime <= '2020-11-18', 'DateTime2'].dt.month.apply(lambda x: ulab[0])




    dmm['SolutionConcentration'] = 10
    dmm['SensorType'] = 'SPC'
    dmm['SolutionVolume'] = 3.0

    #if PF is not valid, assign the mean of PF
    dmm['value_is_NaN'] = 0
    dmm.loc[dmm['PF'].isnull(), 'value_is_NaN'] = 1
    dmm.loc[dmm.value_is_NaN == 1, 'PF'] = PFmean

    dmm['string_bkg_used'] = 'ib2'

    dmm['string_pump_location'] = '0'

    dmm.loc[dmm.Date <= '19981202', 'string_pump_location'] = 'case3'
    dmm.loc[dmm.Date > '19981202', 'string_pump_location'] = 'case5'


    #since there are missing iB2 values, assign the corresponding mean to iB2
    # before and after ibg_split if it is nan
    dmm['bkg_tag'] = 'iB2'
    dmm.loc[(dmm['iB2'].isnull() == 1),'bkg_tag'] = 'mean'
    dmm.loc[(dmm['iB2'].isnull())== 0,'bkg_tag'] = 'iB2'

    mean_before = dmm[dmm.DateTime < '2004'].iB2.mean()
    mean_after = dmm[dmm.DateTime > '2004'].iB2.mean()

    dmm.loc[(dmm['iB2'].isnull()) & (dmm.DateTime < '2004'), 'iB2'] = mean_before
    dmm.loc[(dmm['iB2'].isnull()) & (dmm.DateTime > '2004'), 'iB2'] = mean_after




    return dmm

def rename_variables(dft, pvar, nvar):
    '''
    :param dft: input df
    :param pvar: previous names of the column name (an array of column names)
    :param nvar: new names of the column name
    :return dft:
    '''

    for i in range(len(pvar)):
        dft[nvar[i]] = dft[pvar[i]]

    return dft


def df_missing_variable(dft, dfmean):

    dft['unc_Tpump'] = 0.5

    dft['DateTime'] = pd.to_datetime(dft['Date'], format='%Y-%m-%d')


    dft.loc[dft['SampleTemperature'].isnull(), 'value_is_NaN'] = 1
    dft.loc[dft['SampleTemperature'].notnull(), 'value_is_NaN'] = 0

    # print(df[df.value_is_NaN == 'Yes'][['Pressure','Date', 'I', 'SampleTemperature']])
    pair_missing = dft[dft.value_is_NaN == 1].Pressure.tolist()

    # print('missing temp len' , len(pair_missing))

    if len(pair_missing) >= 1000:
        dft['unc_Tpump'] = 1 #a larger unc. due to interpolation
        month_index = dft['DateTime'].dt.month.tolist()[0]
        # print('no sample temperature', month_index, len(pair_missing), len(df))
        x = dfmean[month_index - 1]['SampleTemperature'].tolist()
        y = dfmean[month_index - 1].index.tolist()
        fb = interp1d(y, x)
        df_pair = dft[dft.value_is_NaN == 1].Pressure.tolist()
        # print('df_pair', df_pair)
        # print('x', x)
        # print('y', y)
        if min(df_pair) < min(y):
            df_pair = dft[(dft.value_is_NaN == 1) & (dft.Pressure >= min(y))].Pressure.tolist()
            df_samptemp = fb(df_pair)
            print('df_samptemp', len(df_samptemp))
            dft.loc[(dft.value_is_NaN == 1) & (dft.Pressure >= min(y)), 'SampleTemperature'] = df_samptemp
            dft.loc[(dft.value_is_NaN == 1) & (dft.Pressure < min(y)), 'SampleTemperature'] = np.NaN


        elif max(df_pair) > max(y):
            df_pair = dft[(dft.value_is_NaN == 1) & (dft.Pressure < max(y))].Pressure.tolist()
            df_samptemp = fb(df_pair)
            dft.loc[(dft.value_is_NaN == 1) & (dft.Pressure < max(y)), 'SampleTemperature'] = df_samptemp
            dft.loc[(dft.value_is_NaN == 1) & (dft.Pressure > max(y)), 'SampleTemperature'] = np.NaN

        else:
            df_pair = dft[(dft.value_is_NaN == 1)].Pressure.tolist()
            fb = interp1d(y, x)
            df_samptemp = fb(df_pair)
            dft.loc[dft.value_is_NaN == 1, 'SampleTemperature'] = df_samptemp
            dft.loc[dft.value_is_NaN == 1, 'SampleTemperature_gen'] = df_samptemp
        #
    if (len(pair_missing) < 1000) & (len(pair_missing) > 0):
        # print('no sample temperature', len(pair_missing), len(dft))


        x = dft[dft.value_is_NaN == 0]['SampleTemperature'].tolist()
        y = dft[dft.value_is_NaN == 0]['Pressure'].tolist()
        fb = interp1d(y, x)
        df_pair = dft[dft.value_is_NaN == 1].Pressure.tolist()

        if min(df_pair) < min(y):
            df_pair = dft[(dft.value_is_NaN == 1) & (dft.Pressure >= min(y))].Pressure.tolist()
            df_samptemp = fb(df_pair)
            dft.loc[(dft.value_is_NaN == 1) & (dft.Pressure >= min(y)), 'SampleTemperature'] = df_samptemp
            dft.loc[(dft.value_is_NaN == 1) & (dft.Pressure < min(y)), 'SampleTemperature'] = np.NaN


        elif max(df_pair) > max(y):
            df_pair = dft[(dft.value_is_NaN == 1) & (dft.Pressure < max(y))].Pressure.tolist()
            df_samptemp = fb(df_pair)
            dft.loc[(dft.value_is_NaN == 1) & (dft.Pressure < max(y)), 'SampleTemperature'] = df_samptemp
            dft.loc[(dft.value_is_NaN == 1) & (dft.Pressure > max(y)), 'SampleTemperature'] = np.NaN

        else:
            df_pair = dft[(dft.value_is_NaN == 1)].Pressure.tolist()
            fb = interp1d(y, x)
            df_samptemp = fb(df_pair)

            dft.loc[dft.value_is_NaN == 1, 'SampleTemperature'] = df_samptemp
            dft.loc[dft.value_is_NaN == 1, 'SampleTemperature_gen'] = df_samptemp

    dft['TboxK'] = dft['SampleTemperature'] + k

    return dft

def organize_sodankyla(dsm):

    # few variables needed in the homogenization code
    # date_start_hom = '19941012'
    # # the date if there is a lower/higher bkg value region
    # IBGsplit = '2005'
    # date_rs80 = '20051124'
    # sonde_tbc = 'ENSCI05'
    # path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
    # dfl = pd.read_hdf(path + 'Metadata/All_metadata.hdf')
    # allFiles = sorted(glob.glob(path + "Current/*961211*rawcurrent.hdf"))
    # roc_table_file = ('/home/poyraden/Analysis/Homogenization_public/Files/sonde_sodankyla_roc.txt')

    dsm = dsm[dsm.iB2 < 9]
    dsm = dsm[dsm.iB0 < 9]

    dsm['PLab'] = dsm['Pground']

    #part related with missing ptupf
    date_missing_p = '19970107'
    date_missing_t = '19981111'
    date_missing_u = '19981111'
    date_missing_pf = '19970107'

    plab = missing_station_values(dsm, 'PLab', False, 'nan')
    tlab = missing_station_values(dsm, 'TLab', False, 'nan')
    ulab = missing_station_values(dsm, 'ULab', False, 'nan')
    pflab = missing_station_values(dsm, 'PF', True, '20040101')  # PF values are

    print(pflab)

    dsm = assign_missing_ptupf(dsm, True, True, True, True, date_missing_p, date_missing_t, date_missing_u,
                                  date_missing_pf, plab, tlab, ulab, pflab)


    dsm['string_pump_location'] = '0'
    dsm.loc[dsm.Date <= '20001101', 'string_pump_location'] = 'case3'
    dsm.loc[dsm.Date > '20001101', 'string_pump_location'] = 'case5'


    dsm.loc[dsm['SolutionVolume'].isnull(), 'value_is_NaN'] = 1
    # dsm.loc[dsm['SolutionVolume'].notnull(), 'value_is_NaN'] = 0
    dsm.loc[dsm.value_is_NaN == 1, 'SolutionVolume'] = '3'
    dsm['SolutionVolume'] = dsm['SolutionVolume'].astype('float')

    dsm.loc[(dsm.Date < '20060201') & (dsm.at[0, 'SensorType'] == 'DMT-Z' ), 'SolutionConcentration'] = 10
    dsm.loc[(dsm.Date >= '20060201') & (dsm.at[0, 'SensorType'] == 'DMT-Z' ), 'SolutionConcentration'] = 5
    dsm.loc[(dsm.Date < '20060201') & (dsm.at[0, 'SensorType'] == 'SPC' ), 'SolutionConcentration'] = 10

    dsm['string_bkg_used'] = '999'
    dsm.loc[dsm.BkgUsed == 'Ibg1', 'string_bkg_used'] = 'ib0'
    dsm.loc[dsm.BkgUsed == 'Constant', 'string_bkg_used'] = 'ib2'


    dsm['TotalO3_Col2A'] = dsm['TotalO3_Col2A'].astype('float')

    return dsm


def organize_lauder(dfl):
    
    dfl.loc[dfl.TLab > k, 'TLab'] = dfl.loc[dfl.TLab > k, 'TLab'] - k
    dfl['PF'] = dfl['Phip']

    dfl['PLab'] = 970.2
    dfl['Pground'] = 970.2

    dfl['DateTime'] = pd.to_datetime(dfl['Date'], format='%Y-%m-%d')

    dfl['Date'] = dfl['DateTime'].dt.strftime('%Y%m%d')

    # ser = dfl[(dfl.TLab < 500) & (dfl.ULab < 99)]
    ser = dfl[(dfl.TLab < 500) ]

    # ser = dfl.copy()
    # part related with missing ptupf
    date_missing = '2014-02-05'

    plab = missing_station_values(ser, 'PLab', False, 'nan')
    tlab = missing_station_values(ser, 'TLab', False, 'nan')
    ulab = missing_station_values(ser, 'ULab', False, 'nan')
    pflab = missing_station_values(ser, 'PF', False, 'nan')  # PF values are

    dfl = assign_missing_ptupf(dfl, False, True, True, False, date_missing, date_missing, date_missing,
                               date_missing, plab, tlab, ulab, pflab)

    # clean some outliers
    dfl.loc[dfl.ULab > 100, 'ULab'] = np.mean(ulab)
    dfl.loc[dfl.TLab > 50, 'TLab'] = np.mean(tlab)

    dfl.loc[dfl.Date > '19861231','SolutionVolume'] = 3
    dfl.loc[dfl.Date <= '19861231','SolutionVolume'] = 2.5

    dfl['SensorType'] = dfl['SondeType']
    dfl['string_bkg_used'] = 'ib2'

    dfl['string_pump_location'] = 'nan'
    dfl.loc[dfl.Pump_loc == '4A','string_pump_location'] = 'case1'
    dfl.loc[dfl.Pump_loc == '5A','string_pump_location'] = 'case3'
    dfl.loc[dfl.Pump_loc == '6A','string_pump_location'] = 'case5'
    dfl.loc[dfl.Pump_loc == 'Z','string_pump_location'] = 'case5'


    dfl.loc[(dfl.Date > '20190101') & (dfl.Pump_loc == 'nan'),'string_pump_location'] = 'case5'
    dfl.loc[(dfl.Date > '20190101') & (dfl.Pump_loc.isnull()),'string_pump_location'] = 'case5'


    return dfl

def df_station(dl, datevalue, dml, station):

    skip_function = 'False'
    return_string = 'fine'
    if ((datevalue == '20020725') | (datevalue == '20050124') | (datevalue == '20191216') | (datevalue == '20190524') | (datevalue == '20190528')) & (station == 'lauder'):
        skip_function = 'True'
        return_string = 'stop'

    if skip_function == 'False':

        if station == 'lauder':
            # get rid of the commas
            dl = dl.replace(",", " ", regex=True)
            dl['Date'] = datevalue
            dl['Date'] = pd.to_datetime(dl['Date'], format='%Y%m%d').dt.date
            # convert dl (which is a str) to float
            dl[['Time', 'Press', 'Alt', 'Temp', 'RH', 'PO3', 'TPump', 'O3CellI', 'EvapCath', 'WindSp', 'WindDir', 'Lat', 'Lon',
                'RH1', 'RH2', 'GPSPres', 'GPSAlt', 'GPSTraw', 'GPSTcor', 'GPSRH']] = dl[
                ['Time', 'Press', 'Alt', 'Temp', 'RH', 'PO3', 'TPump', 'O3CellI', 'EvapCath', 'WindSp', 'WindDir', 'Lat', 'Lon',
                 'RH1', 'RH2', 'GPSPres', 'GPSAlt', 'GPSTraw', 'GPSTcor', 'GPSRH']].astype(float)

            dl['DateTime'] = pd.to_datetime(dl['Date'], format='%Y-%m-%d')

                # for O3 use PO3 from DQA processed by station
            dl['O3'] = dl['PO3']
            # input variables for hom.
            dl['Tpump'] = dl['TPump'].astype(float) + k
            dl['Eta'] = 1
            dl['Pair'] = dl['Press']
            dl['TboxK'] = dl['Tpump']
            dl['I'] = dl['O3CellI']
            dl['iB2'] = dml['iB2']
            dl['Height'] = dl['Alt']

    if station == 'madrid':
        dl = rename_variables(dl,['Pressure','O3PartialPressure'], ['Pair','O3'])


    return return_string, dl