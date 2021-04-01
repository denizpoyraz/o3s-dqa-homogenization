import numpy as np
import math
import pandas as pd

def filter_data(df):
    '''
    a function to remove wrong values
    :param df: data df
    :return: filtered data df
    '''

    df = df[df.Pair < 1100]
    df = df[df.TboxC < 40]
    df = df[df.O3 < 30]

    # ['Pair', 'Time', 'Height', 'TboxK', 'TboxC', 'WindDirection', 'WindSpeed', 'O3', 'T', 'U', 'SensorType',
    #  'SolutionVolume', 'Cef', 'ibg', 'I', 'Date']

    return df


def filter_metadata(df):
    '''
    a function to remove wrong values
    :param df: metadata df
    :return: filtered metadata df
    '''
    df.SolutionVolume = df.SolutionVolume.astype('float')
    df.SolutionConcentration = df.SolutionConcentration.astype('float')
    df.Pground = df.Pground.astype('float')
    df.TLab = df.TLab.astype('float')
    df.ULab = df.ULab.astype('float')


    df = df[df.SolutionVolume.astype('float') < 4]
    df = df[df.SolutionConcentration < 20]
    df = df[df.PF < 35]
    df = df[df.iB0 < 9]
    df = df[df.iB2 < 9]
    df = df[df.Pground < 9999]
    df = df[df.TLab < 40]
    df = df[df.ULab < 9999]

    # ['Pair', 'Time', 'Height', 'TboxK', 'TboxC', 'WindDirection', 'WindSpeed', 'O3', 'T', 'U', 'SensorType',
    #  'SolutionVolume', 'Cef', 'ibg', 'I', 'Date']
    return df