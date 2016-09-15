# -*- coding: utf-8 -*-
"""
Access Fantasy Site - Abridged Version
Created on Wed Sep 14 20:10:24 2016
Written in Python 2
@author: katie
Must run this in pieces so that the information can be
input
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
#Getting League information
import json

response = yql.select('fantasysports.leagues').where(['league_key', '=', 'nfl.l.425859'])
s = response.text
parse = json.loads(s)

#From here we will need the league key
x = parse['query']['results']['league']
league_key = x['league_key']

#Run this when the access token expires
oauth.refresh_access_token()
oauth = OAuth1(None, None, from_file='credentials.json')


#Now let's get a list of players within our league
#This can't be a YQL query. Sad.

url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/' + league_key + '/players;status=A;sort=PTS'
response = oauth.session.get(url, params={'format': 'json'})
s = response.text
parse = json.loads(s)

Available_Players = parse['fantasy_content']['league'][1]['players']

#need to add code here to get the next available players
#could potentially put this in a while look to get 100 players
