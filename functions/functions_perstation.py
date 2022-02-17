import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from re import search
from functions.homogenization_functions import absorption_efficiency, stoichmetry_conversion, conversion_efficiency, \
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency, \
    return_phipcor, o3_integrate, roc_values, missing_station_values, assign_missing_ptupf

def organize_sodankyla(dsm):

    dsm = dsm[dsm.iB2 < 9]
    dsm = dsm[dsm.iB0 < 9]

    dsm['PLab'] = dsm['Pground']

    #part related with missing ptupf
    date_missing_p = '19970107'
    date_missing_t = '19981111'
    date_missing_u = '19981111'
    date_missing_pf = '19970107'

    plab = missing_station_values(dsm, 'PLab', False, 'nan')
    tlab = missing_station_values(dsm, 'TLab', False, 'nan')
    ulab = missing_station_values(dsm, 'ULab', False, 'nan')
    pflab = missing_station_values(dsm, 'PF', True, '20040101')  # PF values are

    print(pflab)

    dsm = assign_missing_ptupf(dsm, True, True, True, True, date_missing_p, date_missing_t, date_missing_u,
                                  date_missing_pf, plab, tlab, ulab, pflab)


    dsm['string_pump_location'] = '0'
    dsm.loc[dsm.Date <= '20001101', 'string_pump_location'] = 'case3'
    dsm.loc[dsm.Date > '20001101', 'string_pump_location'] = 'case5'


    dsm.loc[dsm['SolutionVolume'].isnull(), 'value_is_NaN'] = 1
    # dsm.loc[dsm['SolutionVolume'].notnull(), 'value_is_NaN'] = 0
    dsm.loc[dsm.value_is_NaN == 1, 'SolutionVolume'] = '3'
    dsm['SolutionVolume'] = dsm['SolutionVolume'].astype('float')

    dsm.loc[(dsm.Date < '20060201') & (dsm.at[0, 'SensorType'] == 'DMT-Z' ), 'SolutionConcentration'] = 10
    dsm.loc[(dsm.Date >= '20060201') & (dsm.at[0, 'SensorType'] == 'DMT-Z' ), 'SolutionConcentration'] = 5
    dsm.loc[(dsm.Date < '20060201') & (dsm.at[0, 'SensorType'] == 'SPC' ), 'SolutionConcentration'] = 10

    dsm['string_bkg_used'] = '999'
    dsm.loc[dsm.BkgUsed == 'Ibg1', 'string_bkg_used'] = 'ib0'
    dsm.loc[dsm.BkgUsed == 'Constant', 'string_bkg_used'] = 'ib2'


    dsm['TotalO3_Col2A'] = dsm['TotalO3_Col2A'].astype('float')

    return(dsm)