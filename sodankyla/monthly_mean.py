import pandas as pd
from datetime import datetime
from functions.df_filter import filter_metadata


path = '/home/poyraden/Analysis/Homogenization_public/Files/sodankyla/'
dfmeta = pd.read_csv(path + 'Metadata/All_metadata.csv')
dfmeta = filter_metadata(dfmeta)

series = dfmeta[['Date', 'Pground', 'TLab','ULab','PF']]
series['Date']  = series['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
series = series.set_index('Date')
upsampled = series.resample('1M').mean()

series04 = dfmeta[dfmeta.Date < 20040101][['Date', 'Pground', 'TLab','ULab','PF']]
series04['Date']  = series04['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
series04 = series04.set_index('Date')
upsampled04 = series04.resample('1M').mean()



p = [0] * 12
t = [0] * 12
u = [0] * 12
pf = [0] * 12

for i in range(1,13):
    j = i-1
    p[j] = upsampled[upsampled.index.month == i].mean()[0]
    t[j] = upsampled[upsampled.index.month == i].mean()[1]
    u[j] = upsampled[upsampled.index.month == i].mean()[2]
    pf[j] = upsampled04[upsampled04.index.month == i].mean()[3]

print('PLab = ', p)
print('TLab = ', t)
print('ULab = ', u)
print('PF = ', pf)