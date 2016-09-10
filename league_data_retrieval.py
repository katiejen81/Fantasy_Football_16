# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 20:10:54 2016

@author: Katie
"""
import oauth2 as oauth
import requests
import webbrowser

#Get a request token

oauth_consumer_key = "dj0yJmk9YndwUlpoMnN2Unh6JmQ9WVdrOU1FZEZXWGQzTkdNbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0yMw--"
oauth_signature = "e30bb3c974eb4763941af13013481bde0795b374&"

url = "https://api.login.yahoo.com/oauth/v2/get_request_token?"

params = {"oauth_nonce": oauth.generate_nonce(30), "oauth_timestamp": oauth.generate_timestamp(), "oauth_consumer_key": oauth_consumer_key, "oauth_signature_method": "plaintext",
    "oauth_signature": oauth_signature, "oauth_version": "1.0", "xoauth_lang_pref":'"en-us"', "oauth_callback": "oob"}

r = requests.get(url, params)
s = r.text

#Obtain the request token from the response

p = s.split("&")
p1 = p[0]

#Now ask for authorization

url = "https://api.login.yahoo.com/oauth/v2/request_auth?" + p1

#And now we have to pop open a web browser to grant permission for the API to work

webbrowser.open(url)

 #Let's assign the code to a variable

code = "gfesvm"
