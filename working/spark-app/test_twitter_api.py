# creator
import time
import threading
import socketserver
from pip import main
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json
import socket

import tweepy
from tweepy import OAuthHandler  # to authenticate Twitter API
from tweepy import Stream

#from tweepy.streaming import StreamListener

# Twitter developer Credentials to connect to twitter account
app_name = "dhwbbigdataproject"
API_Key = "TJ5yMVqMi5bb9mTTvfGWYpuuG"
API_Key_Secret = "hiwyl27xXGUz5IB1MKVOW78WmvW0MmJ02idTaLzPc9N3pRawLk"
Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAMLdgQEAAAAApE%2BdLd2GEuEuVimBbopFFB0jcGM%3Df2PD6SjLBxo7IjdD9OfR12bcW7PHjNkJUFY1KuRwVFonBU60dD"
Access_Token = "3154565879-0nE46vwnEMQ55KUCEXRNeZWlMd06IXYfXVIYpLv"
Access_Token_Secret = "zOgVGCXi3Xoho2lM3XtprtbiZ3N5D7pN0192zpFleYLxv"


if __name__ == '__main__':
    # twitter_stream = Stream(API_Key, API_Key_Secret,
    #                         Access_Token, Access_Token_Secret)
    # test = twitter_stream.filter(track=['corona'])
    # print(test)
    client = tweepy.Client(Bearer_Token)
    query = '#petday -is:retweet lang:en'
    tweets = client.search_recent_tweets(query=query, tweet_fields=[
                                         'context_annotations', 'created_at'], max_results=100)
    tweets_text = [tweet.text for tweet in tweets.data]
    print(tweets_text)
    # for tweet in tweets.data:
    #     print(tweet.text)
    #     if len(tweet.context_annotations) > 0:
    #         print(tweet.context_annotations)
