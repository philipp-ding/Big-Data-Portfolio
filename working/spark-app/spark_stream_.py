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


def sendData():
    # Twitter developer Credentials to connect to twitter account
    app_name = "dhwbbigdataproject"
    API_Key = "TJ5yMVqMi5bb9mTTvfGWYpuuG"
    API_Key_Secret = "hiwyl27xXGUz5IB1MKVOW78WmvW0MmJ02idTaLzPc9N3pRawLk"
    Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAMLdgQEAAAAApE%2BdLd2GEuEuVimBbopFFB0jcGM%3Df2PD6SjLBxo7IjdD9OfR12bcW7PHjNkJUFY1KuRwVFonBU60dD"
    Access_Token = "3154565879-0nE46vwnEMQ55KUCEXRNeZWlMd06IXYfXVIYpLv"
    Access_Token_Secret = "zOgVGCXi3Xoho2lM3XtprtbiZ3N5D7pN0192zpFleYLxv"
    client = tweepy.Client(Bearer_Token)
    query = 'music (blues OR classic OR house OR jazz OR country OR electro OR hiphop OR metal OR pop OR rnb OR rock) -is:retweet lang:en'
    tweets = client.search_recent_tweets(
        query=query,
        tweet_fields=['context_annotations', 'created_at'],
        max_results=100)
    tweets_text = [tweet.text for tweet in tweets.data]
    return tweets_text


def start_server_thread():
    class MySocketHandler(socketserver.BaseRequestHandler):
        def handle(self):
            filetosend = sendData()
            for line in filetosend:
                self.request.sendall(line.encode("UTF-8"))
                time.sleep(0.1)

            self.request.close()

    socketserver.TCPServer(("127.0.0.1", 9999),
                           MySocketHandler).serve_forever()


threading.Thread(target=start_server_thread, daemon=True).start()

#######################
# Listener
#######################

# BEGIN-SNIPPET
spark = SparkSession.builder \
    .appName("Structured Streaming").getOrCreate()

spark.sparkContext.setLogLevel('ERROR')

lines = spark.readStream.format("socket") \
    .option("host", "127.0.0.1").option("port", 9999).load()

words = lines.select(explode(split(lines.value, " ")).alias("word"))
wordCounts = words.groupBy("word").count().withColumnRenamed('count', 'views')

query = wordCounts.writeStream.outputMode("complete") \
    .format("console").start()


def databaseconnection(batchDataframe, batchId):
    def save_to_db(iterator):

        dbconnection = mysql.connector.connect(host="10.107.149.126",
                                               port=3306,
                                               database='sportsdb',
                                               user="root",
                                               password="mysecretpw")
        cursor = dbconnection.cursor()
        genres = [
            'blues', 'Blues', 'classic', 'Classic', 'house', 'House', 'jazz',
            'Jazz', 'country', 'Country', 'electro', 'Electro', 'hiphop',
            'Hip Hop', 'metal', 'Metal', 'pop', 'Pop', 'rnb', 'Rnb', 'rock',
            'Rock'
        ]

        for row in iterator:
            if row.word in genres:
                query_mariadb = f"INSERT INTO popular_genres (genre, count) VALUES ('{row.word}', {row.views}) ON DUPLICATE KEY UPDATE count={row.views};"
                cursor.execute(query_mariadb)
        dbconnection.commit()
        cursor.close()
        dbconnection.close()

    # Perform batch UPSERTS per data partition
    batchDataframe.foreachPartition(save_to_db)


dbInsertStream = wordCounts.writeStream \
    .outputMode("update") \
    .foreachBatch(databaseconnection) \
    .start()

query.awaitTermination()
spark.streams.awaitTermination()
