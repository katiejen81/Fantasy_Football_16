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
#os.chdir("C:\Users\Katie\Documents\Fantasy_Football_16")

#This Path is for the Linux machine
os.chdir('/home/katie/Documents/Fantasy_Football_16')

#Start by importing the application
import nflgame
import nflgame.sched
import csv
import nflgame.statmap


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
#runfile('C:\Users\Katie\Anaconda2\Lib\site-packages\nflgame\update_players.py')


#This creates the players.json file, let's bring this into an object
#First we need to bring this into the working directory

import shutil
shutil.copyfile('/home/katie/anaconda2/lib/python2.7/site-packages/nflgame/players.json', '/home/katie/Documents/Fantasy_Football_16/players.json')

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
dictionary2 = nflgame.statmap.idmap
print dictionary2

with open('data dictionary.csv', 'wb') as csvwrite:
    dictwriter = csv.writer(csvwrite, delimiter=',')
    dictwriter.writerow(['Category', 'Description', 'fields'])
    for key in dictionary2:
        item = dictionary2[key]
        dictwriter.writerow([item['cat'], item['desc'], item['fields']])

#Now that we have a data dictionary, we can start to gather statistics
#To make a relational database, let's start with full lists of players
#This joins back to the Schedule Since 2013 file

schedule_games = nflgame.sched.games
print schedule_games


with open('Player_List.csv', 'wb') as csvwrite:
    gmewriter = csv.writer(csvwrite, delimiter = ',')
    gmewriter.writerow(['Gamekey', 'Home_team', 'Away_Team', 'Player_Short_Name', 'Player_Team', 'Home_Team'])
    for key in schedule_games:
        game = schedule_games[key]
        if game['year'] > 2012 and game['season_type'] == 'REG':
            id1 = game['gamekey']
            game1 = game['year']
            week1 = game['week']
            home1 = game['home']
            away1 = game['away']
            games = nflgame.games(game1, week1, home=home1, away=away1)
            players = nflgame.combine(games)            
            for p in players:
                gmewriter.writerow([
                    id1,
                    home1,
                    away1,
                    p.name,
                    p.team,
                    p.home
                    ])

#Next we are going to start with some specific stats - passing, rushing, defense, kicking, puntreturn, etc.
#Then the plan is to join this back to the roster files in order to get data

#Let's Start with Passing

with open('passing_data.csv', 'wb') as csvwriter:
    passwriter = csv.writer(csvwriter, delimiter=',')
    passwriter.writerow(['Gamekey', 'Home_team', 'Away_Team', 'Day_of_week', \
    'Month', 'Day', 'Year', 'Week', 'Player_Short_Name', 'Player_Team', \
    'Home_Team',  'passing_att', 'passing_incmp', 'passing_cmp', 'passing_tds',\
    'passing_int', 'passing_yds', 'passing_twoptm', 'passing_yds_FF_pts', \
    'passing_tds_FF_pts', 'passing_twopt_FF_pts', 'intercept_FF_pts', 'total_FF_pts'])
    for key in schedule_games:
        game = schedule_games[key]
        if game['year'] > 2012 and game['season_type'] == 'REG':
            id1 = game['gamekey']
            game1 = game['year']
            week1 = game['week']
            home1 = game['home']
            away1 = game['away']
            dow1 = game['wday']
            mnth1 = game['month']
            day1 = game['day']
            year1 = game['year']
            games = nflgame.games(game1, week1, home1, away1)
            players = nflgame.combine(games).passing()
            for p in players:
                #Calculating the Fantasy points using our current rules
                #Passing Values
                Pass_FF = round(p.passing_yds / 25)
                #TD Values
                TDS_FF = round(p.passing_tds * 4)
                #Two Point Conversion Values
                TWO_FF = round(p.passing_twoptm * 2)
                #Interception Values
                INT_FF = round(float(p.passing_ints * -1))
                #Total QB Points / game
                Total_FF = Pass_FF + TDS_FF + TWO_FF + INT_FF
                passwriter.writerow([id1,
                    home1,
                    away1,
                    dow1,
                    mnth1,
                    day1,
                    year1,
                    week1,
                    p.name,
                    p.team,
                    p.home,
                    p.passing_att,
                    p.passing_incmp,
                    p.passing_cmp,
                    p.passing_tds,
                    p.passing_ints,
                    p.passing_yds,
                    p.passing_twoptm,
                    Pass_FF,
                    TDS_FF,
                    TWO_FF,
                    INT_FF,
                    Total_FF
                    ])
                    
#Next let's do rushing stats. Shouldn't be as involved
                    
with open('rushing_data.csv', 'wb') as csvwriter:
    rushwriter = csv.writer(csvwriter, delimiter=',')
    rushwriter.writerow(['Gamekey', 'Home_team', 'Away_Team', 'Day_of_week', \
    'Month', 'Day', 'Year', 'Week', 'Player_Short_Name', 'Player_Team', \
    'Home_Team',  'rushing_yds', 'rushing_tds', 'rushing_twoptm', \
	'rushing_yds_FF_pts', 'rushing_tds_FF_pts', 'rushing_twoptm_FF_pts', \
	'total_FF_pts'])
    for key in schedule_games:
        game = schedule_games[key]
        if game['year'] > 2012 and game['season_type'] == 'REG':
            id1 = game['gamekey']
            game1 = game['year']
            week1 = game['week']
            home1 = game['home']
            away1 = game['away']
            dow1 = game['wday']
            mnth1 = game['month']
            day1 = game['day']
            year1 = game['year']
            games = nflgame.games(game1, week1, home1, away1)
            players = nflgame.combine(games).rushing()
            for p in players:
                #Calculating the Fantasy points using our current rules
                #Rushing Values
                Rush_FF = round(p.rushing_yds / 10)
                #TD Values
                TDS_FF = round(p.rushing_tds * 6)
                #Two Point Conversion Values
                TWO_FF = round(p.rushing_twoptm * 2)
                #Total Rush Points / game
                Total_FF = Rush_FF + TDS_FF + TWO_FF
                rushwriter.writerow([id1,
                    home1,
                    away1,
                    dow1,
                    mnth1,
                    day1,
                    year1,
                    week1,
                    p.name,
                    p.team,
                    p.home,
                    p.rushing_yds,
                    p.rushing_tds,
                    p.rushing_twoptm,
                    Rush_FF,
                    TDS_FF,
                    TWO_FF,
                    Total_FF
                    ])

#Receiving Points

with open('receiving_data.csv', 'wb') as csvwriter:
    recwriter = csv.writer(csvwriter, delimiter=',')
    recwriter.writerow(['Gamekey', 'Home_team', 'Away_Team', 'Day_of_week', \
    'Month', 'Day', 'Year', 'Week', 'Player_Short_Name', 'Player_Team', \
    'Home_Team', 'receiving_rec',  'receiving_yds', 'receiving_tds', 'receiving_twoptm', \
	'receiving_rec_FF_pts', 'receiving_yds_FF_pts', 'receiving_tds_FF_pts', \
 'receiving_twoptm_FF_pts', 'total_FF_pts'])
    for key in schedule_games:
        game = schedule_games[key]
        if game['year'] > 2012 and game['season_type'] == 'REG':
            id1 = game['gamekey']
            game1 = game['year']
            week1 = game['week']
            home1 = game['home']
            away1 = game['away']
            dow1 = game['wday']
            mnth1 = game['month']
            day1 = game['day']
            year1 = game['year']
            games = nflgame.games(game1, week1, home1, away1)
            players = nflgame.combine(games).receiving()
            for p in players:
                #Calculating the Fantasy points using our current rules
                #receiving Values
                Rec_FF = round(p.receiving_yds / 10)
                #Reception Values
                RECP_FF = round(p.receiving_rec * 1)
			#Reception touchdown Values
                TDS_FF = round(p.receiving_tds * 6)
                #Two Point Conversion Values
                TWO_FF = round(p.receiving_twoptm * 2)
                #Total Receiving Points / game
                Total_FF = Rec_FF + RECP_FF + TDS_FF + TWO_FF
                recwriter.writerow([id1,
                    home1,
                    away1,
                    dow1,
                    mnth1,
                    day1,
                    year1,
                    week1,
                    p.name,
                    p.team,
                    p.home,
				p.receiving_rec,
                    p.receiving_yds,
                    p.receiving_tds,
                    p.receiving_twoptm,
                    Rec_FF,
				RECP_FF,
                    TDS_FF,
                    TWO_FF,
                    Total_FF
                    ])      