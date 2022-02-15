import pandas as pd
import numpy as np
import re
from re import search
import glob
from datetime import datetime
import time
import math
from scipy.interpolate import interp1d

from functions.homogenization_functions import absorption_efficiency, stoichmetry_conversion, conversion_efficiency, \
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency, \
    return_phipcor, o3_integrate, roc_values, missing_station_values

from functions.df_filter import filter_data, filter_metadata


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

k = 273.15

## parts to be changed by hand!!!!

path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
dfmeta = pd.read_hdf(path + 'Metadata/All_metadata.hdf')
allFiles = sorted(glob.glob(path + "Current/*150924*rawcurrent.hdf"))
roc_table_file = ('/home/poyraden/Analysis/Homogenization_public/Files/sonde_sodankyla_roc.txt')
roc_plevel = 10 # pressure value to obtain roc


humidity_correction = True
missing_ptu = True
# check TLab, PLab, ULab values if some is missing use the following function to get a climatological mean
if missing_ptu:
    plab = missing_station_values(dfmeta, 'Pground', False, 'nan')
    tlab = missing_station_values(dfmeta, 'TLab', False, 'nan')
    ulab = missing_station_values(dfmeta, 'ULab', False, 'nan')
    pflab = missing_station_values(dfmeta, 'PF', True, '20040101') #PF values are

string_bkg_used = 'ib2' #or ib0
string_pump_location = 'InternalPump'


## end of the parts to be changed by hand!!!!

dfmeta = filter_metadata(dfmeta)
#check if dfmeta has "Date" variable, otherwise create it
clms = [i for i in range(1,13)]
table = pd.read_csv(roc_table_file,  skiprows=1, sep="\s *", names = clms,  header=None)
dfmeta = roc_values(dfmeta,table, roc_plevel)
PFmean = np.nanmean(dfmeta[(dfmeta.PF > 0) & (dfmeta.PF < 99)].PF)


if humidity_correction:
    dfmeta = calculate_cph(dfmeta)
    dfmeta['unc_cPH'] = dfmeta['cPH'].std()
    dfmeta['unc_cPL'] = dfmeta['cPL'].std()


#read over all files to do the homogenization

for (filename) in (allFiles):
    file = open(filename, 'r')

    date_tmp = filename.split('/')[-1].split('.')[0][2:8]
    fname = filename.split('/')[-1].split('.')[0][0:8]
    fullname = filename.split('/')[-1].split('.')[0]
    metaname = path + 'Metadata/' + fname + "_metadata.csv"
    if search("2nd", fullname): metaname = path + 'Metadata/' + fname + "_2nd_metadata.csv"


    date = datetime.strptime(date_tmp, '%y%m%d')
    datef = date.strftime('%Y%m%d')
    datestr = str(datef)

    print(filename)

    df = pd.read_hdf(filename)
    dfm = pd.read_csv(metaname)

    df_tmp = dfmeta[dfmeta.Date == datestr]
    df_tmp = df_tmp.reset_index()
    dfm['ROC'] = 0
    dfm['ROC'] = df_tmp.at[0,'ROC']

    print('check 1')


