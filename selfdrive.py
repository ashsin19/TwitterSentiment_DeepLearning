import os
import pandas as pd
import tweepy
import re
import string
from textblob import TextBlob
import preprocessor as p
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


#Twitter credentials for the app
access_key = "79542926-k8Q0X882mB3jTW2fVuWxYapwDK6AWvT8VmUaGHNoO"
access_secret = "mZzCjCfCOi0AmOsBCFAvtNimsJu5PxH2OOj4sqEnOxBFQ"
consumer_key = "CIRtrE8saDklq35lW9coh5uPm"
consumer_secret = "oP3IawdMkVrDQ2wZhgtViA5NXI3HXtPaDaGGVheeVB36NN1RA2"

#pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

selfdrive_tweets = "selfdrive_data.csv"

#columns of the csv file
COLS = ['id', 'created_at', 'source', 'original_text', 'lang',
        'favorite_count', 'retweet_count', 'original_author', 'hashtags',
        'user_mentions', 'place', 'place_coord_boundaries']

#set two date variables for date range
start_date = '2015-01-01'
end_date = '2019-06-23'

#method write_tweets()
def write_tweets(keyword, file):
    # If the file exists, then read the existing data from the CSV file.
    if os.path.exists(file):
        df = pd.read_csv(file, header=0)
    else:
        df = pd.DataFrame(columns=COLS)
    #page attribute in tweepy.cursor and iteration
    for page in tweepy.Cursor(api.search, q=keyword,
                              include_rts=True, since=start_date,tweet_mode = 'extended').pages(100):
        for status in page:
            new_entry = []
            status = status._json

            #when run the code, below code replaces the retweet amount and
            #no of favorires that are changed since last download.
            if status['created_at'] in df['created_at'].values:
                i = df.loc[df['created_at'] == status['created_at']].index[0]
                if status['favorite_count'] != df.at[i, 'favorite_count'] or \
                   status['retweet_count'] != df.at[i, 'retweet_count']:
                    df.at[i, 'favorite_count'] = status['favorite_count']
                    df.at[i, 'retweet_count'] = status['retweet_count']
                continue
            new_entry += [status['id'], status['created_at'],
                          status['source'], status["full_text"], status['lang'],
                          status['favorite_count'], status['retweet_count']]

            #to append original author of the tweet
            new_entry.append(status['user']['screen_name'])

            # hashtagas and mentiones are saved using comma separted
            hashtags = ", ".join([hashtag_item['text'] for hashtag_item in status['entities']['hashtags']])
            new_entry.append(hashtags)
            mentions = ", ".join([mention['screen_name'] for mention in status['entities']['user_mentions']])
            new_entry.append(mentions)

            #get location of the tweet if possible
            try:
                location = status['user']['location']
            except TypeError:
                location = ''
            new_entry.append(location)

            try:
                coordinates = [coord for loc in status['place']['bounding_box']['coordinates'] for coord in loc]
            except TypeError:
                coordinates = None
            new_entry.append(coordinates)

            single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
            df = df.append(single_tweet_df, ignore_index=True)
            csvFile = open(file, 'a' ,encoding='utf-8')
    df.to_csv(csvFile, mode='a', columns=COLS, index=False, encoding="utf-8")

#declare keywords
selfdrive_keywords = '#SelfDrivingCars OR #driverlesscar OR #driverless OR #AutonomousVehicles OR #AutonomousCars OR  #autonomousdriving OR #AutomatedDriving'

#call main method passing keywords and file path
write_tweets(selfdrive_keywords,  selfdrive_tweets)
