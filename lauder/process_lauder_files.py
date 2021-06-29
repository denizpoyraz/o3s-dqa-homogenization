import pandas as pd
import numpy as np
import re
import glob
import math
from math import log
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.offsetbox import AnchoredText
from math import log
from datetime import time
from datetime import datetime
from scipy import signal
from scipy.interpolate import interp1d
from re import search

path = "/home/poyraden/Analysis/Homogenization_public/Files/lauder/csv/"

dataFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_public/Files/lauder/csv/*hdf"))
metadataFiles = sorted(glob.glob("/home/poyraden/Analysis/Homogenization_public/Files/lauder/csv/*csv"))

for (fname,mdname) in zip(dataFiles, metadataFiles):
    # print('one',fname)
    print('one', mdname)

    df = pd.read_hdf(fname)
    dfm = pd.read_csv(mdname)

    # print(list(df))
    # print(list(dfm))

    listm = list(dfm)

    for i in range(len(listm)):

        if (search('Pressure', listm[i])) and (search('flow', listm[i])):
            print(listm[i])


