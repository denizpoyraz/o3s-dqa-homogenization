import pandas as pd
import math
from re import search
from scipy.interpolate import interp1d
from datetime import datetime

from dateutil.relativedelta import relativedelta
from typing import Tuple, Union


def decimal_hours_to_HMS(hours: float, as_tuple: bool = False) -> Union[str, Tuple]:
    """
    Converts a float number representing hours to a readable string of the form "HH:MM:SS"
    - as_tuple: set it to True if instead of a string, you want a tuple as (hours, minutes, seconds)

    Example:
    --------
    >> decimal_hours_to_HMS(hours=72.345)
    '72:20:42'
    >>> decimal_hours_to_HMS(hours=72.345, as_tuple=True)
    (72, 20, 42)
    """
    rd = relativedelta(hours=hours).normalized()
    str_repr = f"{rd.days * 24 + rd.hours}:{rd.minutes}:{rd.seconds}"
    return str_repr if not as_tuple else tuple(map(int, str_repr.split(":")))


K = 273.15
k = 273.15
#code to organize read ames files read using nappy package

def organize_df_nya(df1, df2):
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

        if (search('Pressure', list1[i])) and (search('observation', list1[i])):
            df_out['Pair'] = df1[list1[i]].astype('float')


        df_out['Time'] = df1['Time']

        if (search('Geopotential', list1[i])) and (search('height', list1[i])):
            height = list1[i]
            df_out['Height'] = df1[height]

        if (search('elative ', list1[i])) and (search('umidity', list1[i])):
            df_out['RH'] = df1[list1[i]]

        if (search('wind ', list1[i])) and (search('direction', list1[i])):
            windd = list1[i]
            df_out['WindDirection'] = df1[windd]

        if (search('wind ', list1[i])) and (search('speed', list1[i])):
            winds = list1[i]
            df_out['WindSpeed'] = df1[winds]

        if (search('GPS', list1[i])) and (search('height', list1[i])):
            df_out['GPSHeight'] = df1[list1[i]]

        if (search('GPS', list1[i])) and (search('longitude', list1[i])):
            df_out['Lon'] = df1[list1[i]]

        if (search('GPS', list1[i])) and (search('latitude', list1[i])):
            df_out['Lat'] = df1[list1[i]]

        if (search('zone ', list1[i])) and (search('partial pressure', list1[i])):
            df_out['PO3'] = df1[list1[i]].astype('float')

        if (search('raw', list1[i])) and (search('current', list1[i])):
            pair = list1[i]
            df_out['I'] = df1[pair].astype('float')

        if (search('Battery', list1[i])) and (search('voltage', list1[i])):
            pair = list1[i]
            df_out['BatteryVoltage'] = df1[pair].astype('float')

        if (search('Pump', list1[i])) and (search('current', list1[i])):
            pair = list1[i]
            df_out['PumpCurrent'] = df1[pair].astype('float')

        if (search('Temperature', list1[i])) and (search('radiosonde', list1[i])):
            df_out['Temp'] = df1[list1[i]].astype('float')
        if (search('emperature', list1[i])) and (search('pump', list1[i])):
            df_out['TboxK'] = df1[list1[i]].astype('float')





    list2 = list(df2)
    for j in range(len(list2)):

        if (search('Station longitude', list2[j])):
            dfm_out.at[0,'Lon'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Station latitude', list2[j])):
            dfm_out.at[0,'Lat'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Station height', list2[j])):
            dfm_out.at[0,'StationHeight'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Launch time', list2[j])):
            tmp = df2.at[df2.first_valid_index(), list2[j]]
            dt_out = decimal_hours_to_HMS(hours=tmp)
            dfm_out.at[0,'LaunchTime'] = dt_out
        if (search('Station height', list2[j])):
            dfm_out.at[0,'StationHeight'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('pump flow rate', list2[j])):
            dfm_out.at[0,'PF'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('emperature during flow rate measurement', list2[j])):
            dfm_out.at[0,'TLab'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('humidity during flow rate measurement', list2[j])):
            dfm_out.at[0,'RHLab'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('humidity correction factor', list2[j])):
            dfm_out.at[0,'RHcorrection'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Ib0', list2[j])):
            dfm_out.at[0,'iB0'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Ib1', list2[j])):
            dfm_out.at[0,'iB1'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Ib2', list2[j])):
            dfm_out.at[0,'iB2'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Ozone background used', list2[j])):
            dfm_out.at[0,'iBused'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('solution concentration', list2[j])):
            dfm_out.at[0,'SolutionConcentration'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('olution amount', list2[j])):
            dfm_out.at[0,'SolutionVolume'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Surface pressure', list2[j])):
            dfm_out.at[0,'PLab'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Surface temperature', list2[j])):
            dfm_out.at[0,'TSurface'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Surface humidity', list2[j])):
            dfm_out.at[0,'RHSurface'] = df2.at[df2.first_valid_index(), list2[j]]


    return df_out, dfm_out




def organize_df_scoresby(df1, df2):
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

        if (search('Pressure', list1[i])) and (search('observation', list1[i])):
            df_out['Pair'] = df1[list1[i]].astype('float')


        df_out['Time'] = df1['Time']

        if (search('Geopotential', list1[i])) and (search('height', list1[i])):
            height = list1[i]
            df_out['Height'] = df1[height]

        if (search('elative ', list1[i])) and (search('umidity', list1[i])):
            df_out['RH'] = df1[list1[i]]

        if (search('wind ', list1[i])) and (search('direction', list1[i])):
            windd = list1[i]
            df_out['WindDirection'] = df1[windd]

        if (search('wind ', list1[i])) and (search('speed', list1[i])):
            winds = list1[i]
            df_out['WindSpeed'] = df1[winds]

        if (search('eopotential', list1[i])) and (search('height', list1[i])):
            df_out['GPSHeight'] = df1[list1[i]]

        if (search('GPS', list1[i])) and (search('longitude', list1[i])):
            df_out['Lon'] = df1[list1[i]]

        if (search('GPS', list1[i])) and (search('latitude', list1[i])):
            df_out['Lat'] = df1[list1[i]]

        if (search('zone ', list1[i])) and (search('partial pressure', list1[i])):
            df_out['PO3'] = df1[list1[i]].astype('float')

        if (search('raw', list1[i])) and (search('current', list1[i])):
            pair = list1[i]
            df_out['I'] = df1[pair].astype('float')

        if (search('Battery', list1[i])) and (search('voltage', list1[i])):
            pair = list1[i]
            df_out['BatteryVoltage'] = df1[pair].astype('float')

        if (search('Pump', list1[i])) and (search('current', list1[i])):
            pair = list1[i]
            df_out['PumpCurrent'] = df1[pair].astype('float')

        if (search('Temperature', list1[i])) and (search('radiosonde', list1[i])):
            df_out['Temp'] = df1[list1[i]].astype('float')
        if (search('emperature', list1[i])) and (search('inside', list1[i])):
            df_out['Tbox'] = df1[list1[i]].astype('float')





    list2 = list(df2)
    for j in range(len(list2)):

        if (search('ongitude', list2[j])):
            dfm_out.at[0,'Lon'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('atitude', list2[j])):
            dfm_out.at[0,'Lat'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Launch time', list2[j])):
            tmp = df2.at[df2.first_valid_index(), list2[j]]
            dt_out = decimal_hours_to_HMS(hours=tmp)
            dfm_out.at[0,'LaunchTime'] = dt_out
        if (search('Station height', list2[j])):
            dfm_out.at[0,'StationHeight'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('air flow rate', list2[j]) and search('ozonesonde pump only operating',list2[j])):
            dfm_out.at[0,'PF'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Temperature', list2[j]) and search('laboratory',list2[j])):
            dfm_out.at[0,'TLab'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('humidity', list2[j]) and search('laboratory',list2[j])):
            dfm_out.at[0,'RHLab'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('umidity correction', list2[j])):
            dfm_out.at[0,'RHcorrection'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Background sensor current before cell is exposed to ozone', list2[j])):
            dfm_out.at[0,'iB0'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Ib1', list2[j])):
            dfm_out.at[0,'iB1'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Background sensor current in the end of the pre-flight calibration', list2[j])):
            dfm_out.at[0,'iB2'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Background current correction method', list2[j])):
            dfm_out.at[0,'iBused'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('solution concentration', list2[j])):
            dfm_out.at[0,'SolutionConcentration'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('olution amount', list2[j])):
            dfm_out.at[0,'SolutionVolume'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('surface pressure', list2[j])):
            dfm_out.at[0,'PLab'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Surface temperature', list2[j])):
            dfm_out.at[0,'TSurface'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Surface humidity', list2[j])):
            dfm_out.at[0,'RHSurface'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('COL1', list2[j])):
            dfm_out.at[0,'COL1'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('COL2A', list2[j])):
            dfm_out.at[0,'COL2A'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('COL2B', list2[j])):
            dfm_out.at[0,'COL2B'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Serial number of ECC', list2[j])):
            dfm_out.at[0,'SerialECC'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Serial number of interface card', list2[j])):
            dfm_out.at[0,'SerialInterface'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Serial number of sonde', list2[j])):
            dfm_out.at[0,'SerialSonde'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Concentration of cathode solution', list2[j])):
            dfm_out.at[0,'SolutionConcentration'] = df2.at[df2.first_valid_index(), list2[j]]
        if (search('Amount of cathode solution', list2[j])):
            dfm_out.at[0,'SolutionVolume'] = df2.at[df2.first_valid_index(), list2[j]]


    return df_out, dfm_out