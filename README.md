# o3s-dqa-homogenization
## Needed packages:
python(3.7), pandas, numpy, scipy, matplotlib

### Needed packages if you want to read/write a/to WOUDC file format
please also see: https://github.com/woudc/woudc-extcsv
### Installation

#### Requirements

woudc-extcsv requires Python 3 and [pywoudc](https://github.com/woudc/pywoudc).
This code works with woudc-extcsv==0.3.1
#### Dependencies

See `requirements.txt`
- [pywoudc](https://github.com/woudc/pywoudc)

#### Installing the Package

```bash
# via pip
pip install woudc-extcsv
(pip install woudc-extcsv==0.3.1)
# via easy_install
easy_install woudc-extcsv
```

## Instructions for using this package
- downloading woudc files from WOUDC data-server use woudc/download_files.py
and woudc/read_woudc_csv.py
- downloading nilu/ndacc files: use nilu_ndacc/read_ames.py
  (alternatively->) nilu_ndacc/convert_ozonedata.py and nilu_ndacc/read_nilu.csv
- for homogenization:
- run standard/homogenization_station.py this code read the ozonesonde data, runs DQA recommended
homogenization and write them to woudc csv format.
- if you want to read homogenized dqa woudc csv files you can use standard/read_dqa_woudc.py
##note for woudc_extcsv library
- There is mismatch between  [1] https://guide.woudc.org/en/#334-category-ozonesonde recommendations 
 and woudc_extcsv code. If you want to use [1] recommendation
https://github.com/woudc/woudc-extcsv/blob/dc4de2ca71e4f9676728b59826250ddcced91e3c/woudc_extcsv/__init__.py#L78-L93
need to changed to 
- https://github.com/denizpoyraz/o3s-dqa-homogenization/blob/7030d45f1ab53fabb90899e97a1ca60cf8b74d3d/woudc/example__init__.py#L78-L100


##napB package added to read ames files, do not forget to copy this folder as well