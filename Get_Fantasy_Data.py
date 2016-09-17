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

#Get a list of the top 100 undrafted players by Fantasy Points


for n in [1, 25, 50, 75]:
    url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/' + league_key + '/players;status=A;sort=PTS;start=' + str(n) + '/stats'
    response = oauth.session.get(url, params={'format': 'json'})
    s = response.text
    parse = json.loads(s)

    Available_Players = parse['fantasy_content']['league'][1]['players']

    key_list = Available_Players.keys()
    key_list.remove('count')
    key_list.sort(key=int)
    for i in key_list:
        j = str(i)
        player_key = Available_Players[j]['player'][0][0]['player_key']
        player_name = Available_Players[j]['player'][0][2]['name']['full']
        player_status = Available_Players[j]['player'][0][3].get('status', None)
        #player position
        player_position_a = Available_Players[j]['player'][0][9].get('display_position', None)
        player_position_b = Available_Players[j]['player'][0][10].get('display_position', None)
        player_position = player_position_a or player_position_b
        #player team
        player_team_a = Available_Players[j]['player'][0][5].get('editorial_team_abbr', None)      
        player_team_b = Available_Players[j]['player'][0][6].get('editorial_team_abbr', None)
        player_team_c = Available_Players[j]['player'][0][7].get('editorial_team_abbr', None)
        player_team = player_team_a or player_team_b or player_team_c
        #bye week - this one is weird
        if 'bye_weeks' in Available_Players[j]['player'][0][7]:
            player_bye = Available_Players[j]['player'][0][7]['bye_weeks']['week']
        elif 'bye_weeks' in Available_Players[j]['player'][0][8]:
            player_bye = 'bye_weeks' in Available_Players[j]['player'][0][8]['bye_weeks']['week']
        else:
            player_bye = None
        #Total points this season so far
        player_points = Available_Players[j]['player'][1]['player_points']['total']
        print player_key, player_name, player_position, player_status, player_team, player_bye, player_points
    
