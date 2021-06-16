import pandas as pd
import math
from re import search

VecP_ECC6A = [0, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 1100]
VecC_ECC6A_25 = [1.16, 1.16, 1.124, 1.087, 1.054, 1.033, 1.024, 1.015, 1.010, 1.007, 1.005, 1.002, 1, 1]
VecC_ECC6A_30 = [1.171, 1.171, 1.131, 1.092, 1.055, 1.032, 1.022, 1.015, 1.011, 1.008, 1.006, 1.004, 1, 1]

VecP_MAST = [0, 3, 5, 10, 20, 30, 50, 100, 200, 1100]
VecC_MAST = [1.177, 1.177, 1.133, 1.088, 1.053, 1.037, 1.020, 1.004, 1, 1]

# SensorType = 'DMT-Z'
VecP_ECCZ = [0, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 1100]
VecC_ECCZ = [1.24, 1.24, 1.124, 1.087, 1.066, 1.048, 1.041, 1.029, 1.018, 1.013, 1.007, 1.002, 1, 1]

K = 273.15



## functions copied from read_nilu_functions.py to convert PO3 to current


def o3tocurrent(dft, dfm):
    '''

    :param dft: data df
    :param dfm: metadata df
    :return: dft
    '''
    # o3(mPa) = 4.3087 * 10e-4 * (i - ibg) * tp * t * cef * cref
    # tp: pump temp. in K, t: pumping time for 100 ml of air in seconds, cef: correction due to reduced ambient pressure for pump
    # cref: additional correction factor
    # i = o3 / (4.3087 * 10e-4 * tp * t * cef * cref ) + ibg

    dft['SensorType'] = 'DMT-Z'
    dfm['SensorType'] = 'DMT-Z'



    dft['Cef'] = ComputeCef(dft)

    cref = 1
    dft['ibg'] = 0
    dft['iB2'] = dfm.at[dfm.first_valid_index(), 'iB2']

    # check PF values
    if (dfm.at[dfm.first_valid_index(), 'PF'] > 40) | (dfm.at[dfm.first_valid_index(), 'PF'] < 20): dfm.at[dfm.first_valid_index(), 'PF'] = 28

    # # by default uses iB2 as background current
    # dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB2']
    # if it was mentioned that BkgUsed is Ibg1, then iB0 is used
    # if (dfm.at[dfm.first_valid_index(), 'BkgUsed'] == 'Ibg1') & (dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z'):
    #     dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB0']
    # if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC': dft['ibg'] = ComputeIBG(dft, 'iB2')
    if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z': dft['ibg'] = dfm.at[dfm.first_valid_index(), 'iB2']

    dft['I'] = dft['O3'] / (4.3087 * 10 ** (-4) * dft['TboxK'] * dfm.at[dfm.first_valid_index(), 'PF'] * dft['Cef'] * cref) + dft['ibg']


    return dft


def ComputeCef(dft):
    """ Computes pump efficiency correction factor based on pressure

        Arguments:
        Pressure -- air pressure [hPa]
    """

    dft['SensorType'] = 'DMT-Z'
    dft['SolutionVolume'] = 3.0
    #
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'SPC') and (
            dft.at[dft.first_valid_index(), 'SolutionVolume'] > 2.75):
        dft['Cef'] = VecInterpolate(VecP_ECC6A, VecC_ECC6A_30, dft, 0)
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
