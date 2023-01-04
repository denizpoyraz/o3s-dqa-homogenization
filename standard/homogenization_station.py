# import pickle
# pickle.HIGHEST_PROTOCOL = 5
import os
import pandas as pd
import numpy as np
from re import search
from datetime import datetime
pd.set_option('mode.chained_assignment', None)
#! /usr/bin/env python3


from functions.homogenization_functions import absorption_efficiency, stoichmetry_conversion, conversion_efficiency, \
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency, \
    return_phipcor, o3_integrate, roc_values, RS_pressurecorrection, o3tocurrent, background_correction_3split

from functions.functions_perstation import df_missing_variable, madrid_missing_tpump, df_station, \
    station_inone, station_inbool, station_invar, df_drop
from functions.functions_woudc_writer import f_write_to_woudc_csv



# homogenization code to be used by all stations
### all corrections recommended by the DQA:
## Conversion Efficiency:
#  absorption and stoichiometry->
#  variables:solution volume,
#  sonde type and solution concentration
## Background Current:
#  df of all metadata is needed to calculate the mean and std of bkg.
#  most of the time 2 different periods are needed
#  which has a parameter IBGsplit the year in which
#  bkg values has changed from high to low
#  which bkg is used important, mostly iB2
#  but this can be station specific
## Pump Temp. Measurement (location):
#  pump location. if a change in the type of the sonde was made
#  this would effect this variable
## Pump Flow Rate (moistening effect)
#
## Pump flow efficiency at low pressures
# TON not to be applied but to be kept in the database
# Radiosonde correction (not to be applied)
# At the end also written to WOUDC format

k = 273.15
roc_plevel = 10 # pressure value to obtain roc

##                                         ##
##           TO BE CHANGED By HAND         ##

# station_name = 'ny-alesund'
station_name = 'uccle'

main_rscorrection = False  #if you want to apply rs80 correction
test_ny = False
scoresbysund_tpump = False
file_dfmain = "/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Madrid_AllData_woudc.hdf"
#only needed for madrid (for the moment) to calculate means of the tmpump

##           end of the parts  TO BE CHANGED By HAND           ##
##                                                             ##

filefolder = '/DQA_nors80/'
file_ext = 'test_nors80'

if main_rscorrection:
    filefolder = '/DQA_rs80/'
    file_ext = 'rs80'

path, allFiles, roc_table_file, dfmeta = station_inone(station_name)
humidity_correction, df_missing_tpump, calculate_current, organize_df, descent_data = station_inbool(station_name)
date_start_hom, ibg_split, sonde_tbc, rs80_begin, rs80_end = station_invar(station_name)


if df_missing_tpump:
    dfmain = pd.read_hdf(file_dfmain)
    dfmean = madrid_missing_tpump(dfmain)

if humidity_correction:
    dfmeta = calculate_cph(dfmeta)
    dfmeta.loc[:,'unc_cPH'] = dfmeta['cPH'].std()
    dfmeta.loc[:,'unc_cPL'] = dfmeta['cPL'].std()

clms = [i for i in range(1,13)]
table = pd.read_csv(roc_table_file,  skiprows=1, sep="\s *", names = clms,  header=None)


#read over all files to do the homogenization

for (filename) in (allFiles):
    file = open(filename, 'r')

    date_tmp = filename.split('/')[-1].split('.')[0][2:8]
    fullname = filename.split('/')[-1].split('.')[0]

    # date_tmp = filename.split('/')[-1].split("_")[1][2:8]
    # fullname = filename.split('/')[-1].split("_")[1]
    # if datestr < date_start_hom: continue
       # if datestr < '20190101': continue

    print(filename)

    df = pd.read_hdf(filename)
    datestr = str(df.at[df.first_valid_index(),'Date'])
    dfm = dfmeta[dfmeta.Date == datestr]
    dfm = dfm.reset_index()
    if len(dfm) == 0:
        print('Check dfm')
        continue

    if len(dfm) == 1:
        dfm = dfmeta[dfmeta.Date == datestr][0:1]
    if (len(dfm) == 2) and search("2nd", fullname):
        dfm = dfmeta[dfmeta.Date == datestr][1:2]
    if(len(dfm) > 0) and not search("2nd", fullname):
        dfm = dfmeta[dfmeta.Date == datestr][0:1]
    dfm = dfm.reset_index()

    if organize_df:
        date_bool, df = df_station(df,datestr, dfm, station_name)
        if date_bool == 'stop':
            print('BAD File')
            continue
    if len(df) < 100: continue

    if df_missing_tpump:
        df = df_missing_variable(df, dfmean)

    if calculate_current:
        try:
            df = o3tocurrent(df, dfm) #byault uses ib2, check if another ib is used!
        except (ValueError, KeyError):
            print('BAD File, check FILE')

    # input variables for hom.
    df['Tpump'] = df['TboxK']

    df['Phip'] = 100 / dfm.at[dfm.first_valid_index(), 'PF']
    df['Eta'] = 1

    df['dPhip'] = 0.02
    df['unc_cPH'] = dfm.at[dfm.first_valid_index(), 'unc_cPH']
    df['unc_cPL'] = dfm.at[dfm.first_valid_index(), 'unc_cPL']

    if not df_missing_tpump:
        df['unc_Tpump'] = 0.5  # case II-V
    #if there is missing tpump, the unc. is assgined in  function 'df_missing_variable'

    # #      radiosonde RS80 correction   #
    # # Electronic o3 sonde interface  was replaced with the transfer from RS80 to RS92  in 24 Nov 2005.
    rsmodel = ''
    bool_rscorrection = ''

    if datestr < rs80_end and datestr >= rs80_begin:
        bool_rscorrection = True
    # if datestr > rs80_end:
    if datestr >= rs80_end or datestr < rs80_begin:
        bool_rscorrection = False
    #

    if bool_rscorrection and main_rscorrection:
        df['Crs'], df['unc_Crs'] = RS_pressurecorrection(df, 'Height', rsmodel)
        df['Pair'] = df['Pair'] - df['Crs']

    #ROC calculation from the climatological means
    dfm = roc_values(dfm, df, table)

    # DQA corrections
    #      conversion efficiency        #
    df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair', dfm.at[0,'SolutionVolume'])
    df['stoich'], df['unc_stoich'] = stoichmetry_conversion(df, 'Pair', dfm.at[0, 'SensorType'],
                                                            dfm.at[0, 'SolutionConcentration'], sonde_tbc)
    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    if station_name != 'scoresbysund':
        if dfm.at[0, 'string_bkg_used'] == 'ib2': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2', ibg_split, station_name)
        if dfm.at[0, 'string_bkg_used']  == 'ib0': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB0', ibg_split, station_name)
    if station_name == 'scoresbysund':
        df['iBc'], df['unc_iBc'] = background_correction_3split(df, dfmeta, dfm, 'iB2', '1993', '1995', '2017')

    if (df.Pair.min() <5) & (dfm.loc[0,'string_pump_location'] == 'case3'): print('HERE')
    #       pump temperature correction       #
    df['Tpump_cor'], df['unc_Tpump_cor'] = pumptemp_corr(df, dfm.loc[0,'string_pump_location'], 'Tpump', 'unc_Tpump', 'Pair')
    #      pump flow corrections        #
    # ground correction, humidity correction PTU
    if humidity_correction:
        df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'PLab', 'ULab', True)
    if not humidity_correction:
        df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'PLab', 'ULab', False)
    # efficiency correction
    pumpflowtable = '999 '
    if dfm.at[0, 'SensorType'] == 'SPC': pumpflowtable = 'komhyr_86'
    if dfm.at[0, 'SensorType'] == 'DMT-Z': pumpflowtable = 'komhyr_95'

    df['Cpf'], df['unc_Cpf'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'table_interpolate')
    df['Phip_cor'], df['unc_Phip_cor'] = return_phipcor(df, 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf')

    # all corrections
    df['O3_nc'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'Eta', 'Phip')
    df['O3c_eta'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'eta_c', 'Phip')
    df['O3c_etabkg'] = currenttopo3(df, 'I', 'Tpump', 'iBc', 'eta_c', 'Phip')
    df['O3c_etabkgtpump'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip')
    df['O3c_etabkgtpumpphigr'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_ground')
    df['O3c_etabkgtpumpphigref'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor')
    df['O3c'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor')

    #to correct the data for negative O3c values, in case iBc is larger than I
    df.loc[(df.O3c < 0) & (df.O3c > -999) , 'O3c'] = 0

    # uncertainities
    df['dI'] = 0
    df.loc[df.I < 1, 'dI'] = 0.01
    df.loc[df.I >= 1, 'dI'] = 0.01 * df.loc[df.I > 1, 'I']
    df['dIall'] = (df['dI'] ** 2 + df['unc_iBc'] ** 2) / (df['I'] - df['iBc']) ** 2
    df['dEta'] = (df['unc_eta_c'] / df['eta_c']) ** 2
    df['dPhi_cor'] = (df['unc_Phip_cor'] / df['Phip_cor']) ** 2
    df['dTpump_cor'] = df['unc_Tpump_cor']
    # final uncertainity on O3
    df['dO3'] = np.sqrt(df['dIall'] + df['dEta'] + df['dPhi_cor'] + df['dTpump_cor'])

    # # check all the variables if they are in accepted value range

    if len(df[(df.O3c > -99) & (df.O3c < 0)]) > 0 | (len(df[df['O3c'] > 30]) > 0) :
        print('     BREAK       O3c')
    if (len(df[df['iBc'] > 0.5]) > 0) | (len(df[df.iBc.isnull()])>0):
        print('     BREAK       iBc')

    # TON calculations
    # if there is the descent data, remove those for TON calculation
    if descent_data:
        dfn = df[df.Height > 0]
        maxh = dfn.Height.max()

        index = dfn[dfn["Height"] == maxh].index[0]

        descent_list = dfn[dfn.index > index].index.tolist()
        dfa = dfn.drop(descent_list)

    if not descent_data:
        dfa = df.copy()

    dfa = dfa[(dfa.I > 0) & (dfa.I > -9) ]
    dfa = dfa[(dfa.O3c < 99) & (dfa.O3c > 0) ]

    dfm['O3Sonde_burst'] = o3_integrate(dfa, 'O3')
    dfm['O3Sonde_burst_raw'] = o3_integrate(dfa, 'O3_nc')
    dfm['O3Sonde_burst_hom'] = o3_integrate(dfa, 'O3c')

    if dfa['Pair'].min() < 10:
        dfa = dfa[dfa['Pair'] >= 10]

    if dfa['Pair'].min() < 33:

        # for woudc O3 values
        dfm['O3Sonde'] = o3_integrate(dfa, 'O3')
        dfm['O3SondeTotal'] = dfm['O3Sonde'] + dfm['ROC']
        # the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = o3_integrate(dfa, 'O3c')
        dfm['O3SondeTotal_hom'] = dfm['O3Sonde_hom'] + dfm['ROC']
        # the same for raw no corrected o3 values
        dfm['O3Sonde_raw'] = o3_integrate(dfa, 'O3_nc')
        dfm['O3SondeTotal_raw'] = dfm['O3Sonde_raw'] + dfm['ROC']
        try:
            dfm['O3ratio'] = dfm['TotalO3_Col2A'] / dfm['O3SondeTotal']
            dfm['O3ratio_hom'] = dfm['TotalO3_Col2A'] / dfm['O3SondeTotal_hom']
            dfm['O3ratio_raw'] = dfm['TotalO3_Col2A'] / dfm['O3SondeTotal_raw']
            if dfm.at[0, 'TotalO3_Col2A'] > 999:
                dfm['O3ratio'] = 9999
                dfm['O3ratio_hom'] = 9999
                dfm['O3ratio_raw'] = 9999
        except KeyError:
            dfm['O3ratio'] = 9999
            dfm['O3ratio_hom'] = 9999
            dfm['O3ratio_raw'] = 9999


    if df['Pair'].min() > 32:
        dfm['O3Sonde'] = 9999
        dfm['O3SondeTotal'] = 9999
        dfm['O3ratio'] = 9999
        dfm['O3Sonde_10hpa'] = 9999
        # the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = 9999
        dfm['O3Sonde_10hpa_hom'] = 9999
        dfm['O3SondeTotal_hom'] = 9999
        dfm['O3ratio_hom'] = 9999
        dfm['O3Sonde_raw'] = 9999
        dfm['O3SondeTotal_raw'] = 9999
        dfm['O3ratio_raw'] = 9999

    #
    # print(dfm.at[0,'O3Sonde'], dfm.at[0,'O3Sonde_hom'], dfm.at[0,'ROC'],dfm.at[0,'O3Sonde'] + dfm.at[0,'ROC']  )
    # print(dfm.at[0,'O3SondeTotal'], dfm.at[0,'O3SondeTotal_hom'], df['Pair'].min())

    md_clist = ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
                'unc_eta_c', 'iB2', 'iBc', 'unc_iBc', 'TLab', 'deltat', 'unc_deltat', 'unc_deltat_ppi', 'dEta']

    # merge all the metadata to md df and save it as a csv file
    for j in range(len(md_clist)):
        dfm.at[0, md_clist[j]] = df.at[df.first_valid_index(), md_clist[j]]

    dfm.to_csv(path + filefolder + datestr + "_o3smetadata_" + file_ext + ".csv")


    # data file that has data and uncertainties that depend on Pair or Height or Temperature
    df.to_hdf(path + filefolder + datestr + "_all_hom_" + file_ext + ".hdf", key='df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']

    df = df_drop(df, station_name)

    # print(list(df))

    # df to be converted to WOUDC format together with the metadata
    df.to_hdf(path + filefolder + datestr + "_o3sdqa_" + file_ext + ".hdf", key='df')
    f_write_to_woudc_csv(df, dfm, station_name, path)


