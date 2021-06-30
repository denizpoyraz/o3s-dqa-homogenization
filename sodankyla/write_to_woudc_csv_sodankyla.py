import woudc_extcsv
from woudc_extcsv import Writer, WOUDCExtCSVReaderError, dump
from io import StringIO
from woudc_extcsv import load, WOUDCExtCSVReaderError
import pandas as pd
import glob
import numpy as np
from datetime import datetime
from re import search


#Table Name 	    Field (Column) Names (in order)
#PREFLIGHT_SUMMARY 	Ib0, ib1, ib2, SolutionType, SolutionVolume, PumpFlowRate, OzoneSondeResponseTime
#RADIOSONDE 	Manufacturer, Model, Number
#INTERFACE_CARD 	Manufacturer, Model, Number
#SAMPLING_METHOD 	TypeOzoneFreeAir, CorrectionWettingFlow, SurfaceOzone, DurationSurfaceOzoneExposure, LengthBG, WMOTropopausePressure, BurstOzonePressure, GroundEquipment, ProcessingSoftware
#PUMP_SETTINGS 	MotorCurrent, HeadPressure, VacuumPressure
#PUMP_CORRECTION 	Pressure, PumpCorrectionFactor
#FLIGHT_SUMMARY 	IntegratedO3, CorrectionCode, SondeTotalO3, NormalizationFactor, BackgroundCorrection, SampleTemperatureType
#OZONE_REFERENCE 	Name, Model, Number, Version, TotalO3, WLCode, ObsType, UTC_Mean
#PROFILE 	Duration, Pressure, O3PartialPressure, Temperature, WindSpeed, WindDirection, LevelCode, GPHeight, RelativeHumidity, SampleTemperature, SondeCurrent, PumpMotorCurrent, PumpMotorVoltage, Latitude, Longitude, Height
#PROFILE_UNCERTAINTY 	As in #PROFILE
#PRELAUNCH 	As in #PROFILE
#DESELECTED_DATA 	As in #PROFILE

# now read a metadata file or preapare a template to fill in the metadata
#     extcsv.add_data('CONTENT',   'WOUDC,Spectral,1.0,1', field='Class,Category,Level,Form')

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


path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_upd/'

data_files = sorted(glob.glob(path + "*_o3sdqa_rs80.hdf"))

for (filename) in(data_files):

    metaname = path + filename.split('/')[-1].split('_')[0] + '_o3smetadata_rs80.csv'
    extcsv = woudc_extcsv.Writer(template=True)

    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    # before this date it is BrewerMast
    # if dfm.at[0,'Date'] < 19970401: continue
    if dfm.at[0,'Date'] < 19941012: continue  # # no bkg values
    # if dfm.at[0, 'Date'] < 19970216: continue # alreday written

    print(filename)

    if np.isnan(dfm.at[0, 'Date']):
        print('nan date', filename)
        continue

    try: dfm['LaunchTime_int'] = round(dfm.at[0,'LaunchTime'],2)
    except:
        dfm['LaunchTime'] = 11.30
        dfm['LaunchTime_int'] = round(dfm.at[0,'LaunchTime'],2)

    # print('one', dfm.at[0, 'LaunchTime'], type(dfm.at[0, 'LaunchTime']))

    dfm['test'] = round(dfm.at[0,'LaunchTime'],2)
    if (dfm.at[0,'test'] > 11.59) & (dfm.at[0,'test'] < 12.0): dfm.at[0,'test'] = 12.00
    # clean some values like 13.91, 11.65
    tmp = round(dfm.at[0,'LaunchTime'],2)
    tmp_str = str(tmp)
    print('str tmp', tmp_str, len(tmp_str), tmp_str.split(".")[0], tmp_str.split(".")[1])
    # if len(tmp_str) == 5:     tmp = int(tmp_str[3:5])
    # if tmp_str.split(".")[0]
    hour = float(tmp_str.split(".")[0])
    min = float(tmp_str.split(".")[1])
    time = hour* 60 + min

    if int(tmp_str.split(".")[1]) > 59:
        sec = 59
        lt_str = tmp_str.split(".")[0] + '.' + str(sec)
        print(lt_str)
        dfm['test'] = float(lt_str)
        dfm['LaunchTime_Int'] = float(lt_str)


    # print(tmp_str, tmp, tmp_str[0:2])
    # if (int(str(round(dfm.at[0,'LaunchTime'],2)[3:4]))) > 59:

    dfm['test'] = dfm['test'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
    dfm['LaunchTime'] = dfm['test'].apply(lambda x: x.strftime('%H:%M:%S'))

    #Radisonde changes
    if dfm.at[0,'Date'] < 20051024:
        dfm['RadiosondeModel'] = 'RS80'
    if (dfm.at[0, 'Date'] >= 20051024) & (dfm.at[0, 'Date'] <= 20200826):
        dfm['RadiosondeModel'] = 'RS92'
    if (dfm.at[0, 'Date'] > 20200826):
        dfm['RadiosondeModel'] = 'RS41'


    # dfm['O3Ref_Version'] = 1
    # dfm['WLCode'] = 9
    dfm['O3Ref_Name'] = 'Brewer'
    # dfm['UTC_Mean'] = '12:00:00'

    # BurstOzonePressure

    burst_height = df.Height.max()
    burst_pressure = df[df.Height == burst_height].Pair.tolist()
    # print(burst_pressure, len(burst_pressure))
    #
    # if len(burst_pressure) >1:
    #     print(burst_pressure, len(burst_pressure))
    #     burst_pressure = burst_pressure[0]
    dfm['BurstOzonePressure'] = float(burst_pressure[0])

    dfm['Date'] = dfm['Date'].astype('str')
    dfm['Date'] = dfm['Date'].apply(lambda _: datetime.strptime(_, "%Y%m%d"))
    dfm['Date'] = dfm['Date'].apply(lambda _: datetime.strftime(_, '%Y-%m-%d'))

    df = round(df,3)
    dfm = round(dfm,3)

    extcsv.add_comment('Procedure: https://github.com/denizpoyraz/o3s-dqa-homogenization')

    # CONTENT
    extcsv.add_data('CONTENT',
                    'WOUDC,OzoneSonde,1,1',
                    field='Class,Category,Level,Form')
    extcsv.add_data('DATA_GENERATION',
                    '2021-05-05,FMI,2.1.3,Rigel Kivi',
                    field='Date,Agency,Version,ScientificAuthority')
    extcsv.add_data('PLATFORM',
                    'STN,,SODANKYLA,FI,',
                    field='Type,ID,Name,Country,GAW_ID')
    # INSTRUMENT
    dfm['Name'] = 'ECC'
    # dfm['SensorType'] = 'Z'
    instrument_field = 'Name,Model,Number'
    df_names = 'Name', 'SensorType', 'SerialECC'
    instrument_summary = make_summary(dfm, df_names)
    extcsv.add_data('INSTRUMENT', instrument_summary, instrument_field)
    # LOCATION
    extcsv.add_data('LOCATION',
                    '67.40,26.60,',
                    field='Latitude,Longitude,Height')

   # TIMESTAMP
    try:
        dfm['UTCOffset'] = round((dfm['LaunchTime_Int'] - 11.30),2)
        dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
        dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: x.strftime('%H:%M:%S'))
    except KeyError:
        dfm['LaunchTime_Int'] = 11.30
        dfm['UTCOffset'] = round((dfm['LaunchTime_Int'] - 11.30), 2)
        dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
        dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: x.strftime('%H:%M:%S'))

    time_field = 'UTCOffset,Date,Time'
    df_names = 'UTCOffset', 'Date', 'LaunchTime'
    time_summary = make_summary(dfm, df_names)
    extcsv.add_data('TIMESTAMP', time_summary, time_field)

    # # PREFLIGHT_SUMMARY
    # additional check for ib -1.0 values

    if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = dfm.at[dfm.first_valid_index(), 'iB2']
    if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = dfm.at[dfm.first_valid_index(), 'iBc']
    if dfm.at[dfm.first_valid_index(), 'iB2'] == -1.0: continue
    if dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 5.0: dfm['SolutionType'] = '0.5%'
    if dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 10.0: dfm['SolutionType'] = '1.0%'
    if (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 5.0) & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 10.0) &\
            (dfm.at[0, 'Date'] >= '20060201') & (dfm.at[0, 'SensorType'] == 'DMT-Z'): dfm['SolutionType'] = '0.5%'
    if (dfm.at[0,'Date'] < '20060201') & (dfm.at[0,'SensorType'] == 'DMT-Z'): dfm['SolutionType'] = '1.0%'
    if (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 5.0) & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 10.0) &\
         (dfm.at[0, 'SensorType'] == 'SPC'): dfm['SolutionType'] = '1.0%'

    dfm['SolutionVolume'] = 3.0
        # dfm['iB2'] = 9999
        # dfm['ib_corrected'] = 0.016
    ps_field = 'ib0, ib1, ib2, SolutionType, SolutionVolume, PumpFlowRate, OzoneSondeResponseTime, ibCorrected'
    df_names = 'iB0','iB1','iB2', 'SolutionType', 'SolutionVolume', 'PF', 'TimeResponse', 'ib_corrected'
    preflight_summary = make_summary(dfm, df_names)
    # AUXILIARY_DATA
    extcsv.add_data('PREFLIGHT_SUMMARY', preflight_summary, ps_field)
    # extcsv.add_data('AUXILIARY_DATA', preflight_summary, ps_field)

    # RADIOSONDE
    dfm['RadiosondeManufacturer'] = 'Vaisala'
    rs_field = 'Manufacturer,Model,Number'
    df_names = 'RadiosondeManufacturer', 'RadiosondeModel', 'RadiosondeSerial'
    rs_summary = make_summary(dfm,df_names)
    extcsv.add_data('RADIOSONDE',   rs_summary, field= rs_field)

    # Interface
    dfm['InterfaceManufacturer'] = 'Vaisala'
    int_field = 'Manufacturer,Model,Number'
    df_names = 'InterfaceManufacturer', 'InterfaceModel', 'InterfaceNr'
    int_summary = make_summary(dfm, df_names)
    extcsv.add_data('INTERFACE_CARD', int_summary, field=int_field)

    # SAMPLING_METHOD
    # dfm['LengthBG'] = 15
    #Purified air is in use since 20.7.2001.
    if (dfm.at[0, 'Date'] >= '20010720'): dfm['TypeOzoneFreeAir'] = 'Purified air'
    samp_field = 'TypeOzoneFreeAir,CorrectionWettingFlow,SurfaceOzone,DurationSurfaceOzoneExposure,LengthBG,WMOTropopausePressure,BurstOzonePressure,GroundEquipment,ProcessingSoftware'
    df_names = 'TypeOzoneFreeAir', 'CorrectionWettingFlow', 'SurfaceOzone', 'DurationSurfaceOzoneExposure', 'LengthBG',\
                 'WMOTropopausePressure', 'BurstOzonePressure', 'GroundEquipment', 'ProcessingSoftware'
    samp_summary = make_summary(dfm, df_names)
    extcsv.add_data('SAMPLING_METHOD',   samp_summary, field= samp_field)

    # PUMP_SETTINGS
    pump_field = 'MotorCurrent,HeadPressure,VacuumPressure'
    df_names = 'MotorCurrent', 'HeadPressure', 'VacuumPressure'
    pump_summary = make_summary(dfm, df_names)
    extcsv.add_data('PUMP_SETTINGS', pump_summary, field=pump_field)

    # PUMP_CORRECTION
    pval = np.array([1000, 100, 50, 30, 20, 10, 7, 5, 3])
    komhyr_86 = np.array([1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092, 1.124])  # SP Komhyr
    komhyr_95 = np.array([1, 1.007, 1.018, 1.029, 1.041, 1.066, 1.087, 1.124, 1.241])  # ECC Komhyr
    corr = np.zeros(len(pval))
    if dfm.at[dfm.first_valid_index(),'SensorType'] == 'DMT-Z': corr = komhyr_95
    else: corr = komhyr_86
    correction = [str([x, y])[1:-1] for x, y in zip(pval[::-1], corr[::-1])]
    pumpcor_field = 'Pressure, Correction'
    # pumpcor_field = 'PumpPressure, PumpCorrectionFactor'
    for k in range(len(corr)):
        extcsv.add_data('#PUMP_CORRECTION',   correction[k], field= pumpcor_field)


    # FLIGHT_SUMMARY 	IntegratedO3, CorrectionCode, SondeTotalO3, NormalizationFactor, BackgroundCorrection,
    # dfm['CorrectionCode'] = 6
    dfm['BackgroundCorrection'] = "constant_ib2"
    try: dfm['CorrectionFactor'] = -dfm['CorrectionFactor']
    except TypeError: dfm['CorrectionFactor'] = 9999
    # try: dfm['CorrectionFactor'] = -dfm['CorrectionFactor']
    # except TypeError: dfm['CorrectionFactor'] = 9999
    if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['BackgroundCorrection'] = "constant_ib0"
    if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['BackgroundCorrection'] = "constant_climatologicalmean_ib0"
    flight_field = 'IntegratedO3,CorrectionCode,SondeTotalO3,NormalizationFactor,BackgroundCorrection'
    df_names = 'IntegratedO3', 'CorrectionCode', 'SondeTotalO3', 'CorrectionFactor', 'BackgroundCorrection'
    flight_summary = make_summary(dfm, df_names)
    extcsv.add_data('FLIGHT_SUMMARY', flight_summary, field=flight_field)
    #
    # OZONE_REFERENCE -> O3Ref
    ozoneref_field = 'Name, Model, Number, Version, TotalO3, WLCode, ObsType, UTC_Mean'
    df_names = 'O3Ref_Name', 'O3Ref_Model', 'O3Ref_Number', 'O3Ref_Version', 'TO_Brewer', 'WLCode', 'ObsType', 'UTC_Mean'
    ozoneref_summary = make_summary(dfm,df_names)
    extcsv.add_data('OZONE_REFERENCE', ozoneref_summary, field=ozoneref_field)
    #
    #
    # PROFILE
    data_names = 'Duration, Height, Pressure, Temperature, Humidity, TemperatureSonde, O3PartialPressure, SondeCurrent,UncO3PartialPressure'
    df_names = ['Time', 'Height','Pair', 'T', 'U',  'Tbox', 'O3',  'I', 'dO3']

    size = len(df)

    profile = [0] * size
    for k in range(size):
        profile[k] = df[df_names][k:k + 1].values[0]
        profile[k] = ",".join([str(i) for i in profile[k] if str(i)])
        extcsv.add_data('#PROFILE',   profile[k], field= data_names)


    out_name = path + '/WOUDC_v2/' + str(df.at[df.first_valid_index(),'Date']) + '_sodankyla_woudc.csv'
    # print(out_name)

    woudc_extcsv.dump(extcsv, out_name)



