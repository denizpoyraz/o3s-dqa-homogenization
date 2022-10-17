import pandas as pd
import glob
from datetime import datetime
from re import search


from nilu_ndacc.read_nilu_functions import organize_df, o3tocurrent, missing_tpump

K = 273.15
k = 273.15


filepath = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'

##read datafiles
allFiles = sorted(glob.glob(filepath + "Metadata/*_metadata.csv"))

# print(allFiles)

list_metadata = []


for filename in (allFiles):

    dfm = pd.read_csv(filename)

    list_metadata.append(dfm)

dff = pd.concat(list_metadata, ignore_index=True)
hdfall = filepath + "Metadata/All_metadata.hdf"
csvall = filepath + "Metadata/All_metadata.csv"

dff.to_hdf(hdfall, key = 'df')
dff.to_csv(csvall)




