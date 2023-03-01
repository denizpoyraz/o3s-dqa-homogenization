import metpy
import numpy as np
from datetime import datetime
from metpy.units import units, pandas_dataframe_to_unit_arrays
from metpy.interpolate import interpolate_1d
from siphon.simplewebservice.wyoming import WyomingUpperAir
from matplotlib import pyplot as plt
from metpy.plots import SkewT
from tropCalc import tropCalc
import pandas as pd

# df = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/lauder/DQA_nors80/19890307_o3sdqa_nors80.csv')
df = pd.read_hdf('/home/poyraden/Analysis/Homogenization_public/Files/lauder/DQA_nors80/19890307_o3sdqa_nors80.hdf')

lapseC = 2*units.kelvin/units.km
height = False

dfc = df[['Pair','Temp']].copy()
dfc.units = pd.Series({'Pair': 'hPa',  'Temp': 'kelvin'})

cdict = {'Pair': 'hPa',  'Temp': 'kelvin'}
metpy.units.pandas_dataframe_to_unit_arrays(dfc, column_units = cdict)
print(dfc.units)

pFull2 = dfc["Pair"].values
TFull2 = dfc["Temp"].values
pFull = dfc["Pair"].values * units(dfc.units["Pair"])
# print(df.units["pressure"])
TFull = dfc["Temp"].values * units(dfc.units["Temp"])

print(tropCalc(pFull,TFull ,lapseC=lapseC,height=height,method="wmo"))