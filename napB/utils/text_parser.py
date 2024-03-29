# -*- coding: utf-8 -*-
#   Copyright (C) 2004 CCLRC & NERC( Natural Environment Research Council ).
#   This software may be distributed under the terms of the
#   Q Public License, version 1.0 or later. http://ndg.nerc.ac.uk/public_docs/QPublic_license.txt

"""
textParser.py
=============

A set of functions to parse text file data into lists, strings,
reals, integers etc.

"""

# Standard library imports
import re
import string

# Local imports
from napB.utils.right_strip import *

import logging
#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Global variables
pattnNoQuotes = re.compile("^[\"'].*\1$")


def readItemFromLine(line, rttype=str):
    """
    Reads an item of type ``rttype`` from ``line``.
    """
    line = rightStripCurlyBraces(line)
    rtitem = pattnNoQuotes.sub("", line.strip())

    if rttype is not str:
        rtitem = rttype(rtitem.split()[0])   
    return rtitem

def readItemsFromLine(line, nitems=None, rttype=str):
    """
    Reads ``nitems`` items of type ``rttype`` from ``line``.
    """
    line = rightStripCurlyBraces(line)
    rtitems = re.split(r"\s+", line.strip())
    if nitems and len(rtitems) <nitems:
        raise ValueError("Incorrect number of items (%s) found in line: \n'%s'" % (nitems, line))
    else: rtitems=rtitems[:nitems]
    if rttype is not str:
        rtitems = [rttype(x) for x in rtitems]
    return rtitems

def readItemsFromLines(lines, nitems, rttype=str):
    """
    Reads ``nitems`` items of type ``rttype`` from ``lines``
    """
    lines = [rightStripCurlyBraces(line) for line in lines]
    rtitems = []
    for line in lines:
        rtitems = rtitems + [readItemFromLine(line, rttype)]
    if rttype is not str:
        rtitems = [rttype(x) for x in rtitems]
    return rtitems

def readItemsFromUnknownLines(object, nitems, rttype=str):
    """
    Reads from an unknown number of lines until n items have been collected.
    The 'object' argument can be a filehandle (i.e. obj=open('name.ext', 'r'))
    or a string wrapped in a StringIO object (i.e. obj=StringIO.StringIO('abc')).
    The 'object' argument can also be a list, in which case the partially used/read object is
    also returned.
    """

    rtitems = []
    lines = []        

    if type(object) == type([2,3]): 
        while len(rtitems) < nitems:   
            try: nextitem = object[0]
            except IndexError: logger.error('Could not find %d items: found %s'%(nitems,rtitems)); raise ValueError('Not enough items on dataline %s'%lines)
            object = object[1:]
            items = rightStripCurlyBraces(nextitem).strip().split()
            lines.append(items)
            (rtitems, extras) = (rtitems + items[:nitems], items[nitems:])

    else:
        while len(rtitems) < nitems:
            items = rightStripCurlyBraces(object.readline()).strip().split()
            lines.append(items)
            (rtitems, extras) = (rtitems + items[:nitems], items[nitems:])

    #if len(extras) > 0:
        #raise Exception("Could not split " + `len(lines)` + " lines exactly into required number (" + `nitems` + ") of items: \n" + str(lines))
    #testlogger.info('rttype=%s,rtitems=%s,extras=%s'%(rttype,rtitems,extras))
    if rttype is not str:
        
        for i,x in enumerate(rtitems):
          try: rtitems[i]=rttype(x)
          except ValueError: logger.debug('Could not interprete %s as %s, using "nan"'%(x,rttype));rtitems[i]=rttype('nan') 
        #rtitems = [rttype(x) for x in rtitems]

    if type(object) == type([1,2]):
        return (rtitems, object)
    else:
        return rtitems
