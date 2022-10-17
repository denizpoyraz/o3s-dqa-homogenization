import csv
import numpy as np
from io import StringIO
from woudc_extcsv import load, WOUDCExtCSVReaderError
import pandas as pd
import glob

def calc_average_profile_pressure(dft, xcolumn):
    # nd = len(dataframelist)

    # yref = [1000, 850, 700, 550, 400, 350, 300, 200, 150, 100, 75, 50, 35, 25, 20, 15,
    #         12, 10, 8, 6]

    yref = [1000, 950, 900, 850, 800, 750, 700, 650, 600,  550, 500, 450,  400, 350, 325, 300, 275, 250, 240, 230, 220, 210, 200,
            190, 180, 170, 160, 150, 140, 130, 125, 120, 115, 110, 105,  100,95, 90, 85, 80, 75, 70, 65, 60, 55,
            50, 45, 40,  35, 30, 28, 26, 24, 22,  20, 19, 18, 17, 16, 15,  14, 13.5, 13, 12.5,  12, 11.5, 11, 10.5,
            10, 9.75, 9.50, 9.25, 9, 8.75, 8.5, 8.25,  8, 7.75, 7.5, 7.25,  7, 6.75, 6.50, 6.25, 6]

    # yref = [i * 250 for i in range(0, 160)]

    n = len(yref) - 1
    Ygrid = [-9999.0] * n

    Xgrid = [-9999.0] * n
    Xsigma = [-9999.0] * n
    #
    # Xgrid = [[-9999.0] * n for i in range(nd)]
    # Xsigma = [[-9999.0] * n for i in range(nd)]


# for j in range(nd):
#     dft.PFcor = dft[xcolumn]

    for i in range(n):
        dftmp1 = pd.DataFrame()
        dfgrid = pd.DataFrame()


        grid_min = yref[i+1]
        grid_max = yref[i]
        Ygrid[i] = (grid_min + grid_max) / 2.0

        filta = dft.Pair >= grid_min
        filtb = dft.Pair < grid_max
        filter1 = filta & filtb
        dftmp1['X'] = dft[filter1][xcolumn]

        filtnull = dftmp1.X > -9999.0
        dfgrid['X'] = dftmp1[filtnull].X

        Xgrid[i] = np.nanmean(dfgrid.X)
        Xsigma[i] = np.nanstd(dfgrid.X)


    return Xgrid, Xsigma, Ygrid



def read_woudc(fname, efile, path):
    '''
    :param fname:
    :param efile:
    :return:
    '''

    fi = 0

    dfm = pd.DataFrame()

    print(fname)
    tmp = fname.split('.')[0][-8:]
    # try except is applied for the cases when there is formatting error: WOUDCExtCSVReaderError
    extcsv_to = load(fname)

    try:
        extcsv_to = load(fname)
        # access all tables
        tables = extcsv_to.sections.keys()

        ## first copy the profile data and delete this from the keys to save the metadata. For Praha data it is 'PORFILE',
        # watch out that this naming may change from station to station
        profile_keys = extcsv_to.sections['PROFILE'].keys()
        Profile = extcsv_to.sections['PROFILE']['_raw']
        del extcsv_to.sections['PROFILE']
        # profile_uncertainity = extcsv_to.sections['PROFILE_UNCERTAINTY']['_raw']
        # del extcsv_to.sections['PROFILE_UNCERTAINTY']

    except WOUDCExtCSVReaderError:
        print('error')
        efile.write(fname + '\n')
        tables = [0]

    msize = len(tables)
    # print(msize)

    for i in range(msize):
        dict = list(tables)[i]
        # print('dict',dict)
        keys = extcsv_to.sections[dict].keys()
        # print('keys', keys)
        ksize = len(keys)
        if ksize == 1:
            test = extcsv_to.sections[dict]['_raw']
            test_df = pd.read_csv(StringIO(test))
            tsize = len(test_df.columns)
            for t in range(tsize):
                cstr = test_df.columns.tolist()
                if (len(test_df) > 0):
                    dfm.at[fi, cstr[t]] = test_df.at[test_df.first_valid_index(), cstr[t]]
                if (len(test_df) == 0): continue

        for j in range(1, ksize):
            mstr = dict
            kstr = list(keys)[j]
            if kstr == '_raw': kstr = ""
            astr = mstr + '_' + kstr
            dfm.at[fi, astr] = extcsv_to.sections[dict][list(keys)[j]]

    dfprofile = StringIO(Profile)
    df = pd.read_csv(dfprofile)
    df['Date'] = dfm.at[fi, 'TIMESTAMP_Date']
    df['Station'] = dfm.at[fi, 'DATA_GENERATION_Agency']

    filenamestr = tmp + '_out'
    metastr = tmp + '_metadata'

    df.to_csv(path + "/read_out/" + filenamestr + ".csv")
    df.to_hdf(path + "/read_out/" + filenamestr + ".hdf", key='df')

    dfmt = dfm[fi:fi + 1]
    dfmt.to_csv(path + "/read_out/" + metastr + ".csv")

    fi = fi + 1
    
    
    
    return df, dfm