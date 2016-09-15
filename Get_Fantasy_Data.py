# -*- coding: utf-8 -*-
"""
Access Fantasy Site
Created on Wed Sep 14 20:10:24 2016
Written in Python 2
@author: katie
"""

#Change working directories and location of packages
#Laptop Linux Computer
import sys
sys.path.insert(0, '/home/katie/.local/lib/python2.7/site-packages')
print '\n'.join(sys.path)

import os
os.getcwd()
os.chdir("/home/katie/Documents/Fantasy_Football_16")

#Begin to access the OAUTH library
from yahoo_oauth import OAuth1

#read in the consumer secret and key
oauth = OAuth1(None, None, from_file='credentials.json')

#Code in case it is needed - srbtce
from myql import MYQL
yql = MYQL(format='json', oauth=oauth)

#First Query - this was less painful
import json

response = yql.select('fantasysports.leagues').where(['league_key', '=', 'nfl.l.425859'])
s = response.text
parse = json.loads(s)
