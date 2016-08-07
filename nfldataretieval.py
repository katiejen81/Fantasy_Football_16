#NFL Game Data Import Using Python
#KTanner 8-6-16
#Downloaded using PIP but downloaded to Anaconda3 location
#This is only compatible with Python 2.7, so we need to move it over

#The below was only needed because on the linux machine things were installed 
#in the non default directory. Windows doesn't have this problem

import sys
sys.path.insert(0, '/home/katie/anaconda2/lib/python2.7/site-packages/')
print '\n'.join(sys.path)

#find the working directory and change if needed
import os
os.getcwd()

#I want to change the working directory - this is for Windows Machine
os.chdir("C:\Users\Katie\Documents\Fantasy_Football_16")

#This Path is for the Linux machine
#os.chdir('/home/katie/Fantasy Football Programs and Files/')

#Start by importing the application
import nflgame
import nflgame.sched
import csv


#get the schedule for the last three seasons. We want to train on the last three seasons
schedule_games = nflgame.sched.games
print schedule_games

#write these to csv so that I can look at them
with open('Schedule since 2013.csv', 'wb') as csvfile:
    schedulewriter = csv.writer(csvfile, delimiter=',')
    schedulewriter.writerow(['Game_Key', 'Home', 'Away', 'Day_of_Week', 'Month', 'Day', 'Year', 'Week'])
    for key in schedule_games:
        game = schedule_games[key]
        if game['year'] > 2012 and game['season_type'] == 'REG':
            schedulewriter.writerow([game['gamekey'], game['home'], game['away'], game['wday'], game['month'], game['day'], game['year'], game['week']])
            
#Now let's get some player information
#The cookbook Code doesn't appear to be working. Let's MacGyver this
#There is a JSON file in the package directory. Let's see if we can update it
#Run the Update_Players file

#runfile('C:/Users/Katie/Anaconda2/Lib/site-packages/nflgame/update_players.py', wdir='C:\Users\Katie\Documents\Fantasy_Football_16')
runfile('/home/katie/anaconda2/lib/python2.7/site-packages/nflgame/update_players.py')



#This creates the players.json file, let's bring this into an object
#First we need to bring this into the working directory

import shutil
shutil.copyfile('/home/katie/anaconda2/lib/python2.7/site-packages/nflgame/players.json', '/home/katie/Fantasy Football Programs and Files/players.json')

import json
with open('players.json') as json_data:
    players = json.load(json_data)
    print players

#Creating the csv file
#this was a really interesting point - If the key value in the dictionary is missing, python throws an error
#We need to tell python what to do if a key is missing. The dictionary.get() function does that
#This way, if a value is missing, I can tell python to leave it blank, and then there are no errors and I define
#missing values

import csv
with open('All Players.csv', 'wb') as csvfile2:
    playerwriter = csv.writer(csvfile2, delimiter=',')
    playerwriter.writerow(['NFLID', 'Short_Name', 'Full_Name', 'Date_of_Birth', 'Height', 'Weight', 'College', 'Years_Pro', 'Jersey_Number'])
    for key in players:
        player = players[key]
        playerwriter.writerow([
            player.get('gsis_id', ''),
            player.get('gsis_name', ''),
            player.get('full_name', ''),
            player.get('birthdate', ''),
            player.get('height', ''),
            player.get('weight', ''),
            player.get('college', ''),
            player.get('years_pro', ''),
            player.get('number', '')
            ])
            
#Let's now see what kinds of game statistics are available to us
dictionary2 = nflgame.statmap.idmap()
print dictionary2

with open('data dictionary.csv', 'wb') as csvwrite:
    dictwriter = csv.writer(csvwrite, delimiter=',')
    dictwriter.writerow(['Category', 'Description', 'fields'])
    for key in dictionary2:
        item = dictionary2[key]
        dictwriter.writerow([item['cat'], item['desc'], item['fields']])

#Now that we have a data dictionary, we can start to gather statistics
    
nflgame.combine(nflgame.games(2013)).csv('season2013.csv')

nflgame.combine()

games = nflgame.games(2013, week=1, home='DEN', away='BAL')
players = nflgame.combine_game_stats(games)
for p in players.rushing():
    print p, p.rushing_att, p.rushing_yards, p.rushing_tds

