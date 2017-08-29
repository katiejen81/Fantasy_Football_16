# -*- coding: utf-8 -*-
"""
Rethinking the API grab - Getting more from the nfl.com API
Created on Thu Aug 11 20:35:59 2016

@author: Katie
"""
#Change working directories and location of packages

import sys
sys.path.insert(0, '/home/katie/anaconda2/lib/python2.7/site-packages/')
print '\n'.join(sys.path)

#find the working directory and change if needed
import os
os.getcwd()

#I want to change the working directory - this is for Windows Machine
#os.chdir("C:\Users\Katie\Documents\Fantasy_Football_16")

#Linux Laptop
os.chdir("/home/katie/Documents/Fantasy_Football_16")

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
header_row = f + g + stats_list

#write the header row - this is only done once
with open('full_data.csv', 'wb') as csvwriter:
    datawriter = csv.writer(csvwriter, delimiter=',')
    datawriter.writerow(header_row)

#Now let's get the game stat data

#Get 2013 data
for l in range (1, 18):
    url = "http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=2013&week=" + str(l) + "&format=json"
    r = requests.get(url)
    d = json.loads(r.text)
    for key in d:
        f1 = ([d['season'], d['week']])
        players = d['players']
        for i in players:
            f2 = [i['esbid'], i['gsisPlayerId'], i['id'], i['name'], i['position'], i['teamAbbr']]
            game_stats = i['stats']
            f3 = []
            for j in range(1,94):
                k = str(j)
                z = game_stats.get(k, '')
                f3.append(z)
            f4 = f1 + f2 + f3
            with open('full_data.csv', 'a') as csvwriter:
                datawriter = csv.writer(csvwriter, delimiter=',')
                datawriter.writerow(f4)

#Get the 2014 Data
for l in range (1, 18):
    url = "http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=2014&week=" + str(l) + "&format=json"
    r = requests.get(url)
    d = json.loads(r.text)
    for key in d:
        f1 = ([d['season'], d['week']])
        players = d['players']
        for i in players:
            f2 = [i['esbid'], i['gsisPlayerId'], i['id'], i['name'], i['position'], i['teamAbbr']]
            game_stats = i['stats']
            f3 = []
            for j in range(1,94):
                k = str(j)
                z = game_stats.get(k, '')
                f3.append(z)
            f4 = f1 + f2 + f3
            with open('full_data.csv', 'a') as csvwriter:
                datawriter = csv.writer(csvwriter, delimiter=',')
                datawriter.writerow(f4)  
                
#Get the 2015 Data
for l in range (1, 18):
    url = "http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=2015&week=" + str(l) + "&format=json"
    r = requests.get(url)
    d = json.loads(r.text)
    for key in d:
        f1 = ([d['season'], d['week']])
        players = d['players']
        for i in players:
            f2 = [i['esbid'], i['gsisPlayerId'], i['id'], i['name'], i['position'], i['teamAbbr']]
            game_stats = i['stats']
            f3 = []
            for j in range(1,94):
                k = str(j)
                z = game_stats.get(k, '')
                f3.append(z)
            f4 = f1 + f2 + f3
            with open('full_data.csv', 'a') as csvwriter:
                datawriter = csv.writer(csvwriter, delimiter=',')
                datawriter.writerow(f4) 
                
#Get the 2016 Data
for l in range (1, 18):
    url = "http://api.fantasy.nfl.com/v1/players/stats?statType=weekStats&season=2016&week=" + str(l) + "&format=json"
    r = requests.get(url)
    d = json.loads(r.text)
    for key in d:
        f1 = ([d['season'], d['week']])
        players = d['players']
        for i in players:
            f2 = [i['esbid'], i['gsisPlayerId'], i['id'], i['name'], i['position'], i['teamAbbr']]
            game_stats = i['stats']
            f3 = []
            for j in range(1,94):
                k = str(j)
                z = game_stats.get(k, '')
                f3.append(z)
            f4 = f1 + f2 + f3
            with open('full_data.csv', 'a') as csvwriter:
                datawriter = csv.writer(csvwriter, delimiter=',')
                datawriter.writerow(f4) 
                
#There are some weird blank spaces in the csv file. Let's get rid of them
infile = open('full_data.csv', 'rb')
outfile = open('full_stats.csv', 'wb')
datawriter = csv.writer(outfile)
for row in csv.reader(infile):
    if row:
        datawriter.writerow(row)
infile.close()
outfile.close()