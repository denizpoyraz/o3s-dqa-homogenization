import csv
import urllib
import requests
import pandas as pd
from re import search

## this code takes a csv file that has the urls of the each data day, and downloads the corresponding url csv file
## First one needs to download data-file url list from https://woudc.org/data/explore.php?lang=en

# path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'
path = '/home/poyraden/Analysis/Homogenization_public/Files/valentia/'

df = pd.read_csv(path + 'woudc-DataURLFileList_valentia_TO.csv', low_memory=False)
# df = pd.read_csv(path + 'woudc-DataURLFileList_lerwick.csv', low_memory=False)

station_name = 'valentia'
size = len(df)

print(len(df))

for i in range(size):
    print(i)

    url = df.at[i, 'url']
    if search('TO1',str(url)):continue
    # print('url', url)
    # print('split', url.split(".TO1")[-2])
    # print('split', url.split(".TO1")[0][-6:])

    # name = str(url.split(".TO1")[-1].split(".")[0]) + '.csv'
    # year = name[2:6]
    # print(name)

    name = ' '
    if station_name == 'valentia':

        if url[len(url)-3:] == 'TO1':
            year = str(url.split(".TO1")[0][-6:])
            name = year + '.csv'
            print(name)

        if url[len(url)-6:] == 'ME.csv':
            # print('split', url.split("/brewer/")[1].split('/')[1][0:6])
            # year = str(url.split(".Brewer.MKIV.088.ME.csv")[0][-8:-2])
            year =  url.split("/brewer/")[1].split('/')[1][0:6]
            print('year', year)
            name = year + '.csv'


        # if url[len(url) - 6:] == 'ME.csv':
        #     year = str(url.split(".ECC")[0].split('/')[-1].split('.')[-1])
        #     name = year + '.csv'

        if url[len(url) - 6:] == 'me.csv':
            year = str(url.split(".ecc")[0].split('/')[-1].split('.')[-1])
            print(year)
            name = year + '.csv'




    req = requests.get(url)
    url_content = req.content

    csv_file = open(path + 'WOUDC_TO/' + name, 'wb')
    csv_file.write(url_content)
    csv_file.close()



