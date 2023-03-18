import tweepy
import pandas as pd
import matplotlib.pyplot as plt

from tweepy import Stream
from tweepy import OAuthHandler
# from tweepy.streaming import StreamListener
from tweepy.streaming import Stream

import json

consumer_key ='aJ8sfZ6a7IC7fncSIGKy9YHp3'
consumer_secret = 'NlrLeIKPpwfKzXaJNKpNLM2dXLnxcSJWB6Xr3RYsTvqEfrBlsE'
auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
api = tweepy.API(auth)

atoken = '909765471217508354-X9qJDspMiPGGE795Y97RDF4aXdXW5uK'
asecret = '909765471217508354-X9qJDspMiPGGE795Y97RDF4aXdXW5uK'


korea_geo = "%s,%s,%s" % ("35.95", "128.25", "1000km")

statuses = api.search_tweets(q='방탄', geocode=korea_geo, count=5)
status = statuses[0]

print(status.text)  # tweet 내용
print(status.created_at)  # 게시 일자
print(status.retweet_count)  # retweet된 횟수
print(status.favorite_count)  # 좋아요 받은 횟수
print(type(status))
statuses_len = len(statuses)
# with open('try.json', 'w') as outfile:
#     json_str = json.dumps({'salary': statuses})
#
#     json.dump(statuses, outfile)

json_str = json.dumps(status._json, ensure_ascii=False)

with open('try2.json', 'w') as outfile:
    # json_str = json.dumps({'salary': statuses})
    # json.dump(json_str, outfile)
    outfile.write(json_str, encoding='utf-8-sig')


a=0