# -*- coding: utf-8 -*- 

import json
import tweepy
import socket
import sys
from utils import Util

def initialize():
    with open('data/config.json') as config_data:
        config = json.load(config_data)

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    api = tweepy.API(auth)

    stream = TwitterStreamListener()
    twitter_stream = tweepy.Stream(auth = api.auth, listener=stream)
    twitter_stream.filter(track=['python'], async=True)


class TwitterStreamListener(tweepy.StreamListener):
    def on_data(self, data):
        text_i = data.find("text")
        source_i = data.find("source")
        text = data[text_i + 8: source_i].decode('utf_8')
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 9999)
        print >> sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        
        try:
            print >>sys.stderr, 'sending "%s"' % text
            sock.sendall(Util.normalize(text) + '\n')

        finally:
            print >>sys.stderr, 'closing socket'
            sock.close()

    def on_error(self, status_code):
        if status_code == 420:
            return False


if __name__ == "__main__":
    initialize()