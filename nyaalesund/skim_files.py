import pandas as pd
import glob



path = '/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/DQA_nors80/'

data_files = sorted(glob.glob(path + "*_o3sdqa_nors80.hdf"))

for (filename) in(data_files):

    print(filename)
    df = pd.read_hdf(filename)

    # print(list(df))
    # dfc = df.drop(['WindDir', 'WindSp', 'ibg_tmp', 'Pground', 'CorP', 'Pcor', 'PFcurrent', 'PF_ground',
    #                 'Ical', 'Ical1', 'Ical2', 'Ical3', 'TPump'], axis=1)
    dft = pd.DataFrame()
    dft['Date'] = df['Date']
    dft['Pair'] = df['Pair']
    dft['Time'] = df['Time']
    dft['Alt'] = df['Alt']
    dft['Temp'] = df['Temp']
    dft['I'] = df['I']
    dft['TPump'] = df['Tbox']
    dft['O3'] = df['O3']
    dft['dO3'] = df['dO3']

    name_out = path + 'skim/' + str(dft.at[dft.first_valid_index(),'Date']) + '.csv'
    dft.to_csv(name_out)


    # print(list(dfc))
