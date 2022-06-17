import woudc_extcsv
from woudc_extcsv import Writer, WOUDCExtCSVReaderError, dump
from io import StringIO
from woudc_extcsv import load, WOUDCExtCSVReaderError
import pandas as pd
import glob
import numpy as np
from datetime import datetime
from re import search

K = 273.15

# /home/poyraden/Analysis/Homogenization_public/Files/scoresby/DQA_nonors80/20190723_all_hom_nonors80.hdf
# Traceback (most recent call last):
#   File "/home/poyraden/Analysis/Homogenization_public/o3s-dqa-homogenization/scoresby/write_to_woudc_csv_scoresby.py", line 251, in <module>
#     fileout = str(dfm.at[0,'Datenf']) + ".ECC." + dfm.at[0,'SensorType'] + "." + str(dfm.at[0,'SerialECC']) + ".NIWA-LAU.csv"
# TypeError: can only concatenate str (not "numpy.float64") to str

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

def launch_time(sta,end):
    return str(sta) + ":" + str(end) + ":" "00"

def lt_condition(x):
    if len(x) == 1: return float(x) * 60/10
    if len(x) == 2: return float(x) * 60/100
    if  len(x) == 3: return float(x) * 60/1000
    if  len(x) == 4: return float(x) * 60/10000

path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/DQA_nors80/'
path2 = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'


dfm_main = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files//scoresby/Metadata/Scoresby_Metadata.csv')

data_files = sorted(glob.glob(path + "*_o3sdqa_nors80.hdf"))
# data_files = sorted(glob.glob(path + "*all_hom_nors80.hdf"))

for (filename) in(data_files):

    print('one', filename)


    metaname = path + filename.split('/')[-1].split('_')[0] + '_o3smetadata_nors80.csv'
    extcsv = woudc_extcsv.Writer(template=True)

    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)



    if (len(str(dfm.loc[0, 'LaunchTime'])) == 2) | (len(str(dfm.loc[0, 'LaunchTime'])) == 1):
        dfm['LaunchTime_fx'] = str(dfm.loc[0, 'LaunchTime']) + ':00:00'

    if (len(str(dfm.loc[0, 'LaunchTime'])) > 2):
        dfm['test0'] = dfm['LaunchTime'].apply(lambda x: str(x).split('.')[0])
        dfm['test1'] = dfm['LaunchTime'].apply(lambda x: str(x).split('.')[1])
        # dfm['test11'] = dfm['test1'].apply(lambda x: float(x) * 60 / 100 if len(x) == 2  float(x) * 60 / 10 elif len(x) == 1 else float(x) * 60 / 1000)
        dfm['test11'] = dfm['test1'].apply(lambda x: lt_condition(x))

        dfm['test11'] = dfm['test11'].apply(lambda x: str(x).split(".")[0])
        if len(dfm.loc[0, 'test11']) == 1: dfm['test11'] = '0' + dfm['test11']
        dfm['LaunchTime_fx'] = dfm.apply(lambda x: launch_time(x.test0, x.test11), axis=1)
        # dfm['test'] = dfm['test'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
    dfm['LaunchTime_tf'] = dfm['LaunchTime_fx']




    # BurstOzonePressure
    burst_pressure = df.Pair.min()
    dfm['BurstOzonePressure'] = float(burst_pressure)

    dfm['Date'] = pd.to_datetime(dfm['DateTime'], format='%Y-%m-%d')
    dfm['Date'] = dfm['Date'].dt.strftime('%Y%m%d')

    dfm['Datenf'] = dfm['Date'].astype('str')
    # dfm['Date'] = dfm['Datenf'].apply(lambda _: datetime.strptime(_, "%Y%m%d"))
    # dfm['Date'] = dfm['Date'].apply(lambda _: datetime.strftime(_, '%Y-%m-%d'))

    # if dfm.at[0,'Datenf'] < '20190716': continue  # already homogenized

    print('two',filename)


    df = round(df,3)
    dfm = round(dfm,3)

    extcsv.add_comment('Procedure: https://github.com/denizpoyraz/o3s-dqa-homogenization')

    # CONTENT
    extcsv.add_data('CONTENT',
                    'WOUDC,OzoneSonde,1,1',
                    field='Class,Category,Level,Form')
    extcsv.add_data('DATA_GENERATION',
                    '2022-06-17,DMI,2.1.3,Brnlund M.',
                    field='Date,Agency,Version,ScientificAuthority')
    extcsv.add_data('PLATFORM',
                    'STN,406,Scoresbysund,GRL,SCB',
                    field='Type,ID,Name,Country,GAW_ID')


    # print(dfm.at[0,'SerialECC'], type(dfm.at[0,'SerialECC']))
    if search('zzzzz', str(dfm.at[0,'SerialECC'])):
        dfm.at[0, 'SerialECC'] = 'NaN'

    # INSTRUMENT
    dfm['Name'] = 'ECC'
    instrument_field = 'Name,Model,Number'
    df_names = 'Name', 'Pump_loc', 'SerialECC'
    instrument_summary = make_summary(dfm, df_names)
    extcsv.add_data('INSTRUMENT', instrument_summary, instrument_field)
    # LOCATION
    extcsv.add_data('LOCATION',
                    '70.48,-21.95,UNKNOWN',
                    field='Latitude,Longitude,Height')

   # TIMESTAMP
    difs = 1
    try:
        dif = round((dfm.at[0,'LaunchTime'] - 11.50),2)
        if dif < 0:
            difs =0
            dif = abs(dif)
        offseth = str(dif).split(".")[0]
        offsetm = int(float("0." + str(dif).split(".")[1])*60)
        offset = offseth + "." +str(offsetm)
        dfm['UTCOffset'] = offset
        dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
        dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: x.strftime('%H:%M:%S'))

    except KeyError:

        dfm['UTCOffset'] = "00:00:00"

    time_field = 'UTCOffset,Date,Time'
    df_names = 'UTCOffset', 'DateTime', 'LaunchTime_tf'
    time_summary = make_summary(dfm, df_names)
    extcsv.add_data('TIMESTAMP', time_summary, time_field)

    # # PREFLIGHT_SUMMARY
    # additional check for ib -1.0 values

    if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = dfm.at[dfm.first_valid_index(), 'iB2']
    if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = dfm.at[dfm.first_valid_index(), 'iBc']
    if dfm.at[0,'SolutionConcentration'] == 10: dfm['SolutionType'] = '1.0%KIFullBuffer'
    if dfm.at[0,'SolutionConcentration'] == 5: dfm['SolutionType'] = '0.5%KIHalfBuffer'
    dfm['SolutionVolume'] = 3.0

    ps_field = 'ib0, ib1, ib2, SolutionType, SolutionVolume, PumpFlowRate, OzoneSondeResponseTime, ibCorrected'
    df_names = 'iB0','iB1','iB2', 'SolutionType', 'SolutionVolume', 'Phip', 'TimeResponse', 'ib_corrected'
    preflight_summary = make_summary(dfm, df_names)
    # AUXILIARY_DATA
    extcsv.add_data('PREFLIGHT_SUMMARY', preflight_summary, ps_field)
    # extcsv.add_data('AUXILIARY_DATA', preflight_summary, ps_field)

    # RADIOSONDE
    dfm['RadiosondeManufacturer'] = 'Vaisala'
    rs_field = 'Manufacturer,Model,Number'
    df_names = 'RadiosondeManufacturer', 'RadiosondeModel', 'mRadioSondeNr'
    rs_summary = make_summary(dfm,df_names)
    extcsv.add_data('RADIOSONDE',   rs_summary, field= rs_field)

    # Interface
    dfm['InterfaceManufacturer'] = 'Vaisala'
    int_field = 'Manufacturer,Model,Number'
    df_names = 'InterfaceManufacturer', 'InterfaceModel', 'InterfaceNr'
    int_summary = make_summary(dfm, df_names)
    extcsv.add_data('INTERFACE_CARD', int_summary, field=int_field)

    # SAMPLING_METHOD
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
    dfm['CorrectionCode'] = 6
    dfm['BackgroundCorrection'] = "constant_ib0"
    # print(list(dfm))
    # print('O3SondeTotal_hom', dfm.at[0,'O3SondeTotal_hom'])
    try:
        dfm['O3ratio_hom'] = round(dfm['Dobson'] / dfm['O3SondeTotal_hom'],2)
    except KeyError: dfm['O3ratio_hom'] = 9999
    try: dfm['O3ratio_hom'] = -dfm['O3ratio_hom']
    except KeyError: dfm['O3ratio_hom'] = 9999
    if burst_pressure > 32:
        dfm['O3ratio_hom'] = 9999

    if dfm.at[dfm.first_valid_index(), 'BurstOzonePressure'] > 10: dfm['O3ratio_hom'] = 9999
    if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['BackgroundCorrection'] = "constant_ib0"
    if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['BackgroundCorrection'] = "constant_climatologicalmean_ib0"
    flight_field = 'IntegratedO3,CorrectionCode,SondeTotalO3,NormalizationFactor,BackgroundCorrection'
    df_names = 'O3Sonde_hom', 'CorrectionCode', 'O3SondeTotal_hom', 'O3ratio_hom', 'BackgroundCorrection'
    flight_summary = make_summary(dfm, df_names)
    extcsv.add_data('FLIGHT_SUMMARY', flight_summary, field=flight_field)
    #
    # OZONE_REFERENCE -> O3Ref
    ozoneref_field = 'Name, Model, Number, Version, TotalO3, WLCode, ObsType, UTC_Mean'
    df_names = 'O3Ref_Name', 'O3Ref_Model', 'O3Ref_Number', 'O3Ref_Version', 'Dobson', 'WLCode', 'ObsType', 'UTC_Mean'
    ozoneref_summary = make_summary(dfm,df_names)
    extcsv.add_data('OZONE_REFERENCE', ozoneref_summary, field=ozoneref_field)
    #
    #
    # PROFILE

    # df['Phip'] = df['Phip_cor']
    data_names = 'Duration, Height, Pressure, Temperature, Humidity, TemperatureSonde, O3PartialPressure, SondeCurrent,UncO3PartialPressure'
    df_names = ['Time', 'Height','Pair', 'T', 'U',  'Tbox', 'O3',  'I', 'dO3']

    size = len(df)

    profile = [0] * size
    for k in range(size):
        profile[k] = df[df_names][k:k + 1].values[0]
        profile[k] = ",".join([str(i) for i in profile[k] if str(i)])
        extcsv.add_data('#PROFILE',   profile[k], field= data_names)

    if pd.isna(dfm.at[0,'SensorType']):
        print('is null')
        dfm['SensorType'] = dfm['SensorType'].astype(str)
        dfm.at[0, 'SensorType'] = 'nan'
    fileout = str(dfm.at[0,'Datenf']) + ".ECC." + dfm.at[0,'SensorType'] + "." + str(dfm.at[0,'SerialECC']) + ".DMI.csv"

    out_name = path2 + '/WOUDC_nors80/' + fileout

    woudc_extcsv.dump(extcsv, out_name)




