import pandas as pd
import math
from re import search
from scipy.interpolate import interp1d
from datetime import datetime


from functions.homogenization_functions import stoichmetry_conversion, calculate_cph,pf_groundcorrection,\
    pf_groundcorrection_noerr

komhyr_86 = [1, 1, 1.007, 1.018, 1.022, 1.032, 1.055, 1.070, 1.092, 1.124]  # SP Komhyr
pval = [1100, 200, 100, 50, 30, 20, 10, 7, 5, 3]
komhyr_86.reverse()
pval.reverse()


VecP_ECC6A = [0, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 1100]
VecC_ECC6A_25 = [1.16, 1.16, 1.124, 1.087, 1.054, 1.033, 1.024, 1.015, 1.010, 1.007, 1.005, 1.002, 1, 1]
VecC_ECC6A_30 = [1.171, 1.171, 1.131, 1.092, 1.055, 1.032, 1.022, 1.015, 1.011, 1.008, 1.006, 1.004, 1, 1]

VecP_MAST = [0, 3, 5, 10, 20, 30, 50, 100, 200, 1100]
VecC_MAST = [1.177, 1.177, 1.133, 1.088, 1.053, 1.037, 1.020, 1.004, 1, 1]

# SensorType = 'DMT-Z'
VecP_ECCZ = [0, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 1100]
VecC_ECCZ = [1.24, 1.24, 1.124, 1.087, 1.066, 1.048, 1.041, 1.029, 1.018, 1.013, 1.007, 1.002, 1, 1]

K = 273.15
k = 273.15


def organize_df(df1, df2):
    '''
    searches for patterns to read metadata and writes them into a new dataframe
    :param df1: main data dataframe in pandas format
    :param df2: metadata dataframe in pandas format
    :return: df_out: a dataframe that has data and the metadata
    '''

    df_out = pd.DataFrame()
    dfm_out = pd.DataFrame()

    list1 = list(df1)
    for i in range(len(list1)):

        if (search('Temperature', list1[i])) and (search('inside', list1[i])):
            pump_temp = list1[i]
            df_out['TboxK'] = df1[pump_temp].astype('float') + K
            df_out['TboxC'] = df1[pump_temp].astype('float')

        if (search('Time', list1[i])) and (search('after', list1[i])):
            time = list1[i]
            df_out['Time'] = df1[time]

        if (search('Geopotential', list1[i])) and (search('height', list1[i])):
            height = list1[i]
            df_out['Height'] = df1[height]

        if (search('wind ', list1[i])) and (search('direction', list1[i])):
            windd = list1[i]
            df_out['WindDirection'] = df1[windd]

        if (search('wind ', list1[i])) and (search('speed', list1[i])):
            winds = list1[i]
            df_out['WindSpeed'] = df1[winds]

        if (search('ressure ', list1[i])) and (search('observation', list1[i])):
            pair = list1[i]
            df_out['Pair'] = df1[pair].astype('float')

    list2 = list(df2)
    for j in range(len(list2)):

        if (search('ackground', list2[j])) and (search('before', list2[j])) and (search('exposed', list2[j])):
            bkg = list2[j]
            dfm_out.at[0,'iB0'] = df2.at[df2.first_valid_index(), bkg]

        if (search('ackground', list2[j])) and (search('sensor current', list2[j])) and (
        search('after 10min', list2[j])):
            bkg = list2[j]
            dfm_out.at[0,'iB1'] = df2.at[df2.first_valid_index(), bkg]

        if (search('ackground', list2[j])) and (search('end', list2[j])) and (search('pre-flight', list2[j])):
            bkg = list2[j]
            dfm_out.at[0,'iB2'] = df2.at[df2.first_valid_index(), bkg]

        if (search('ackground', list2[j])) and (search('launch', list2[j])  and
                                                ( (search('current', list2[j])) or (search('b2', list2[j]))) ):
            bkg = list2[j]
            dfm_out.at[0,'iB2'] = df2.at[df2.first_valid_index(), bkg]

        dfm_out.at[0,'BkgUsed'] = 'Constant'
        if (search('ackground', list2[j])) and (search('current', list2[j])) and (search('used', list2[j])) and (
        search('computation', list2[j])):
            bkg = list2[j]
            # print('in function', bkg)
            dfm_out.at[0,'BkgUsed'] = df2.at[df2.first_valid_index(), bkg]

        if ((search('Sensor', list2[j])) and (search('air', list2[j])) and (search('flow', list2[j]))) and \
                not (search('calibrator', list2[j])):
            pumpt = list2[j]
            dfm_out.at[0,'PF'] = df2.at[df2.first_valid_index(), pumpt]

        if (search('pump flow rate', list2[j])):
            dfm_out.at[0,'PF'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('emperature during flow rate measurement', list2[j])):
            dfm_out.at[0,'TLab'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('elative humidity during flow rate measurement', list2[j])):
            dfm_out.at[0,'RHLab'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('umidity correction factor to flow rate', list2[j])):
            dfm_out.at[0,'RHCor'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Solution amount', list2[j])):
            dfm_out.at[0,'SolutionVolume'] = df2.at[df2.first_valid_index(),  list2[j]]

        if (search('Buffer amount', list2[j])):
            dfm_out.at[0,'buffer'] = df2.at[df2.first_valid_index(),  list2[j]]
        if (search('KBr amount', list2[j])):
            dfm_out.at[0,'kbr'] = df2.at[df2.first_valid_index(),  list2[j]]


        if (search('Surface pressure', list2[j])):
            dfm_out.at[0, 'GroundPre'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Surface temperature', list2[j])):
            dfm_out.at[0, 'GroundTemp'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Surface humidity', list2[j])):
            dfm_out.at[0, 'GroundRH'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Serial number of ozonesonde', list2[j])):
            dfm_out.at[0, 'SondeSerial'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Radiosonde type', list2[j])):
            dfm_out.at[0, 'RSType'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Radiosonde type', list2[j])):
            dfm_out.at[0, 'RSType'] = df2.at[df2.first_valid_index(), list2[j]]


        if (search('Serial number', list2[j])) and ((search('RS-80', list2[j]))):
            rs80 = 'RS80'
            dfm_out.at[0,'RadiosondeModel'] = rs80

        if (search('Serial number', list2[j])) and (
                (search('RS', list2[j])) or (search('radiosonde', list2[j])) or (search('Radiosonde', list2[j]))):
            try:
                dfm_out.at[0,'RadiosondeSerial'] = df2.at[df2.first_valid_index(), list2[j]]
            except KeyError:
                dfm_out.at[0,'RadiosondeSerial'] = '9999'

        if ((search('interface', list2[j]) or (search('Interface', list2[j]))) and not (search('parameter', list2[j]))):
            dfm_out.at[0,'InterfaceSerial'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Surface', list2[j])) or ((search('surface', list2[j])) and (search('ozone', list2[j])) or
                                             (search('Ozone', list2[j]))) and not (search('Time', list2[j])) and not (
        search('sensor', list2[j])):
            dfm_out.at[0,'SurfaceOzone'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('round equipment', list2[j])) or (search('equipment', list2[j])):
            dfm_out.at[0,'GroundEquipment'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Correction factor ', list2[j])) or (search('correction factor', list2[j])):
            dfm_out.at[0,'CorrectionFactor'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Total ozone', list2[j])) and (search('sonde', list2[j])):
            dfm_out.at[0,'SondeTotalO3'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Total ozone', list2[j])) and (search('Dobson/Brewer', list2[j])) and (search('COL2A', list2[j])):
            dfm_out.at[0,'TotalO3_Col2A'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Total ozone', list2[j])) and (search('Dobson/Brewer', list2[j])) and (search('COL2B', list2[j])):
            dfm_out.at[0,'TotalO3_Col2B'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Background', list2[j])) and (search('correction', list2[j])):
            print(list2[j])
            dfm_out.at[0,'BackgroundCorrection'] = df2.at[df2.first_valid_index(), list2[j]]
            # print(df2.at[df2.first_valid_index(), list2[j]])

        if (search('Launch time', list2[j])):
            dfm_out.at[0,'LaunchTime'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Hour of launch', list2[j])):
            dfm_out.at[0,'HourLaunchTime'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Minute of launch', list2[j])):
            dfm_out.at[0,'MinuteLaunchTime'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Longitude', list2[j])) or (search('longitude', list2[j])):
            dfm_out.at[0,'Longitude'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Latitude', list2[j])) or (search('latitude', list2[j])):
            dfm_out.at[0,'Latitude'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Time', list2[j])) and (search('sonde', list2[j])) and (search('surface ozone', list2[j])):
            dfm_out.at[0,'DurationSurfaceOzoneExposure'] = df2.at[df2.first_valid_index(), list2[j]]
            # 'Time the sonde was run for surface ozone (min)'

        if not ((search('Ozone', list2[j])) and (search('sensor', list2[j]))) and (
        search('Serial number of ECC', list2[j])):
            serial = list2[j]
            dfm_out.at[0,'SerialECC'] = df2.at[df2.first_valid_index(), serial]
            if (df2.at[df2.first_valid_index(), serial][0] == "z") | (df2.at[df2.first_valid_index(), serial][0] == "Z") \
                    | (df2.at[df2.first_valid_index(), serial][1] == "Z") | (
                    df2.at[df2.first_valid_index(), serial][1] == "z"):
                dfm_out.at[0,'SensorType'] = 'DMT-Z'
            if (df2.at[df2.first_valid_index(), serial][0] == "4"): dfm_out.at[0,'SensorType'] = 'SPC-4A'
            if (df2.at[df2.first_valid_index(), serial][0] == "5"): dfm_out.at[0,'SensorType'] = 'SPC-5A'
            if (df2.at[df2.first_valid_index(), serial][0] == "6"): dfm_out.at[0,'SensorType'] = 'SPC-6A'

        if (search('Serial number of ECC', list2[j])):
            serial = list2[j]
            if (df2.at[df2.first_valid_index(), serial][0] == "z") | (df2.at[df2.first_valid_index(), serial][0] == "Z") \
                    | (df2.at[df2.first_valid_index(), serial][1] == "Z") | (
                    df2.at[df2.first_valid_index(), serial][1] == "z"):
                dfm_out.at[0,'SensorType'] = 'DMT-Z'
            if (df2.at[df2.first_valid_index(), serial][0] == "4"): dfm_out.at[0,'SensorType'] = 'SPC-4A'
            if (df2.at[df2.first_valid_index(), serial][0] == "5"): dfm_out.at[0,'SensorType'] = 'SPC-5A'
            if (df2.at[df2.first_valid_index(), serial][0] == "6"): dfm_out.at[0,'SensorType'] = 'SPC-6A'

        if (search('Ozone', list2[j])) and (search('sensor', list2[j])):
            serial = list2[j]

            # print('ozone sensor type', list2[j], df2.at[df2.first_valid_index(),serial][-1])
            if (df2.at[df2.first_valid_index(), serial][0] == "z") | (df2.at[df2.first_valid_index(), serial][0] == "Z") \
                    | (df2.at[df2.first_valid_index(), serial][1] == "Z") | (
                    df2.at[df2.first_valid_index(), serial][1] == "z") | (
                    df2.at[df2.first_valid_index(), serial][-1] == "Z"):
                dfm_out.at[0,'SensorType'] = 'DMT-Z'
                # print('why not', dfm_out.at[0,'SensorType'])
            if (df2.at[df2.first_valid_index(), serial][0] == "4"): dfm_out.at[0,'SensorType'] = 'SPC-4A'
            if (df2.at[df2.first_valid_index(), serial][0] == "5"): dfm_out.at[0,'SensorType'] = 'SPC-5A'
            if (df2.at[df2.first_valid_index(), serial][0] == "6"): dfm_out.at[0,'SensorType'] = 'SPC-6A'

        if (search('Background', list2[j])) and (search('surface pressure', list2[j])):
            pground = list2[j]
            dfm_out.at[0,'Pground'] = df2.at[df2.first_valid_index(), pground]
            if (float(df2.at[df2.first_valid_index(), pground]) > 1090) | (
                    float(df2.at[df2.first_valid_index(), pground]) < 900):
                dfm_out.at[0,'Pground'] = 1000

        if (search('Surface pressure', list2[j])) and (search('sonde flow', list2[j])):
            pground = list2[j]
            dfm_out.at[0,'Pground'] = df2.at[df2.first_valid_index(), pground]
            # if (float(df2.at[df2.first_valid_index(), pground]) > 1090) | (
            #         float(df2.at[df2.first_valid_index(), pground]) < 900):
            #     dfm_out.at[0,'Pground'] = 1000

        if (search('Amount', list2[j])) and (search('cathode', list2[j])):
            cathodesol = list2[j]
            dfm_out.at[0,'SolutionVolume'] = df2.at[df2.first_valid_index(), cathodesol]

        if (search('Concentration', list2[j])) and (search('cathode', list2[j])):
            cathodecon = list2[j]
            dfm_out.at[0,'SolutionConcentration'] = df2.at[df2.first_valid_index(), cathodecon]

        if (search('Place', list2[j])) and (search('box', list2[j])) and (search('measurement', list2[j])):
            pt_location = list2[j]
            dfm_out.at[0,'PumpTempLoc'] = df2.at[df2.first_valid_index(), pt_location]

        if (search('Temperature', list2[j])) and (search('laboratory', list2[j])) and (search('during', list2[j])) and (
        search('sonde', list2[j])):
            t_lab = list2[j]
            dfm_out.at[0,'TLab'] = df2.at[df2.first_valid_index(), t_lab]

        if (search('Relative humidity', list2[j])) and (search('laboratory', list2[j])) and (
        search('during', list2[j])) and (search('sonde', list2[j])):
            u_lab = list2[j]
            dfm_out.at[0,'ULab'] = df2.at[df2.first_valid_index(), u_lab]

        if (search('Pump', list2[j])) and (search('correction', list2[j])):
            pump_table = list2[j]
            dfm_out.at[0,'PumpTable'] = df2.at[df2.first_valid_index(), pump_table]
    try:
        df_out['O3'] = df1['Ozone partial pressure (mPa)'].astype('float')
    except KeyError:
        df_out['O3'] = df1['PO3'].astype('float')

    try:
        df_out['T'] = df1['Temperature (C)'].astype('float')
    except KeyError:
        df1['Temp'].astype('float')

    try:
        df_out['U'] = df1['Relative humidity (%)'].astype('float')
    except KeyError:
        df_out['U'] = df1['RH'].astype('float')

    #     dfm_out['LaunchTime'] = dfm_out['LaunchTime'].astype('str')
    # except KeyError:
    #     df_out['O3'] = df1['PO3'].astype('float')
    #     df_out['T'] = df1['Temp'].astype('float')
    #     df_out['U'] = df1['RH'].astype('float')
    #     df_out['TboxK'] = df1['TPump'].astype('float')
    #     df_out['TboxC'] = df1['TPump'].astype('float') - K
    #     df_out['I'] = df1['I'].astype('float')
    #     df_out['Alt'] = df1['Alt'].astype('float')
    #     df_out['GPSAlt'] = df1['GPSAlt'].astype('float')


        dfm_out['LaunchTime'] = dfm_out['LaunchTime'].astype('str')

    if ( dfm_out.at[0, 'buffer'] == '1.00') & (dfm_out.at[0, 'kbr'] == '1.00'):
        dfm_out.at[0, 'SolutionConcentration'] = 10

    # in case there is no PF it is written to 9999

    # dfm_out['Pground'] = dfm_out['Pground'].astype('float')
    # dfm_out['SolutionConcentration'] = dfm_out['SolutionConcentration'].astype('float')
    # dfm_out['SolutionVolume'] = dfm_out['SolutionVolume'].astype('float')
    # dfm_out['TLab'] = dfm_out['TLab'].astype('float')

    try:
        dfm_out['PF'] = dfm_out['PF'].astype('float')
    except KeyError:
        dfm_out['PF'] = 28
    # in case there is no iB0 or iB2 it is written to 9999
    try:
        dfm_out['iB0'] = dfm_out['iB0'].astype('float')
    except KeyError:
        dfm_out['iB0'] = 9999
    try:
        dfm_out['iB2'] = dfm_out['iB2'].astype('float')
    except KeyError:
        dfm_out['iB2'] = 9999
    # df_out['Cef'] = 1

    return df_out, dfm_out


def organize_df_nya(df1, df2,dates):
    '''
    searches for patterns to read metadata and writes them into a new dataframe
    :param df1: main data dataframe in pandas format
    :param df2: metadata dataframe in pandas format
    :return: df_out: a dataframe that has data and the metadata
    '''

    df_out = df1.copy()
    dfm_out = pd.DataFrame()

    list1 = list(df1)

    # df1 = df1[]

    if dates <= '20170313':

        df_out['TboxC'] = df_out['TPump']
        df_out['TboxK'] = df_out['TPump']

        # df_out[(df_out.TboxK > K) & (df_out.TboxK < 999)]['TboxK'] = df_out[(df_out.TboxK > K) & (df_out.TboxK < 999)][
        #     'TboxK']
        df_out.loc[(df_out.TboxK < 150), 'TboxK'] = df_out.loc[(df_out.TboxK < 150), 'TboxK'] + K

        # df_out[(df_out.TboxC < K)]['TboxC'] = df_out[(df_out.TboxC < K)]['TboxC']
        df_out.loc[(df_out.TboxC > 50) & (df_out.TboxC < 999), 'TboxC'] = df_out.loc[(df_out.TboxC > K) & (df_out.TboxC < 999),
                                                                         'TboxC'] - K
        # for i in range(len(list1)):

            # if (search('TPump', list1[i])):
            #     pump_temp = list1[i]
            #     df1 = df1[df1.pump_temp != 999.9]
            #     print('temp', df1.at[df1.first_valid_index(),pump_temp])
            #     if (df1[df1[pump_temp] < K]):
            #         df_out['TboxK'] = df1[pump_temp].astype('float') + K
            #         df_out['TboxC'] = df1[pump_temp].astype('float')
            #     if (df1.at[df1.first_valid_index(),pump_temp] > K) and (df1.at[df1.first_valid_index(),pump_temp] < 999):
            #         df_out['TboxK'] = df1[pump_temp].astype('float')
            #         df_out['TboxC'] = df1[pump_temp].astype('float') - K

        list2 = list(df2)
        for j in range(len(list2)):

            dfm_out.at[0, 'buffer'] = '0'
            dfm_out.at[0, 'kbr'] = '0'

            if (search('our of launch', list2[j])) :
                dfm_out.at[0,'HourLaunch'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('inute of launch', list2[j])) :
                dfm_out.at[0,'MinuteLaunch'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('ongitude', list2[j])) and (search('station', list2[j])):
                dfm_out.at[0,'Lon'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('atitude', list2[j])) and (search('station', list2[j])):
                dfm_out.at[0,'Lat'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('mount', list2[j])) and (search('cathode', list2[j]) and (search('solution',list2[j]))):
                dfm_out.at[0,'SolutionVolume'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('air flow', list2[j])) and not (search('calibrator', list2[j])):
                dfm_out.at[0,'PF'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('ackground', list2[j])) and (search('sensor current', list2[j])) and (
            search('before', list2[j])):
                dfm_out.at[0,'iB0'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('ackground', list2[j])) and (search('end', list2[j])) and (search('pre-flight', list2[j])):
                bkg = list2[j]
                dfm_out.at[0,'iB2'] = df2.at[df2.first_valid_index(), bkg]

            if (search('ackground', list2[j])) and (search('surface', list2[j])) and (search('pressure', list2[j])):
                dfm_out.at[0,'SurfacePressure'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('ressure', list2[j])) and (search('corection', list2[j])) and (search('ground', list2[j])):
                dfm_out.at[0,'PCor'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('emperature', list2[j])) and (search('corection', list2[j])) and (search('ground', list2[j])):
                dfm_out.at[0, 'TCor'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('umidity', list2[j])) and (search('corection', list2[j])):
                dfm_out.at[0, 'RHCor'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('otal', list2[j])) and (search('ozone', list2[j])) and (search('COL2A', list2[j])):
                dfm_out.at[0, 'TotalO3_Col2A'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('otal', list2[j])) and (search('ozone', list2[j])) and (search('COL2B', list2[j])):
                dfm_out.at[0, 'TotalO3_Col2B'] = df2.at[df2.first_valid_index(), list2[j]]



            dfm_out.at[0,'BkgUsed'] = 'Constant'
            if (search('ackground', list2[j])) and (search('current', list2[j])) and (search('used', list2[j])) and (
            search('computation', list2[j])):
                bkg = list2[j]
                # print('in function', bkg)
                dfm_out.at[0,'BkgUsed'] = df2.at[df2.first_valid_index(), bkg]

            if (search('emperature', list2[j])) and (search('laboratory', list2[j])):
                dfm_out.at[0,'TLab'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('elative humidity', list2[j])) and (search('laboratory during sonde flow', list2[j])) :
                dfm_out.at[0,'RHLab'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('Serial number of', list2[j])) and (search('ECC',list2[j])):
                dfm_out.at[0, 'SondeSerial'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('Radiosonde type', list2[j])):
                dfm_out.at[0, 'RSType'] = df2.at[df2.first_valid_index(), list2[j]]


            if (search('oncentration', list2[j])) and (search('cathode', list2[j])):
                dfm_out.at[0, 'SolutionConcentration'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('ECC', list2[j])) and (search('erial', list2[j])):
                serial = list2[j]
                # print('ozone sensor type', list2[j], df2.at[df2.first_valid_index(),serial][-1])
                if (df2.at[df2.first_valid_index(), serial][0] == "z") | (
                        df2.at[df2.first_valid_index(), serial][0] == "Z") \
                        | (df2.at[df2.first_valid_index(), serial][1] == "Z") | (
                        df2.at[df2.first_valid_index(), serial][1] == "z") | (
                        df2.at[df2.first_valid_index(), serial][-1] == "Z"):
                    dfm_out.at[0, 'SensorType'] = 'DMT-Z'
                    # print('why not', dfm_out.at[0,'SensorType'])
                if (df2.at[df2.first_valid_index(), serial][0] == "4"): dfm_out.at[0, 'SensorType'] = 'SPC-4A'
                if (df2.at[df2.first_valid_index(), serial][0] == "5"): dfm_out.at[0, 'SensorType'] = 'SPC-5A'
                if (df2.at[df2.first_valid_index(), serial][0] == "6"): dfm_out.at[0, 'SensorType'] = 'SPC-6A'




    if dates >= '20170313':
        # for i in range(len(list1)):
        #
        #     if (search('TPump', list1[i])):
        #         pump_temp = list1[i]
        #         if (df1.at[10,pump_temp] < K):
        #             df_out['TboxK'] = df1[pump_temp].astype('float') + K
        #             df_out['TboxC'] = df1[pump_temp].astype('float')
        #         if (df1.at[10,pump_temp] > K):
        #             df_out['TboxK'] = df1[pump_temp].astype('float')
        #             df_out['TboxC'] = df1[pump_temp].astype('float') - K
        df_out['TboxC'] = df_out['TPump']
        df_out['TboxK'] = df_out['TPump']

        # df_out.loc[(df_out.TboxK > K ) & (df_out.TboxK < 999), 'TboxK'] = \
        #     df_out.loc[(df_out.TboxK > K ) & (df_out.TboxK < 999), 'TboxK']
        df_out.loc[(df_out.TboxK < 150 ), 'TboxK'] = df_out.loc[(df_out.TboxK < 150 ), 'TboxK'] + K

        # df_out.loc[(df_out.TboxC < K ), 'TboxC'] = df_out.loc[ (df_out.TboxC < K ), 'TboxC']
        df_out.loc[(df_out.TboxC > 50 ) & (df_out.TboxC < 999), 'TboxC'] = \
            df_out.loc[ (df_out.TboxC > 50 ) & (df_out.TboxC < 999), 'TboxC'] - K


        list2 = list(df2)
        for j in range(len(list2)):

            dfm_out.at[0, 'buffer'] = '0'
            dfm_out.at[0, 'kbr'] = '0'

            if (search('Launch time', list2[j])):
                dfm_out.at[0, 'LaunchTime'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('Inverse pump flow rate', list2[j])):
                dfm_out.at[0, 'PF'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('Temperature during flow rate measurement', list2[j])):
                dfm_out.at[0, 'TLab'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('Relative humidity during flow rate', list2[j])):
                dfm_out.at[0, 'RHLab'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('umidity correction', list2[j])):
                dfm_out.at[0, 'RHCor'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('Ib0', list2[j])):
                dfm_out.at[0, 'iB0'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('Ib1', list2[j])):
                dfm_out.at[0, 'iB1'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('Ib2', list2[j])):
                dfm_out.at[0, 'iB2'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('Buffer amount', list2[j])):
                dfm_out.at[0, 'buffer'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('KBr amount', list2[j])):
                dfm_out.at[0, 'kbr'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('mount', list2[j])) and (search('olution',list2[j])):
                dfm_out.at[0,'SolutionVolume'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('urface pressure correction', list2[j])) :
                dfm_out.at[0,'PCor'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('urface temperature correction', list2[j])) :
                dfm_out.at[0,'TCor'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('urface humidity correction', list2[j])) :
                dfm_out.at[0,'RHCor'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('urface pressure', list2[j])) :
                dfm_out.at[0,'PLab'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('Background subtraction', list2[j])):
                # print('here', list2[j])
                dfm_out.at[0, 'BkgCorrection'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('Background subtracted', list2[j])):
                # print('here', list2[j])
                dfm_out.at[0, 'BkgCorrectionBool'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('Serial number of ozonesonde', list2[j])):
                dfm_out.at[0, 'SondeSerial'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('Radiosonde type', list2[j])):
                dfm_out.at[0, 'RSType'] = df2.at[df2.first_valid_index(), list2[j]]
            if (search('Serial number of radiosonde', list2[j])):
                dfm_out.at[0, 'RSSerial'] = df2.at[df2.first_valid_index(), list2[j]]

            if (search('ozonesonde', list2[j])) and (search('erial', list2[j])):
                serial = list2[j]
                # print('ozone sensor type', list2[j], df2.at[df2.first_valid_index(),serial][-1])
                if (df2.at[df2.first_valid_index(), serial][0] == "z") | (
                        df2.at[df2.first_valid_index(), serial][0] == "Z") \
                        | (df2.at[df2.first_valid_index(), serial][1] == "Z") | (
                        df2.at[df2.first_valid_index(), serial][1] == "z") | (
                        df2.at[df2.first_valid_index(), serial][-1] == "Z"):
                    dfm_out.at[0, 'SensorType'] = 'DMT-Z'
                    # print('why not', dfm_out.at[0,'SensorType'])
                if (df2.at[df2.first_valid_index(), serial][0] == "4"): dfm_out.at[0, 'SensorType'] = 'SPC-4A'
                if (df2.at[df2.first_valid_index(), serial][0] == "5"): dfm_out.at[0, 'SensorType'] = 'SPC-5A'
                if (df2.at[df2.first_valid_index(), serial][0] == "6"): dfm_out.at[0, 'SensorType'] = 'SPC-6A'


    if ( dfm_out.at[0, 'buffer'] == '1.00') & (dfm_out.at[0, 'kbr'] == '1.00'):
        dfm_out.at[0, 'SolutionConcentration'] = 10

    try:
        dfm_out['PF'] = dfm_out['PF'].astype('float')
    except KeyError:
        dfm_out['PF'] = 27.5
        # in case there is no iB0 or iB2 it is written to 9999
    try:
        dfm_out['iB0'] = dfm_out['iB0'].astype('float')
    except KeyError:
        dfm_out['iB0'] = 9999
    try:
        dfm_out['iB2'] = dfm_out['iB2'].astype('float')
    except KeyError:
        dfm_out['iB2'] = 9999

    return df_out, dfm_out

def missing_tpump(dfl):

    dfl.loc[dfl['TboxC'] > 99, 'value_is_NaN'] = 1
    dfl.loc[dfl['TboxC']< 99, 'value_is_NaN'] = 0

    pair_missing = dfl[dfl.TboxC > 99].TboxC.tolist()


    if len(pair_missing) > 0:
        # print('no sample temperature', len(pair_missing), len(dfl))

        x = dfl[dfl.value_is_NaN == 0]['TboxC'].tolist()
        y = dfl[dfl.value_is_NaN == 0]['Pair'].tolist()
        fb = interp1d(y, x)

        df_pair = dfl[dfl.value_is_NaN == 1].Pair.tolist()

        # print('min dfpair', min(df_pair), 'min y', min(y))
        # print('max dfpair', max(df_pair), 'max y', max(y))


        if min(df_pair) < min(y):
            df_pair = dfl[(dfl.value_is_NaN == 1) & (dfl.Pair >= min(y))].Pair.tolist()
            df_samptemp = fb(df_pair)
            dfl.loc[(dfl.value_is_NaN == 1) & (dfl.Pair >= min(y)), 'TboxC'] = df_samptemp
            dfl.loc[dfl.value_is_NaN == 1, 'TboxK'] = df_samptemp + k


        elif max(df_pair) > max(y):
            df_pair = dfl[(dfl.value_is_NaN == 1) & (dfl.Pair < max(y))].Pair.tolist()
            df_samptemp = fb(df_pair)
            dfl.loc[(dfl.value_is_NaN == 1) & (dfl.Pair < max(y)), 'TboxC'] = df_samptemp
            dfl.loc[dfl.value_is_NaN == 1, 'TboxK'] = df_samptemp + k


        else:
            df_pair = dfl[(dfl.value_is_NaN == 1)].Pair.tolist()
            fb = interp1d(y, x)
            df_samptemp = fb(df_pair)

            dfl.loc[dfl.value_is_NaN == 1, 'TboxC'] = df_samptemp
            # dfl.loc[dfl.value_is_NaN == 1, 'TboxC'] = df_samptemp
            dfl.loc[dfl.value_is_NaN == 1, 'TboxK'] = df_samptemp + k


    return dfl


def o3tocurrent(dft, dfm, dfmmain):
    '''

    :param dft: data df
    :param dfm: metadata df
    :return: dft
    '''
    # o3(mPa) = 4.3087 * 10e-4 * (i - ibg) * tp * t * cef * cref
    # tp: pump temp. in K, t: pumping time for 100 ml of air in seconds, cef: correction due to reduced ambient pressure for pump
    # cref: additional correction factor
    # i = o3 / (4.3087 * 10e-4 * tp * t * cef * cref ) + ibg

    sensortype = dfm.at[dfm.first_valid_index(), 'SensorType']
    # print(sensortype)

    enscitag = (search('DMT-Z', sensortype)) or (search('Z', sensortype)) or (search('ECC6Z', sensortype)) or (
        search('_Z', sensortype))
    if enscitag:
        dft['SensorType'] = 'DMT-Z'
        dfm['SensorType'] = 'DMT-Z'
    spctag = (search('SPC', sensortype)) or (search('4A', sensortype)) or (search('5A', sensortype)) or (
        search('6A', sensortype))
    if spctag:
        dft['SensorType'] = 'SPC'
        dfm['SensorType'] = 'SPC'

        # check PF values
    if (dfm.at[dfm.first_valid_index(), 'PF'] > 35) | (dfm.at[dfm.first_valid_index(), 'PF'] < 20): dfm.at[
        dfm.first_valid_index(), 'PF'] = dfmmain.PF.mean()

    dft['Cef'] = ComputeCef(dft,dfm)

    cref = 1
    dft['ibg'] = 0
    dft['ibg_tmp'] = 0

    dft['iB2'] = dfm.at[dfm.first_valid_index(), 'iB2']
    dft['iB0'] = dfm.at[dfm.first_valid_index(), 'iB0']

    # # # by default uses iB2 as background current

    dfmmain['Date2'] = dfmmain['Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
    dfmmain['Date3'] = dfmmain['Date2'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))

    dfm_date = dfm.at[dfm.first_valid_index(), 'Date']

    #if iB2 is missing uses mean of the iB2
    if (dfm.at[dfm.first_valid_index(), 'iB2'] > 0.9):
        # print('here bad ib2', dfm.at[dfm.first_valid_index(), 'iB2'],
        #       dfm_date, dfmmain.loc[dfmmain.Date3 == dfm_date, 'ib2_mean'])
        # print(dfmmain[['Date','Date2','Date3']][0:4])

        dfm['iB2'] = dfmmain.loc[dfmmain.Date3 == dfm_date, 'ib2_mean']



    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': dft['ibg'] = ComputeIBG(dft, 'iB2')
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB2']

    #if iB2 values are missing
    # if  (dfm.at[dfm.first_valid_index(), 'iB0'] < 0.9) & (dfm.at[dfm.first_valid_index(), 'iB2'] > 0.9):
    #     dfm['BkgUsed'] = 'Ibg1'

    # # # if it was mentioned that BkgUsed is Ibg1, then iB0 is used
    # if (dfm.at[dfm.first_valid_index(), 'BkgUsed'] == 'Ibg1') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z'):
    #     dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB0']
    # if (dfm.at[dfm.first_valid_index(), 'BkgUsed'] == 'Ibg1') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC'):
    #     dft['ibg'] = ComputeIBG(dft, 'iB0')

    dft['I'] = dft['O3'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dfm.at[dfm.first_valid_index(), 'PF'] * dft['Cef'] * cref) + dft['ibg']


    return dft

def o3tocurrent_nya(dft, dfm, dfmmain):
    '''

    :param dft: data df
    :param dfm: metadata df
    :return: dft
    '''
    # o3(mPa) = 4.3087 * 10e-4 * (i - ibg) * tp * t * cef * cref
    # tp: pump temp. in K, t: pumping time for 100 ml of air in seconds, cef: correction due to reduced ambient pressure for pump
    # cref: additional correction factor
    # i = o3 / (4.3087 * 10e-4 * tp * t * cef * cref ) + ibg

    # dft.loc[dft.TboxK < K, 'TboxK'] = dft.loc[dft.TboxK < K, 'TboxK'] + K


    sensortype = dfm.at[dfm.first_valid_index(), 'SensorType']
    # print(sensortype)

    enscitag = (search('DMT-Z', sensortype)) or (search('Z', sensortype)) or (search('ECC6Z', sensortype)) or (
        search('_Z', sensortype))
    if enscitag:
        dft['SensorType'] = 'DMT-Z'
        dfm['SensorType'] = 'DMT-Z'
    spctag = (search('SPC', sensortype)) or (search('4A', sensortype)) or (search('5A', sensortype)) or (
        search('6A', sensortype))
    if spctag:
        dft['SensorType'] = 'SPC'
        dfm['SensorType'] = 'SPC'

        # check PF values
    if (dfm.at[dfm.first_valid_index(), 'PF'] > 35) | (dfm.at[dfm.first_valid_index(), 'PF'] < 20): dfm.at[
        dfm.first_valid_index(), 'PF'] = dfmmain.PFcurrent.mean()

    dft['Cef'] = ComputeCef(dft,dfm)

    cref = 1
    dft['ibg'] = 0
    dft['ibg_tmp'] = 0

    dfm_date = int(dfm.at[dfm.first_valid_index(), 'Date'])

    # print('dfm_date', dfm_date, type(dfm_date))

    # dfm['iB2current'] = dfmmain.loc[dfmmain.Date == dfm_date,'iB2current']
    dfm['PFcurrent'] = dfmmain.loc[dfmmain.Date == dfm_date,'PFcurrent']

    dft['iB2'] = dfmmain.loc[dfmmain.Date == dfm_date,'iB2']
    dfm['iB2'] = dfmmain.loc[dfmmain.Date == dfm_date,'iB2']

    # dft['iB0'] = dfm.at[dfm.first_valid_index(), 'iB0']

    # # # by default uses iB2 as background current

    dfmmain['Date2'] = dfmmain['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
    dfmmain['Date3'] = dfmmain['Date2'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))

    # dfm2 = dfmmain[dfmmain.Date == dfm_date]
    #
    #
    # dfm['ULab'] = dfm2['RHLab']
    # dfmmain['ULab'] = dfmmain['RHLab']
    # dfmmain = calculate_cph(dfmmain)
    #
    # dfmmain.loc[:, 'unc_cPH'] = dfmmain['cPH'].std()
    # dfmmain.loc[:, 'unc_cPL'] = dfmmain['cPL'].std()
    dfm2 = dfmmain[dfmmain.Date == dfm_date]

    # dft['dPhip'] = 0.02
    # dft['unc_cPH'] = dfm2.at[dfm2.first_valid_index(), 'unc_cPH']
    # dft['unc_cPL'] = dfm2.at[dfm2.first_valid_index(), 'unc_cPL']
    #
    try:    dft['Pground'] = dfm2.at[dfm2.first_valid_index(),'PLab']
    except KeyError: dft['Pground'] = dfmmain.PLab.median()
    try:    dft['iB2'] = dfm2.at[dfm2.first_valid_index(),'iB2']
    except KeyError: dft['iB2'] = dfmmain.iB2.median()


    #if iB2 is missing uses mean of the iB2
    if (dfm.at[dfm.first_valid_index(), 'iB2'] > 0.9):
        print('here bad ib2', dfm.at[dfm.first_valid_index(), 'iB2'])
        #       dfm_date, dfmmain.loc[dfmmain.Date3 == dfm_date, 'ib2_mean'])
        # print(dfmmain[['Date','Date2','Date3']][0:4])

        dfm['iB2'] = dfmmain.loc[dfmmain.Date3 == dfm_date, 'ib2_mean']

        dft['iB2'] = dfmmain.loc[dfmmain.Date3 == dfm_date, 'ib2_mean']

    # dft['Pground'] = dft['PLab']
    # if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC':
    dft['ibg'] = ComputeIBG(dft, 'iB2')
    # if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB2current']

    #if iB2 values are missing
    # if  (dfm.at[dfm.first_valid_index(), 'iB0'] < 0.9) & (dfm.at[dfm.first_valid_index(), 'iB2'] > 0.9):
    #     dfm['BkgUsed'] = 'Ibg1'

    # # # if it was mentioned that BkgUsed is Ibg1, then iB0 is used
    # if (dfm.at[dfm.first_valid_index(), 'BkgUsed'] == 'Ibg1') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z'):
    #     dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB0']
    # if (dfm.at[dfm.first_valid_index(), 'BkgUsed'] == 'Ibg1') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC'):
    #     dft['ibg'] = ComputeIBG(dft, 'iB0')

    try: dft['PFcurrent'] = dfm2.at[dfm2.first_valid_index(), 'PFcurrent']
    except KeyError: dft['PFcurrent'] = dfmmain.PFcurrent.median()
    dft['Phip'] = 100/dft.at[dft.first_valid_index(), 'PFcurrent']

    try: dfm['PFcurrent'] = dfm2.at[dfm2.first_valid_index(), 'PFcurrent']
    except KeyError: dfm['PFcurrent'] = dfmmain.PFcurrent.median()
    try: dfm['PLab'] = dfm2.at[dfm2.first_valid_index(), 'PLab']
    except KeyError: dfm['PLab'] = dfmmain.PLab.median()
    try: dfm['TLab'] = dfm2.at[dfm2.first_valid_index(), 'TLab']
    except KeyError: dfm['TLab'] = dfmmain.TLab.median()
    try: dfm['ULab'] = dfm2.at[dfm2.first_valid_index(), 'ULab']
    except KeyError: dfm['ULab'] = dfmmain.ULab.median()


    # # calculate RH humidty correction
    dft['Phip_ground'] = pf_groundcorrection_noerr(dft, dfm, 'Phip', 'dPhip', 'TLab', 'PLab', 'ULab',
                                                                   True)
    dft['PF_ground'] = 100/dft['Phip_ground']

    # dft['Ical'] = dft['O3'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dft.at[dft.first_valid_index(), 'PF_ground']
    # * dft['Cef'] * cref) + dft['ibg']
    dft['Ical'] = dft['O3'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dft.at[dft.first_valid_index(), 'PFcurrent']
                               * dft['Cef'] * cref) + dft['ibg']
    dft['Ical1'] = dft['O3'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dft.at[dft.first_valid_index(), 'PFcurrent']
                                * dft['Cef'] * cref) + dft['iB2']
    dft['Ical2'] = dft['O3'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dft.at[dft.first_valid_index(), 'PF_ground']
                               * dft['Cef'] * cref) + dft['ibg']
    dft['Ical3'] = dft['O3'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dft.at[dft.first_valid_index(), 'PF_ground']
                                * dft['Cef'] * cref) + dft['iB2']

    # dft['Ical3'] = dft['O3'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dft.at[dft.first_valid_index(), 'PF_ground'] * dft['Cef'] * cref) + dft['iB2']


    return dft, dfm


def o3tocurrent_stoich(dft, dfm):
    '''

    :param dft: data df
    :param dfm: metadata df
    :return: dft
    '''
    # o3(mPa) = 4.3087 * 10e-4 * (i - ibg) * tp * t * cef * cref
    # tp: pump temp. in K, t: pumping time for 100 ml of air in seconds, cef: correction due to reduced ambient pressure for pump
    # cref: additional correction factor
    # i = o3 / (4.3087 * 10e-4 * tp * t * cef * cref ) + ibg

    sensortype = dfm.at[dfm.first_valid_index(), 'SensorType']
    # print(sensortype)

    # spctag4A = (search('SPC', sensortype)) or (search('4A', sensortype))
    # if spctag4A: dfm['SensorType'] = 'SPC-4A'
    # spctag5A = (search('SPC', sensortype)) or (search('5A', sensortype))
    # if spctag5A: dfm['SensorType'] = 'SPC-5A'
    # spctag6A = (search('SPC', sensortype)) or (search('6A', sensortype))
    # if spctag6A: dfm['SensorType'] = 'SPC-6A'

    enscitag = (search('DMT-Z', sensortype)) or (search('Z', sensortype)) or (search('ECC6Z', sensortype)) or (
        search('_Z', sensortype))
    if enscitag:
        dft['SensorType'] = 'DMT-Z'
        dfm['SensorType'] = 'DMT-Z'
    spctag = (search('SPC', sensortype)) or (search('4A', sensortype)) or (search('5A', sensortype)) or (
        search('6A', sensortype))
    if spctag:
        dft['SensorType'] = 'SPC'
        dfm['SensorType'] = 'SPC'

        # check PF values
    if (dfm.at[dfm.first_valid_index(), 'PF'] > 40) | (dfm.at[dfm.first_valid_index(), 'PF'] < 20): dfm.at[
        dfm.first_valid_index(), 'PF'] = 28

    dft['Cef'] = ComputeCef(dft,dfm)

    dft['stoich'], dft['unc_stoich'] = stoichmetry_conversion(dft, 'Pair', dfm.at[0, 'SensorType'],
                                                            dfm.at[0, 'SolutionConcentration'], 'SPC10')

    # print(dft.at[10,'stoich'])

    cref = 1
    dft['ibg'] = 0
    dft['ibg_tmp'] = 0

    dft['iB2'] = dfm.at[dfm.first_valid_index(), 'iB2']
    dft['iB0'] = dfm.at[dfm.first_valid_index(), 'iB0']

    # # # by default uses iB2 as background current
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': dft['ibg'] = ComputeIBG(dft, 'iB2')
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB2']

    #if iB2 values are missing use iB0
    if  (dfm.at[dfm.first_valid_index(), 'iB0'] < 0.9) & (dfm.at[dfm.first_valid_index(), 'iB2'] > 0.9):
        dfm['BkgUsed'] = 'Ibg1'

    # # if it was mentioned that BkgUsed is Ibg1, then iB0 is used
    if (dfm.at[dfm.first_valid_index(), 'BkgUsed'] == 'Ibg1') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z'):
        dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB0']
    if (dfm.at[dfm.first_valid_index(), 'BkgUsed'] == 'Ibg1') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC'):
        dft['ibg'] = ComputeIBG(dft, 'iB0')

    dft['O3_uncor'] = dft['O3'] / dft['stoich'] #original


    dft['I'] = dft['O3_uncor'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dfm.at[dfm.first_valid_index(), 'PF'] * dft['Cef'] *
                            cref) + dft['ibg']


    return dft




def ComputeCef(dft, dfm):
    """ Computes pump efficiency correction factor based on pressure

        Arguments:
        Pressure -- air pressure [hPa]
    """
    sensortype = dfm.at[dfm.first_valid_index(), 'SensorType']
    #
    spctag = (search('SPC', sensortype)) or (search('6A', sensortype)) or (search('5A', sensortype)) or (
        search('4A', sensortype))
    if spctag: dft['SensorType'] = 'SPC'
    enscitag = (search('DMT-Z', sensortype)) or (search('Z', sensortype)) or (search('ECC6Z', sensortype)) or (
        search('_Z', sensortype))
    if enscitag: dft['SensorType'] = 'DMT-Z'

    try:
        dft['SolutionVolume'] = dft['SolutionVolume'].astype('float')
    except KeyError:
        dft['SolutionVolume'] = 3.0

    # print(dft.at[dft.first_valid_index(), 'SensorType'],dft.at[dft.first_valid_index(), 'SolutionVolume'] )
    #
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'SPC') and (
            dft.at[dft.first_valid_index(), 'SolutionVolume'] > 2.75):
        dft['Cef'] = VecInterpolate(VecP_ECC6A, VecC_ECC6A_30, dft, 0)
    # if (dft.at[dft.first_valid_index(), 'SensorType'] == 'SPC') and (
    #         dft.at[dft.first_valid_index(), 'SolutionVolume'] > 2.75):
    #     dft['Cef'] = VecInterpolate(pval, komhyr_86, dft, 0)
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'SPC') and (
            dft.at[dft.first_valid_index(), 'SolutionVolume'] < 2.75):
        dft['Cef'] = VecInterpolate(VecP_ECC6A, VecC_ECC6A_25, dft, 0)
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'DMT-Z'):
        dft['Cef'] = VecInterpolate(VecP_ECCZ, VecC_ECCZ, dft, 0)

    return dft['Cef']


def VecInterpolate(XValues, YValues, dft, LOG):
    dft['Cef'] = 0.0

    i = 1
    ilast = len(XValues) - 1
    # return last value if xval out of xvalues range
    y = float(YValues[ilast])

    dft = dft.reset_index()

    for k in range(len(dft)):
        for i in range(len(XValues) - 1):
            # just check that value is in between xvalues
            if (XValues[i] <= dft.at[k, 'Pair'] <= XValues[i + 1]):

                x1 = float(XValues[i])
                x2 = float(XValues[i + 1])
                if LOG == 1:
                    x = math.log(x)
                    x1 = math.log(x1)
                    x2 = math.log(x2)
                y1 = float(YValues[i])
                y2 = float(YValues[i + 1])

                dft.at[k, 'Cef'] = y1 + (dft.at[k, 'Pair'] - x1) * (y2 - y1) / (x2 - x1)

    return dft['Cef']


def ComputeIBG(dft, bkg):
    """ Corrects background current value based on pressure

  Arguments:
  dft  -- dataframe
  ibg  -- background current used
  :returns corrected background current
    """

    try:
        dft['Pcor'] = ComputeCorP(dft, 'Pair') / ComputeCorP(dft, 'Pground')
    except KeyError:
        # dft['Pground'] = 1000
        dft['Pground'] = 997

        dft['Pcor'] = ComputeCorP(dft, 'Pair') / ComputeCorP(dft, 'Pground')

    if bkg == 'iB0': dft.ibg = dft.Pcor * dft.iB0
    if bkg == 'iB2': dft.ibg = dft.Pcor * dft.iB2

    return dft.ibg


def ComputeCorP(dft, Pressure):

    dft['CorP'] = 0
    A0 = 0.0012250380415
    A1 = 0.000124111475632
    A2 = -0.00000002687066130
    dft['CorP'] = A0 + A1 * dft[Pressure].astype('float') + A2 * dft[Pressure].astype('float') * dft[Pressure].astype(
        'float')

    return dft['CorP']
#####################################################################

    # if dfm.at[dfm.first_valid_index(), 'iB0'] == dfm.at[dfm.first_valid_index(), 'iB2']:
    #     dft['ibg_tmp'] = dfm.at[dfm.first_valid_index(), 'iB0']
    # if dfm.at[dfm.first_valid_index(), 'iB2'] > 1:
    #     print('one')
    #     dft['ibg_tmp'] = dfm.at[dfm.first_valid_index(), 'iB2']
    # if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC':
    #     print('why not')
    #     dft['ibg'] = ComputeIBG(dft, 'ibg_tmp')
    # if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z':
    #     print('why not')
    #     dft['ibg'] = dfm.at[dfm.first_valid_index(), 'ibg_tmp']
    # # if dft.at[dft.first_valid_index(), 'ibg'] > 0.9: print('ATTENTION', dft.at[dft.first_valid_index(), 'ibg'])

    # # by default uses iB2 as background current
    # dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB2']
    # if it was mentioned that BkgUsed is Ibg1, then iB0 is used
    # if (dfm.at[dfm.first_valid_index(), 'BkgUsed'] == 'Ibg1') & (
    #         dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z'):
    #     dft['ibg'] = dfm.at[dfm.first_valid_index(), 'ibg_tmp']
    # if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': dft['ibg'] = ComputeIBG(dft, 'ibg_tmp')
    # if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': dft['ibg'] = dfm.at[dfm.first_valid_index(), 'ibg_tmp']