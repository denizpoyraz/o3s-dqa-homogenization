## Instructions for reading ames (nilu,ndacc servers) formats
### convert_ozonedata.py: 
This code reads ames files and extracts the data and metadata using regular expressions. 
Plase pay attention that the code may not work 100% for all files.
This code gives two outputs: one dataframe for the data and one dataframe for the metadata
### read_nilucsv.py:
This code reads the output of convert_ozonedata.py and calculates the raw current as it is done in the
Vaisala software. The output is written to a dataframe with "rawcurrent" extension and all the metadata is saved in
one dataframe which will be used in homogenisation code to calculate some uncertainties.  

### homogenize_ozonesonde.py:
This code homogenizes the ozoensonde data. Please pay attention to the remarks about changes (solution type, radiosonde type..)
mentioned in the code.

