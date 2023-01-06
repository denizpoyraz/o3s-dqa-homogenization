from woudc_extcsv import Reader, ExtendedCSV, load
import woudc_extcsv
import pandas as pd
import numpy as np
import glob
import os

# path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/CSV/'



# read from file
station_name = 'uccle'
folder = f'/home/poyraden/Analysis/Homogenization_public/Files/{station_name}/WOUDC_nors80/'
# f_write_to_woudc_csv(os.path.join(pathfile, datestr + "_o3sdqa" + file_ext + ".hdf"))

allFiles = sorted(glob.glob(f"{folder}*.csv"))
# allFiles = sorted(glob.glob(f"{path}*.csv"))

dfm = pd.DataFrame()
fi = 0

for filename in allFiles:
    print(filename)
    filename = 'data_test.csv'
    extcsv_to = load(filename)
    # extcsv_to = load(filename)
    print((extcsv_to))


