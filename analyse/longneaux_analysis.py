import csv

import tweepy
import time
import os
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from datetime import datetime
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

# bot twitter account access keys and authentication
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# target tweeter account
userId = os.environ.get('TARGET_ID')


# get last 10 tweets excludings retweets & replies
def get_tweets():
    tweets = []
    timeline = api.user_timeline(screen_name=userId,
                                 count=500,
                                 include_rts=False,
                                 exclude_replies=True,
                                 tweet_mode="extended"
                                 )
    for tweet in timeline:
        if not is_tweet_analysed(tweet.id):
            tweets.append(tweet)
            write_id(tweet.id)
    return tweets


def get_all_tweets():
    tweets = []
    timeline = api.user_timeline(screen_name=userId,
                                 count=500,
                                 include_rts=False,
                                 exclude_replies=True,
                                 tweet_mode="extended"
                                 )
    for tweet in timeline:
        tweets.append(tweet)
    return tweets


# enter the id in the file so that the bot does not replies multiple times
def write_id(tweet_id):
    with open('analysed.txt', 'a') as opened_file:
        opened_file.write(str(tweet_id) + "\n")


def write_time_diff(text_to_write):
    with open('time_average.txt', 'a') as opened_file:
        opened_file.write(str(text_to_write) + "\n")


def write_to_csv(processed_tweets):
    with open('word_counts.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the data
        writer.writerows(processed_tweets)


# check if the tweet has already been replied
def is_tweet_analysed(tweet_id):
    analysed_ids = []
    with open('analysed.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            analysed_ids.append(int(line.strip("\n")))

    return tweet_id in analysed_ids


def process_tweets(tweets):
    tweet_word_list = []
    for tweet in tweets:
        for txt in tweet.full_text.split(" "):

            if ";" in txt:
                for element in txt.split(";"):
                    tweet_word_list.append(element.strip("&gt").strip("\n").strip("(").strip(")"))

            elif "\n" in txt:
                for element in txt.split("\n"):
                    if element != ":":
                        tweet_word_list.append(element.strip("(").strip(")"))
            else:
                tweet_word_list.append(txt.strip("\n").strip(":\n").strip("(").strip(")").strip(".").strip(","))

    return tweet_word_list


def count_words(word_list):
    word_count_list = {}
    word_count_list_process = []
    for word in word_list:
        if word not in word_count_list:
            word_count_list[word] = 1
        else:
            word_count_list[word] += 1

    for key in word_count_list:
        word_count_list_process.append([key, word_count_list[key]])
    return [word_count_list, word_count_list_process]


def top_x(value):
    d = dict()
    with open('word_counts.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            d[line[0]] = line[1]

    return dict(Counter(d).most_common(value))


def to_pie(word_counts):
    labels = []
    sizes = []

    for x, y in word_counts.items():
        labels.append(x)
        sizes.append(y)

    # Plot
    plt.pie(sizes, labels=labels)
    plt.axis('equal')
    plt.show()


def time_average(tweets):
    total_time = []
    prev_time = tweets[0].created_at.timestamp()
    for tweet in tweets:
        total_time.append(prev_time - tweet.created_at.timestamp())
        prev_time = tweet.created_at.timestamp()

    del total_time[0]

    return round((sum(total_time) / len(total_time)) / 86400, 2)


def avg_hours_to_chart(tweets):
    hours = {}
    for tweet in tweets:
        if tweet.created_at.hour not in hours:
            hours[tweet.created_at.hour] = 1
        else:
            hours[tweet.created_at.hour] = hours[tweet.created_at.hour] + 1

    keys = hours.keys()
    values = hours.values()

    plt.bar(keys, values)
    x = list(range(0, 24))
    plt.xticks(x)
    plt.show()


def avg_words_per_tweet(tweets):
    total_words = []

    for tweet in tweets:
        tweet_word_count = 0
        for txt in tweet.full_text.split(" "):

            if ";" in txt:
                for element in txt.split(";"):
                    tweet_word_count = tweet_word_count + 1

            elif "\n" in txt:
                for element in txt.split("\n"):
                    if element != ":":
                        tweet_word_count = tweet_word_count + 1
            else:
                tweet_word_count = tweet_word_count + 1
        total_words.append(tweet_word_count)

    return round((sum(total_words) / len(total_words)), 2)


def run():
    # tweets = get_tweets()
    # data = count_words(process_tweets(tweets))
    # write_to_csv(data[1])
    # to_pie(top_x(20))
    # print(time_average(get_all_tweets()))
    # print(avg_words_per_tweet(get_all_tweets()))
    avg_hours_to_chart(get_all_tweets())


# the bot checks every x hours for new tweets to analyse
if __name__ == "__main__":
    run()
