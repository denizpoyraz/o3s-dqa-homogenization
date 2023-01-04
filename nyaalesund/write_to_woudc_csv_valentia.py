import woudc_extcsv
from woudc_extcsv import Writer, WOUDCExtCSVReaderError, dump
from io import StringIO
from woudc_extcsv import load, WOUDCExtCSVReaderError
import pandas as pd
import glob
import numpy as np
from datetime import datetime
from re import search

#Notes: LaunchTime and UTCOffset values are problematic, thats why Launch time is directly taken from the metadata
# and UTCOffset is always set to 9999


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


path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/DQA_rs80/'

data_files = sorted(glob.glob(path + "*_o3sdqa_rs80.hdf"))

for (filename) in(data_files):

    metaname = path + filename.split('/')[-1].split('_')[0] + '_o3smetadata_rs80.csv'
    extcsv = woudc_extcsv.Writer(template=True)
    # print(metaname)

    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    if dfm.at[0,'Date'] < 19941012: continue  # # no bkg values
    # if dfm.at[0, 'Date'] > 19991229: continue # alreday written
    # if dfm.at[0, 'Date'] < 20000101: continue # alreday written



    print(filename)

    if np.isnan(dfm.at[0, 'Date']):
        print('nan date', filename)
        continue

    # print(len(str(dfm.loc[0,'LaunchTime'])), dfm.loc[0,'LaunchTime'])

    if (len(str(dfm.loc[0,'LaunchTime'])) == 2) | (len(str(dfm.loc[0,'LaunchTime'])) == 1):
        dfm['LaunchTime_fx'] = str(dfm.loc[0,'LaunchTime']) + ':00:00'


    if (len(str(dfm.loc[0,'LaunchTime'])) > 2):
        dfm['test0'] = dfm['LaunchTime'].apply(lambda x: str(x).split('.')[0])
        dfm['test1'] = dfm['LaunchTime'].apply(lambda x: str(x).split('.')[1])
        # dfm['test11'] = dfm['test1'].apply(lambda x: float(x) * 60 / 100 if len(x) == 2  float(x) * 60 / 10 elif len(x) == 1 else float(x) * 60 / 1000)
        dfm['test11'] = dfm['test1'].apply(lambda x: lt_condition(x))

        dfm['test11'] = dfm['test11'].apply(lambda x: str(x).split(".")[0])
        if len(dfm.loc[0,'test11']) == 1: dfm['test11'] = '0' + dfm['test11']
        dfm['LaunchTime_fx'] = dfm.apply(lambda x: launch_time(x.test0, x.test11), axis=1)
    # dfm['test'] = dfm['test'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
    dfm['LaunchTime'] =  dfm['LaunchTime_fx']

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

    burst_pressure = df.Pair.min()

    dfm['BurstOzonePressure'] = float(burst_pressure)

    dfm['Date'] = dfm['Date'].astype('str')
    dfm['Datenf'] = dfm['Date'].astype('str')

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
                    '2022-04-27,FMI,2.1.3,Rigel Kivi',
                    field='Date,Agency,Version,ScientificAuthority')
    extcsv.add_data('PLATFORM',
                    'STN,262,SODANKYLA,FI,9999',
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
                    '67.3666,26.6297,179',
                    field='Latitude,Longitude,Height')



   # # # TIMESTAMP
   #  try:
   #      dfm['UTCOffset'] = round((dfm['LaunchTime_int'] - 11.30),2)
   #      print(dfm['UTCOffset'])
   #      dfm['UTCOffsetf'] = dfm['UTCOffset'].astype(float)
   #      if(dfm.at[0,'UTCOffsetf'] > 0):
   #          dfm['UTCOffset'] = dfm['UTCOffsetf'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
   #          dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: x.strftime('%H:%M:%S'))
   #      if(dfm.at[0,'UTCOffsetf'] < 0):
   #          dfm['UTCOffsetf'] = -1 * dfm['UTCOffsetf']
   #          print('in', dfm['UTCOffsetf'])
   #          dfm['UTCOffset'] = dfm['UTCOffsetf'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
   #          dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: x.strftime('%H:%M:%S'))
   #          dfm['UTCOffset'] = "-"+dfm['UTCOffset']
   #  except KeyError:
   #      dfm['LaunchTime_int'] = 11.30
   #      dfm['UTCOffset'] = round((dfm['LaunchTime_int'] - 11.30), 2)
   #      dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: pd.to_datetime(str(x), format='%H.%M'))
   #      dfm['UTCOffset'] = dfm['UTCOffset'].apply(lambda x: x.strftime('%H:%M:%S'))
   #
   #
   #  print('end',dfm['UTCOffset'])

    ## problems with Launch time and its offset: therefore it is set to 9999
    dfm['UTCOffset'] = 9999

    time_field = 'UTCOffset,Date,Time'
    df_names = 'UTCOffset', 'Date', 'LaunchTime'
    time_summary = make_summary(dfm, df_names)
    extcsv.add_data('TIMESTAMP', time_summary, time_field)

    # # PREFLIGHT_SUMMARY
    # additional check for ib -1.0 values

    if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = dfm.at[dfm.first_valid_index(), 'iB2']
    if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = dfm.at[dfm.first_valid_index(), 'iBc']
    if dfm.at[dfm.first_valid_index(), 'iB2'] == -1.0: continue
    if dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 5.0: dfm['SolutionType'] = '0.5%KIHalfBuffer'
    if dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] == 10.0: dfm['SolutionType'] = '1.0%KIFullBuffer'
    if (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 5.0) & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 10.0) &\
            (dfm.at[0, 'Date'] >= '20060201') & (dfm.at[0, 'SensorType'] == 'DMT-Z'): dfm['SolutionType'] = '0.5%KIHalfBuffer'
    if (dfm.at[0,'Date'] < '20060201') & (dfm.at[0,'SensorType'] == 'DMT-Z'): dfm['SolutionType'] = '1.0%KIFullBuffer'
    if (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 5.0) & (dfm.at[dfm.first_valid_index(), 'SolutionConcentration'] != 10.0) &\
         (dfm.at[0, 'SensorType'] == 'SPC'): dfm['SolutionType'] = '1.0%KIFullBuffer'

    dfm['SolutionVolume'] = 3.0
    ps_field = 'ib0, ib1, ib2, SolutionType, SolutionVolume, PumpFlowRate, OzoneSondeResponseTime, ibCorrected'
    df_names = 'iB0','iB1','iB2', 'SolutionType', 'SolutionVolume', 'PF', 'TimeResponse', 'ib_corrected'
    preflight_summary = make_summary(dfm, df_names)
    # PREFLIGHT_SUMMARY
    extcsv.add_data('PREFLIGHT_SUMMARY', preflight_summary, ps_field)

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
    for k in range(len(corr)):
        extcsv.add_data('#PUMP_CORRECTION',   correction[k], field= pumpcor_field)


    # FLIGHT_SUMMARY 	IntegratedO3, CorrectionCode, SondeTotalO3, NormalizationFactor, BackgroundCorrection,
    dfm['CorrectionCode'] = 6
    dfm['BackgroundCorrection'] = "constant_ib2"

    try:
        dfm['O3ratio_hom'] = round(dfm['TotalO3_Col2A'] / dfm['O3SondeTotal_hom'], 3)
    except KeyError:
        dfm['O3ratio_hom'] = 9999

    if burst_pressure > 32:
        dfm['O3ratio_hom'] = 9999

    try:
        dfm['O3ratio_hom'] = -dfm['O3ratio_hom']
    except KeyError:
        dfm['O3ratio_hom'] = 9999

    try:
        if dfm.at[0,'TotalO3_Col2A'] > 700: dfm['O3ratio_hom'] = 9999
    except KeyError: dfm['O3ratio_hom'] = 9999

    if dfm.at[dfm.first_valid_index(), 'iB2'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['BackgroundCorrection'] = "constant_ib2"
    if dfm.at[dfm.first_valid_index(), 'iB2'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['BackgroundCorrection'] = "constant_climatologicalmean_ib2"
    flight_field = 'IntegratedO3,CorrectionCode,SondeTotalO3,NormalizationFactor,BackgroundCorrection'
    df_names = 'O3Sonde_hom', 'CorrectionCode', 'O3SondeTotal_hom', 'O3ratio_hom', 'BackgroundCorrection'
    flight_summary = make_summary(dfm, df_names)
    extcsv.add_data('FLIGHT_SUMMARY', flight_summary, field=flight_field)

    #
    # OZONE_REFERENCE -> O3Ref
    ozoneref_field = 'Name, Model, Number, Version, TotalO3, WLCode, ObsType, UTC_Mean'
    df_names = 'O3Ref_Name', 'O3Ref_Model', 'O3Ref_Number', 'O3Ref_Version', 'TotalO3_Col2A', 'WLCode', 'ObsType', 'UTC_Mean'
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

    try:
        fileout = str(dfm.at[dfm.first_valid_index(), 'Datenf']) + ".ECC." + dfm.at[0, 'SensorType'] + "." + dfm.at[
        0, 'SerialECC'][0:-1] + ".FMI.csv"
    except IndexError:
        dfm['SerialECC'] = dfm['SerialECC'].astype(str)
        fileout = str(dfm.at[dfm.first_valid_index(), 'Datenf']) + ".ECC." + dfm.at[0, 'SensorType'] + "." + dfm.at[
        0, 'SerialECC'] + ".FMI.csv"


    # print(dfm.at[0, 'SerialECC'][:-1])
    # print(fileout)Ftmp

    out_name = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/WOUDC_rs80/' + fileout
    # print(out_name)

    woudc_extcsv.dump(extcsv, out_name)




