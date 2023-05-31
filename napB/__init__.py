# -*- coding: utf-8 -*-
from .nappy_api import *
import os

with open(os.path.join(os.path.dirname(__file__),'AMES_NDACC_abbrev.txt'),'r') as fid:
  AN={}
  fid.readline()
  #header instrument, filename abbreviation (last character), species, filename characters 2,3
  for l in fid:
    line=[ll.strip() for ll in l.split('\t')]
    if len(line[0]): header=line[0];AN.setdefault(line[0],{}).update(dict(list(zip(['abbr','species'],[line[1],{line[2]:line[3]}]))))
    else: AN[header]['species'][line[2]]=line[3]
  AN['UVVIS']=AN['UV/VIS']
  AN['UV_SPECT']=AN['UV/SPECT']
  AN['MWR']=AN['MWAVE']
  AN['WVSONDE']=AN['O3SONDE']
