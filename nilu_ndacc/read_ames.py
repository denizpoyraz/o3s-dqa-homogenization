import sys   # Imports the sys module
sys.path.append("/home/poyraden/napB/")   # Adds the directory to others # used when searching for a module.
import napB as nappy
import pandas as pd
import glob

efile = open("ames_errorfile.txt", "w")


#code that uses modified napy package from Bavo Langerock

K = 273.15
k = 273.15


# filepath = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
filepath = '/home/poyraden/Analysis/Homogenization_public/Files/lerwick/nilu/'
station_name = 'lerwick'

allFiles = sorted(glob.glob(filepath + "le*.*"))
#
for filename in (allFiles):
    df = pd.DataFrame()
    dfm = pd.DataFrame()

    print('filename', filename.split("/nilu/")[1].split(".")[0].split("le")[1])
    date = filename.split("/nilu/")[1].split(".")[0].split("le")[1]
    idate = int(date)
    # print('date', date+"test", type(date))


    if idate == 140312:
        date = str(idate)
    #     print('why not')
    #     continue
    # sdate = str(idate)
    dfm.at[0,'date'] = date
    dfm.at[0, 'DateTime'] = pd.to_datetime(dfm.at[0,'date'], format='%y%m%d')
    # dfm.at[0,'date'] = dfm.at[0, 'DateTime'].datetime.strftime('%Y-%m-%d')
    dfm['date'] = dfm['DateTime'].dt.strftime('%Y%m%d')
    fname = dfm.at[0,'date']

    # if (date == '021210') | (date == '030108') | (date == '030206'):
    #
    #     continue

    #
    try:
        X = nappy.openNAFile(filename)
    except (UnicodeDecodeError, ValueError):
        print('Opening error write to error-file', fname)
        efile.write('Opening Error ' + filename + '\n')
        continue

    #
    try:
        X.readData()
    except (ValueError, UnicodeDecodeError):
        print('ReadingError ', fname)
        efile.write('ReadingError ' +  filename + '\n')
        continue

    # try:
    #     X.readData()
    # except UnicodeDecodeError:
    #     print('UnicodeDecodeError write to error-file', fname)
    #     efile.write('UnicodeDecodeError ' + filename + '\n')

    #
    datac = [' '] * (X.NV)
    for v in range(X.NV):
        (varname, unit, miss, scal) = X.getVariable(v);
        datac[v] = varname
        df[datac[v]] = X.V[v][0]

    df['Pair'] = X.X[0][1]

    mdatac = [''] * len(X.A)

    for j in range(len(X.A)):
        mdatac[j] = X.ANAME[j]
        varname = X.ANAME[j]
        value = X.A[j][0]
        dfm.at[0, mdatac[j]] = value

    dout = filepath + "read_out/" + fname + ".csv"
    mout = filepath + "read_out/" + fname + "_metadata.csv"

    df.to_csv(dout)
    dfm.to_csv(mout)

    #

efile.close()
