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

#let's see now what this thing can do

#get the schedule for the season
schedule_games = nflgame.sched.games
print schedule_games

#write these to csv so that I can look at them
with open('Schedule since 2013.csv', 'wb') as csvfile:
    schedulewriter = csv.writer(csvfile, delimiter=',')
    schedulewriter.writerow(['Home', 'Away', 'Week', 'Year'])
    for key in schedule_games:
        game = schedule_games[key]
        if game['year'] > 2012 and game['season_type'] == 'REG':
            schedulewriter.writerow([game['home'], game['away'], game['week'], game['year']])
            
