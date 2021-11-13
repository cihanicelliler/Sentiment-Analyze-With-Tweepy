import json
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch
import re
import string
import csv
import os

# import twitter keys and tokens
from config import *

# create instance of elasticsearch
es = Elasticsearch()

if es.ping():
    print("We are connected......")
else:
    print("Connection error!")


def write_to_csv(tweet, dict_data, sentiment):
    csvFile = open('tweetsResults.csv', 'a')
    
    dict_data["text"] = clear_tweets(dict_data["text"])
    
    csvWriter = csv.writer(csvFile)

    if(os.stat(r"C:\Users\icell\Desktop\Programlama\Python\TwintForTwitter\tweepy\tweetsResults.csv").st_size == 0):
        csvWriter.writerow(["Created At", "Source", "Tweet", "Sentiment",
                            "Polarity", "Subjectivity", "User Name", "Place"])

    # Write a row to the CSV file. I use encode UTF-8
    csvWriter.writerow([dict_data["created_at"], dict_data["source"].encode('utf-8'), dict_data["text"].encode('utf-8'), sentiment,
                        tweet.sentiment.polarity, tweet.sentiment.subjectivity, dict_data["user"]["screen_name"], dict_data["place"]])
    csvFile.close()


def clear_tweets(tweet):
    # clear Emoji patterns
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    tweet = emoji_pattern.sub(r'', tweet)

    # clear punctions
    tweet = tweet.translate(
        str.maketrans('', '', string.punctuation))

    return tweet


class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        # decode json
        dict_data = json.loads(data)

        # call clear_tweets function
        dict_data["text"] = clear_tweets(dict_data["text"])

        # pass tweet into TextBlob wihout reTweets
        tweet = TextBlob(dict_data["text"])
        # print(tweet)

        # output sentiment polarity
        # print(tweet.sentiment.polarity)

        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

        # output sentiment
        # print(sentiment)

        write_to_csv(tweet, dict_data, sentiment)
        # add text and sentiment info to elasticsearch
        es.index(index="sentiment",
                 doc_type="test-type",
                 body={"author": dict_data["user"]["screen_name"],
                       "date": dict_data["created_at"],
                       "message": dict_data["text"],
                       "source": dict_data["source"],
                       "polarity": tweet.sentiment.polarity,
                       "subjectivity": tweet.sentiment.subjectivity,
                       "sentiment": sentiment,
                       "place": dict_data["place"]})
        return True

    # on failure
    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key,
                        consumer_secret)
    auth.set_access_token(access_token,
                          access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for "covid" keyword
    stream.filter(languages=["en"], track=['covid'])
