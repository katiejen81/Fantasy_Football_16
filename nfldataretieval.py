#NFL Game Data Import Using Python
#KTanner 8-6-16
#Downloaded using PIP but downloaded to Anaconda3 location
#This is only compatible with Python 2.7, so we need to move it over

#The below was only needed because on the linux machine things were installed 
#in the non default directory. Windows doesn't have this problem

#import sys
#sys.path.insert(0, '/home/katie/anaconda2/lib/python2.7/site-packages/')
#print '\n'.join(sys.path)

#find the working directory and change if needed
import os
os.getcwd()

#I want to change the working directory - this is for Windows Machine
os.chdir("C:\Users\Katie\Documents\Fantasy_Football_16")

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
    schedulewriter.writerow(['Home', 'Away', 'Day of Week', 'Month', 'Day', 'Year', 'Week'])
    for key in schedule_games:
        game = schedule_games[key]
        if game['year'] > 2012 and game['season_type'] == 'REG':
            schedulewriter.writerow([game['home'], game['away'], game['wday'], game['month'], game['day'], game['year'], game['week']])
            
#Now let's get some player information
#The cookbook Code doesn't appear to be working. Let's MacGyver this
#There is a JSON file in the package directory. Let's see if we can update it
#Run the Update_Players file

runfile('C:/Users/Katie/Anaconda2/Lib/site-packages/nflgame/update_players.py', wdir='C:\Users\Katie\Documents\Fantasy_Football_16')

#This creates the players.json file, let's bring this into an object
#First we need to bring this into the working directory
#getting errors when I try to do this programmatically. Will just copy and paste for now

import json
with open('players.json') as json_data:
    players = json.load(json_data)
    print players

#Creating the csv file
import csv
with open('All Players.csv', 'wb') as csvfile:
    playerwriter = csv.writer(csvfile, delimiter=',')
    playerwriter.writerow(['NFLID', 'Short_Name', 'Full_Name', 'Date_of_Birth', 'Height', 'Weight', 'College', 'Years_Pro', 'Jersey_Number'])
    for p in players:
        players.writerow([p, players['gsis_id']])

            

            
