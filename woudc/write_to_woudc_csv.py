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


path = '/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/version2/DQA/'

data_files = glob.glob(path + "200504*_o3sdqa.hdf")

for (filename) in(data_files):

    print(filename)
    metaname = path + filename.split('/')[-1].split('_')[0] + '_o3smetadata.csv'
    extcsv = woudc_extcsv.Writer(template=True)
    # extcsv = woudc_extcsv.Writer()

    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    dfm['LaunchTime'] = round(dfm['LaunchTime'],2).astype('str')
    dfm['Date'] = dfm['Date'].astype('str')
    dfm['LaunchTime'] = dfm['LaunchTime'].apply(lambda _: datetime.strptime(_, "%H.%M"))
    dfm['LaunchTime'] = dfm['LaunchTime'].apply(lambda _: datetime.strftime(_, "%H.%M"))
    dfm['Date'] = dfm['Date'].apply(lambda _: datetime.strptime(_, "%Y%m%d"))
    dfm['Date'] = dfm['Date'].apply(lambda _: datetime.strftime(_, '%Y-%m-%d'))

    df = round(df,3)
    dfm = round(dfm,3)

    # CONTENT
    extcsv.add_data('CONTENT',
                    'WOUDC,Spectral,1.0,1',
                    field='Class,Category,Level,Form')
    extcsv.add_data('DATA_GENERATION',
                    '2005-04-30,EPA_UGA,2.00',
                    field='Date,Agency,Version,ScientificAuthority')
    extcsv.add_data('PLATFORM',
                    'STN,388,Shenandoah,USA',
                    field='Type,ID,Name,Country,GAW_ID')
    # INSTRUMENT
    dfm['Name'] = 'ECC'
    instrument_field = 'Name,Model,Number'
    df_names = 'Name',  'SensorType', 'SerialECC'
    instrument_summary = make_summary(dfm, df_names)
    extcsv.add_data('INSTRUMENT', instrument_summary, instrument_field)

    # LOCATION
    location_field = 'Latitude,Longitude,Height'
    df_names = 'Latitude', 'Longitude', 'Height'
    location_summary = make_summary(dfm, df_names)
    extcsv.add_data('LOCATION',   location_summary, field= location_field)

   # TIMESTAMP
    time_field = 'UTCOffset,Date,Time'
    df_names = 'UTCOffset', 'Date', 'LaunchTime'
    time_summary = make_summary(dfm, df_names)
    extcsv.add_data('TIMESTAMP', time_summary, time_field)

    # # PREFLIGHT_SUMMARY
    ps_field = 'Ib0, ib1, ib2, SolutionType, SolutionVolume, PumpFlowRate, OzoneSondeResponseTime'
    df_names = 'iB0', 'iB1','iB2', 'SolutionConcentration', 'SolutionVolume', 'PF', 'TimeResponse'
    preflight_summary = make_summary(dfm, df_names)
    # AUXILIARY_DATA
    # extcsv.add_data('PREFLIGHT_SUMMARY', preflight_summary, ps_field)
    extcsv.add_data('AUXILIARY_DATA', preflight_summary, ps_field)

    # RADIOSONDE
    rs_field = 'Manufacturer,Model,Number'
    df_names = 'RadiosondeModel', 'RadiosondeModel', 'RadiosondeSerial'
    rs_summary = make_summary(dfm,df_names)
    extcsv.add_data('RADIOSONDE',   rs_summary, field= rs_field)

    # Interface
    int_field = 'Manufacturera,Modela,Numbera'
    df_names = 'InterfaceModel', 'InterfaceModel', 'InterfaceSerial'
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
    flight_field = 'IntegratedO3,CorrectionCode,SondeTotalO3,NormalizationFactor,BackgroundCorrection'
    df_names = 'IntegratedO3', 'CorrectionFactor', 'SondeTotalO3', 'NormalizationFactor', 'BackgroundCorrection'
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
    data_names = 'Duration, Height, Pressure, Temperature, Humidity, TemperatureSonde, O3PartialPressure, SondeCurrent,O3PartialPressure_Uncertainty'
    df_names = ['Time', 'Height','Pair', 'T', 'U',  'Tbox', 'O3',  'I', 'dO3']

    size = len(df)

    profile = [0] * size
    for k in range(size):
        profile[k] = df[df_names][k:k + 1].values[0]
        profile[k] = ",".join([str(i) for i in profile[k] if str(i)])
        extcsv.add_data('#PROFILE',   profile[k], field= data_names)


    out_name = path + str(df.at[df.first_valid_index(),'Date']) + '_testwoudc.csv'
    print(out_name)

    woudc_extcsv.dump(extcsv, out_name)




