#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
NFL Player Import using Python
Created on Sun Aug 27 21:42:35 2017
Written in Python2
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

#Refresh the Access token. Run again when it expires
oauth = OAuth1(None, None, from_file='credentials.json')
oauth.refresh_access_token()

#Get our league information
from myql import MYQL
yql = MYQL(format='json', oauth=oauth)

import json

response = yql.select('fantasysports.leagues').where(['league_key', '=', 'nfl.l.648761'])
s = response.text
parse = json.loads(s)

#From here we will need the league key
x = parse['query']['results']['league']
league_key = x['league_key']

#Get available players
n = 1
url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/' + league_key + '/players;status=A;sort=PTS;start=' + str(n)
response = oauth.session.get(url, params={'format': 'json'})
s = response.text
parse = json.loads(s)
