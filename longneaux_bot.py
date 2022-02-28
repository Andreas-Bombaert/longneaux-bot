import tweepy
import time
import os
from datetime import datetime
from dotenv import load_dotenv
import json
import random
import imghdr
import urllib.request
import urllib.parse

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

# google image search credentials
API_KEY = os.environ.get('GIS_API')
SEARCH_ENGINE_ID = os.environ.get('GIS_CX')

image_name = ""


def search_image(query):
    request = urllib.request.Request(
        'https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' +
        SEARCH_ENGINE_ID + '&q=' + query + '&searchType=image')

    with urllib.request.urlopen(request) as f:
        data = f.read().decode('utf-8')

    data = json.loads(data)
    results = data['items']
    url = random.choice(results)['link']
    urllib.request.urlretrieve(url, './' + query)
    imagetype = imghdr.what('./' + query)

    global image_name
    image_name = './' + query + '.' + imagetype
    if not type(imagetype) is None:
        os.rename('./' + query, './' + query + '.' + imagetype)
        image_name = './' + query + '.' + imagetype


# get last 10 tweets excludings retweets & replies
def get_tweets():
    timeline = api.user_timeline(screen_name=userId,
                                 count=100,
                                 include_rts=False,
                                 exclude_replies=True,
                                 tweet_mode="extended"
                                 )
    return timeline


# enter the id in the file so that the bot does not replies multiple times
def write_id(tweet_id):
    with open('replied.txt', 'a') as opened_file:
        opened_file.write(str(tweet_id) + "\n")


# write log when replying to a tweet
def write_log(tweet_id):
    with open('logs', 'a') as opened_file:
        opened_file.write(str(tweet_id) + " replied at " + str(datetime.now()) + "\n")


# check if the tweet has already been replied
def is_tweet_replied(tweet_id):
    replied_ids = []
    with open('replied.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            replied_ids.append(int(line.strip("\n")))

    return tweet_id in replied_ids


# main loop
def loop():
    tweets = get_tweets()
    for tweet in tweets:
        if not is_tweet_replied(tweet.id):
            write_id(tweet.id)
            write_log(tweet.id)

            word_list = tweet.full_text.split(" ")
            rand = word_list[random.randint(0, len(word_list))-1]
            search_image(rand)

            img_source = "./" + image_name
            status_txt = "@longneaux malédiction nulle basée sur le mot  " + rand
            api.update_status_with_media(filename=img_source, status=status_txt, in_reply_to_status_id=tweet.id)

            os.remove("./" + image_name)

        else:
            pass


# the bot checks every x hours for new tweets to answer
if __name__ == "__main__":
    print("bot started")
    while True:
        loop()
        time.sleep(7200)
