# o3s-dqa-homogenization
## Needed packages:
python(3.7), pandas, numpy, scipy, matplotlib

### Needed packages if you want to read/write a/to WOUDC file format
please also see: https://github.com/woudc/woudc-extcsv
### Installation

#### Requirements

woudc-extcsv requires Python 3 and [pywoudc](https://github.com/woudc/pywoudc).

#### Dependencies

See `requirements.txt`
- [pywoudc](https://github.com/woudc/pywoudc)

#### Installing the Package

```bash
# via pip
pip install woudc-extcsv
# via easy_install
easy_install woudc-extcsv
```

## Instructions for using this package
These codes are written to read WOUDC csv format or AMES format from NILU or NDACC servers.
If you will read WOUDC format please follow the instructions and codes in woudc folder, if it is for ames format please
 do the same in nilu_ndacc folder.
 
 The third option is for the case if you already have files in txt format, under the folder standard. Please pay attention
 the asumption is to read in 2 txt files always, one for the data and one for the metadata
