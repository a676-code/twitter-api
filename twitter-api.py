import tweepy
import configparser
import pandas as pd

# read configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# getting timelines
public_tweets = api.home_timeline()
mentions = api.mentions_timeline()
statuses = api.user_timeline()

# getting my favorites
favorites = api.get_favorites()

# get ids of my blocks?
bids = api.get_blocked_ids()
for b in bids:
    print(b)

search = api.search_users('soccer')

# ?
# trends = api.available_trends()

# getting a user
potus = api.get_user(screen_name="POTUS")
print(potus.screen_name)
print(potus.followers_count)
for friend in potus.friends():
    print(friend.screen_name)

print("\n", end='')
# getting my blocks
blocks = api.get_blocks()
for b in blocks:    
    print(b.screen_name)

# api.update_status("test status")

client = tweepy.Client()

# tweepy.errors.Unauthorized: 401 Unauthorized
# allTweets = client.search_all_tweets("Ratio")
# print(allTweets)

# tweepy.errors.Unauthorized: 401 Unauthorized
# recentTweets = client.search_recent_tweets("Ratio")
# print(recentTweets[0])

print(public_tweets[1].text)
print(public_tweets[0].created_at)
print(public_tweets[1].user.screen_name)

# Saving data from timeline in a list
columns = ['Time', 'User', 'Tweet']
data = []
for tweet in public_tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

# Converting list to pandas df
df = pd.DataFrame(data, columns = columns)

print(df)

# df.to_csv('timeline_tweets.csv')

# user tweets #####################################################
user = 'POTUS'
limit=300

# old
# tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')

user_tweets = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)

columns = ['User', 'Date', 'Tweet']
data = []
for tweet in user_tweets:
    data.append([tweet.user.screen_name, tweet.created_at, tweet.full_text])

df = pd.DataFrame(data, columns=columns)

print(df)

# df.to_csv("POTUS_tweets.csv")

# keyword tweets #####################################################

keywords = '@POTUS'
limit=300

keyword_tweets = tweepy.Cursor(api.search_tweets, q = keywords, count=100, tweet_mode='extended').items(limit)

# create DataFrame
data = []
for tweet in keyword_tweets:
    data.append([tweet.user.screen_name, tweet.created_at, tweet.full_text])

df = pd.DataFrame(data, columns=columns)

print(df)

# df.to_csv("tweets_about_POTUS.csv")

tweets = tweepy.Cursor(api.search_tweets, q = keywords, tweet_mode='extended').items(1)

data = []
for t in tweets:
    data.append([tweet.user.screen_name, tweet.created_at, tweet.full_text])

df = pd.DataFrame(data, columns=columns)

print(df)

df.to_csv("stuff.csv")