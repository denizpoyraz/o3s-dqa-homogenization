import woudc_extcsv
from woudc_extcsv import Writer, WOUDCExtCSVReaderError, dump
from io import StringIO
from woudc_extcsv import load, WOUDCExtCSVReaderError
import pandas as pd
import glob
import numpy as np
from datetime import datetime
from re import search
from functions.functions_woudc_writer import organize_metadata_woudc, exception_files, organize_df_woudc


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

station_name= 'ny-aalesund'

path = '/home/poyraden/Analysis/Homogenization_public/Files/' + station_name

data_files = sorted(glob.glob(path + "/DQA_nors80/*200819*_o3sdqa_nors80.hdf"))
# 200819
# 120217

for (filename) in(data_files):

    metaname = path + '/DQA_nors80/' + filename.split('/')[-1].split('_')[0] + '_o3smetadata_nors80.csv'
    print(metaname)

    #woudc writer object
    extcsv = woudc_extcsv.Writer(template=True)

    #homogenized data-set and metadata
    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    burst_pressure = df.Pair.min()
    dfm['BurstOzonePressure'] = float(burst_pressure)

    df = organize_df_woudc(df, station_name)

    if station_name == 'madrid':
        dfm, bool_cont = exception_files(dfm, filename)
        if bool_cont: continue

    dfm = organize_metadata_woudc(dfm,station_name)

    df = df.reset_index()
    # dfm = dfm.reset_index()
    df = round(df, 3)
    dfm = round(dfm, 3)

    # data generation date
    today = pd.to_datetime("today").strftime("%Y-%m-%d")

    #start writing the woudc file
    extcsv.add_comment('Procedure: https://github.com/denizpoyraz/o3s-dqa-homogenization')

    # CONTENT
    extcsv.add_data('CONTENT',
                    'WOUDC,OzoneSonde,1,1',
                    field='Class,Category,Level,Form')

    #DATA_GENERATION
    datagen_field = 'Date,Agency,Version,ScientificAuthority'
    df_names = 'today', 'agency', 'version', 'stationPI'
    datagen_summary = make_summary(dfm, df_names)
    extcsv.add_data('DATA_GENERATION', datagen_summary, datagen_field)

    #PLATFORM
    platform_field = 'Type,ID,Name,Country,GAW_ID'
    df_names ='type', 'id', 'name', 'country', 'gaw_id'
    platform_summary = make_summary(dfm, df_names)
    extcsv.add_data('PLATFORM',platform_summary, platform_field)

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
    df_names = 'iB0','iB1','iB2', 'SolutionType', 'SolutionVolume', 'PF', 'TimeResponse', 'ib_corrected'
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
    # data_names = 'Duration, Height, Pressure, Temperature, Humidity, TemperatureSonde, O3PartialPressure, SondeCurrent,UncO3PartialPressure'
    # df_names = ['Time', 'Height', 'Pair', 'T', 'U', 'Tbox', 'O3', 'I', 'dO3']
    # df_names = ['Time',  'Pair', 'O3', 'T','WindSpeed', 'WindDirection', 'LevelCode',
    #               'GPHeight', 'U', 'Tbox', 'I','PumpMotorCurrent',
    #               'PumpMotorVoltage', 'Latitude', 'Longitude', 'Height', 'dO3']
    df_names = ['Time',  'Pair', 'O3', 'T','WindSp', 'WindDir', 'LevelCode',
                  'GPHeight', 'U', 'Tbox', 'I','PumpMotorCurrent',
                  'PumpMotorVoltage', 'Lat', 'Lon', 'Height', 'dO3']
    # data_names = ['Duration ,Pressure ,O3PartialPressure ,Temperature ,WindSpeed ,WindDirection ,LevelCode,GPHeight'
    #               ',RelativeHumidity ,SampleTemperature ,SondeCurrent ,PumpMotorCurrent,PumpMotorVoltage ,Latitude '
    #               ',Longitude ,Height,UncO3PartialPressure']
    data_names_tmp = ['Duration','Pressure','O3PartialPressure', 'Temperature', 'WindSpeed', 'WindDirection', 'LevelCode',
                      'GPHeight','RelativeHumidity', 'SampleTemperature', 'SondeCurrent', 'PumpMotorCurrent'
        , 'PumpMotorVoltage', 'Latitude','Longitude', 'Height', 'UncO3PartialPressure']


    n = 0
    for j in range(len(df_names)):
        j = j-n
        if df_names[j] not in df.columns.tolist():
            del df_names[j]
            del data_names_tmp[j]
            n=n+1

    data_names = ",".join(data_names_tmp)

    size = len(df)
    profile = [0] * size

    for k in range(size):

        profile[k] = df[df_names][k:k + 1].values[0]
        profile[k] = ",".join([str(i) for i in profile[k] if str(i)])
        extcsv.add_data('PROFILE', profile[k], field=data_names)

    fileout = str(dfm.at[0, 'Date']) + ".ECC." + str(dfm.at[0, 'SensorType']) + "." + str(
        dfm.at[0, 'SerialECC']) + "." + str(dfm.at[0, 'agency']) + ".csv"

    out_name = path + '/WOUDC_nors80/check_' + fileout
    # print(out_name)

    #this is not working anymore, gives error:
    # woudc_extcsv.dump(extcsv, out_name)
    #TypeError: a bytes-like object is required, not 'str'

    ecsvs = woudc_extcsv.dumps(extcsv)
    with open(out_name, 'w') as f:
        f.write(ecsvs)



