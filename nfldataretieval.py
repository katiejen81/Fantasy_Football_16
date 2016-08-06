#NFL Game Data Import Using Python
#KTanner 8-6-16
#Downloaded using PIP but downloaded to Anaconda3 location
#This is only compatible with Python 2.7, so we need to move it over

#The below was only needed because on the linux machine things were installed 
#in the non default directory. Windows doesn't have this problem

import sys
#sys.path.insert(0, '/home/katie/anaconda2/lib/python2.7/site-packages/')
print '\n'.join(sys.path)

#Start by importing the application
import nflgame
import nflgame.sched
import csv

#let's see now what this thing can do

#get the schedule for the season
schedule_games = nflgame.sched.games

#write these to csv so that I can look at them
with open