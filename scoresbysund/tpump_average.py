import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

import calendar


path = '/home/poyraden/Analysis/Homogenization_public/Files/scoresby/'

km_low = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
km_up = [i + 0.1 for i in km_low]
rows, cols = (35, 12)
tpump_cor = [[0]*cols]*rows
tpump = [[0]*cols]*rows

# tpump_cor = [0]* len(km_low)
stpump = ['tpump_' + str(i) for i in km_low]
stpump_cor = ['tpumpcor_' + str(i) for i in km_low]

df = pd.read_csv( "/home/poyraden/Analysis/Homogenization_public/Files/scoresby/TPump_data.csv")

# df = df[df.Date > 19970101]
df = df[df.Date > 20160601]

df['DateTime'] = pd.to_datetime(df['Date'], format='%Y%m%d')


df['Date'] = df['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
series = df.set_index('Date')
upsampled = series.resample('1M').mean()

print(list(upsampled))

var_list = [0] * 12

for i in range(1, 13):
    j = i - 1
    var_list[j] = upsampled[upsampled.index.month == i].median()



print(var_list[0]['tpumpcor_35'])

months = [x for x in calendar.month_name if x]


# for i, (m, k) in enumerate(zip( stpump_cor, months)):
#     print(i, m, k)

for k in range(len(km_low)-1):
    tpump_cor[k] = [var_list[0][stpump_cor[k]], var_list[1][stpump_cor[k]], var_list[2][stpump_cor[k]],
               var_list[3][stpump_cor[k]], var_list[4][stpump_cor[k]], var_list[5][stpump_cor[k]]
    , var_list[6][stpump_cor[k]], var_list[7][stpump_cor[k]], var_list[8][stpump_cor[k]],
               var_list[9][stpump_cor[k]], var_list[10][stpump_cor[k]], var_list[11][stpump_cor[k]]]
    tpump[k] = [var_list[0][stpump[k]], var_list[1][stpump[k]], var_list[2][stpump[k]],
                    var_list[3][stpump[k]], var_list[4][stpump[k]], var_list[5][stpump[k]]
        , var_list[6][stpump[k]], var_list[7][stpump[k]], var_list[8][stpump[k]],
                    var_list[9][stpump[k]], var_list[10][stpump[k]], var_list[11][stpump[k]]]

print(tpump_cor)


for j in range(35):

    fig, ax = plt.subplots(figsize=(17, 9))
    plot_title = 'Scoresbysund Pump temperature monthly means (' + str(km_low[j]) + 'km) after 2016-06'
    plt.title(plot_title)
    plt.plot(months, tpump_cor[j], label = 'DQA')
    plt.plot(months, tpump[j], label = 'NDACC')
    ax.legend(loc='best', frameon=True, fontsize='small')

    plt.ylim([275,305])

    plt.savefig(path + 'Plots/TPump/DQA_monthlymean_after2016_v2' + str(km_low[j]) + '.png')
    # plt.show()
    plt.close()

