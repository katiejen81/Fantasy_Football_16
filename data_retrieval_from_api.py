# -*- coding: utf-8 -*-
"""
Rethinking the API grab - Getting more from the nfl.com API
Created on Thu Aug 11 20:35:59 2016

@author: Katie
"""

#Importing needed packages

import requests
import nflgame
import nflgame.sched
import csv
import json

#Now Let's Get Statistics Names

url = "http://api.fantasy.nfl.com/v1/game/stats?format=json"
stats = requests.get(url)
#get the status of the request Status of 200 = OK
stats.json
#and bring the results into a dictionary
stats_d = json.loads(stats.text)

#Now make a list of these names so that we can add them to the file
s = stats_d['stats']
stats_list = [];
for i in s:
    obj = i['shortName']
    obj = obj.replace(" ", "_")
    stats_list.append(obj)
   
#Get the game schedule from nflgame
schedule_games = nflgame.sched.games

#Get a list of what is in this information
game_info = schedule_games['2014091413']
game_list = game_info.keys()

#Run once to get the header row of the csv file

f = ['season', 'week']
g = ['esbid', 'gsisPlayerID', 'id', 'name', 'position', 'team_abbr']

#bring together the header row

#Now let's get the game stat data
d2013 = dict()
#et 2013 data
for j in range (1, 18):
    url = "http://api.fantasy.nfl.com/v1/players/stats?statType=seasonStats&season=2013&week=" + str(j) + "&format=json"
    r = requests.get(url)
    d[j] = json.loads(r.text)
    d4 = {"week": j }
    d2013 = dict(d2013, **d2); d2013.update(d4)
        