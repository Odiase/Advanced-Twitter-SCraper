import snscrape.modules.twitter as sntwitter
from datetime import datetime
from urllib.parse import urlencode, quote_plus
import requests
import math 

from flask import Flask, render_template, request



app = Flask(__name__)

### Sentiment Data
def sentiment_data(url):
    response = requests.get(url).json()

    negative = int(response["negative"] * 100)
    positive = int(response["positive"] * 100)
    
    if positive > negative:
        return f"{int(positive)}% Positive"
    else:
        return f"{int(negative)}% Negative"




# function to get tweets from user's twitter handle
def get_tweets(handle, limit, date_from, date_to):
    query = f"(from:{handle}) until:{date_to} since:{date_from}"
    tweet_limit = int(limit) -1

    tweets = []
    sentiment_url = "https://api.uclassify.com/v1/uclassify/sentiment/classify?"

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        tweet_data = {}
        if len(tweets) <= tweet_limit:
            tweet = vars(tweet)
            payload = {"readKey" : "0hIf15vXIlcy", "text" : tweet}
            payload = urlencode(payload, quote_via=quote_plus)
            url = sentiment_url + payload
            result = sentiment_data(url)

            tweet_data["tweet"] = tweet
            tweet_data["sentiment_analysis"] = result
            tweets.append(tweet_data)
        else:
            break
            
    return tweets




@app.route('/', methods = ['GET'])
def home():
    return render_template("index.html")


@app.route('/tweets', methods = ['GET','POST'])
def tweets():
    if request.method == "POST":
        handle = request.form['twitter_handle']
        limit = request.form['tweet_limit']
        date_from = request.form['date_from'] 
        date_to = request.form['date_to']

        try:
            tweets = get_tweets(handle, limit, date_from, date_to)
        except:
            tweets = []
        context = {
            "tweets":tweets,
            "handle":handle,
            "date_from":date_from,
            "date_to":date_to,
            "limit":limit
        }
    else:
       context = {
            
       }

    return render_template("tweets.html", context = context)

if __name__ == '__main__':
    app.run(debug=True)