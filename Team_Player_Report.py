# -*- coding: utf-8 -*-
"""
Benchmarking the Fantasy Players
Created on Sun Sep 18 20:28:35 2016
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

#Refresh the Access token. Run again when it expires
oauth = OAuth1(None, None, from_file='credentials.json')
oauth.refresh_access_token()

#Get our league information
from myql import MYQL
yql = MYQL(format='json', oauth=oauth)

import json

response = yql.select('fantasysports.leagues').where(['league_key', '=', 'nfl.l.425859'])
s = response.text
parse = json.loads(s)

#From here we will need the league key
x = parse['query']['results']['league']
league_key = x['league_key']

#Get our team information
url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/' + league_key + '/teams'
response = oauth.session.get(url, params={'format': 'json'})
s = response.text
parse = json.loads(s)

teams = parse['fantasy_content']['league'][1]['teams']

#Initialize the team_key variable
#I want the loop to stop when we find the right value
#So I am going to initialize the team_key variable to empty
#And tell the loop to stop when a value is put in the variable
team_key = None
key_list = teams.keys()
key_list.remove('count')
while team_key == None:
    for i in key_list:
        key = i
        name = teams[key]['team'][0][2]['name']
        if name == "Go Bulls!":
            team_key = teams[key]['team'][0][0]['team_key']
