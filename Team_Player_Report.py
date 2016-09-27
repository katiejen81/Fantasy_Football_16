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
            
#Now that we have a team key, let's get our players
#We can also get weekly stats
#Let's Start by getting our week information so that we can
#loop that way
current_week = parse['fantasy_content']['league'][0]['current_week']

url = 'http://fantasysports.yahooapis.com/fantasy/v2/team/' + team_key + '/roster'
response = oauth.session.get(url, params={'format': 'json'})
s = response.text
parse = json.loads(s)
players = parse['fantasy_content']['team'][1]['roster']['0']['players']
key_list = players.keys()
key_list.remove('count')
key_list.sort(key=int)
player_list = []
for i in key_list:
    key = i
    player_key = players[key]['player'][0][0]['player_key']
    #Make a list of player ids so that we can line these up
    #Week after week. Despite changes
    player_list.append(player_key)

#Now that we have a list of players from our most recent roster,
#let's loop through them and get all of their weekly fantasy stats
#The below code creates a player centric dictionary for each player, by week
player_stats = {}  
iteration = 0  
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

#---Below this line, we need to add code to get in to the player/week dictionaries
#and create a csv file that has a weekly trend for each of these---
variables = ['week_' + str(w) for w in range(1, current_week+1)]

import csv
with open('team_roster_week.csv', 'wb') as csvwriter:
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

