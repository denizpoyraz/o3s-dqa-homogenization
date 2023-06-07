## How to process Lauder files:
Files are provided by the station PI. 
#### Step 1:
Read the files (.dat) by code read_lauder_files.py
The output of this code is 2 files per each date, 1 file that has the data and 2nd file has the metadata.
#### Step 2:
process_lauder_files.py organizes the naming conventions and makes a merged metadata of the full time series.
The output of this code is a merged metadata file which contains all time-series.
If you like to process new files, please run this code on new files and do not forget to merge the new processed merged
metada with the previous one which is under lauder/files/Lauder_MetadataAll.csv
The time range of Lauder_MetadataAll.csv is from 1986-08-03 to 2021-06-22 	

#### Step 3:
https://github.com/denizpoyraz/o3s-dqa-homogenization/blob/2c79e99275ff5fdf391084f2f0392813dabd1d33/functions/functions_perstation.py#L60-L65
dfmetaf: the merged metadata files of the all time-series. For period 1986-08-03 to 2021-06-22 it is under lauder/files/
allFilesf: the location of data files which are output of Step1
roc_table_filef: this is under lauder/files/

With these input you can run standard/homogenization_station.py just need to change line 49 station_name to 'lauder'
The output will be homogenized files that are written in WOUDC format.
