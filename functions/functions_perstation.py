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

def station_inone(st_name):

    if st_name == 'madrid':
        pathf = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'
        dfmetaf = pd.read_csv(pathf + 'Madrid_Metadata.csv')  #
        allFilesf = sorted(glob.glob(pathf + "CSV/out/*hdf"))
        roc_table_filef = ('/home/poyraden/Analysis/Homogenization_public/Files/sonde_madrid_roc.txt')
        dfmetaf = organize_madrid(dfmetaf)

    if st_name == 'lauder':
        pathf = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/'
        dfmetaf = pd.read_csv(pathf + 'metadata/Lauder_MetadaAll.csv')  #
        allFilesf = sorted(glob.glob(pathf + "CSV/*hdf"))
        roc_table_filef = ('/home/poyraden/Analysis/Homogenization_public/Files/sonde_lauder_roc.txt')
        dfmetaf = organize_lauder(dfmetaf)

    if st_name == 'uccle':
        pathf = '/home/poyraden/Analysis/Homogenization_public/Files/uccle/'
        dfmetaf = pd.read_csv(pathf + 'Raw_upd/All_metadata.csv')
        allFilesf = sorted(glob.glob(pathf + "/Raw_upd/*hdf"))
        roc_table_filef = ('/home/poyraden/Analysis/Homogenization_public/Files/sonde_uccle_roc.txt')
        dfmetaf = organize_uccle(dfmetaf)

    if st_name == 'scoresbysund':
        pathf = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'
        dfmetaf = pd.read_csv(pathf + 'metadata/Scoresby_MetadaAll.csv')
        allFilesf = sorted(glob.glob(pathf + "/Current/*sc03*hdf"))
        roc_table_filef = ('/home/poyraden/Analysis/Homogenization_public/Files/sonde_scoresbysund_roc.txt')
        dfmetaf = organize_scoresby(dfmetaf)

    return pathf, allFilesf, roc_table_filef, dfmetaf


def station_inbool(st_name):

    if st_name == 'madrid':
        humidity_correctionf = True
        df_missing_tpumpf = True  # if there are missing variables in df like tpump in madrid
        calculate_currentf = True
        organize_dff = True
        descent_dataf = False

    if st_name == 'lauder':
        humidity_correctionf = True
        df_missing_tpumpf = False  # if there are missing variables in df like tpump in madrid
        calculate_currentf = False
        organize_dff = True
        descent_dataf = True

    if st_name == 'uccle':
        humidity_correctionf = False
        df_missing_tpumpf = False  # if there are missing variables in df like tpump in madrid
        calculate_currentf = False
        organize_dff = True
        descent_dataf = True

    if st_name == 'scoresbysund':
        humidity_correctionf = True
        df_missing_tpumpf = False  # if there are missing variables in df like tpump in madrid
        calculate_currentf = False
        organize_dff = True
        descent_dataf = False


    return humidity_correctionf, df_missing_tpumpf, calculate_currentf, organize_dff, descent_dataf

def station_invar(st_name):

    if st_name == 'madrid':
        date_start_homf = '' # the date when the homogenization starts, there is a continue statement in the main loop for the dates before this date, "may not be needed always"
        rs80_beginf = '' # the date where there was a change from nors80
        rs80_endf = ''
        IBGsplitf = '2004'  # the date if there is a lower/higher bkg value region
        sonde_tbcf = 'SPC10'

    if st_name == 'lauder':
        date_start_homf = '19941012'  # the date when the homogenization starts, there is a continue statement in the main loop for the dates before this date, "may not be needed always"
        rs80_beginf = '19890101'  # the date where there was a change from nors80
        rs80_endf = '20070501'
        IBGsplitf = '1996'  # the date if there is a lower/higher bkg value region
        sonde_tbcf = 'ENSCI05'

    if st_name == 'uccle':
        date_start_homf = '19961001'  # the date when the homogenization starts, there is a continue statement in the main loop for the dates before this date, "may not be needed always"
        rs80_beginf = '20070901'  # the date where there was a change from nors80
        rs80_endf = '20070901'
        IBGsplitf = '2008'  # the date if there is a lower/higher bkg value region
        sonde_tbcf = 'ENSCI05'

    if st_name == 'scoresbysund':
        date_start_homf = '19961001'  # the date when the homogenization starts, there is a continue statement in the main loop for the dates before this date, "may not be needed always"
        rs80_beginf = '19890208'  # the date where there was a change from nors80
        rs80_endf = '20070104'
        # IBGsplitf = '2008'  # the date if there is a lower/higher bkg value region
        IBGsplitf = ''  # the date if there is a lower/higher bkg value region

        sonde_tbcf = 'ENSCI05'

    return date_start_homf, IBGsplitf, sonde_tbcf, rs80_beginf, rs80_endf


def organize_uccle(dum):


    dum['string_bkg_used'] = 'ib0'

    dum.loc[dum.Datenf.isnull() == 1,'DateTime'] = dum.loc[dum.Datenf.isnull() == 1,'Date']



    dum['Date'] = pd.to_datetime(dum['DateTime'], format='%Y-%m-%d %H:%M:%S')
    dum['Date'] = dum['Date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))

    dum['unc_cPH'] = 0
    dum['unc_cPL'] = 0

    dum.loc[dum.iB0 == -1, 'iB0'] = 0

    dum.loc[dum.Date <= '19981201', 'string_pump_location'] = 'case3'
    dum.loc[dum.Date > '19981201', 'string_pump_location'] = 'case5'

    dum['TLab'] = 20

    dum['SensorType'] = 'DMT-Z'
    dum['SolutionConcentration'] = 5.0

    dum['iB2'] = dum['iB0']

    return dum


def organize_madrid(dmm):

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

def organize_scoresby(dms):

    dms['Date2'] = pd.to_datetime(dms['Date'], format='%Y-%m-%d')
    dms['Date2'] = dms['Date2'].dt.date
    dms['DateTime2'] = pd.to_datetime(dms['Date2'], format='%Y-%m-%d')

    dms['DateTime'] = pd.to_datetime(dms['Date'], format='%Y%m%d')
    dms['Date'] = dms['DateTime'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))


    dms['PLab'] = dms['Pground']
    dms['string_bkg_used'] = 'ib2'

    dms['string_pump_location'] = 'case0'
    dms.loc[dms['SerialECC'].str.contains("4a", case=False), 'string_pump_location'] = 'case1'
    dms.loc[dms['SerialECC'].str.contains("5a", case=False), 'string_pump_location'] = 'case3'
    dms.loc[dms['SerialECC'].str.contains("6a", case=False), 'string_pump_location'] = 'case5'
    dms.loc[dms['SerialECC'].str.contains("Z", case=False), 'string_pump_location'] = 'case5'



    # part related with missing ptupf
    date_missing_p = '2009-12-31'
    date_missing_t = '2000-10-06'
    date_missing_u = '2010-10-06'
    # date_missing_pf = '2020-11-18'

    plab = missing_station_values(dms, 'PLab', False, 'nan')
    tlab = missing_station_values(dms, 'TLab', False, 'nan')
    ulab = missing_station_values(dms, 'ULab', False, 'nan')
    pflab = [0]

    dms.loc[dms.Date > date_missing_p, 'PLab'] = \
        dms.loc[dms.Date > date_missing_p, 'DateTime2'].dt.month.apply(lambda x: plab[x - 1])

    dms = assign_missing_ptupf(dms, False, True, True, False, date_missing_p, date_missing_t, date_missing_u,
                               date_missing_u, plab, tlab, ulab, pflab)
    #there are also some values where OTU are missing:
    dms.loc[dms.PLab == 1000, 'PLab'] = \
        dms.loc[dms.PLab == 1000, 'DateTime2'].dt.month.apply(lambda x: plab[x - 1])
    dms.loc[dms.TLab == 99.9, 'TLab'] = \
        dms.loc[dms.TLab == 99.9, 'DateTime2'].dt.month.apply(lambda x: tlab[x - 1])
    dms.loc[dms.ULab == 999, 'ULab'] = \
        dms.loc[dms.ULab == 999, 'DateTime2'].dt.month.apply(lambda x: ulab[x - 1])


    #fix the values whwre soleution concentraiton is 3, should be 10 (I assume, no answer from PI yet)
    dms.loc[dms.SolutionConcentration == 3, 'SolutionConcentration'] = 10

    return dms

def organize_lauder(dfl):

    # path = '/home/poyraden/Analysis/Homogenization_public/Files/lauder/'
    # dfmeta = pd.read_csv(path + 'metadata/Lauder_MetadaAll.csv')  #
    # allFiles = sorted(glob.glob(path + "CSV/*hdf"))
    # print('All Files:', len(allFiles))
    # roc_table_file = ('/home/poyraden/Analysis/Homogenization_public/Files/sonde_lauder_roc.txt')
    # roc_plevel = 10  # pressure value to obtain roc
    
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

    #to skip some bad files
    skip_function = 'False'
    return_string = 'fine'
    if ((datevalue == '20020725') | (datevalue == '20050124') | (datevalue == '20191216') | (datevalue == '20190524') | (datevalue == '20190528')) & (station == 'lauder'):
        skip_function = 'True'
        return_string = 'stop'

    if ((datevalue == '20140604') | (datevalue == '20140402') | (datevalue == '20210428')) & (station == 'madrid'):
        skip_function = 'True'
        return_string = 'stop'


    if ((datevalue == '20070525') | (datevalue == '20070629') | (datevalue == '20070702') | (datevalue == '20070706')  | (datevalue == '20070709')
        | (datevalue == '20070711') | (datevalue == '20070716') | (datevalue == '20070718')    ) & (station == 'uccle'):
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
            dl['iB2'] = dml.at[dml.first_valid_index(),'iB2']
            dl['Height'] = dl['Alt']

    if station == 'madrid':
        dl = rename_variables(dl,['Pressure','O3PartialPressure','SampleTemperature'], ['Pair','O3','Tpump'])


    if station == 'uccle':
        #to remove some bad values in the df
        dl['fix'] = 'fix'
        if dl.I.dtypes == dl.fix.dtypes:
            dl['bad_I'] = dl['I'].apply(lambda x: True if type(x) == type(None) else False)
            dl = dl.drop(dl.index[dl['bad_I'] == 1], inplace=False)
            dl['drop_two'] = dl['I'].apply(lambda x: True if len(x) > 6 else False)
            dl = dl.drop(dl.index[dl['drop_two'] == 1], inplace=False)
            dl = dl.reset_index()
            dl['I'] = dl.I.astype(float)

        dl['O3'] = dl['PO3_dqar']
        dl['TboxK'] = dl['Tbox'] + k
        # input variables for hom.
        dl['Tpump'] = dl['Tbox'] + k
        dl['iB0'] = dml.at[dml.first_valid_index(), 'iB0']
        dl['Pair'] = dl['P']
        dl['TLab'] = 20
        dl['iB2'] = dml.at[dml.first_valid_index(), 'iB0']

    if station == 'scoresbysund':
        dl = rename_variables(dl,['Tbox'], ['TboxK'])


    return return_string, dl