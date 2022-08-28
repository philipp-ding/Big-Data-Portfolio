import json
import socket

import tweepy
from tweepy import Stream
from tweepy.auth import OAuthHandler

# from tweepy.streaming import StreamListener

# request to get credentials at http://apps.twitter.com
consumer_key = 'TJ5yMVqMi5bb9mTTvfGWYpuuG'
consumer_secret = 'hiwyl27xXGUz5IB1MKVOW78WmvW0MmJ02idTaLzPc9N3pRawLk'
access_token = '3154565879-0nE46vwnEMQ55KUCEXRNeZWlMd06IXYfXVIYpLv'
access_secret = 'Secret zOgVGCXi3Xoho2lM3XtprtbiZ3N5D7pN0192zpFleYLxv'


# we create this class that inherits from the StreamListener in tweepy StreamListener
class TweetsListener(tweepy.Stream):
    def __init__(self, csocket):
        self.client_socket = csocket

    # we override the on_data() function in StreamListener
    def on_data(self, data):
        try:
            message = json.loads(data)
            print(message['text'].encode('utf-8'))
            self.client_socket.send(message['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def if_error(self, status):
        print(status)
        return True


def send_tweets(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['football'
                                 ])  #we are interested in this topic.


if __name__ == "__main__":
    new_skt = socket.socket()  # initiate a socket object
    host = "127.0.0.1"  # local machine address
    port = 5555  # specific port for your service.
    new_skt.bind((host, port))  # Binding host and port

    print("Now listening on port: %s" % str(port))

    new_skt.listen(5)  # waiting for client connection.
    c, addr = new_skt.accept(
    )  # Establish connection with client. it returns first a socket object,c, and the address bound to the socket
    print('Check')

    print("Received request from: " + str(addr))
    # and after accepting the connection, we aill sent the tweets through the socket
    send_tweets(c)
