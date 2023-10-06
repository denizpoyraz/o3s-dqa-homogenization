import pandas as pd
import glob
from datetime import datetime
from re import search
from functions.homogenization_functions import missing_station_values, assign_missing_ptupf, ComputeCef, ComputeIBG
from functions.functions_perstation import rename_variables
kelvin = 273.15


filepath = '/home/poyraden/Analysis/Homogenization_public/Files/lerwick/'

dfmeta = pd.read_csv(filepath + "nilu/Metadata/All_metadata_nilu.csv" )
dfmeta_woudc = pd.read_csv(filepath + "all_csv_current/metadata/Lerwick_WOUDC_Metadata.csv")

niluFiles = sorted(glob.glob(filepath + "nilu/read_out/*.csv"))
woFiles = sorted(glob.glob(filepath + "WOUDC_CSV/read_out/*.hdf"))
wo_md_Files = sorted(glob.glob(filepath + "WOUDC_CSV/read_out/*metadata.csv"))

allFiles = sorted(glob.glob(filepath + "all_csv/*.csv"))
read_woudc = False
read_md_woudc = False
read_nilu = False
write_all_md = False
use_metadata_woudc = False
calculate_current = False
assign_missing = True
#first read all woudc files and correct metadata and data naming

list_md = []
if read_md_woudc:
    for (filename) in (wo_md_Files):
        print('read_md_woudc',filename)
        dfw = pd.read_csv(filename)
        list_md.append(dfw)

    name_out = 'Lerwick_WOUDC_Metadata.csv'
    dfmaw = pd.concat(list_md, ignore_index=True)
    dfmaw.to_csv(filepath + "all_csv_current/" + name_out)




if read_nilu:
    for (filename) in (niluFiles):
        if search('metadata', filename):continue
        print('read_nilu',filename)
        ndate = filename.split("read_out/")[1].split(".")[0]
        print(ndate)
        dfn = pd.read_csv(filename)

        dfn['Date'] = ndate
        dfn['O3'] = dfn['Ozone partial pressure']
        dfn['Tpump'] = dfn['Temperature inside styrofoam box'].astype(float) + kelvin
        dfn['Eta'] = 1
        dfn['TboxK'] = dfn['Tpump']
        dfn['Height'] = dfn['Geopotential height']
        dfn['RelativeHumidity'] = dfn['Relative humidity']
        dfn['WindSpeed'] = dfn[ 'Horizontal wind speed']
        dfn['WindDirection'] = dfn[ 'Horizontal wind direction']
        dfn['Duration'] = dfn['Time after launch']

        dfn.to_csv(f'/home/poyraden/Analysis/Homogenization_public/Files/lerwick/all_csv/{ndate}.csv')

if read_woudc:
    for (filename) in (woFiles):
        print('read_woudc', filename)
        dfw = pd.read_hdf(filename)
        dfw['Date1'] = dfw['Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
        dfw['Datet'] = dfw['Date1'].dt.strftime('%Y%m%d')
       
        dfw['Date'] = dfw['Datet']
        ndate = dfw.at[10,'Date']
        dfw['O3'] = dfw['O3PartialPressure']
        dfw['Tpump'] = dfw['SampleTemperature'].astype(float) + kelvin
        dfw['Eta'] = 1
        dfw['Pair'] = dfw['Pressure']
        dfw['TboxK'] = dfw['Tpump']
        dfw['Height'] = dfw['GPHeight']

        dfw.to_csv(f'/home/poyraden/Analysis/Homogenization_public/Files/lerwick/all_csv/{ndate}.csv')
    

##now organize metada, calculate climatlogical means and overall means
date_missing = '2004-02-19'
# date_missing = 20040219

dfmeta['Date1'] = dfmeta['DateTime'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
dfmeta['Date'] = dfmeta['Date1'].dt.strftime('%Y%m%d')
dfmeta['Datet'] = dfmeta['Date'].astype(int)


dfmeta['PLab'] = dfmeta['Pground']
# dfmeta['Date'] = dfmeta['DateTime']
dfmeta['PF_NaN'] = 0
dfmeta.loc[dfmeta['PF'].isnull(), 'PF_NaN'] = 1
dfmeta['iB0_NaN'] = 0
dfmeta['iB2_NaN'] = 0
dfmeta.loc[dfmeta['iB0'].isnull(), 'iB0_NaN'] = 1
dfmeta.loc[dfmeta['iB2'].isnull(), 'iB2_NaN'] = 1

filt_ib0 = (dfmeta.iB0 < 1) & (dfmeta.iB0 >-1)
filt_ib2 = (dfmeta.iB2 < 1) & (dfmeta.iB2 >-1)


pf_mean = dfmeta[dfmeta.PF_NaN == 0].PF.mean()
ib0_mean = dfmeta[(dfmeta.iB0_NaN == 0) & (filt_ib0)].iB0.mean()
ib2_mean = dfmeta[(dfmeta.iB2_NaN == 0) & (filt_ib2)].iB2.mean()

pf_median = dfmeta[dfmeta.PF_NaN == 0].PF.median()
ib0_median = dfmeta[(dfmeta.iB0_NaN == 0) & filt_ib0].iB0.median()
ib2_median = dfmeta[(dfmeta.iB2_NaN == 0) & (filt_ib2)].iB2.median()

pf_std = dfmeta[dfmeta.PF_NaN == 0].PF.std()
ib0_std = dfmeta[(dfmeta.iB0_NaN == 0) & (filt_ib0)].iB0.std()
ib2_std = dfmeta[(dfmeta.iB2_NaN == 0) & (filt_ib2)].iB2.std()

pf_mad = dfmeta[dfmeta.PF_NaN == 0].PF.mad()
ib0_mad = dfmeta[(dfmeta.iB0_NaN == 0) & (filt_ib0)].iB0.mad()
ib2_mad = dfmeta[(dfmeta.iB2_NaN == 0) & (filt_ib2)].iB2.mad()

print('means', pf_mean, ib0_mean, ib2_mean)
print('medians', pf_median, ib0_median, ib2_median)
print('stds', pf_std, ib0_std, ib2_std)

print('mads', pf_mad, ib0_mad, ib2_mad)

plab = missing_station_values(dfmeta, 'PLab', False, 'nan')
tlab = missing_station_values(dfmeta, 'TLab', False, 'nan')
ulab = missing_station_values(dfmeta, 'ULab', False, 'nan')

pflab = missing_station_values(dfmeta, 'PF', False, 'nan')  # PF values are

dfmeta = assign_missing_ptupf(dfmeta, True, True, True, False, date_missing, date_missing, date_missing,
                              date_missing, plab, tlab, ulab, pflab)

# dfmeta['SensorType'] = dfmeta['SerialECC']

listall = []

if calculate_current:
#now calculate current
    for (filename) in (allFiles):
        if search('metadata', filename): continue
        df = pd.read_csv(filename)
        datet = df.at[10,'Date']

        df['SolutionVolume'] = 3.0

        # if datet > 20030101:continue
        # if datet < 19991001:continue

        print('main', filename)

        ##set dfm for before 2002 and after
        if datet >= 20021202:
            # print(datet)
            dfm = dfmeta[dfmeta.Datet == datet][0:1]
            dfm = dfm.reset_index()
            if len(dfm) == 1:
                dfm['SolutionVolume'] = 3.0
                sensortype = dfm.at[0,'SerialECC']
                dfm.at[0, 'SensorType'] = 'SPC'

            if len(dfm) == 0:
                dfm = pd.DataFrame()
                dfm.at[0, 'iB2'] = ib2_median
                dfm['iB0'] = ib0_median
                dfm['PF'] = pf_median
                dfm['SerialECC'] = '6Axxx'
                dfm['SensorType'] = 'SPC'
                dfm['Date'] = datet
                # dfm['Date'] = dfm['Date1'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
                # dfm['Date'] = pd.to_datetime(dfm['Date'], format='%Y-%m-%d')
                sensortype = dfm.at[0,'SerialECC']


            if not((search('SPC', sensortype)) or (search('6A', sensortype)) or (search('5A', sensortype)) or (
                search('6a', sensortype)) or (search('5a', sensortype)) or (search('Z', sensortype)) or (search('z', sensortype))
            or (search('ENSCI', sensortype))):
                dfm.at[0,'SerialECC'] = '6Axxx'
                dfm.at[0, 'SensorType'] = 'SPC'
            # print(dfm.at[0,'SerialECC'])
            if datet <= 20040219:
                dfm.at[0, 'iB2'] = ib2_median
                dfm['iB0'] = ib0_median
                dfm['PF'] = pf_median
                dfm['SolutionVolume'] = 3.0
                dfm['Date'] = int(datet)
                dfm.at[0, 'SensorType'] = 'SPC'

        if datet <= 20021202:
            dfm = pd.DataFrame()
            dfm.at[0,'iB2'] = ib2_median
            dfm['iB0'] = ib0_median
            dfm['PF'] = pf_median
            dfm['SolutionVolume'] = 3.0
            dfm['Date'] = int(datet)
            # dfm['Date'] = dfm['Date1'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
            dfm['Date'] = pd.to_datetime(dfm['Date'], format='%Y-%m-%d')


            dfm = assign_missing_ptupf(dfm, True, True, True, False, date_missing, date_missing, date_missing,
                                       date_missing, plab, tlab, ulab, pflab)
            dfm.at[0, 'SensorType'] = 'SPC'
            # dfm['Date'] = dfm['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
            dfm['Date'] = int(datet)


            # if datet <= 19970910:
            #     dfm.at[0, 'SerialECC'] = 'ZENSCIxxx'
            #     dfm.at[0, 'SensorType'] = 'DMT-Z'

        # print(dfm.at[0, 'SensorType'])
        df['Cef'] = ComputeCef(df, dfm)

        cref = 1
        df['ibg'] = 0
        df['iB2'] = dfm.at[0,'iB2']

        if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'SPC':
            df['ibg'] = ComputeIBG(df, 'iB2')
        if dfm.at[dfm.first_valid_index(), 'SensorType'] == 'DMT-Z':
            df['ibg'] = dfm.at[dfm.first_valid_index(), 'iB2']

        df['I'] = df['O3'] / (
                4.3085 * 10 ** (-4) * df['TboxK'] * dfm.at[dfm.first_valid_index(), 'PF'] * df['Cef'] * cref) + \
                   df['ibg']


        #now add woudc variables to the dfm
        if use_metadata_woudc:
            # dt2 = dfm.at[0,'Date2']
            # print('use meta woudc')
            dfm['date_tmp'] = df.at[10,'Date']
            dfm['dates'] = pd.to_datetime(dfm['date_tmp'], format='%Y%m%d')
            dt2 = dfm.at[0, 'dates'].date()
            # .date()
            dfmw = dfmeta_woudc[dfmeta_woudc.TIMESTAMP_Date == str(dt2)]
            dfmw = dfmw.reset_index()
            if len(dfmw) ==1:
                # print(list(dfmw))
                dfm['agency'] = dfmw['DATA_GENERATION_Agency']
                dfm['stationPI'] = dfmw['DATA_GENERATION_ScientificAuthority']
                dfm['type'] = dfmw['PLATFORM_Type']
                dfm['id'] = dfmw['PLATFORM_ID']
                dfm['name'] = dfmw['PLATFORM_Name']
                dfm['country'] = dfmw['PLATFORM_Country']
                dfm['gaw_id'] = dfmw['PLATFORM_GAW_ID']
                dfm['Name'] = dfmw['INSTRUMENT_Name']
                # if search('5A', eccmodel) | search('5a', eccmodel)
                dfm['SensorType'] = dfmw['INSTRUMENT_Model']
                dfm['SerialECC'] = dfmw['INSTRUMENT_Number']
                dfm['latitude'] = dfmw['LOCATION_Latitude']
                dfm['longitude'] = dfmw['LOCATION_Longitude']
                dfm['height'] = dfmw['LOCATION_Height']
                # df_names = 'UTCOffset', 'Date', 'LaunchTime'
                dfm['UTCOffset'] = dfmw['TIMESTAMP_UTCOffset']
                dfm['DateTime'] = dfmw['TIMESTAMP_Date']
                dfm['LaunchTime'] = dfmw['TIMESTAMP_Time']
            if len(dfmw) == 0:
                dfm['agency'] = 9999
                dfm['stationPI'] = 9999
                dfm['type'] = 9999
                dfm['id'] = 9999
                dfm['name'] = 9999
                dfm['country'] = 9999
                dfm['gaw_id'] = 9999
                dfm['Name'] = 9999
                # dfm['SensorType'] = 9999
                # dfm['SerialECC'] = dfmw['INSTRUMENT_Number']
                dfm['latitude'] = 9999
                dfm['longitude'] = 9999
                dfm['height'] = 9999
                dfm['UTCOffset'] = 9999
                dfm['DateTime'] = 9999
                dfm['LaunchTime'] = 9999



        df.to_csv(f'/home/poyraden/Analysis/Homogenization_public/Files/lerwick/all_csv_current/{datet}.csv')
        dfm.to_csv(f'/home/poyraden/Analysis/Homogenization_public/Files/lerwick/all_csv_current/{datet}_metadata.csv')

        listall.append(dfm)

if write_all_md:
    
    name_out = 'Lerwick_Metadata_combined.csv'
    dfall = pd.concat(listall, ignore_index=True)
    dfall.loc[dfall.DateTime==9999,'DateTime'] = dfall.loc[dfall.DateTime==9999,'Date2']
    dfall.loc[dfall.LaunchTime==9999,'LaunchTime'] = "11:30:00"
    date_missing = '20040219'

    # dfall = assign_missing_ptupf(dfall, True, True, True, False, date_missing, date_missing, date_missing,
    #                               date_missing, plab, tlab, ulab, pflab)

    dfall.to_csv(filepath + "all_csv_current/metadata/" + name_out)



if assign_missing:
    name = 'Lerwick_Metadata_combined.csv'
    dfmm = pd.read_csv(filepath + "all_csv_current/metadata/" + name)

    date_missing = 20040219

    print(dfmm.Date[0:5])

    dfmm_out = assign_missing_ptupf(dfmm, True, True, True, False, date_missing, date_missing, date_missing,
                                  date_missing, plab, tlab, ulab, pflab)

    dfmm_out.to_csv(filepath + "all_csv_current/metadata/" + "Lerwick_Metadata_combined_final.csv")




# ulab = [0] * 12, tlab=[0]*12, plab=[0]*12


# print('P')


# list_one = ['DATA_GENERATION_Date', 'DATA_GENERATION_Agency', 'DATA_GENERATION_ScientificAuthority',
#             'PLATFORM_Type', 'PLATFORM_ID', 'PLATFORM_Name', 'PLATFORM_Country', 'PLATFORM_GAW_ID',
#             'INSTRUMENT_Name', 'INSTRUMENT_Model', 'INSTRUMENT_Number',
#             'LOCATION_Latitude', 'LOCATION_Longitude', 'LOCATION_Height',
#             'TIMESTAMP_UTCOffset', 'TIMESTAMP_Date', 'TIMESTAMP_Time']
# list_two = ['wDate', 'Agency', 'Station_PI', 'Type', 'ID', 'Station', 'Country', 'GAW_ID', 'InsName', 'InsModel',
#             'InsNumber', ]
# dfw = rename_variables(dfw,,
#       ['wDate', 'wAgency', 'wStation_PI', 'Height'])