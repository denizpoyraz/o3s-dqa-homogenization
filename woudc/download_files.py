import csv
import urllib
import requests
import pandas as pd

## this code takes a csv file that has the urls of the each data day, and downloads the corresponding url csv file
## First one needs to download data-file url list from https://woudc.org/data/explore.php?lang=en

path = '/home/poyraden/Analysis/Homogenization_public/Files/madrid/'

df = pd.read_csv(path + 'woudc-DataURLFileList_missingMadrid.csv', low_memory=False)

size = len(df)


for i in range(size):
    print(i)

    url = df.at[i, 'url']

    name = str(url.split("/")[-1].split(".")[0]) + '.csv'
    year = name[0:4]
    print(name, year)

    req = requests.get(url)
    url_content = req.content

    csv_file = open(path + 'CSV/' + name, 'wb')
    csv_file.write(url_content)
    csv_file.close()



