# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests, json, certifi, pycurl, time
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "fSm4RXOixMvO1y0vQPbCBC2Kw"
CONSUMER_SECRET = "wzFARcKEOrW36rzpWQHQ7FQV2JumkUW8vGav9wrYPcfdT656Ws"

OAUTH_TOKEN = "761329334-qN7iJoAqsIkyI6r4BY1Fy6d45faM4MgusV5Qfmpe"
OAUTH_TOKEN_SECRET = "kUikBUuGQOrxYrv3WU3tAVwVB5CtYEIihIkTXOU4xErwm"

def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials= parse_qs(r.content)
    
    resource_owner_key = credentials.get(b'oauth_token')
    resource_owner_secret = credentials.get(b'oauth_token_secret')


    def get_auth_Token(credentials):
        for x in credentials:
            if len(x) == 11:
                auth_Token = (str(credentials[x])[3:-2])
        return auth_Token

    def get_auth_Token_sec(credentials):
        for y in credentials:
            if len(y) == 18:
                auth_Token_sec = (str(credentials[y])[3:-2])
        return auth_Token_sec
    
    # Authorize
    authorize_url = AUTHORIZE_URL + get_auth_Token(credentials)
    print ('Please go here and authorize: ' + authorize_url)

    verifier = input('Please input the verifier: ')

    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=get_auth_Token(credentials),
                   resource_owner_secret=get_auth_Token_sec(credentials),
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    
    token = credentials.get(b'oauth_token')
    secret = credentials.get(b'oauth_token_secret')

    return token, secret
 

def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()

        print ("OAUTH_TOKEN: " + str(token)[3:-2])
        print ("OAUTH_TOKEN_SECRET: " + str(secret)[3:-2])
        print ()
    else:
        oauth = get_oauth()

        r = requests.get(url="https://api.twitter.com/1.1/trends/place.json?id=1&count=10", auth=oauth)

        #ctime = time.ctime()
        #print ("Top 10 Twitter Trends as of %s" % ctime)

        trending_topic = " "
        count = 0

        while count < 10:
            print (r.json()[0]["trends"][count]["name"])
            trending_topic = trending_topic + (r.json()[0]["trends"][count]["name"]) + '\n'
            count += 1

        jresult = json.dumps({"text":str(trending_topic)})
        pc = pycurl.Curl()
        webhook_url = 'https://hooks.slack.com/services/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'

        pc.setopt(pycurl.CAINFO, certifi.where())
        pc.setopt(pycurl.URL, webhook_url)
        pc.setopt(pycurl.POST, 1)
        pc.setopt(pycurl.POSTFIELDS, jresult)
        pc.perform()
