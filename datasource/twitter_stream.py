# -*- coding: utf-8 -*-

import json
import tweepy
import socket
import sys
import time

from utils import Util
from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.client import KafkaClient

def initialize():
    with open('data/config.json') as config_data:
        config = json.load(config_data)

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    api = tweepy.API(auth)

    stream = TwitterStreamListener()
    twitter_stream = tweepy.Stream(auth = api.auth, listener=stream)
    twitter_stream.filter(track=['iphone'], async=True)


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self):
      self.producer = KafkaProducer(bootstrap_servers='docker:9092', value_serializer=lambda v: json.dumps(v))
      self.tweets = []

    def on_data(self, data):
      text_i = data.find("text")
      source_i = data.find("source")
      text = data[text_i + 8: source_i].decode('ascii')
      print(text)
      self.producer.send('iphone', text)
      self.producer.flush()

    def on_error(self, status_code):
        if status_code == 420:
            return False


if __name__ == "__main__":
    initialize()