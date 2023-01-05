import numpy as np
import pandas as pd
from datetime import datetime
from re import search
import glob
import woudc_extcsv

K = 273.15

pval = np.array([1000, 100, 50, 30, 20, 10, 7, 5, 3])
komhyr_86 = np.array([1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092, 1.124])  # SP Komhyr
komhyr_95 = np.array([1, 1.007, 1.018, 1.029, 1.041, 1.066, 1.087, 1.124, 1.241])  # ECC Komhyr


def util_func(df, a):
    '''
    :param df: metadata sf
    :param a: column name
    :return: the corresponding value of the column
    '''
    try:
        tmp = df.at[df.first_valid_index(), a]
        if search(",", str(tmp)):
            tmp = tmp.replace(',', '')
        return tmp
    except KeyError:
        return 9999


def make_summary(df, column_names):
    '''
    :param df:
    :param column_names:
    :return:
    '''

    field_summary = [util_func(df, i) for i in column_names]
    # print(field_summary)
    field_summary = ",".join(map(str, field_summary))
    # print(field_summary)

    return field_summary


def launch_time(sta, end):
    return str(sta) + ":" + str(end) + ":" "00"


def lt_condition(x):
    if len(x) == 1: return float(x) * 60 / 10
    if len(x) == 2: return float(x) * 60 / 100
    if len(x) == 3: return float(x) * 60 / 1000
    if len(x) == 4: return float(x) * 60 / 10000


def calculate_utcoffset(dfm):
    hour = str(dfm.at[0, 'LaunchTime'])[0:2]
    minute = str(dfm.at[0, 'LaunchTime'])[3:5]
    # print(dfm.at[0, 'LaunchTime'])
    # print(hour)
    # print(minute)
    # i know very bad way but works for utc offset
    try:
        utcoffset = (int(hour) * 60 + int(minute)) - (11 * 60 + 30)
        if (utcoffset > 0) and (utcoffset < 60):
            s_utc = str(utcoffset)
            if len(s_utc) == 1: s_utc = "0" + s_utc
            dfm['UTCOffset'] = "00:" + s_utc + ":00"
        if (utcoffset > 0) and (utcoffset >= 60):
            ho = int(utcoffset / 60.);
            s_ho = str(ho)
            mo = np.mod(utcoffset, 60);
            s_mo = str(mo)
            if len(s_ho) == 1: s_ho = "0" + s_ho
            if len(s_mo) == 1: s_mo = "0" + s_mo
            dfm['UTCOffset'] = s_ho + ":" + s_mo + ":00"

        if utcoffset < 0:
            utcoffset = -1 * utcoffset
            if utcoffset < 60:
                s_utc = str(utcoffset)
                if len(s_utc) == 1: s_utc = "0" + s_utc
                dfm['UTCOffset'] = "-00:" + s_utc + ":00"
            if utcoffset >= 60:
                ho = int(utcoffset / 60.);
                s_ho = str(ho)
                mo = np.mod(utcoffset, 60);
                s_mo = str(mo)
                if len(s_ho) == 1: s_ho = "0" + s_ho
                if len(s_mo) == 1: s_mo = "0" + s_mo
                dfm['UTCOffset'] = "-" + s_ho + ":" + s_mo + ":00"

    except (KeyError, ValueError):
        dfm['UTCOffset'] = "00:00:00"

    return dfm['UTCOffset']


def station_info(dfm, spi, sage, typ, id, sname, country, gawid):
    dfm['stationPI'] = spi
    dfm['agency'] = sage
    # platfrom related
    dfm['type'] = typ
    dfm['id'] = id
    dfm['name'] = sname
    dfm['country'] = country
    dfm['gaw_id'] = gawid

    return dfm


#### writing woudc file related functions:

def organize_df_woudc(df, sname):
    if sname == 'uccle':
        df['WindDir'] = df['Winddir']
        df['WindSp'] = df['Windv']

    if sname == 'madrid':
        df['Time'] = df['Duration']
        # df['Height'] = df['GPHeight']
        df['T'] = df['Temperature']
        df['U'] = df['RelativeHumidity']
        df['WindDir'] = df['WindDirection']
        df['WindSp'] = df['WindSpeed']

    if sname == 'lauder':
        df = df.drop(
            ['EvapCath', 'RH1', 'RH2', 'GPSTraw', 'GPSTcor', 'GPSRH',
             'TboxK', 'iB2', 'Tpump', 'Phip', 'Eta', 'dPhip', 'unc_cPH', 'unc_cPL', 'unc_Tpump', 'unc_alpha_o3',
             'alpha_o3', 'stoich',
             'unc_stoich', 'eta_c', 'unc_eta', 'unc_eta_c', 'iBc', 'unc_iBc', 'unc_Tpump_cor',
             'deltat', 'unc_deltat', 'deltat_ppi', 'unc_deltat_ppi', 'TLab', 'ULab', 'PLab', 'x',
             'psaturated', 'cPH', 'TLabK', 'cPL', 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf',
             'Phip_cor', 'unc_Phip_cor', 'O3', 'O3cor', 'O3_nc', 'O3c_eta', 'O3c_etabkg', 'O3c_etabkgtpump',
             'O3c_etabkgtpumpphigr', 'O3c_etabkgtpumpphigref', 'dI', 'dIall', 'dEta', 'dPhi_cor',
             'dTpump_cor'
             ], axis=1)

        df['Pair'] = df['Press']
        df['Height'] = df['Alt']
        df['U'] = df['RH']
        df['O3'] = df['O3c']
        df['T'] = round((df['Temp'] - K), 3)
        # df['']

        df = df.drop(['Press', 'Alt', 'Temp', 'RH', 'O3c'], axis=1)

    if sname == 'ny-aalesund':
        print(list(df))
        df['T'] = df['Temp']
        df['U'] = df['RH']

    if sname == 'valentia':
        df_names = ['Time', 'Height', 'Pair', 'T', 'U', 'Tbox', 'O3', 'I', 'dO3']
        df['Time'] = df['Duration']
        df['T'] = df['Temperature']
        df['Pair'] = df['Pressure']
        df['U'] = df['RelativeHumidity']

    return df


def organize_metadata_woudc(dfm, stationname):
    dfm['today'] = pd.to_datetime("today").strftime("%Y-%m-%d")
    dfm['version'] = '2.1.3'
    dfm['Name'] = 'ECC'
    dfm['CorrectionCode'] = 6

    if stationname == 'uccle':
        dfm = station_info(dfm, 'Roeland Van Malderen', 'RMIB', 'STN', '053', 'UCCLE', 'BEL', '6447')
        # instrument related
        dfm['Name'] = 'ECC';
        dfm['SensorType'] = 'Z'
        # location related
        dfm['latitude'] = '50.48';
        dfm['longitude'] = '4.21';
        dfm['height'] = '100'
        # timestamp
        dfm['test'] = dfm.at[0, 'LaunchTime']
        if dfm.at[0, 'test'] == 9999: dfm.at[0, 'test'] = 11.30
        dfm['test'] = dfm['test'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
        dfm['LaunchTime'] = dfm['test'].apply(lambda x: x.strftime('%H:%M:%S'))
        dfm['UTCOffset'] = calculate_utcoffset(dfm)
        dfm['RadiosondeSerial'] = dfm['mRadioSondeNr']

        # PREFLIGHT_SUMMARY
        if dfm.at[dfm.first_valid_index(), 'iB0'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
        dfm.at[
            dfm.first_valid_index(), 'iB0']
        if dfm.at[dfm.first_valid_index(), 'iB0'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
        dfm.at[
            dfm.first_valid_index(), 'iBc']
        dfm['SolutionType'] = '0.5%KIHalfBuffer'

        dfm['RadiosondeManufacturer'] = 'Vaisala'
        dfm['InterfaceManufacturer'] = 'Vaisala'
        if dfm.at[0, 'Datenf'] < 20070901:
            dfm['RadiosondeModel'] = 'RS80-A'
            dfm['InterfaceModel'] = 'OIF11'
        if (dfm.at[0, 'Datenf'] > 20070831) & (dfm.at[0, 'Datenf'] < 20160615):
            dfm['RadiosondeModel'] = 'RS92-SGP'
            dfm['InterfaceModel'] = 'OIF92'
        if dfm.at[0, 'Datenf'] > 20160615:
            dfm['RadiosondeModel'] = 'RS41-SGP'
            dfm['InterfaceModel'] = 'OIF411'
        if dfm.at[0, 'Datenf'] < 20170701:
            dfm['GroundEquipment'] = "KTU-2"
        if dfm.at[0, 'Datenf'] > 20170701:
            dfm['GroundEquipment'] = "KTU-3"

        if dfm.at[0, 'Datenf'] <= 20171027:
            dfm['O3Ref_Number'] = 16
            dfm['O3Ref_Model'] = 'MK-II'
        if (dfm.at[0, 'Datenf'] > 20171027) & (dfm.at[0, 'Datenf'] <= 20191028):
            dfm['O3Ref_Number'] = 178
            dfm['O3Ref_Model'] = 'MK-III'
        if (dfm.at[0, 'Datenf'] > 20191028) & (dfm.at[0, 'Datenf'] <= 20200116):
            dfm['O3Ref_Number'] = 16
            dfm['O3Ref_Model'] = 'MK-II'
        if (dfm.at[0, 'Datenf'] > 20200116) & (dfm.at[0, 'Datenf'] <= 20201209):
            dfm['O3Ref_Number'] = 178
            dfm['O3Ref_Model'] = 'MK-III'
        if (dfm.at[0, 'Datenf'] > 20201209) & (dfm.at[0, 'Datenf'] <= 20201215):
            dfm['O3Ref_Number'] = 16
            dfm['O3Ref_Model'] = 'MK-II'
        if dfm.at[0, 'Datenf'] > 20201215:
            dfm['O3Ref_Number'] = 178
            dfm['O3Ref_Model'] = 'MK-III'

        dfm['O3Ref_Version'] = 1;
        dfm['WLCode'] = 9;
        dfm['O3Ref_Name'] = 'Brewer';
        dfm['UTC_Mean'] = '12:00:00'
        dfm['LengthBG'] = 15
        dfm['CorrectionCode'] = 6;
        dfm['BackgroundCorrection'] = "constant_ib0"

        try:
            dfm['O3ratio_hom'] = round(dfm['TO_Brewer'] / dfm['O3SondeTotal_hom'], 3)
        except KeyError:
            dfm['O3ratio_hom'] = 9999

        try:
            dfm['O3ratio_hom'] = -dfm['O3ratio_hom']
        except KeyError:
            dfm['O3ratio_hom'] = 9999
        if dfm.at[dfm.first_valid_index(), 'iB0'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_ib0"
        if dfm.at[dfm.first_valid_index(), 'iB0'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_climatologicalmean_ib0"

    if stationname == 'madrid':
        # some of the metadata is read by madrid non-homogenized woudc files, and the other from processed
        # metafiles
        dfm_woudc = pd.read_csv(
            '/home/poyraden/Analysis/Homogenization_public/Files/madrid/CSV/out/Madrid_WOUDC_Metadata.csv')

        dfm['Date'] = pd.to_datetime(dfm['DateTime'], format='%Y-%m-%d')
        dfm['Datenf'] = dfm['Date'].apply(lambda x: x.strftime('%Y%m%d'))
        dfm['Datenf'] = dfm['Datenf'].astype('int')

        # data generation related
        dfm = station_info(dfm, 'Jose Luis Hernandez', 'AEMET', 'STN', '308', 'Madrid', 'ESP', 'MAD')
        # print(dfm.loc[0, 'DateTime'])
        dfmw = dfm_woudc[dfm_woudc['TIMESTAMP_Date'] == dfm.loc[0, 'DateTime']]
        dfmw = dfmw.reset_index()
        # print('dfmw',dfmw.loc[0, 'TIMESTAMP_Date'] )
        # instrument
        # INSTRUMENT
        dfm['Name'] = dfmw.loc[0, 'INSTRUMENT_Name']
        dfm['SensorType'] = dfmw.loc[0, 'INSTRUMENT_Model']
        dfm['SerialECC'] = dfmw.loc[0, 'INSTRUMENT_Number']
        # location
        dfm['latitude'] = '40.47';

        if dfm.at[0, 'Datenf'] <= 19970130:
            dfm['longitude'] = '-3.75';
            dfm['height'] = '640.0'
        if dfm.at[0, 'Datenf'] > 19970130:
            dfm['longitude'] = '-3.58';
            dfm['height'] = '631.0'
        # TIMESTAMP

        # dfm['UTCOffset'] = dfmw.at[0, 'TIMESTAMP_UTCOffset']
        dfm['Date'] = dfm['DateTime']
        dfm['LaunchTime'] = dfmw.loc[0, 'TIMESTAMP_Time']
        try:
            dfm['UTCOffset'] = calculate_utcoffset(dfm)
        except KeyError:
            dfm['UTCOffset'] = "+00:00:00"

        # # PREFLIGHT_SUMMARY
        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[dfm.first_valid_index(), 'iB2']
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[dfm.first_valid_index(), 'iBc']

        dfm['SolutionType'] = '1.0%KIFullBuffer'
        # radiosonde
        dfm['RadiosondeManufacturer'] = 'Vaisala'
        dfm['InterfaceManufacturer'] = 'Vaisala'

        # set radiosonde, interface nmber etc..
        if dfm.at[0, 'Datenf'] <= 20060301:
            dfm['RadiosondeModel'] = 'RS80'
            dfm['InterfaceModel'] = 'RSA-921'
        if (dfm.at[0, 'Datenf'] > 20060301) & (dfm.at[0, 'Datenf'] < 20180322):
            dfm['RadiosondeModel'] = 'RS92-SGPQ '
            dfm['InterfaceModel'] = 'RSA-921'
        if dfm.at[0, 'Datenf'] > 20180322:
            dfm['RadiosondeModel'] = 'RS41-SGP'
            dfm['InterfaceModel'] = 'RSA-411'

        dfm['O3Ref_Number'] = 186
        dfm['O3Ref_Model'] = 'MK-III'

        dfm['O3Ref_Version'] = 9999
        dfm['WLCode'] = 9999
        dfm['O3Ref_Name'] = 'Brewer'
        dfm['UTC_Mean'] = '12:00:00'
        dfm['TO_Brewer'] = dfm['BrewO3']

        # flight summary
        dfm['CorrectionCode'] = 6
        dfm['BackgroundCorrection'] = "constant_ib2"
        try:
            dfm['O3ratio_hom'] = round(dfm['BrewO3'] / dfm['O3SondeTotal_hom'], 3)
        except KeyError:
            dfm['O3ratio_hom'] = 9999

        try:
            dfm['O3ratio_hom'] = -dfm['O3ratio_hom']
        except KeyError:
            dfm['O3ratio_hom'] = 9999
        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_ib2"
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_climatologicalmean_ib2"

    if stationname == 'lauder':
        # data generation related
        dfm = station_info(dfm, 'Richard Querel', 'NIWA-LAU', 'STN', '256', 'Lauder', 'NZL', '93817')
        # INSTRUMENT
        dfm['Name'] = 'ECC'
        dfm['SensorType'] = dfm['Pump_loc']
        dfm['SerialECC'] = dfm['SondeSerial']
        # LOCATION
        dfm['latitude'] = '-45.044'
        dfm['longitude'] = '169.684'
        dfm['height'] = '370'
        # TIMESTAMP
        try:
            dfm['UTCOffset'] = calculate_utcoffset(dfm)
        except KeyError:
            dfm['UTCOffset'] = "00:00:00"
        # PREFLIGHT_SUMMARY
        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
        dfm.at[dfm.first_valid_index(), 'iB2']
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
        dfm.at[dfm.first_valid_index(), 'iBc']
        if dfm.at[0, 'SolutionConcentration'] == 10: dfm['SolutionType'] = '1.0%KIFullBuffer'
        if dfm.at[0, 'SolutionConcentration'] == 5: dfm['SolutionType'] = '0.5%KIHalfBuffer'
        # RADIOSONDE
        dfm['RadiosondeManufacturer'] = 'Vaisala'
        dfm['InterfaceManufacturer'] = 'Vaisala'
        dfm['CorrectionCode'] = 6

        try:
            dfm['O3ratio_hom'] = round(dfm['Dobson'] / dfm['O3SondeTotal_hom'], 2)
        except KeyError:
            dfm['O3ratio_hom'] = 9999
        try:
            dfm['O3ratio_hom'] = -dfm['O3ratio_hom']
        except KeyError:
            dfm['O3ratio_hom'] = 9999

        if dfm.at[dfm.first_valid_index(), 'BurstOzonePressure'] > 10: dfm['O3ratio_hom'] = 9999
        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_ib2"
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_climatologicalmean_ib2"
        dfm['TO_Brewer'] = dfm['Dobson']

    if stationname == 'ny-aalesund':
        dfm = station_info(dfm, 'Peter von der Gathen', 'AWI-NA', 'STN', '089', 'Ny-Aalesund', 'NOR', '01004')

        if pd.isna(dfm.at[0, 'LaunchTime']) == 1:
            try:
                minute = int(dfm.loc[0, 'MinuteLaunch'])
                sminute = str(minute)
                if len(str(minute)) == 1: sminute = '0' + str(minute)
                hour = int(dfm.loc[0, 'HourLaunch'])
                shour = str(hour)
                if len(str(hour)) == 1: shour = '0' + str(hour)
                dfm['LaunchTime_new'] = shour + ":" + sminute + ':00'
            except ValueError:
                shour = "11"
                sminute = "30"
                dfm['LaunchTime_new'] = shour + ":" + sminute + ':00'

        if pd.isna(dfm.at[0, 'LaunchTime']) == 0:
            if search(":", str(dfm.at[0, 'LaunchTime'])) == 1:
                print('apple')
                dfm['LaunchTime_new'] = dfm.at[0, 'LaunchTime']
            else:
                # search(":", str(dfm.at[0, 'LaunchTime'])) == 0:
                hour = int(dfm.at[0, 'LaunchTime'])
                minute = int(float('0' + str(dfm.at[0, 'LaunchTime'])[2:]) * 60)
                dfm['LaunchTime_new'] = str(hour) + ":" + str(minute) + ':00'

        dfm['LaunchTime'] = dfm.at[0, 'LaunchTime_new']
        print('after', dfm.at[0, 'LaunchTime'])
        dfm['O3Ref_Name'] = 'Brewer'
        dfm['latitude'] = '78.93'
        dfm['longitude'] = '11.95'
        dfm['height'] = '11'
        dfm['DateTime'] = dfm.at[0, 'DateTime2']

        try:
            dfm['UTCOffset'] = calculate_utcoffset(dfm)
        except KeyError:
            dfm['UTCOffset'] = '00:00:00'
        dfm['SerialECC'] = dfm['SondeSerial']

        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[dfm.first_valid_index(), 'iB2']
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[dfm.first_valid_index(), 'iBc']
        if dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 5.0: dfm['SolutionType'] = '0.5%KIHalfBuffer'
        if dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 10.0: dfm['SolutionType'] = '1.0%KIFullBuffer'

        if (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 5.0) & (
                dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 10.0) & \
                (dfm.at[0, 'SensorType'] == 'SPC'): dfm['SolutionType'] = '1.0%KIFullBuffer'

        dfm['SolutionVolume'] = 3.0
        dfm['RadiosondeManufacturer'] = 'Vaisala'
        dfm['InterfaceManufacturer'] = 'Vaisala'

        dfm['CorrectionCode'] = 6
        dfm['BackgroundCorrection'] = "constant_ib2"

        try:
            dfm['O3ratio_hom'] = round(dfm['TotalO3_Col2A'] / dfm['O3SondeTotal_hom'], 3)
        except KeyError:
            dfm['O3ratio_hom'] = 9999

        if dfm.at[0, 'BurstOzonePressure'] > 32:
            dfm['O3ratio_hom'] = 9999

        try:
            dfm['O3ratio_hom'] = -dfm['O3ratio_hom']
        except KeyError:
            dfm['O3ratio_hom'] = 9999

        try:
            if dfm.at[0, 'TotalO3_Col2A'] > 700: dfm['O3ratio_hom'] = 9999
        except KeyError:
            dfm['O3ratio_hom'] = 9999

        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_ib2"
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_climatologicalmean_ib2"

    if stationname == 'scoresby':
        dfm = station_info(dfm, 'Brnlund M.', 'DMI', 'STN', '406', 'Scoresbysund', 'GRL', 'SCB')

        if (len(str(dfm.loc[0, 'LaunchTime'])) == 2) | (len(str(dfm.loc[0, 'LaunchTime'])) == 1):
            dfm['LaunchTime_fx'] = str(dfm.loc[0, 'LaunchTime']) + ':00:00'

        if (len(str(dfm.loc[0, 'LaunchTime'])) > 2):
            dfm['test0'] = dfm['LaunchTime'].apply(lambda x: str(x).split('.')[0])
            dfm['test1'] = dfm['LaunchTime'].apply(lambda x: str(x).split('.')[1])
            dfm['test11'] = dfm['test1'].apply(lambda x: lt_condition(x))
            dfm['test11'] = dfm['test11'].apply(lambda x: str(x).split(".")[0])
            if len(dfm.loc[0, 'test11']) == 1: dfm['test11'] = '0' + dfm['test11']
            dfm['LaunchTime_fx'] = dfm.apply(lambda x: launch_time(x.test0, x.test11), axis=1)
        dfm['LaunchTime'] = dfm['LaunchTime_fx']

        if search('zzzzz', str(dfm.at[0, 'SerialECC'])):
            dfm.at[0, 'SerialECC'] = 'NaN'
        # dfm['SensorType'] = dfm['Pump_loc']
        dfm['latitude'] = '70.48'
        dfm['longitude'] = '-21.95'

        try:
            dfm['UTCOffset'] = calculate_utcoffset(dfm)
        except KeyError:
            dfm['UTCOffset'] = "00:00:00"
        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[dfm.first_valid_index(), 'iB2']
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[dfm.first_valid_index(), 'iBc']
        if dfm.at[0, 'SolutionConcentration'] == 10: dfm['SolutionType'] = '1.0%KIFullBuffer'
        if dfm.at[0, 'SolutionConcentration'] == 5: dfm['SolutionType'] = '0.5%KIHalfBuffer'
        dfm['SolutionVolume'] = 3.0
        dfm['PF'] = 100 / dfm['Phip']
        dfm['RadiosondeManufacturer'] = 'Vaisala'
        dfm['InterfaceManufacturer'] = 'Vaisala'

        dfm['CorrectionCode'] = 6
        dfm['BackgroundCorrection'] = "constant_ib2"
        # print(list(dfm))
        # print('O3SondeTotal_hom', dfm.at[0,'O3SondeTotal_hom'])
        try:
            dfm['O3ratio_hom'] = round(dfm['Dobson'] / dfm['O3SondeTotal_hom'], 2)
        except KeyError:
            dfm['O3ratio_hom'] = 9999
        try:
            dfm['O3ratio_hom'] = -dfm['O3ratio_hom']
        except KeyError:
            dfm['O3ratio_hom'] = 9999
        if dfm.at[0, 'BurstOzonePressure'] > 32:
            dfm['O3ratio_hom'] = 9999

        if dfm.at[dfm.first_valid_index(), 'BurstOzonePressure'] > 10: dfm['O3ratio_hom'] = 9999
        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_ib2"
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_climatologicalmean_ib2"

    if stationname == 'sodankyla':

        dfm = station_info(dfm, 'Rigel Kivi', 'FMI', 'STN', '262', 'SODANKYLA', 'FI', '9999')
        dfm['latitude'] = '67.36'
        dfm['longitude'] = '26.62'
        dfm['height'] = '179'

        if (len(str(dfm.loc[0, 'LaunchTime'])) == 2) | (len(str(dfm.loc[0, 'LaunchTime'])) == 1):
            dfm['LaunchTime_fx'] = str(dfm.loc[0, 'LaunchTime']) + ':00:00'

        if (len(str(dfm.loc[0, 'LaunchTime'])) > 2):
            dfm['test0'] = dfm['LaunchTime'].apply(lambda x: str(x).split('.')[0])
            dfm['test1'] = dfm['LaunchTime'].apply(lambda x: str(x).split('.')[1])
            dfm['test11'] = dfm['test1'].apply(lambda x: lt_condition(x))
            dfm['test11'] = dfm['test11'].apply(lambda x: str(x).split(".")[0])
            if len(dfm.loc[0, 'test11']) == 1: dfm['test11'] = '0' + dfm['test11']
            dfm['LaunchTime_fx'] = dfm.apply(lambda x: launch_time(x.test0, x.test11), axis=1)
        dfm['LaunchTime'] = dfm['LaunchTime_fx']

        try:
            dfm['UTCOffset'] = calculate_utcoffset(dfm)
        except KeyError:
            dfm['UTCOffset'] = "00:00:00"

        if dfm.at[0, 'Date'] < 20051024:
            dfm['RadiosondeModel'] = 'RS80'
        if (dfm.at[0, 'Date'] >= 20051024) & (dfm.at[0, 'Date'] <= 20200826):
            dfm['RadiosondeModel'] = 'RS92'
        if (dfm.at[0, 'Date'] > 20200826):
            dfm['RadiosondeModel'] = 'RS41'
        dfm['O3Ref_Name'] = 'Brewer'

        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[dfm.first_valid_index(), 'iB2']
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[dfm.first_valid_index(), 'iBc']
        if dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 5.0: dfm['SolutionType'] = '0.5%KIHalfBuffer'
        if dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 10.0: dfm['SolutionType'] = '1.0%KIFullBuffer'
        if (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 5.0) & (
                dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 10.0) & \
                (dfm.at[0, 'Date'] >= 20060201) & (dfm.at[0, 'SensorType'] == 'DMT-Z'): dfm[
            'SolutionType'] = '0.5%KIHalfBuffer'
        if (dfm.at[0, 'Date'] < 20060201) & (dfm.at[0, 'SensorType'] == 'DMT-Z'): dfm[
            'SolutionType'] = '1.0%KIFullBuffer'
        if (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 5.0) & (
                dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 10.0) & \
                (dfm.at[0, 'SensorType'] == 'SPC'): dfm['SolutionType'] = '1.0%KIFullBuffer'

        dfm['SolutionVolume'] = 3.0
        dfm['RadiosondeManufacturer'] = 'Vaisala'
        dfm['InterfaceManufacturer'] = 'Vaisala'
        if (dfm.at[0, 'Date'] >= 20010720): dfm['TypeOzoneFreeAir'] = 'Purified air'

        try:
            dfm['O3ratio_hom'] = round(dfm['TotalO3_Col2A'] / dfm['O3SondeTotal_hom'], 3)
        except KeyError:
            dfm['O3ratio_hom'] = 9999

        if dfm.at[0, 'BurstOzonePressure'] > 32:
            dfm['O3ratio_hom'] = 9999

        try:
            dfm['O3ratio_hom'] = -dfm['O3ratio_hom']
        except KeyError:
            dfm['O3ratio_hom'] = 9999

        try:
            if dfm.at[0, 'TotalO3_Col2A'] > 700: dfm['O3ratio_hom'] = 9999
        except KeyError:
            dfm['O3ratio_hom'] = 9999

        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_ib2"
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm[
            'BackgroundCorrection'] = "constant_climatologicalmean_ib2"

    if stationname == 'valentia':
        date = dfm.at[0, 'Date']
        pf = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/CSV/read_out/'
        wfile = pf + str(date) + '_metadata.csv'
        dfmw = pd.read_csv(wfile)
        # print(list(dfmw))
        # for valentia read and write metadata from woudc metadata files
        spi = dfmw.at[0, 'DATA_GENERATION_ScientificAuthority']
        # print(spi)
        dfm = station_info(dfm, spi, 'ME', 'STN', '318', 'Valentia', 'IRL', dfmw.at[0, 'PLATFORM_GAW_ID'])
        dfm['Name'] = dfmw.at[0, 'INSTRUMENT_Name']
        dfm['SensorType'] = dfmw.at[0, 'INSTRUMENT_Model']
        dfm['SerialECC'] = dfmw.at[0, 'INSTRUMENT_Number']
        dfm['latitude'] = dfmw.at[0, 'LOCATION_Latitude']
        dfm['longitude'] = dfmw.at[0, 'LOCATION_Longitude']
        dfm['height'] = dfmw.at[0, 'LOCATION_Height']
        dfm['UTCOffset'] = dfmw.at[0, 'TIMESTAMP_UTCOffset']
        dfm['DateTime'] = dfmw.at[0, 'TIMESTAMP_Date']
        dfm['LaunchTime'] = dfmw.at[0, 'TIMESTAMP_Time']
        # dfm['DateTime'] = dfmw.at[0, 'TIMESTAMP_Date']
        if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[
                dfm.first_valid_index(), 'iB2']
        if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = \
            dfm.at[
                dfm.first_valid_index(), 'iBc']
        dfm['SolutionType'] = '1%KIFullBuffer'

        dfm['RadiosondeManufacturer'] = 'Vaisala'
        dfm['InterfaceManufacturer'] = 'Vaisala'
        dfm['SolutionVolume'] = 3.0

    return dfm


def exception_files(dfm, fname):
    bool_continue = False

    if fname == '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/20190605_o3sdqa_nors80.hdf':
        dfm['DateTime'] = '2019-06-06'
    if fname == '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/20191006_o3sdqa_nors80.hdf':
        dfm['DateTime'] = '2019-10-06'
    if fname == '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/20191010_o3sdqa_nors80.hdf':
        dfm['DateTime'] = '2019-10-09'
    if fname == '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/20200902_o3sdqa_nors80.hdf':
        # dfm['Date'] = '2020-09-03'
        dfm['DateTime'] = '2020-09-03'
    if fname == '/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/20191226_o3sdqa_nors80.hdf':
        bool_continue = True

    return dfm, bool_continue


def f_write_to_woudc_csv(df, dfm, station_name, path):
    # woudc writer object
    extcsv = woudc_extcsv.Writer(template=True)

    burst_pressure = df.Pair.min()
    dfm['BurstOzonePressure'] = float(burst_pressure)

    df = organize_df_woudc(df, station_name)

    # if station_name == 'madrid':
    #     dfm, bool_cont = exception_files(dfm, filename)
    #     if bool_cont: continue

    dfm = organize_metadata_woudc(dfm, station_name)

    df = df.reset_index()
    # dfm = dfm.reset_index()
    df = round(df, 3)
    dfm = round(dfm, 3)

    # start writing the woudc file
    extcsv.add_comment('Procedure: https://github.com/denizpoyraz/o3s-dqa-homogenization')

    # CONTENT
    extcsv.add_data('CONTENT',
                    'WOUDC,OzoneSonde,1,1',
                    field='Class,Category,Level,Form')

    # DATA_GENERATION
    datagen_field = 'Date,Agency,Version,ScientificAuthority'
    df_names = 'today', 'agency', 'version', 'stationPI'
    datagen_summary = make_summary(dfm, df_names)
    extcsv.add_data('DATA_GENERATION', datagen_summary, datagen_field)

    # PLATFORM
    platform_field = 'Type,ID,Name,Country,GAW_ID'
    df_names = 'type', 'id', 'name', 'country', 'gaw_id'
    platform_summary = make_summary(dfm, df_names)
    extcsv.add_data('PLATFORM', platform_summary, platform_field)

    # INSTRUMENT
    instrument_field = 'Name,Model,Number'
    df_names = 'Name', 'SensorType', 'SerialECC'
    instrument_summary = make_summary(dfm, df_names)
    extcsv.add_data('INSTRUMENT', instrument_summary, instrument_field)

    # LOCATION
    location_field = 'Latitude,Longitude,Height'
    df_names = 'latitude', 'longitude', 'height'
    location_summary = make_summary(dfm, df_names)
    extcsv.add_data('LOCATION', location_summary, location_field)

    # TIMESTAMP
    time_field = 'UTCOffset,Date,Time'
    df_names = 'UTCOffset', 'DateTime', 'LaunchTime'
    time_summary = make_summary(dfm, df_names)
    extcsv.add_data('TIMESTAMP', time_summary, time_field)

    # PREFLIGHT_SUMMARY
    ps_field = 'ib0, ib1, ib2, SolutionType, SolutionVolume, PumpFlowRate, OzoneSondeResponseTime, ibCorrected'
    df_names = 'iB0', 'iB1', 'iB2', 'SolutionType', 'SolutionVolume', 'PF', 'TimeResponse', 'ib_corrected'
    preflight_summary = make_summary(dfm, df_names)
    extcsv.add_data('PREFLIGHT_SUMMARY', preflight_summary, ps_field)

    # RADIOSONDE
    dfm['RadiosondeManufacturer'] = 'Vaisala'
    rs_field = 'Manufacturer,Model,Number'
    df_names = 'RadiosondeManufacturer', 'RadiosondeModel', 'RadiosondeSerial'
    rs_summary = make_summary(dfm, df_names)
    extcsv.add_data('RADIOSONDE', rs_summary, field=rs_field)

    # Interface
    int_field = 'Manufacturer,Model,Number'
    df_names = 'InterfaceManufacturer', 'InterfaceModel', 'InterfaceNr'
    int_summary = make_summary(dfm, df_names)
    extcsv.add_data('INTERFACE_CARD', int_summary, field=int_field)

    # SAMPLING_METHOD
    samp_field = 'TypeOzoneFreeAir,CorrectionWettingFlow,SurfaceOzone,DurationSurfaceOzoneExposure,LengthBG,WMOTropopausePressure,BurstOzonePressure,GroundEquipment,ProcessingSoftware'
    df_names = 'TypeOzoneFreeAir', 'CorrectionWettingFlow', 'SurfaceOzone', 'DurationSurfaceOzoneExposure', 'LengthBG', \
               'WMOTropopausePressure', 'BurstOzonePressure', 'GroundEquipment', 'ProcessingSoftware'
    samp_summary = make_summary(dfm, df_names)
    extcsv.add_data('SAMPLING_METHOD', samp_summary, field=samp_field)

    # PUMP_SETTINGS
    pump_field = 'MotorCurrent,HeadPressure,VacuumPressure'
    df_names = 'MotorCurrent', 'HeadPressure', 'VacuumPressure'
    pump_summary = make_summary(dfm, df_names)
    extcsv.add_data('PUMP_SETTINGS', pump_summary, field=pump_field)

    # PUMP_CORRECTION
    corr = np.zeros(len(pval))
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z':
        corr = komhyr_95
    else:
        corr = komhyr_86
    correction = [str([x, y])[1:-1] for x, y in zip(pval[::-1], corr[::-1])]
    pumpcor_field = 'Pressure, Correction'
    for k in range(len(corr)):
        extcsv.add_data('PUMP_CORRECTION', correction[k], field=pumpcor_field)

    if burst_pressure > 32:
        dfm['O3ratio_hom'] = 9999

    # FLIGHT_SUMMARY
    flight_field = 'IntegratedO3,CorrectionCode,SondeTotalO3,NormalizationFactor,BackgroundCorrection'
    df_names = 'O3Sonde_hom', 'CorrectionCode', 'O3SondeTotal_hom', 'O3ratio_hom', 'BackgroundCorrection'
    flight_summary = make_summary(dfm, df_names)
    extcsv.add_data('FLIGHT_SUMMARY', flight_summary, field=flight_field)

    # OZONE_REFERENCE -> O3Ref
    ozoneref_field = 'Name, Model, Number, Version, TotalO3, WLCode, ObsType, UTC_Mean'
    df_names = 'O3Ref_Name', 'O3Ref_Model', 'O3Ref_Number', 'O3Ref_Version', 'TO_Brewer', 'WLCode', 'ObsType', 'UTC_Mean'
    ozoneref_summary = make_summary(dfm, df_names)
    extcsv.add_data('OZONE_REFERENCE', ozoneref_summary, field=ozoneref_field)

    # PROFILE

    df_names = ['Time', 'Pair', 'O3', 'T', 'WindSp', 'WindDir', 'LevelCode',
                'GPHeight', 'U', 'Tbox', 'I', 'PumpMotorCurrent',
                'PumpMotorVoltage', 'Lat', 'Lon', 'Height', 'dO3']
    # data_names = ['Duration ,Pressure ,O3PartialPressure ,Temperature ,WindSpeed ,WindDirection ,LevelCode,GPHeight'
    #               ',RelativeHumidity ,SampleTemperature ,SondeCurrent ,PumpMotorCurrent,PumpMotorVoltage ,Latitude '
    #               ',Longitude ,Height,UncO3PartialPressure']
    data_names_tmp = ['Duration', 'Pressure', 'O3PartialPressure', 'Temperature', 'WindSpeed', 'WindDirection',
                      'LevelCode',
                      'GPHeight', 'RelativeHumidity', 'SampleTemperature', 'SondeCurrent', 'PumpMotorCurrent'
        , 'PumpMotorVoltage', 'Latitude', 'Longitude', 'Height', 'UncO3PartialPressure']

    n = 0
    for j in range(len(df_names)):
        j = j - n
        if df_names[j] not in df.columns.tolist():
            del df_names[j]
            del data_names_tmp[j]
            n = n + 1

    data_names = ",".join(data_names_tmp)

    size = len(df)
    profile = [0] * size

    for k in range(size):
        profile[k] = df[df_names][k:k + 1].values[0]
        profile[k] = ",".join([str(i) for i in profile[k] if str(i)])
        extcsv.add_data('PROFILE', profile[k], field=data_names)

    fileout = str(dfm.at[0, 'Date']) + ".ECC." + str(dfm.at[0, 'SensorType']) + "." + str(
        dfm.at[0, 'SerialECC']) + "." + str(dfm.at[0, 'agency']) + ".csv"

    out_name = path + '/WOUDC_nors80/' + fileout
    # print(out_name)

    # this is not working anymore, gives error:
    # woudc_extcsv.dump(extcsv, out_name)
    # TypeError: a bytes-like object is required, not 'str'

    ecsvs = woudc_extcsv.dumps(extcsv)
    with open(out_name, 'w') as f:
        f.write(ecsvs)
