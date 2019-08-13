from tweepy import OAuthHandler
import json
import pandas as pd
import matplotlib.pyplot as plt
import tweepy
f = open('twitter_credentials.json')
cred = json.load(f)
f.close()
auth = OAuthHandler(cred['consumer_key'], cred['consumer_secret'])
auth.set_access_token(cred['access_token'], cred['access_secret'])

from tweepy import Stream
from tweepy.streaming import StreamListener
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('autonomousDriveMulti.json', 'a') as f:
                f.write(data)
                return True
        except KeyboardInterrupt:
            print("Data Live Streaming Stopped")
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#driverlesscar','#autonomouscars','#autonomousvehicles'])

