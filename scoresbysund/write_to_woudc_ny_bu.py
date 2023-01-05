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

# # make a df of woudc metadata
allFiles = sorted(glob.glob('/home/poyraden/Analysis/Homogenization_public/Files//scoresby/Metadata/*metadata.csv'))

dfmeta = pd.DataFrame()
metadata = []

for (filename) in (allFiles):
    df = pd.read_csv(filename)

    metadata.append(df)
#
name_out = 'Scoresby_Metadata'
dfall = pd.concat(metadata, ignore_index=True)

dfall.to_csv('/home/poyraden/Analysis/Homogenization_public/Files//scoresby/Metadata/' + name_out + ".csv")

dfm_woudc = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files//scoresby/Metadata/Scoresby_WOUDC_Metadata.csv')

print('done')

path = '/home/poyraden/Analysis/Homogenization_public/Files//scoresby/DQA_nors80/'
path2 = '/home/poyraden/Analysis/Homogenization_public/Files//scoresby/'

data_files = sorted(glob.glob(path + "*_o3sdqa_nors80.hdf"))

for (filename) in(data_files):

    metaname = path + filename.split('/')[-1].split('_')[0] + '_o3smetadata_nors80.csv'
    extcsv = woudc_extcsv.Writer(template=True)

    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    #
    # # some exceptions
    # if filename == '/home/poyraden/Analysis/Homogenization_public/Files//scoresby/DQA_nors80/20190605_o3sdqa_nors80.hdf':
    #     dfm['DateTime'] = '2019-06-06'
    # if filename == '/home/poyraden/Analysis/Homogenization_public/Files//scoresby/DQA_nors80/20191006_o3sdqa_nors80.hdf':
    #     dfm['DateTime'] = '2019-10-06'
    # if filename == '/home/poyraden/Analysis/Homogenization_public/Files//scoresby/DQA_nors80/20191010_o3sdqa_nors80.hdf':
    #     dfm['DateTime'] = '2019-10-09'
    # if filename == '/home/poyraden/Analysis/Homogenization_public/Files//scoresby/DQA_nors80/20200902_o3sdqa_nors80.hdf':
    #     # dfm['Date'] = '2020-09-03'
    #     dfm['DateTime'] = '2020-09-03'
    #     print('why noyt')
    #     print(dfm['Date'])
    #
    #
    # if filename == '/home/poyraden/Analysis/Homogenization_public/Files//scoresby/DQA_nors80/20191226_o3sdqa_nors80.hdf':continue

    dfm['Date'] = pd.to_datetime(dfm['DateTime'], format='%Y-%m-%d')
    dfm['Date2'] = pd.to_datetime(dfm['Date'], format='%Y%m%d')
    dfm['Datenf'] = dfm['Date'].apply(lambda x: x.strftime('%Y%m%d'))
    dfm['Datenw'] = dfm['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    dfm['Datenf'] = dfm['Datenf'].astype('int')

    # if dfm.at[0,'Datenf'] < 20200810: continue  # already homogenized

    print(filename)

    dfmw = dfm_woudc[dfm_woudc['TIMESTAMP_Date'] == dfm.loc[0,'Datenw']]
    dfmw = dfmw.reset_index()

    if np.isnan(dfm.at[0, 'Datenf']):
        print('nan date', filename)
        continue

    dfm['LaunchTime'] = dfmw.loc[0, 'TIMESTAMP_Time']

    # set radiosonde, interface nmber etc..
    if dfm.at[0,'Datenf'] <= 20060301:
        dfm['RadiosondeModel'] = 'RS80'
        dfm['InterfaceModel'] = 'RSA-921'
    if (dfm.at[0,'Datenf'] > 20060301) & (dfm.at[0,'Datenf'] < 20180322):
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

    # BurstOzonePressure

    burst_pressure = df.Pair.min()

    dfm['BurstOzonePressure'] = float(burst_pressure)
    dfm['Datenf'] = dfm['Datenf'].astype('str')
    dfm['Date'] = dfm['Datenf'].apply(lambda _: datetime.strptime(_, "%Y%m%d"))
    dfm['Date'] = dfm['Date'].apply(lambda _: datetime.strftime(_, '%Y-%m-%d'))

    df = round(df,3)
    dfm = round(dfm,3)

    extcsv.add_comment('Procedure: https://github.com/denizpoyraz/o3s-dqa-homogenization')

    # CONTENT
    extcsv.add_data('CONTENT',
                    'WOUDC,OzoneSonde,1,1',
                    field='Class,Category,Level,Form')
    extcsv.add_data('DATA_GENERATION',
                    '2022-04-26,AEMET,2.1.3,Jose Luis Hernandez',
                    field='Date,Agency,Version,ScientificAuthority')
    extcsv.add_data('PLATFORM',
                    'STN,308,Scoresby,ESP,MAD',
                    field='Type,ID,Name,Country,GAW_ID')
    # INSTRUMENT
    dfm['Name'] = dfmw.loc[0,'INSTRUMENT_Name']
    dfm['SensorType'] = dfmw.loc[0,'INSTRUMENT_Model']
    dfm['SerialECC'] = dfmw.loc[0, 'INSTRUMENT_Number']
    instrument_field = 'Name,Model,Number'
    df_names = 'Name', 'SensorType', 'SerialECC'
    instrument_summary = make_summary(dfm, df_names)
    extcsv.add_data('INSTRUMENT', instrument_summary, instrument_field)
    # LOCATION
    if dfm.at[0,'Datenf'] <= '19970130':
        extcsv.add_data('LOCATION',
                        '40.47,-3.75,640.0',
                        field='Latitude,Longitude,Height')
    if dfm.at[0,'Datenf'] > '19970130':
        extcsv.add_data('LOCATION',
                        '40.47,-3.58,631.0',
                        field='Latitude,Longitude,Height')

   # TIMESTAMP
    dfm['UTCOffset'] = dfmw.at[0, 'TIMESTAMP_UTCOffset']


    time_field = 'UTCOffset,Date,Time'
    df_names = 'UTCOffset', 'Date', 'LaunchTime'
    time_summary = make_summary(dfm, df_names)
    extcsv.add_data('TIMESTAMP', time_summary, time_field)

    # # PREFLIGHT_SUMMARY
    # additional check for ib -1.0 values
    if dfm.at[dfm.first_valid_index(), 'iB0'] == dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = dfm.at[dfm.first_valid_index(), 'iB0']
    if dfm.at[dfm.first_valid_index(), 'iB0'] != dfm.at[dfm.first_valid_index(), 'iBc']: dfm['ib_corrected'] = dfm.at[dfm.first_valid_index(), 'iBc']

    dfm['SolutionType'] = '1.0%KIFullBuffer'
    ps_field = 'ib0, ib1, ib2, SolutionType, SolutionVolume, PumpFlowRate, OzoneSondeResponseTime, ibCorrected'
    df_names = 'iB0','iB1','iB2', 'SolutionType', 'SolutionVolume', 'PF', 'TimeResponse', 'ib_corrected'
    preflight_summary = make_summary(dfm, df_names)
    # AUXILIARY_DATA
    extcsv.add_data('PREFLIGHT_SUMMARY', preflight_summary, ps_field)

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
    dfm['BackgroundCorrection'] = "constant_ib2"
    try:
        dfm['O3ratio_hom'] = round(dfm['BrewO3'] / dfm['O3SondeTotal_hom'], 3)
    except KeyError:
        dfm['O3ratio_hom'] = 9999

    if burst_pressure > 32:
        dfm['O3ratio_hom'] = 9999

    try: dfm['O3ratio_hom'] = -dfm['O3ratio_hom']
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
    df_names = 'O3Ref_Name', 'O3Ref_Model', 'O3Ref_Number', 'O3Ref_Version', 'BrewO3', 'WLCode', 'ObsType', 'UTC_Mean'
    ozoneref_summary = make_summary(dfm,df_names)
    extcsv.add_data('OZONE_REFERENCE', ozoneref_summary, field=ozoneref_field)
    #
    #
     # PROFILE
    data_names = 'Duration, Height, Pressure, Temperature, Humidity, TemperatureSonde, O3PartialPressure, SondeCurrent,UncO3PartialPressure'
    df_names = ['Duration', 'GPHeight','Pair', 'Temperature', 'RelativeHumidity',  'Tbox', 'O3',  'I', 'dO3']

    size = len(df)

    profile = [0] * size
    for k in range(size):
        profile[k] = df[df_names][k:k + 1].values[0]
        profile[k] = ",".join([str(i) for i in profile[k] if str(i)])
        extcsv.add_data('#PROFILE',   profile[k], field= data_names)

    fileout = str(dfm.at[dfm.first_valid_index(),'Datenf']) + ".ECC." + dfm.at[0,'SensorType'] + "." + dfm.at[0,'SerialECC'] + ".AEMET.csv"
    # print(fileout)

    out_name = path2 + '/WOUDC_nors80/' + fileout
    # print(out_name)

    woudc_extcsv.dump(extcsv, out_name)




