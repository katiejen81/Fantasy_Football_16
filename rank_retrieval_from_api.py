# -*- coding: utf-8 -*-
"""
Pulling in editor draft ranks from nfl.com api
Created on Sun Sep 04 08:59:10 2016

@author: Katie
"""

#Change working directories and location of packages

#import sys
#sys.path.insert(0, '/home/katie/anaconda2/lib/python2.7/site-packages/')
#print '\n'.join(sys.path)

#find the working directory and change if needed
import os
os.getcwd()

#I want to change the working directory - this is for Windows Machine
os.chdir("C:\Users\Katie\Documents\Fantasy_Football_16")

#Importing needed packages

import requests
import csv
import json

#Now let's get the rankings
url = "http://api.fantasy.nfl.com/v1/players/editordraftranks?format=json&count=100"
ranks = requests.get(url)

#Status of the API call
ranks.json

#Bring the results into a dictionary
ranks_d = json.loads(ranks.text)

#get to the information
r = ranks_d['players']

#Set up to get the headers to print
#Get a single value to grab keys
h = r[0] #List r at index 0 (first rank)
headers = list(h.keys())

#Write this information to csv
with open('draft_ranks.csv', 'wb') as csvwriter:
    datawriter = csv.writer(csvwriter, delimiter=',')
    datawriter.writerow(headers)
    for key in r:
        datawriter.writerow([key['esbid']
            , key['firstName']
            , key['auction']
            , key['lastName']
            , key['gsisPlayerId']
            , key['rank']
            , key['teamAbbr']
            , key['position']
            , key['id']
            , key['stock']])

#Let's get the next 100
url = "http://api.fantasy.nfl.com/v1/players/editordraftranks?format=json&count=100&offset=100"
ranks = requests.get(url)
ranks.json
ranks_d = json.loads(ranks.text)
r = ranks_d['players']

#Write this information to csv
with open('draft_ranks.csv', 'a') as csvwriter:
    datawriter = csv.writer(csvwriter, delimiter=',')
    for key in r:
        datawriter.writerow([key['esbid']
            , key['firstName']
            , key['auction']
            , key['lastName']
            , key['gsisPlayerId']
            , key['rank']
            , key['teamAbbr']
            , key['position']
            , key['id']
            , key['stock']])
            
#Get the final 100
url = "http://api.fantasy.nfl.com/v1/players/editordraftranks?format=json&count=100&offset=200"
ranks = requests.get(url)
ranks.json
ranks_d = json.loads(ranks.text)
r = ranks_d['players']

#Write this information to csv
with open('draft_ranks.csv', 'a') as csvwriter:
    datawriter = csv.writer(csvwriter, delimiter=',')
    for key in r:
        datawriter.writerow([key['esbid']
            , key['firstName']
            , key['auction']
            , key['lastName']
            , key['gsisPlayerId']
            , key['rank']
            , key['teamAbbr']
            , key['position']
            , key['id']
            , key['stock']])
            
#Clean up those funky blank rows that happen when appending
infile = open('draft_ranks.csv', 'rb')
outfile = open('draft_ranks2.csv', 'wb')
datawriter = csv.writer(outfile)
for row in csv.reader(infile):
    if row:
        datawriter.writerow(row)
infile.close()
outfile.close()

#Clean up our unwanted files
os.remove('draft_ranks.csv')
os.rename('draft_ranks2.csv', 'draft_ranks.csv')