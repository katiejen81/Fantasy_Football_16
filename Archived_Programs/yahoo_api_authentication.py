# -*- coding: utf-8 -*-
"""
Fantasy League OAuth Flow Program
Created on Fri Sep 09 20:10:54 2016
Written in Python 2
@author: Katie
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
sys.path.insert(0, '/home/katie/anaconda2/lib/python2.7/site-packages')
print '\n'.join(sys.path)

import os
os.getcwd()
os.chdir("/home/katie/Fantasy Football Programs and Files/")


#Import the packages needed for the OAuth Authorization flow

import oauth2 as oauth
import requests
import webbrowser

import json
keys = json.loads(open('API Keys.json').read())

#Get a request token

oauth_consumer_key = keys['Key']
oauth_signature = keys['Secret'] + '&'

url = "https://api.login.yahoo.com/oauth/v2/get_request_token?"

params = {"oauth_nonce": oauth.generate_nonce(30), "oauth_timestamp": oauth.generate_timestamp(), 
          "oauth_consumer_key": oauth_consumer_key, "oauth_signature_method": "plaintext",
          "oauth_signature": oauth_signature, "oauth_version": "1.0", "xoauth_lang_pref":'"en-us"', 
          "oauth_callback": "oob"}

r = requests.get(url, params)
s = r.text

#Obtain the request token from the response

p = s.split("&")
#request token
p2 = p[0].split("=")[1]
#Token secret
p4 = p[1].split("=")[1]

#Now ask for authorization

url = "https://api.login.yahoo.com/oauth/v2/request_auth?" + p2

#And now we have to pop open a web browser to grant permission for the API to work

webbrowser.open(url)

#Let's assign the code to a variable

code = "s9axza"

#Now we have to exchange all of this information for an Access Token
#Define the request URL
url = "https://api.login.yahoo.com/oauth/v2/get_token"

#Create a dictionary as above to pass through our parameters
params = {"oauth_consumer_key":oauth_consumer_key, "oauth_signature_method":"plaintext", 
          "oauth_nonce": oauth.generate_nonce(30), "oauth_signature": oauth_signature + p4, 
          "oauth_timestamp": oauth.generate_timestamp(), "oauth_verifier":code, 
          "oauth_version": "1.0", "oauth_token":p2}

#Call the API to get the token
r1 = requests.get(url, params)
s1 = r1.text

#Parse the response to get the access token that can be used
#To make the requests

t = s1.split("&")
token = t[0].split("=")[1]
token_secret = t[1].split("=")[1]

#The access token is only good for an hour. Run the below code
#To refresh the token, run the below code

#Get the access handle. This is a more persistent access credential

handle = t[3].split("=")[1]

params = {"oauth_nonce": oauth.generate_nonce(30), "oauth_consumer_key":oauth_consumer_key, 
          "oauth_timestamp": oauth.generate_timestamp(), "oauth_signature_method":"plaintext", 
          "oauth_signature": oauth_signature + token_secret, "oauth_version": "1.0", 
          "oauth_token":token, "oauth_session_handle":handle}

#Call the API to get the new Access token

r1 = requests.get(url, params)
s1 = r1.text

#Finally parse the new token into the variable

t = s1.split("&")
token = t[0].split("=")[1]
token_secret = t[1].split("=")[1]