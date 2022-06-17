import pandas as pd
import glob
from datetime import datetime
from re import search

K = 273.15


#paper md
np = ['SerialNumber', 'DateManufactured', 'LabPressure', 'LabTemp', 'LabRH', 'Airflows', 'Airflowc',
      'Date', 'BackgroundCurrentib', 'Surf.Pressure', 'GroundOzone','Date_1stprep']
dfp = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_8812_ib.csv'
                  ,names=np, header=0)
dfp = dfp[dfp.Date < '2014-01-01']
dfp = dfp.reset_index()
#ames md
dfa = pd.read_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Metadata/All_metadata.csv')
#error md
dfe = pd.read_excel('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/Nyaalesund_Metadata_ib_discrepancy.xlsx')

#date format fixing

print('dfp paper', list(dfp))
print('dfa ames', list(dfa))
print('dfe error file',list(dfe))


dfp['Date'] = pd.to_datetime(dfp['Date'], format='%Y-%m-%d')
dfp['Date'] = dfp['Date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
# dfp = dfp[dfp.Date < '20150101']
dfa['Date'] = pd.to_datetime(dfa['Date'], format='%Y%m%d')
dfa['Date'] = dfa['Date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
dfe['Date'] = dfe['Datib0'].astype(str)

print('paper',len(dfp), dfp.Date.min(), dfp.Date.max())
print('ames',len(dfa),dfa.Date.min(), dfa.Date.max())
print('error',len(dfe), dfe.Date.min(), dfe.Date.max())

#First assign iB2, PF, PLab, TLab, RHLab to dfa, df ames the main metadata df
for d in range(len(dfp)):
    dtmp = dfp.loc[d,'Date']
    dfa.loc[dfa.Date == dtmp,'PLab'] = dfp.at[d,'LabPressure']

# error file
dfe['value_is_NaN'] = 0
dfe.loc[dfe['Error Code'].isnull(), 'value_is_NaN'] = 1
dfe = dfe[dfe['value_is_NaN'] == 0 ]
dfe = dfe.reset_index()



#
# * code PFX: impact on profile --> convert ozone partial pressure with erroneous PF from metadata header to currents,
# and use true airflow (from metadata Excel sheet) in the reprocessing (and conversion to ozone partial pressures in the end)
# * code oA: smaller impact on profile --> same action as here above
# * code ib2X: impact on profile --> convert ozone partial pressure with erroneous
# IB2 from metadata header to currents, and use true IB2 (from metadata Excel sheet)
# in the reprocessing (and conversion to ozone partial pressures in the end)
# * code X: impact on profile --> the measured IB2 value was way to high.
# Use it to convert the ozone partial pressure to current, but use a climatological IB2 value for the reprocessing.

dfa['PFcurrent'] = dfa['PF']
# dfa['iB2current'] = 0

# dfa['iB2current'] = dfa['iB2']


for p in range(len(dfp)):
    pdate = dfp.at[p,'Date']
    if pdate < '20030905':
        # print(pdate, (len(dfa[dfa.Date == pdate])),len(dfp[dfp.Date == pdate]) )
        # print(dfa[dfa.Date == pdate])
        if (len(dfa[dfa.Date == pdate]) == 0) :continue
        # print(dfp[dfp.Date == pdate]['Airflows'])
        # print('start dfa iB2', dfa.loc[dfa.Date == pdate, 'iB2'])
        # print('dfp iB2',dfp[dfp.Date == pdate]['BackgroundCurrentib'])
        # print('dfp two', dfp.loc[dfp.Date == pdate, 'BackgroundCurrentib'].tolist()[0])
        dfa.loc[dfa.Date == pdate, 'PF'] = dfp.loc[dfp.Date == pdate, 'Airflows'].tolist()[0]
        dfa.loc[dfa.Date == pdate, 'iB2'] = dfp.loc[dfp.Date == pdate, 'BackgroundCurrentib'].tolist()[0]
        dfa.loc[dfa.Date == pdate, 'PLab'] = dfp[dfp.Date == pdate]['LabPressure'].tolist()[0]
        print(pdate,dfp.loc[dfp.Date == pdate, 'BackgroundCurrentib'].tolist()[0] )

        dfa.loc[dfa.Date == pdate, 'TLab'] = dfp[dfp.Date == pdate]['LabTemp'].tolist()[0]
        dfa.loc[dfa.Date == pdate, 'RHLab'] = dfp[dfp.Date == pdate]['LabRH'].tolist()[0]
        # print('after', dfa.loc[dfa.Date == pdate, 'iB2'])



dfa['iB2current'] = dfa['iB2']
dfa['PFcurrent'] = dfa['PF']


for i in range(len(dfe)):
    ddate = dfe.at[i,'Date']
    if (len(dfa[dfa.Date == ddate]) == 0): continue
    if (len(dfp[dfp.Date == ddate]) == 0):continue

    if search('PFX',dfe.at[i,'Error Code'] ):
        # print(ddate, dfe.at[i, 'Error Code'] )

        dfa.loc[dfa.Date == ddate, 'PFcurrent'] = dfa[dfa.Date == ddate]['PF'].tolist()[0]
        dfa.loc[dfa.Date == ddate, 'PF'] = dfp[dfp.Date == ddate]['Airflows'].tolist()[0]
        # print(ddate, dfe.at[i, 'Error Code'] )

    if search('oA',dfe.at[i,'Error Code'] ):
        dfa.loc[dfa.Date == ddate, 'PFcurrent'] = dfa[dfa.Date == ddate]['PF'].tolist()[0]
        dfa.loc[dfa.Date == ddate, 'PF'] = dfp[dfp.Date == ddate]['Airflows'].tolist()[0]
        # print(ddate, dfe.at[i, 'Error Code'] )

    if search('ib2X', dfe.at[i, 'Error Code']):
        dfa.loc[dfa.Date == ddate, 'iB2current'] = dfa[dfa.Date == ddate]['iB2'].tolist()[0]
        dfa.loc[dfa.Date == ddate, 'iB2'] = dfp[dfp.Date == ddate]['BackgroundCurrentib'].tolist()[0]

        print(ddate, dfe.at[i, 'Error Code'] )


dfb = dfa[dfa.iB2 < 1]
dfp = dfa[dfa.PF != 28.0]

dfa.loc[dfa.iB2 > 1, 'iB2'] = dfb.iB2.median()
dfa.loc[dfa.PF == 28.0, 'PF'] = dfp.PF.median()

dfa.loc[dfa.iB2 > 1,'iB2current'] = dfb.iB2.median()
dfa.loc[dfa.PF == 28.0, 'PFcurrent'] = dfp.PF.median()
dfa['TLab'] = dfa.TLab.astype(float)

dfa.loc[dfa.TLab > K, 'TLab'] = dfa.loc[dfa.TLab > K,'TLab'] - K

dfa.to_csv('/home/poyraden/Analysis/Homogenization_public/Files/ny-aalesund/NY_metadata.csv')