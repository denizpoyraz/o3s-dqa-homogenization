import pandas as pd
import math
from re import search

VecP_ECC6A =    [    0,     2,     3,      5,    10,    20,    30,    50,   100,   200,   300,   500, 1000, 1100]
VecC_ECC6A_25 = [ 1.16,  1.16, 1.124,  1.087, 1.054, 1.033, 1.024, 1.015, 1.010, 1.007, 1.005, 1.002,    1,    1]
VecC_ECC6A_30 = [ 1.171, 1.171, 1.131, 1.092, 1.055, 1.032, 1.022, 1.015, 1.011, 1.008, 1.006, 1.004,    1,    1]

VecP_MAST = [     0,     3,     5,    10,    20,    30,    50,   100,   200,  1100]
VecC_MAST = [ 1.177, 1.177, 1.133, 1.088, 1.053, 1.037, 1.020, 1.004,     1,     1]

# SensorType = 'DMT-Z'
VecP_ECCZ = [   0,    3,     5,     7,    10,    15,    20,    30,    50,    70,    100,   150,   200, 1100]
VecC_ECCZ = [1.24, 1.24, 1.124, 1.087, 1.066, 1.048, 1.041, 1.029, 1.018, 1.013,  1.007, 1.002,     1,    1]

K = 273.15


def organize_df(df1, df2):
    '''
    searches for patterns to read metadata and writes them into a new dataframe
    :param df1: main data dataframe in pandas format
    :param df2: metadata dataframe in pandas format
    :return: df_out: a dataframe that has data and the metadata
    '''

    df_out = pd.DataFrame()
    list1 = list(df1)
    for i in range(len(list1)):

        if (search('Temperature', list1[i])) and (search('inside', list1[i])):
            pump_temp = list1[i]
            df_out['Tbox'] = df1[pump_temp].astype('float') + K
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

        if (search('Background', list2[j])) and (search('before', list2[j])) and (search('exposed', list2[j])) :
            bkg = list2[j]
            df_out['iB0'] = df2.at[df2.first_valid_index(), bkg]

        if (search('Background', list2[j])) and (search('sensor current', list2[j])) and (search('after 10min', list2[j])) :
            bkg = list2[j]
            df_out['iB1'] = df2.at[df2.first_valid_index(), bkg]

        if (search('Background', list2[j])) and (search('end', list2[j])) and (search('pre-flight', list2[j])) :
            bkg = list2[j]
            df_out['iB2'] = df2.at[df2.first_valid_index(), bkg]

        if (search('Background', list2[j])) and (search('current', list2[j])) and (search('launch', list2[j])) :
            bkg = list2[j]
            df_out['iB2'] = df2.at[df2.first_valid_index(), bkg]

        df_out['BkgUsed'] = 'Constant'
        if (search('Background', list2[j])) and (search('current', list2[j])) and (search('used', list2[j])) and (search('computation', list2[j])) :
            bkg = list2[j]
            df_out['BkgUsed'] = df2.at[df2.first_valid_index(), bkg]

        if ((search('Sensor', list2[j])) and (search('air', list2[j])) and (search('flow', list2[j]))) and \
               not(search('calibrator', list2[j])):
            pumpt = list2[j]
            df_out['PF'] = df2.at[df2.first_valid_index(), pumpt]

            # if (float(df2.at[df2.first_valid_index(), pumpt]) < 25) | (float(df2.at[df2.first_valid_index(), pumpt]) > 35):
            #     df_out['PF'] = 29

        if (search('Serial number', list2[j])) and ((search('RS-80', list2[j]))):
            rs80 = 'RS80'
            df_out['RadiosondeModel'] = rs80

        if (search('Serial number', list2[j])) and ((search('RS', list2[j])) or (search('radiosonde', list2[j])) or (search('Radiosonde',list2[j]))):
            try:
                df_out['RadiosondeSerial'] = df2.at[df2.first_valid_index(), list2[j]]
            except KeyError:
                df_out['RadiosondeSerial'] = '9999'

        if ((search('interface', list2[j]) or(search('Interface',list2[j]))) and not(search('parameter', list2[j]))):
            df_out['InterfaceSerial'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Surface', list2[j])) or ((search('surface', list2[j])) and (search('ozone', list2[j])) or
                        (search('Ozone',list2[j]))) and not (search('Time', list2[j])) and not (search('sensor', list2[j])):
            df_out['SurfaceOzone'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('round equipment', list2[j])) or (search('equipment', list2[j])):
            df_out['GroundEquipment'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Correction factor ', list2[j])) or (search('correction factor', list2[j])):
            df_out['CorrectionFactor'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Total ozone', list2[j])) and (search('sonde', list2[j])):
            df_out['SondeTotalO3'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Total ozone', list2[j])) and (search('Dobson/Brewer', list2[j])) and (search('COL2A', list2[j])):
            df_out['TotalO3_Col2A'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Total ozone', list2[j])) and (search('Dobson/Brewer', list2[j])) and (search('COL2B', list2[j])):
            df_out['TotalO3_Col2B'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Background', list2[j])) and (search('correction', list2[j])):
            df_out['BackgroundCorrection'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Launch time', list2[j])) :
            df_out['LaunchTime'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Hour of launch', list2[j])) :
            df_out['HourLaunchTime'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Minute of launch', list2[j])) :
            df_out['MinuteLaunchTime'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Longitude', list2[j])) or  (search('longitude', list2[j])):
            df_out['Longitude'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Latitude', list2[j])) or  (search('latitude', list2[j])):
            df_out['Latitude'] = df2.at[df2.first_valid_index(), list2[j]]

        if (search('Time',list2[j])) and (search('sonde',list2[j])) and (search('surface ozone', list2[j])):
            df_out['DurationSurfaceOzoneExposure'] = df2.at[df2.first_valid_index(), list2[j]]
            # 'Time the sonde was run for surface ozone (min)'

        if not((search('Ozone', list2[j])) and (search('sensor', list2[j]))) and (search('Serial number of ECC', list2[j])) :
            serial = list2[j]
            df_out['SerialECC'] = df2.at[df2.first_valid_index(), serial]
            if (df2.at[df2.first_valid_index(), serial][0] == "z") | (df2.at[df2.first_valid_index(), serial][0] == "Z")\
                    | (df2.at[df2.first_valid_index(), serial][1] == "Z") | (df2.at[df2.first_valid_index(), serial][1] == "z"):
                df_out['SensorType'] = 'DMT-Z'
            if (df2.at[df2.first_valid_index(), serial][0] == "4"): df_out['SensorType'] = 'SPC-4A'
            if (df2.at[df2.first_valid_index(), serial][0] == "5"): df_out['SensorType'] = 'SPC-5A'
            if (df2.at[df2.first_valid_index(), serial][0] == "6"): df_out['SensorType'] = 'SPC-6A'

        if (search('Serial number of ECC', list2[j])):
            serial = list2[j]
            if (df2.at[df2.first_valid_index(), serial][0] == "z") | (df2.at[df2.first_valid_index(), serial][0] == "Z") \
                    | (df2.at[df2.first_valid_index(), serial][1] == "Z") | (
                    df2.at[df2.first_valid_index(), serial][1] == "z"):
                df_out['SensorType'] = 'DMT-Z'
            if (df2.at[df2.first_valid_index(), serial][0] == "4"): df_out['SensorType'] = 'SPC-4A'
            if (df2.at[df2.first_valid_index(), serial][0] == "5"): df_out['SensorType'] = 'SPC-5A'
            if (df2.at[df2.first_valid_index(), serial][0] == "6"): df_out['SensorType'] = 'SPC-6A'

        if (search('Ozone', list2[j])) and (search('sensor', list2[j])):
            if (df2.at[df2.first_valid_index(), serial][0] == "z") | (df2.at[df2.first_valid_index(), serial][0] == "Z") \
                    | (df2.at[df2.first_valid_index(), serial][1] == "Z") | (
                    df2.at[df2.first_valid_index(), serial][1] == "z"):
                df_out['SensorType'] = 'DMT-Z'
            if (df2.at[df2.first_valid_index(), serial][0] == "4"): df_out['SensorType'] = 'SPC-4A'
            if (df2.at[df2.first_valid_index(), serial][0] == "5"): df_out['SensorType'] = 'SPC-5A'
            if (df2.at[df2.first_valid_index(), serial][0] == "6"): df_out['SensorType'] = 'SPC-6A'


        if (search('Background', list2[j])) and (search('surface pressure', list2[j])):
            pground = list2[j]
            df_out['Pground'] = df2.at[df2.first_valid_index(), pground]
            if (float(df2.at[df2.first_valid_index(), pground]) > 1090) | (
                    float(df2.at[df2.first_valid_index(), pground]) < 900):
                df_out['Pground'] = 1000

        if (search('Surface pressure', list2[j])) and (search('sonde flow', list2[j])):
            pground = list2[j]
            df_out['Pground'] = df2.at[df2.first_valid_index(), pground]
            # if (float(df2.at[df2.first_valid_index(), pground]) > 1090) | (
            #         float(df2.at[df2.first_valid_index(), pground]) < 900):
            #     df_out['Pground'] = 1000

        if (search('Amount', list2[j])) and (search('cathode', list2[j])):
            cathodesol = list2[j]
            df_out['SolutionVolume'] = df2.at[df2.first_valid_index(), cathodesol]

        if (search('Concentration', list2[j])) and (search('cathode', list2[j])):
            cathodecon = list2[j]
            df_out['SolutionConcentration'] = df2.at[df2.first_valid_index(), cathodecon]

        if (search('Place', list2[j])) and (search('box', list2[j])) and (search('measurement', list2[j])):
            pt_location = list2[j]
            df_out['PumpTempLoc'] = df2.at[df2.first_valid_index(), pt_location]

        if (search('Temperature', list2[j])) and (search('laboratory', list2[j])) and (search('during', list2[j])) and (search('sonde', list2[j])) :
            t_lab = list2[j]
            df_out['TLab'] = df2.at[df2.first_valid_index(), t_lab]

        if (search('Relative humidity', list2[j])) and (search('laboratory', list2[j])) and (search('during', list2[j])) and (search('sonde', list2[j])) :
            u_lab = list2[j]
            df_out['ULab'] = df2.at[df2.first_valid_index(), u_lab]

        if (search('Pump', list2[j])) and (search('correction', list2[j])):
            pump_table = list2[j]
            df_out['PumpTable'] = df2.at[df2.first_valid_index(), pump_table]

    df_out['O3'] = df1['Ozone partial pressure (mPa)'].astype('float')
    df_out['T'] = df1['Temperature (C)'].astype('float')
    df_out['U'] = df1['Relative humidity (%)'].astype('float')
    # in case there is no PF it is written to 9999
    try:df_out['PF'] = df_out['PF'].astype('float')
    except KeyError: df_out['PF'] = 9999
    # in case there is no iB0 or iB2 it is written to 9999
    try: df_out['iB0'] = df_out['iB0'].astype('float')
    except KeyError: df_out['iB0'] = 9999
    try: df_out['iB2'] = df_out['iB2'].astype('float')
    except KeyError: df_out['iB2'] = 9999
    # df_out['Cef'] = 1

    return df_out


def o3tocurrent(dft):
    # o3(mPa) = 4.3087 * 10e-4 * (i - ibg) * tp * t * cef * cref
    # tp: pump temp. in K, t: pumping time for 100 ml of air in seconds, cef: correction due to reduced ambient pressure for pump
    # cref: additional correction factor
    # i = o3 / (4.3087 * 10e-4 * tp * t * cef * cref ) + ibg

    sensortype = dft.at[dft.first_valid_index(), 'SensorType']

    spctag4A = (search('SPC', sensortype)) or (search('4A', sensortype))
    if spctag4A: dft['SensorType'] = 'SPC-4A'
    spctag5A = (search('SPC', sensortype)) or (search('5A', sensortype))
    if spctag5A: dft['SensorType'] = 'SPC-5A'
    spctag6A = (search('SPC', sensortype)) or (search('6A', sensortype))
    if spctag6A: dft['SensorType'] = 'SPC-6A'

    enscitag = (search('DMT-Z', sensortype)) or (search('Z', sensortype)) or (search('ECC6Z', sensortype)) or (
        search('_Z', sensortype))
    if enscitag: dft['SensorType'] = 'DMT-Z'

    ensci = (dft.SensorType == 'DMT-Z')
    spc = ((dft.SensorType == 'SPC') | (dft.SensorType == 'SPC-4A') | (dft.SensorType == 'SPC-5A') | (dft.SensorType == 'SPC-6A'))

    dft['Cef'] = ComputeCef(dft)

    cref = 1
    dft['ibg'] = 0

    # by default uses iB2 as background current
    dft['ibg'] = dft['iB2']
    # if it was mentioned that BkgUsed is Ibg1, then iB0 is used
    if dft.at[dft.first_valid_index(), 'BkgUsed'] == 'Ibg1': dft['ibg'] = dft['iB0']

    dft.loc[spc, 'ibg'] = ComputeIBG(dft[spc], 'ibg')
    dft.loc[ensci, 'ibg'] = dft.loc[ensci, 'ibg']

    dft.loc[ensci,'I'] = dft.loc[ensci,'O3'] / \
                                       (4.3087 * 10**(-4) * dft.loc[ensci,'Tbox'] * dft.loc[ensci, 'PF'] * dft.loc[ensci,'Cef'] * cref) + dft.loc[ensci,'ibg']
    dft.loc[spc, 'I'] = dft.loc[spc, 'O3'] / \
                          (4.3087 * 10 ** (-4) * dft.loc[spc, 'Tbox'] * dft.loc[spc, 'PF'] * dft.loc[
                              spc, 'Cef'] * cref) + dft.loc[spc, 'ibg']

    return dft

def ComputeCef(dft):
    """ Computes pump efficiency correction factor based on pressure

        Arguments:
        Pressure -- air pressure [hPa]
    """
    sensortype = dft.at[dft.first_valid_index(),'SensorType']
    #
    # # print('sensortype', sensortype)
    #
    spctag = (search('SPC', sensortype)) or (search('6A', sensortype)) or (search('5A', sensortype)) or (search('4A', sensortype))
    if spctag: dft['SensorType'] = 'SPC'
    enscitag = (search('DMT-Z', sensortype)) or (search('Z', sensortype)) or (search('ECC6Z', sensortype)) or (search('_Z', sensortype))
    if enscitag: dft['SensorType'] = 'DMT-Z'


    try: dft['SolutionVolume'] = dft['SolutionVolume'].astype('float')
    except KeyError: dft['SolutionVolume'] = 3.0
    #
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'SPC') and (dft.at[dft.first_valid_index(), 'SolutionVolume'] > 2.75):
        dft['Cef'] = VecInterpolate(VecP_ECC6A, VecC_ECC6A_30, dft, 0)
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'SPC') and (dft.at[dft.first_valid_index(), 'SolutionVolume'] < 2.75):
        dft['Cef'] = VecInterpolate(VecP_ECC6A, VecC_ECC6A_25, dft, 0)
    if (dft.at[dft.first_valid_index(), 'SensorType'] == 'DMT-Z') and (dft.at[dft.first_valid_index(), 'SolutionVolume'] > 2.75):
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
        for i in range(len(XValues)-1):
            # just check that value is in between xvalues
            if (XValues[i] <= dft.at[k, 'Pair'] <= XValues[i + 1]):

                x1 = float(XValues[i])
                x2 = float(XValues[i+1])
                if LOG == 1:
                    x = math.log(x)
                    x1 = math.log(x1)
                    x2 = math.log(x2)
                y1 = float(YValues[i])
                y2 = float(YValues[i+1])

                dft.at[k,'Cef'] = y1 + (dft.at[k,'Pair'] - x1) * (y2 - y1) / (x2 - x1)

    return dft['Cef']

def ComputeIBG(dft, bkg):
    """ Corrects background current value based on pressure

  Arguments:
  dft  -- dataframe
  ibg  -- background current used
  :returns corrected background current
    """
    try: dft.Pcor = ComputeCorP(dft, 'Pair') / ComputeCorP(dft, 'Pground')
    except KeyError:
        dft['Pground'] = 1000
        dft.Pcor = ComputeCorP(dft, 'Pair') / ComputeCorP(dft, 'Pground')

    if bkg == 'iB0': dft.ibg = dft.Pcor*dft.iB0
    if bkg == 'iB2': dft.ibg = dft.Pcor*dft.iB2

    return dft.ibg


def ComputeCorP(dft, Pressure):

  A0 = 0.0012250380415
  A1 = 0.000124111475632
  A2 = -0.00000002687066130
  dft.CorP = A0 + A1*dft[Pressure].astype('float') + A2*dft[Pressure].astype('float')*dft[Pressure].astype('float')

  return dft.CorP
