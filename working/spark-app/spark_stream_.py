# creator
import json
import socket
import socketserver
import threading
import time

import tweepy
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from tweepy import OAuthHandler  # to authenticate Twitter API
from tweepy import Stream

#from tweepy.streaming import StreamListener

# Twitter developer Credentials to connect to twitter account
access_token = "TJ5yMVqMi5bb9mTTvfGWYpuuG"
access_secret = "hiwyl27xXGUz5IB1MKVOW78WmvW0MmJ02idTaLzPc9N3pRawLk"
consumer_key = "3154565879-0nE46vwnEMQ55KUCEXRNeZWlMd06IXYfXVIYpLv"
consumer_secret = "zOgVGCXi3Xoho2lM3XtprtbiZ3N5D7pN0192zpFleYLxv"

# class TweetsListener(Stream):
#     # initialized the constructor
#     def __init__(self, csocket):
#         self.client_socket = csocket

#     def on_data(self, data):
#         try:
#             # read the Twitter data which comes as a JSON format
#             msg = json.loads(data)

#             # the 'text' in the JSON file contains the actual tweet.
#             print(msg['text'].encode('utf-8'))

#             # the actual tweet data is sent to the client socket
#             # time.sleep(0.1)
#             self.client_socket.send(msg['text'].encode('utf-8'))
#             return True

#         except BaseException as e:
#             # Error handling
#             print("Ahh! Look what is wrong : %s" % str(e))
#             return True

#     def on_error(self, status):
#         print(status)
#         return True


def sendData():
    # Twitter developer Credentials to connect to twitter account
    app_name = "dhwbbigdataproject"
    API_Key = "TJ5yMVqMi5bb9mTTvfGWYpuuG"
    API_Key_Secret = "hiwyl27xXGUz5IB1MKVOW78WmvW0MmJ02idTaLzPc9N3pRawLk"
    Bearer_Token = "AAAAAAAAAAAAAAAAAAAAAMLdgQEAAAAApE%2BdLd2GEuEuVimBbopFFB0jcGM%3Df2PD6SjLBxo7IjdD9OfR12bcW7PHjNkJUFY1KuRwVFonBU60dD"
    Access_Token = "3154565879-0nE46vwnEMQ55KUCEXRNeZWlMd06IXYfXVIYpLv"
    Access_Token_Secret = "zOgVGCXi3Xoho2lM3XtprtbiZ3N5D7pN0192zpFleYLxv"
    client = tweepy.Client(Bearer_Token)
    query = 'music -is:retweet lang:en'
    tweets = client.search_recent_tweets(
        query=query,
        tweet_fields=['context_annotations', 'created_at'],
        max_results=100)
    tweets_text = [tweet.text for tweet in tweets.data]
    return tweets_text


# def server_function():
#     # create a socket object
#     s = socket.socket()

#     # Get local machine name : host and port
#     host = "127.0.0.1"
#     port = 3333

#     # Bind to the port
#     s.bind((host, port))
#     print("Listening on port: %s" % str(port))

#     # Wait and Establish the connection with client.
#     s.listen(5)
#     c, addr = s.accept()

#     print("Received request from: " + str(addr))

#     # Keep the stream data available
#     sendData(c)

# threading.Thread(target=server_function, daemon=True).start()


def start_server_thread():
    class MySocketHandler(socketserver.BaseRequestHandler):
        def handle(self):
            filetosend = sendData()
            for line in filetosend:
                self.request.sendall(line.encode("UTF-8"))
                time.sleep(0.1)

            # filetosend.close()
            self.request.close()

    socketserver.TCPServer(("127.0.0.1", 9999),
                           MySocketHandler).serve_forever()


threading.Thread(target=start_server_thread, daemon=True).start()

#######################
# Listener
#######################

# BEGIN-SNIPPET

# Create local StreamingContext with a batch interval of 10s
sc = SparkContext("local[*]", "DStream Example")
ssc = StreamingContext(sc, 10)  # seconds
lines = ssc.socketTextStream("127.0.0.1", 9999)

# Perform transformations/actions
# words = lines.flatMap(lambda line: line.split(" "))
# pairs = words.map(lambda word: (word, 1))  # reduce on the genre
# wordCounts = pairs.reduceByKey(lambda x, y: x + y)
# wordCounts.pprint()
# pairs.pprint()

# split each tweet into words
words = lines.flatMap(lambda line: line.split(" "))
# filter the words to get only hashtags, then map each hashtag to be a pair of (hashtag,1)
genres = [
    'blues', 'Blues', 'classic', 'Classic', 'house', 'House', 'jazz', 'Jazz',
    'country', 'Country', 'electro', 'Electro', 'hiphop', 'Hip Hop', 'metal',
    'Metal', 'pop', 'Pop', 'rnb', 'Rnb', 'rock', 'Rock'
]
# genres = words.filter(lambda w: 'pop' in w).map(lambda x: (x, 1))
# genres.pprint()
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda z, y: z + y)

bluesCount = wordCounts.filter(lambda w: 'blues' in w)
classicCount = wordCounts.filter(lambda w: 'classic' in w)
houseCount = wordCounts.filter(lambda w: 'house' in w)
jazzCount = wordCounts.filter(lambda w: 'jazz' in w)
countryCount = wordCounts.filter(lambda w: 'country' in w)
electroCount = wordCounts.filter(lambda w: 'electro' in w)
hiphopCount = wordCounts.filter(lambda w: 'hiphop' in w)
metalCount = wordCounts.filter(lambda w: 'metal' in w)
popCount = wordCounts.filter(lambda w: 'pop' in w)
rnbCount = wordCounts.filter(lambda w: 'rnb' in w)
rockCount = wordCounts.filter(lambda w: 'rock' in w)

bluesCount.pprint()
classicCount.pprint()
houseCount.pprint()
jazzCount.pprint()
countryCount.pprint()
electroCount.pprint()
hiphopCount.pprint()
metalCount.pprint()
popCount.pprint()
rnbCount.pprint()
rockCount.pprint()

# wordCounts.pprint()
# genres.pprint()

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
