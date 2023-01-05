import woudc_extcsv

# create new writer object with common/metadata tables and fields available
ecsv = woudc_extcsv.Writer(template=True)

# Add file comments
ecsv.add_comment('This is a file level comment.')
ecsv.add_comment('This is another file level comment.')

# Add metadata
ecsv.add_data('CONTENT',
              'WOUDC,Spectral,1.0,1')
ecsv.add_data('DATA_GENERATION',
              '2002-05-29,JMA,1.0')
ecsv.add_data('PLATFORM',
              'STN,7,Kagoshima,JPN,47827')
ecsv.add_data('INSTRUMENT',
              'Brewer,MKII,059')
ecsv.add_data('LOCATION',
              '31.63,130.6,283')

# Add new table
ecsv.add_table('TIMESTAMP')
# Add fields
ecsv.add_field('TIMESTAMP', 'UTCOffset,Date,Time')
# Add data
ecsv.add_data('TIMESTAMP', '+08:38:47,1991-01-01,06:38:47')

# Add new table, fields, and data at the same time
ecsv.add_data('GLOBAL_SUMMARY',
              '06:38:47,7.117E-04,8.980E-03,94.12,99.99,114.64,001000,999',
              field='Time,IntACGIH,IntCIE,ZenAngle,MuValue,AzimAngle,Flag,TempC')
ecsv.add_data('GLOBAL',
              '290.0,0.000E+00',
              field='Wavelength,S-Irradiance,Time')
ecsv.add_data('GLOBAL',
              '290.5,0.000E+00')
ecsv.add_data('GLOBAL',
              '291.0,0.000E+00')
ecsv.add_table_comment('GLOBAL', 'This is a table level comment', index=1)
# Add table for new groupings
ecsv.add_data('TIMESTAMP',
              '+08:38:46,1991-01-01,07:38:46',
              field='UTCOffset,Date,Time',
              index=2)

ecsv.add_data('GLOBAL_SUMMARY',
              '07:38:46,2.376E-02,3.984E-01,82.92,6.75,122.69,100000,999',
              field='Time,IntACGIH,IntCIE,ZenAngle,MuValue,AzimAngle,Flag,TempC',
              index=2, table_comment='This is a table level comment.')
ecsv.add_table_comment('GLOBAL_SUMMARY', 'This is another table level comment', index=2)
# Write to string
ecsvs = woudc_extcsv.dumps(ecsv)

# Write to file
# validate (check if all common tables and their fields are present), if so dump to file
# if not, print violations
woudc_extcsv.dump(ecsv, 'spectral-sample.csv')