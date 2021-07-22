from dataclasses import dataclass
import re
import pandas as pd
from typing import List, Dict
from pathlib import Path

from utils import get_arguments

## this code reads the ames files from NILU or NDACC servers and works for most of the stations.
## this code did not work to read Lauder files and NY-Aalesund files after 2017
## this code gives two outputs: one file for the data and one file for the metadata

## usage
# python convert_ozonedata.py path/filename
# or
# python convert_ozonedata.py path
# filename convention: /example/path/tofiles/uc212903.xyz general ames output format

#testing tool in case neede for egexp: https://regex101.com/


@dataclass
class Header:
    lines: int
    column_names: List[str]
    meta_data: Dict[str, float]


def convert_ozonedata(files: List[Path]) -> None:
    """Convert ozone data to hdf and csv files"""

    # Compile regular expressions
    regexp = compile_regexp()
    column_names_regexp = compile_column_names_regexp()

    files = sorted(files)
    size = (len(files))
    datelist = [0]*size

    j = 0
    for file in files:
        fileout = file
        print(file)

        # this part till "end" section is for the naming convention if there are two launches in one day, in other words
        # if there are two launches with same dates
        # begin #
        tmp = file.name.split(".")[0][2:8] # assumes a file format as: "/path/to/files/uc210329.xyz
        datelist[j] = tmp
        if(j > 0) and (j < (size-1)):
            if (datelist[j] == datelist[j-1]):
                tmp = files[j].name.split(".")[0] + "_2nd." + files[j].name.split(".")[1]
                fileout = str(files[j].parent) + "/" + tmp
                fileout = Path(fileout)
        j = j+1
        # end #

        with open(file, 'r', encoding='ISO-8859-1') as rfile:
            data = rfile.read()

        if len(data) < 5000: continue

        header = get_header(file, regexp, column_names_regexp)
        df = get_data(file, header)

        # Write data to hdf and metadata to csv
        constants = extract_constants_from_header(header.meta_data)
        filename = str(fileout)
        #md stands for metadata
        filenamecsv = filename.split(".")[-2] + ('_md.csv')
        filenamehdf = filename.split(".")[-2] + ('_md.hdf')

        # metadata written to hdf and csv format, you can choose only one as well
        pd.Series(constants).to_csv(filenamecsv, header=False)
        pd.Series(constants).to_hdf(filenamehdf, key = 'df')
        # data written to hdf and csv format, you can choose only one as well
        df.to_hdf(fileout.with_suffix('.hdf'), key='df')
        df.to_csv(fileout.with_suffix('.csv'))



def get_header(p: Path, regexp, column_names_regexp) -> Header:
    """Return data contained in the header of the file"""
    with open(p, 'r', encoding='ISO-8859-1') as file:
        data = file.read()


    column_names = column_names_regexp.findall(data)
    match = regexp.search(data)
    position_data = match.span(2)[0]
    header_lines = data[0:position_data].count("\n")
    meta_data = match.groups()[0]

    return Header(header_lines, column_names, meta_data)


def get_data(file: Path, header: Header) -> pd.DataFrame:
    return (pd.read_csv(file,
                        delim_whitespace=True,
                        skiprows=header.lines,
                        names=header.column_names[0:10])).dropna(axis=1)


def compile_column_names_regexp() -> re.Pattern:
    return re.compile(r'''
        ^[^\n]*\([^\s@]+\)
        ''', re.VERBOSE|re.MULTILINE)


def compile_regexp() -> re.Pattern:
    return re.compile(r'''
        ^[z\s]{2,}\n                        # z characters
        ([\s\S]+?)                          # Metadata
    #   (^[-\d\.\s]{1000,}$)                # Numbers separated by whitespace only
       (\d{3,}\.\d[-\d\.\s]{1000,}$)                       #empty lines
        ''', re.VERBOSE|re.MULTILINE)


def extract_constants_from_header(text: str) -> Dict[str, float]:
    pattern = re.compile(r'''
        (^[\s\S]+?)
        ^\d[\s\S]+?
        (^                                    # Numbers separated by whitespace only
          #\s*\d{3}                             # Line starts with spaces (optional) then 3 digits (pressure levels)
          \s*\d{2,}
          [^\n]                        # should not be a new line after 3 digits
          [-\d\.\s]{10,}
          [\s\S]*
        $)      
        ''', re.VERBOSE|re.MULTILINE)
    variables, values = pattern.search(text).groups()
    variables = variables.split("\n")
    variables = [v for v in variables if len(v) > 0]
    values = values.split('\n')
    cleaned_values = []
    for v in values:
        # Remove leading spaces
        v = v.lstrip('File').lstrip()
        if len(v) == 0:
            continue
        # don't split text values (contains any letter that is not E used in exponential numbers)
        if re.search('(?!e)(?!E)[a-zA-Z]', v):
            cleaned_values.append(v)
        else:
            cleaned_values.extend(v.split())
    constants = dict(zip(variables, cleaned_values))
    return constants


if __name__ == "__main__":
    # Get the input files from the arguments
    files = get_arguments()
    convert_ozonedata(files)