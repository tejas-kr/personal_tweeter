from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from flask_dance.contrib.twitter import twitter
from decouple import config
import tweepy
from datetime import datetime, date, timedelta

m_func = Blueprint("main_functions", __name__, template_folder="templates")

consumer_key, consumer_secret, access_token, access_token_secret = (
    config("twitter_consumer_key"),
    config("twitter_consumer_secret"),
    config("twitter_access_token"),
    config("twitter_access_token_secret"),
)
tweepy_api_auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(tweepy_api_auth)

def get_timeline_tweets(user_name, all_tweet=0, tweets=["default"], other_tweets=False):
    if all_tweet==0:
        tweets = api.user_timeline(screen_name=user_name, count=200, exclude_replies=True, include_rts=False, tweet_mode = 'extended')
    tweets_list = []
    for tweet in tweets:
        twitter_status_url = f'https://twitter.com/{user_name}/status/{tweet.id}'
        
        current_date = date.today()
        tweet_date = (tweet.created_at).date()
        
        if tweet_date == current_date or other_tweets:
            formatted_date = datetime.strftime(tweet.created_at, '%d-%m-%Y')
            formatted_time = datetime.strftime(tweet.created_at, '%H:%M')
            l1 = {}
            l1["full_text"] = (tweet.full_text)
            l1["formatted_date"] = (formatted_date)
            l1["formatted_time"] = (formatted_time)
            l1["twitter_status_url"] = (twitter_status_url)
            l1["retweet_count"] = (tweet.retweet_count)
            l1["favorite_count"] = (tweet.favorite_count)
            tweets_list.append(l1)
    return tweets_list

@m_func.route('/')
def index():
    if not twitter.authorized:
        return render_template("login.html")
    resp = twitter.get("account/settings.json")

    user_name = resp.json()["screen_name"]
    
    tweets_list = get_timeline_tweets(user_name=user_name)

    context = {}
    context["user_name"] = user_name
    context["tweets_list"] = tweets_list


    return render_template('home.html', context=context)

@m_func.route('/other_tweets')
def other_tweets():
    if not twitter.authorized:
        return render_template("login.html")
    resp = twitter.get("account/settings.json")

    user_name = resp.json()["screen_name"]
    date_format = "%Y-%m-%d"
    last_date_from_current_date = (datetime.today() - timedelta(days=7)).date()
    current_date = date.today()
    context = {}
    context["last_date_from_current_date"] = last_date_from_current_date
    context["current_date"] = current_date

    return render_template('other_tweets.html', context=context)

@m_func.route('/search_tweets', methods=["GET"])
def search_tweets():
    """
        Example string - http://127.0.0.1:5000/search_tweets?date=2022-07-22&query=sdf
        date is the until date 
        for reference - https://docs.tweepy.org/en/stable/api.html#search-tweets
    """
    if not twitter.authorized:
        abort(400, "need to login")
    resp = twitter.get("account/settings.json")

    user_name = resp.json()["screen_name"]
    date = request.args.get("date")
    query = request.args.get("query")

    date = (datetime.strptime(date, "%Y-%m-%d")).date()

    result = api.search_tweets(q=query, until=date, tweet_mode = 'extended')
    tweets_list = get_timeline_tweets(user_name=user_name, all_tweet=1, tweets=result, other_tweets=True)

    context = {}
    context["tweets_list"] = tweets_list

    return jsonify(context)

