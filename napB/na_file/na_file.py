# -*- coding: utf-8 -*-
#   Copyright (C) 2004 CCLRC & NERC( Natural Environment Research Council ).
#   This software may be distributed under the terms of the
#   Q Public License, version 1.0 or later. http://ndg.nerc.ac.uk/public_docs/QPublic_license.txt

"""
naFile.py
=========

A containter module for the mixin base class NAFile that is subclassed
for individual FFIs. Each FFI class is held in an individual file.

"""
   
# 08/05/04 updated by selatham for bug fixes and new write methods

# Imports from python standard library
import sys
import time,datetime
import re
import io
import numpy as np

# Imports from nappy package
import napB.na_file.na_core
import napB.utils.text_parser
import napB.utils.common_utils
import napB.na_error

default_delimiter = napB.utils.getDefault("default_delimiter")
default_float_format = napB.utils.getDefault("default_float_format")
getAnnotation = napB.utils.common_utils.getAnnotation
wrapLine = napB.utils.common_utils.annotateLine
wrapLines = napB.utils.common_utils.annotateLines
stripQuotes = napB.utils.common_utils.stripQuotes

import logging
#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NAFile(napB.na_file.na_core.NACore):

    """
    NAFile class is a sub-class of NACore abstract classes.
    NAFile is also an abstract class and should not be called directly.
    
    NAFile holds all the methods that are common to either all or more than
    one NASA Ames FFI class. These methods set up the main read and write
    functionality for the NASA Ames format.

    When a sub-class of NAFile is called with a read ('r' - default) 
    mode the header in the file is automatically read. To read the data
    section the user must call the 'readData' method.
      
    When a sub-class of NAFile is called with the write ('w') mode
    then the file is opened but nothing is written. The user must then 
    send an 'na_dict' object to the 'write' method to write the output.
    The output file is then flushed to ensure the data is written even if 
    the user forgets to close it.
    """

    def __init__(self, filename, mode="r", na_dict={}): 
        """
        Initialization of class, decides if user wishes to read or write
        NASA Ames file.
        """
        napB.na_file.na_core.NACore.__init__(self)
        self.filename = filename
        self._open(mode)
        self.mode = mode
        self.na_dict = na_dict

        if self.mode == "r":
            self._normalized_X = True
            self.readHeader()
        elif self.mode == "w":
            # Self flag to check if data written
            self.data_written = False
        else:
            raise "Unknown file mode '%s'." % self.mode

        
    def _open(self, mode):
        "Wrapper to builtin open file function."
        self.file = open(self.filename, mode)
        self.is_open = True

         
    def close(self):
        "Wrapper to builtin close file function."
        self.file.close()
        self.is_open = False

    def _parseDictionary(self):
        """
        Parser for the optional na_dict argument containing a dictionary
        of NASA Ames internal variables. These are saved as instance attributes
        with the name used in the NASA Ames documentation.
        """
        for i in list(self.na_dict.keys()):
            setattr(self, i, self.na_dict[i])

    def _readTopLine(self):
        """
        Reads number of header lines and File Format Index from top line.
        Also assigns a value to NIV for the number of independent variables
        based on the first character in the FFI.

        Returns NLHEAD and FFI in a tuple.
        """
        firstline=self.file.readline();
        try: (self.NLHEAD, self.FFI) = napB.utils.text_parser.readItemsFromLine(firstline, 2, int)
        except ValueError: 
          secondline=self.file.readline();self.ndaccheader=firstline.strip()
          (self.NLHEAD, self.FFI) = napB.utils.text_parser.readItemsFromLine(secondline, 2, int);self.NLHEAD+=1
        self.NIV = int(self.FFI/1000)
        return (self.NLHEAD, self.FFI)
        
    def _readNDACCheader(self):
        """Reads the NDACC header"""
        if hasattr(self,'ndaccheader'):
          hf=[('investigator',20,str),('instrument',12,str),('station',12,str),('species',12,str),\
              ('starttime',20,datetime.datetime),('stoptime',20,datetime.datetime),('quality',4,int)]
          NH={};lasti=0
          for k,i,t in hf:
            NH[k]=self.ndaccheader[lasti:lasti+i];lasti+=i
            if t==datetime.datetime: 
              timeformats=['%d-%b-%Y %H:%M:%S','%d-%b-%Y %H:%M','%d-%b-%y %H:%M:%S','%d-%b-%y %H:%M','%d-%b-%y','%d-%^b-%y','%d-%b-%Y','%d-%b-%Y%H:%M:%S','%d %b %Y %H:%M:%S']
              for tfmt in timeformats:
                if ' %H:%M:%S'==tfmt[-9:]:
                  #fix bad formatted times
                  try: tmp_t=t.strptime(NH[k][:-9]+' 00:00:00',tfmt);h,m,s=list(map(int,NH[k][-9:].split(':')))
                  except ValueError as e: pass
                  else: 
                    NH[k]=(tmp_t+datetime.timedelta(hours=h,minutes=m,seconds=s)).strftime(tfmt)
                try: NH[k]=t.strptime(NH[k].strip(),tfmt)
                except ValueError as e: pass
                else: break
              if type(NH[k])!=t: 
                logger.error('Unable to read time format in %s for %s: %s'%(self.filename,k,NH[k]))
                if k=='starttime': raise e
                if k=='stoptime' and type(NH['starttime'])==t: NH[k]=NH['starttime']#try to fix this...
            else: 
              try: NH[k]=t(NH[k].strip())
              except Exception as e: 
                if k=='quality': NH[k]=np.nan
                else: logger.error('Unable to read NDACCheader: %s from %s:%s'%(k,NH[k],repr(e)));raise e
          return NH
        else: pass
          
    def _readLines(self, nlines):
        "Reads nlines lines from a file and returns them in a list."
        lines = []
        for i in range(nlines):
            lines.append(self.file.readline().strip())
        return lines

    def _checkForBlankLines(self, datalines):
        """
        Searches for empty lines in the middle of the data section and raises
        as error if found. It ignores empty lines at the end of the file but
        strips them out before returning a list of lines for reading.
        """
        empties = None
        count = 0
        rtlines = []
        for line in datalines:
            if line.strip() == "":
                empties = 1
            else:
                if empties == 1:   # If data line found after empty line then raise
                    if True: logger.warning('Empty line in the data section at line %s'%count);rtlines.append(line);empties=0
                    else: raise Exception("Empty line found in data section at line: " + repr(count))
                else:
                    rtlines.append(line)
            count = count + 1
        return rtlines


    def _readCommonHeader(self):
        """
        Reads the header section common to all NASA Ames files.
        """
        self._readTopLine()
        self.ONAME = napB.utils.text_parser.readItemFromLine(self.file.readline(), str)
        self.ORG = napB.utils.text_parser.readItemFromLine(self.file.readline(), str)
        self.SNAME = napB.utils.text_parser.readItemFromLine(self.file.readline(), str)
        self.MNAME = napB.utils.text_parser.readItemFromLine(self.file.readline(), str)
        (self.IVOL, self.NVOL) = napB.utils.text_parser.readItemsFromLine(self.file.readline(), 2, int)
        dates = napB.utils.text_parser.readItemsFromLine(self.file.readline(), 6, int)
        (self.DATE, self.RDATE) = (dates[:3], dates[3:])

    def _writeCommonHeader(self):
        """
        Writes the header section common to all NASA Ames files.
        """
        #Line 1 if often overwritten at _fixHeaderLength
        self.header.write(wrapLine("NLHEAD_FFI", self.annotation, self.delimiter, "%d%s%d\n" % (self.NLHEAD, self.delimiter, self.FFI)))
        self.header.write(getAnnotation("ONAME", self.annotation, delimiter = self.delimiter) + stripQuotes(self.ONAME) + "\n")
        self.header.write(getAnnotation("ORG", self.annotation, delimiter = self.delimiter) + stripQuotes(self.ORG) + "\n")
        self.header.write(getAnnotation("SNAME", self.annotation, delimiter = self.delimiter) + stripQuotes(self.SNAME) + "\n")
        self.header.write(getAnnotation("MNAME", self.annotation, delimiter = self.delimiter) + stripQuotes(self.MNAME) + "\n")
        self.header.write(wrapLine("IVOL_NVOL", self.annotation, self.delimiter, "%d%s%d\n" % (self.IVOL, self.delimiter, self.NVOL)))
        line = "%d %d %d%s%d %d %d\n" % (self.DATE[0], self.DATE[1], self.DATE[2], self.delimiter, self.RDATE[0], self.RDATE[1], self.RDATE[2])
        self.header.write(wrapLine("DATE_RDATE", self.annotation, self.delimiter, line))

    def _readVariablesHeaderSection(self):
        """
        Reads the variables section of the header.
        Assumes we are at the right point in the file.
        """
        self.NV = napB.utils.text_parser.readItemFromLine(self.file.readline(), int)
        self.VSCAL = napB.utils.text_parser.readItemsFromUnknownLines(self.file, self.NV, float)
        self.VMISS = napB.utils.text_parser.readItemsFromUnknownLines(self.file, self.NV, float)
        self.VNAME = napB.utils.text_parser.readItemsFromLines(self._readLines(self.NV), self.NV, str)

    def _writeVariablesHeaderSection(self):
        """
        Writes the variables section of the header.
        Assumes we are at the right point in the file.
        """
        self.header.write(wrapLine("NV", self.annotation, self.delimiter, "%d\n" % self.NV))
        self.header.write(wrapLine("VSCAL", self.annotation, self.delimiter, (("%s" + self.delimiter) * (self.NV - 1) + "%s\n") % tuple(self.VSCAL)))
        self.header.write(wrapLine("VMISS", self.annotation, self.delimiter, (("%s" + self.delimiter) * (self.NV - 1) + "%s\n") % tuple(self.VMISS)))
        self.header.write(wrapLines("VNAME", self.annotation, self.delimiter, "%s\n" * self.NV % tuple(self.VNAME)))

    def _readAuxVariablesHeaderSection(self):
        """
        Reads the auxiliary variables section of the header.
        Assumes we are at the right point in the file.
        """
        self.NAUXV = napB.utils.text_parser.readItemFromLine(self.file.readline(), int)
        if self.NAUXV > 0:        
            self.ASCAL = napB.utils.text_parser.readItemsFromUnknownLines(self.file, self.NAUXV, float)
            self.AMISS = napB.utils.text_parser.readItemsFromUnknownLines(self.file, self.NAUXV, float)
            self.ANAME = napB.utils.text_parser.readItemsFromLines(self._readLines(self.NAUXV), self.NAUXV, str)


    def _readCharAuxVariablesHeaderSection(self):
        """
        Reads the character-encoded auxiliary variables section of the header.
        Assumes we are at the right point in the file.
        """
        self.NAUXV = napB.utils.text_parser.readItemFromLine(self.file.readline(), int)
        self.NAUXC = napB.utils.text_parser.readItemFromLine(self.file.readline(), int)
        nonCharAuxVars = self.NAUXV - self.NAUXC
        if self.NAUXV > 0:
            self.ASCAL = napB.utils.text_parser.readItemsFromUnknownLines(self.file, nonCharAuxVars, float)
            self.AMISS = napB.utils.text_parser.readItemsFromUnknownLines(self.file, nonCharAuxVars, float)
            self.LENA = napB.utils.text_parser.readItemsFromUnknownLines(self.file, self.NAUXC, int)
            for i in range(nonCharAuxVars):
                self.LENA.insert(0, None)
            self.AMISS = self.AMISS + napB.utils.text_parser.readItemsFromUnknownLines(self.file, self.NAUXC, str)    
            self.ANAME = napB.utils.text_parser.readItemsFromLines(self._readLines(self.NAUXV), self.NAUXV, str)        
            
    def _readComments(self):
        """
        Reads the special and normal comments sections.
        Assumes we are at the right point in the file.
        """        
        self.NSCOML = napB.utils.text_parser.readItemFromLine(self.file.readline(), int)
        self._readSpecialComments()
        self.NNCOML = napB.utils.text_parser.readItemFromLine(self.file.readline(), int)
        self._readNormalComments()

    def _fixHeaderLength(self):
        """
        Takes the self.header StringIO object and counts the number of lines
        and corrects the NLHEAD value in the header line.
        Resets to start of self.header.
        """
        self.header.seek(0)
        lines = self.header.readlines()
        headlength = len(lines)
        lines[0] = wrapLine("NLHEAD_FFI", self.annotation, self.delimiter, "%d%s%d\n" % (headlength, self.delimiter, self.FFI))
        self.header = io.StringIO("".join(lines))
        self.header.seek(0) 

    def _readSpecialComments(self):
        """
        Reads the special comments section.        
        Assumes that we are at the right point in the file and that NSCOML
        variable is known.
        """
        self.SCOM = self._readLines(self.NSCOML)
        return self.SCOM

    def _readNormalComments(self):
        """
        Reads the normal comments section.        
        Assumes that we are at the right point in the file and that NNCOML
        variable is known.
        """
        self.NCOM = self._readLines(self.NNCOML)
        return self.NCOM

    def readData(self):
        """
        Reads the data section of the file. This method actually calls a number
        of FFI specific methods to setup the data arrays (lists of lists) and
        read the various data sections.

        This method can be called directly by the user.
        """
        self._setupArrays()
        datalines = open(self.filename).readlines()[self.NLHEAD:]
        datalines = self._checkForBlankLines(datalines)
        if len(datalines): logger.debug('First datalines=%s'%list(map(str.strip,datalines[:4])))
        # Set up loop over unbounded indpendent variable
        m = 0   # Unbounded independent variable mark        
        while len(datalines) > 0:
            datalines = self._readData1(datalines, m)
            datalines = self._readData2(datalines, m)
            m = m + 1
        
            
