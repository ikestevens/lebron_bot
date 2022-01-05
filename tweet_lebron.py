import tweepy
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
from Lebron import Bron

# get keys and secrets
consumer_key = os.environ.get('BRON_BOT_CONSUMER_KEY')
consumer_secret = os.environ.get('BRON_BOT_CONSUMER_SECRET')
access_key = os.environ.get('BRON_BOT_ACCESS_KEY')
access_secret = os.environ.get('BRON_BOT_ACCESS_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Create API object
api = tweepy.API(auth)

def create_tweet(home):
    if home:
        tweet_string = '''Over the past 10 games, Lebron is averaging {} points. If he stays on this pace,

He'll pass Malone in {} games on {} at home against the {}.
He'll pass Kareem in {} games which would be around {}.
        '''.format(bron.points_avg, bron.games_to_pass_karl, bron.projected_karl_pass_date, bron.projected_karl_opponent, bron.games_to_pass_kareem, bron.projected_kareem_pass_date)
    else:
        tweet_string = '''Over the past 10 games, Lebron is averaging {} points. If he stays on this pace,

He'll pass Malone in {} games on {} against the {}.
He'll pass Kareem in {} games which would be around {}.
        '''.format(bron.points_avg, bron.games_to_pass_karl, bron.projected_karl_pass_date, bron.projected_karl_opponent, bron.games_to_pass_kareem, bron.projected_kareem_pass_date)
    return tweet_string

bron = Bron()
tweet_contents = create_tweet(bron.projected_karl_home)

#api.update_status(tweet_contents)

print('just tweeted this: \n{}'.format(tweet_contents))
