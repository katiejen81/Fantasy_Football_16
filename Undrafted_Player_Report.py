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

#Desktop Linux Computer
import sys
sys.path.insert(0, '/home/katie/anaconda2/lib/python2.7/site-packages/')
print '\n'.join(sys.path)

import os
os.getcwd()
os.chdir('/media/katie/d97cda70-8ba6-4a37-9d37-edeaed2ee339/Katie/Fantasy Football Programs and Files/')

#Begin to access the OAUTH library
from yahoo_oauth import OAuth1

#read in the consumer secret and key
oauth = OAuth1(None, None, from_file='credentials.json')

#Code in case it is needed - d7nf6n
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

#Get a list of the top 100 undrafted players by Fantasy Points
import csv
with open('undrafted_players.csv', 'wb') as csvwriter:
    datawriter = csv.writer(csvwriter, delimiter = ',')
    datawriter.writerow(['player_id', 'player_name', 'player_status', 
                         'player_position', 'player_team', 'player_bye', 
                         'player_season_total_points'])

    player_list = []

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
            #add player to a list
            player_list.append(player_key)
            datawriter.writerow([player_key, player_name, player_status, player_position, 
                                 player_team, player_bye, player_points])
    
#Now let's get a week by week breakdown
current_week = parse['fantasy_content']['league'][0]['current_week']

player_stats = {}  
for player in player_list:
    key = 'player_' + player
    player_stats[key] = {}
    for i in range (1, current_week+1):  
        week = 'week_' + str(i)
        wk = str(i)
        url = 'http://fantasysports.yahooapis.com/fantasy/v2/league/' + league_key + '/players;player_keys=' + player +  '/stats;type=week;week=' + wk 
        response = oauth.session.get(url, params={'format': 'json'})
        s = response.text
        parse = json.loads(s)
        value = parse['fantasy_content']['league'][1]['players']['0']['player']
        player_stats[key][week] = value

variables = ['week_' + str(w) for w in range(1, current_week+1)]

import csv
with open('undrafted_player_week.csv', 'wb') as csvwriter:
    datawriter = csv.writer(csvwriter, delimiter = ',')
    datawriter.writerow(['player_id', 'player_name', 
                         'player_position', 'player_team', 
                         'player_bye'] + variables)
    for i in player_stats:
        player_id = player_stats[i]['week_1'][0][0]['player_key']
        player_name = player_stats[i]['week_1'][0][2]['name']['full']
        player_position_a = player_stats[i]['week_' + str(current_week)][0][9].get('display_position', None)
        player_position_b = player_stats[i]['week_' + str(current_week)][0][10].get('display_position', None)
        player_position = player_position_a or player_position_b
         #player team
        player_team_a = player_stats[i]['week_1'][0][6].get('editorial_team_abbr', None)
        player_team_b = player_stats[i]['week_1'][0][7].get('editorial_team_abbr', None)
        player_team = player_team_a or player_team_b
        #player bye
        if 'bye_weeks' in player_stats[i]['week_1'][0][7]:
            player_bye = player_stats[i]['week_1'][0][7]['bye_weeks']['week']
        elif 'bye_weeks' in player_stats[i]['week_1'][0][8]:
            player_bye = player_stats[i]['week_1'][0][8]['bye_weeks']['week']
        else:
            player_bye = None
        list1 = [player_id, player_name, player_position, player_team, player_bye]
        #Week Stats
        for j in variables:
            list1.append(player_stats[i][j][1]['player_points']['total'])
        datawriter.writerow(list1)

