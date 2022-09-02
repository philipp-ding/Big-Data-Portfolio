# creator
import json
import socket
import socketserver
import sys
import threading
import time

import mysql.connector
import tweepy
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import desc, explode, regexp_extract, split
from pyspark.streaming import StreamingContext
from tweepy import OAuthHandler  # to authenticate Twitter API
from tweepy import Stream

# Twitter developer Credentials to connect to twitter account
# access_token = "TJ5yMVqMi5bb9mTTvfGWYpuuG"
# access_secret = "hiwyl27xXGUz5IB1MKVOW78WmvW0MmJ02idTaLzPc9N3pRawLk"
# consumer_key = "3154565879-0nE46vwnEMQ55KUCEXRNeZWlMd06IXYfXVIYpLv"
# consumer_secret = "zOgVGCXi3Xoho2lM3XtprtbiZ3N5D7pN0192zpFleYLxv"
# Access_Token = "3154565879-0nE46vwnEMQ55KUCEXRNeZWlMd06IXYfXVIYpLv" # public access token of the app
# Access_Token_Secret = "zOgVGCXi3Xoho2lM3XtprtbiZ3N5D7pN0192zpFleYLxv" # private access token of the app
# app_name = "dhwbbigdataproject" # name of the app on the twitter developer platform
# API_Key = "TJ5yMVqMi5bb9mTTvfGWYpuuG" # public api key of the app
# API_Key_Secret = "hiwyl27xXGUz5IB1MKVOW78WmvW0MmJ02idTaLzPc9N3pRawLk"  # private api key of the app


def sendData():
    # Twitter developer credentials to connect to the twitter API
    Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAMLdgQEAAAAApE%2BdLd2GEuEuVimBbopFFB0jcGM%3Df2PD6SjLBxo7IjdD9OfR12bcW7PHjNkJUFY1KuRwVFonBU60dD"  # bearer token of the app
    client = tweepy.Client(
        Bearer_Token)  # connection to the twitter API via tweepy client
    query = 'music (blues OR classic OR house OR jazz OR country OR electro OR hiphop OR metal OR pop OR rnb OR rock) -is:retweet lang:en'  # search query for selecting the tweets to stream
    tweets = client.search_recent_tweets(
        query=query,  # initializing the search query
        tweet_fields=['context_annotations', 'created_at'
                      ],  # selecting which of the tweets fields to stream
        max_results=100
    )  # number of tweets to stream at once (limited by the API)
    tweets_text = [tweet.text for tweet in tweets.data
                   ]  # saving the text of the tweets into a list
    return tweets_text  # returning the text of the tweets


def start_server_thread():
    class MySocketHandler(socketserver.BaseRequestHandler
                          ):  # defining a class for streaming the tweets
        def handle(self):  # function for streaming the tweets
            filetosend = sendData()  # selecting the data to stream
            for line in filetosend:
                self.request.sendall(line.encode("UTF-8"))
                time.sleep(0.1)

            self.request.close()

    socketserver.TCPServer(("127.0.0.1", 9999), MySocketHandler).serve_forever(
    )  # starting a TCP server for streaming the tweets


threading.Thread(target=start_server_thread, daemon=True).start()

#######################
# Listener
#######################

# BEGIN-SNIPPET
spark = SparkSession.builder \
    .appName("Structured Streaming").getOrCreate() # creating a spark session for Structured Streaming Calculations

spark.sparkContext.setLogLevel('ERROR')  # setting the LogLevel to Error

lines = spark.readStream.format("socket") \
    .option("host", "127.0.0.1").option("port", 9999).load() # reading the tweets from the tcp server

words = lines.select(
    explode(split(lines.value, " ")).alias("word")
)  # reducing the tweets to the words and splitting them into several parts to get a list with all words
wordCounts = words.groupBy("word").count().withColumnRenamed(
    'count', 'views')  # counting the apperance in the list for each word

query = wordCounts.writeStream.outputMode("complete") \
    .format("console").start() # printing the words with their count to the console


def databaseconnection(batchDataframe, batchId):
    def save_to_db(iterator):
        dbconnection = mysql.connector.connect(
            host="localhost",
            port=3306,
            database='sportsdb',
            user="root",
            password="mysecretpw"
        )  # connection to the database to save the calculations
        cursor = dbconnection.cursor(
        )  # creating a cursor to perform SQL actions
        genres = [
            'blues', 'Blues', 'classic', 'Classic', 'house', 'House', 'jazz',
            'Jazz', 'country', 'Country', 'electro', 'Electro', 'hiphop',
            'Hip Hop', 'metal', 'Metal', 'pop', 'Pop', 'rnb', 'Rnb', 'rock',
            'Rock'
        ]  # list with the music genres to only select them from the word count data frame

        for row in iterator:  # loop for iterating through the data frame
            if row.word in genres:  # if statement to only select the words which are music genres
                query_mariadb = f"INSERT INTO popular_genres (genre, count) VALUES ('{row.word}', {row.views}) ON DUPLICATE KEY UPDATE count={row.views};"  # creating the SQL statement for saving the genres and their counts
                cursor.execute(
                    query_mariadb
                )  # executing the SQL query to save the genre and the count to the database
        dbconnection.commit()  # commiting the change to the database
        cursor.close()  # closing the cursor
        dbconnection.close()  # closing the database connection

    # Perform batch UPSERTS per data partition
    batchDataframe.foreachPartition(
        save_to_db
    )  # calling the function to save the results of the batches calculations

dbInsertStream = wordCounts.writeStream \
    .outputMode("update") \
    .foreachBatch(databaseconnection) \
    .start() # creating a writing stream to save the batches calculations to the database

spark.streams.awaitTermination()
