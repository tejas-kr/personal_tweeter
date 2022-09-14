from flask import Blueprint, render_template, abort, request, redirect, url_for, session
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from decouple import config

auth = Blueprint("auth", __name__, template_folder="templates")
twitter_bp = make_twitter_blueprint(api_key=config('twitter_consumer_key'), api_secret=config('twitter_consumer_secret'))
auth.register_blueprint(twitter_bp, url_prefix="/login")

@auth.route('/login')
def login():
    if not twitter.authorized:
        return redirect(url_for("auth.twitter.login"))
    # resp = twitter.get("account/verify_credentials.json")
    resp = twitter.get("account/verify_credentials.json")
    return redirect(url_for('index'))

@auth.route('/logout')
def twitter_logout():
    if not twitter.authorized:
        return redirect(url_for('index'))
    session.clear()
    return redirect(url_for('main_functions.index'))