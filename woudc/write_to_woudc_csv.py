import woudc_extcsv
from woudc_extcsv import Writer, WOUDCExtCSVReaderError, dump
from io import StringIO
from woudc_extcsv import load, WOUDCExtCSVReaderError
import pandas as pd
import glob
import numpy as np


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
    try:
        # print(a)
        # print(df.at[df.first_valid_index(), a])
        return df.at[df.first_valid_index(), a]
    except KeyError:
        return 9999


path = '/home/poyraden/Analysis/Homogenization_Analysis/Files/Nilu/Sodankyl/version2/DQA/'

data_files = glob.glob(path + "20050406_o3sdqa.hdf")
meta_files = glob.glob(path + "20050406*o3smetadata.csv")

for (filename) in(data_files):

    print(filename)
    metaname = path + filename.split('/')[-1].split('_')[0] + '_o3smetadata.csv'
    extcsv = woudc_extcsv.Writer(template=True)
    # extcsv = woudc_extcsv.Writer()


    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

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
    extcsv.add_data('INSTRUMENT', 'Brewer,MKIV,137', field='Name,Model,Number')
    extcsv.add_data('LOCATION',
                    '38.52,-78.44,1073',
                    field='Latitude,Longitude,Height')

    extcsv.add_data('TIMESTAMP',
                    '-05:27:17,2004-01-31,07:28:49',
                    field='UTCOffset,Date,Time')

    # PREFLIGHT_SUMMARY
    ps_field = 'iB0, iB2, SolutionVolume, SolutionConcentration, PumpFlowRate, OzoneSondeResponseTime'
    df_names = 'iB0', 'iB2',  'SolutionVolume', 'SolutionConcentration', 'PF', 'TimeResponse'
    preflight_summary = [util_func(dfm,i) for i in df_names]
    preflight_summary = str(preflight_summary)[1:-1]
    extcsv.add_data('PREFLIGHT_SUMMARY',   preflight_summary, field= ps_field)

    # RADIOSONDE
    rs_field = 'Manufacturer, Model, Number'
    df_names = 'RadiosondeModel', 'RadiosondeModel', 'RadiosondeSerial'
    rs_summary = [util_func(dfm,i) for i in df_names]
    test = [0]*3
    rs_summary = np.array(rs_summary)
    print(rs_summary[1])
    # rs_summary = str(rs_summary)[1:-1]
    for j in range(len(rs_summary)):
        print(rs_summary[j])
        test[j] = rs_summary[j]
    # print(rs_summary)
    print(test)
    print('test', np.array2string(test, separator=',', formatter={'str_kind': lambda x: x}))

    extcsv.add_data('RADIOSONDE',   rs_summary, field= rs_field)

    # Interface
    int_field = 'Manufacturer, Model, Number'
    df_names = 'InterfaceModel', 'InterfaceModel', 'InterfaceSerial'
    int_summary = [util_func(dfm,i) for i in df_names]
    print(int_summary)

    int_summary = str(int_summary)[1:-1]
    print(int_summary.strip(''))
    extcsv.add_data('INTERFACE',   int_summary, field= int_field)

    # SAMPLING_METHOD
    samp_field = 'TypeOzoneFreeAir, CorrectionWettingFlow, SurfaceOzone, DurationSurfaceOzoneExposure, LengthBG, ' \
                 'WMOTropopausePressure, BurstOzonePressure, GroundEquipment, ProcessingSoftware'
    df_names = 'TypeOzoneFreeAir', 'CorrectionWettingFlow', 'SurfaceOzone', 'DurationSurfaceOzoneExposure', 'LengthBG',  \
                 'WMOTropopausePressure', 'BurstOzonePressure', 'GroundEquipment', 'ProcessingSoftware'
    samp_summary = [util_func(dfm,i) for i in df_names]
    samp_summary = str(samp_summary)[1:-1]
    extcsv.add_data('SAMPLING_METHOD',   samp_summary, field= samp_field)

    # PUMP_SETTINGS
    pump_field = 'MotorCurrent, HeadPressure, VacuumPressure'
    df_names = 'MotorCurrent', 'HeadPressure', 'VacuumPressure'
    pump_summary = [util_func(df, i) for i in df_names]
    pump_summary = str(pump_summary)[1:-1]
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



    # PROFILE
    data_names = 'Duration, Height, Pressure, Temperature, Humidity, TemperatureSonde, O3PartialPressure, SondeCurrent'
    df_names = ['Time', 'Height','Pair', 'T', 'U',  'Tbox', 'O3',  'I']

    size = len(df)

    profile = [0] * size
    for k in range(size):
        profile[k] = df[df_names][k:k + 1].values[0]
        profile[k] = ",".join([str(i) for i in profile[k] if str(i)])
        extcsv.add_data('#PROFILE',   profile[k], field= data_names)


    out_name = path + str(df.at[df.first_valid_index(),'Date']) + '_testwoudc.csv'

    woudc_extcsv.dump(extcsv, out_name)




