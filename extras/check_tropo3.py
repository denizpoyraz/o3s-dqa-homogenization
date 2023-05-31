import os
import pickle
pickle.HIGHEST_PROTOCOL = 5
import pandas as pd
import numpy as np
from re import search
from datetime import datetime
import glob

from calc_trop import tropopause_height, tropopause_height_birner

station_name = 'uccle'
path = f'/home/poyraden/Analysis/Homogenization_public/Files/{station_name}'


#non-homogenized time series
# df.to_hdf(path + filefolder + datestr + "_all_hom_" + file_ext + ".hdf", key='df')
allFilesnh = sorted(glob.glob(f'{path}/DQA_nors80/*_all_hom*.hdf'))
#homogenized time-series
allFilesh = sorted(glob.glob(f'{path}/DQA_nors80/*o3sdqa*hdf'))

for (fnh) in (allFilesnh):
    if search('test', fnh):continue
    print('fnh', fnh.split(".")[0])

    outnh = fnh.split(".")[0]+".csv"

    # file = open(filename, 'r')
    # dfm = pd.DataFrame()
    # dfh = pd.read_hdf(fh)
    dfn = pd.read_hdf(fnh)
    #convert to csv for test
    # dfh.to_csv(outh)
    dfn.to_csv(outnh)

