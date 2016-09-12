# -*- coding: utf-8 -*-
"""
Fantasy League get information
Created on Sun Sep 11 18:27:45 2016
Written in Python 2
@author: katie
"""

#First things first. Let's set up our authentication dictionary

#we have to encode the oauth_signature and the token_secret to double encode RFC3986
          
params = {"oauth_nonce": oauth.generate_nonce(30), "oauth_consumer_key":oauth_consumer_key, 
          "oauth_timestamp": oauth.generate_timestamp(), "oauth_signature_method":"HMAC-SHA1", 
          "oauth_signature": oauth_signature + token_secret, "oauth_version": "1.0", 
          "oauth_token":token}
          
sorted(params)

# team ID 5
import requests
import oauth2

#Let's first test to see if this call will get us the league
League = "nfl.l.425859"

url = "http://fantasysports.yahooapis.com/fantasy/v2/league/" + League

r = requests.get(url, params)
s = r.text

requests.get()
