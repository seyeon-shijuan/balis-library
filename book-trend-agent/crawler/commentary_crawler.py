# from tweepy import Stream
# from tweepy import OAuthHandler
# # from tweepy.streaming import StreamListener
# from tweepy.streaming import Stream
# import json
import tweepy
import pandas as pd
import datetime as dt
from dateutil.tz import gettz
try:
    import mysecrets
except:
    pass


class TwitterCrawler:

    def __init__(self, consumer_key, consumer_secret):
        self.auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key,
                                             consumer_secret=consumer_secret)
        self.api = tweepy.API(self.auth)
        self.korea_geo = "%s,%s,%s" % ("35.95", "128.25", "1000km")

    def fetch_tweets(self, q, count):
        statuses = self.api.search_tweets(q=q, geocode=self.korea_geo, count=count)
        return statuses

    def get_values_from_statuses(self, statuses, title, params: list):
        num = len(statuses)
        if num ==0:
            return None

        value_list = []

        for i in range(num):
            status = statuses[i]
            ori_dict = {'title': title}
            # values = {param: getattr(status, param).replace("\n", " ") if param != 'created_at' else getattr(status, param).strftime('%Y-%m-%d') for param in params}
            values = {param: getattr(status, param) for param in params}
            values['created_at'] = values['created_at'].strftime('%Y-%m-%d')
            values['text'] = values['text'].replace("\n", " ")
            ori_dict.update(values)
            value_list.append(ori_dict)

        return value_list

    def export_to_csv(self, in_list, outfile):
        df = pd.DataFrame.from_records(in_list)
        today = dt.datetime.now(gettz('Asia/Seoul')).today().strftime('%Y-%m-%d')
        df['date'] = today
        df.to_csv(f'../outfile/rank/{outfile}_{today}.csv', mode='w', index=False, header=True, encoding='utf-8-sig')
        print(outfile+' is saved')




if __name__ == '__main__':

    twitter_crawler = TwitterCrawler(mysecrets.consumer_key, mysecrets.consumer_secret)
    search_list = ['created_at', 'text', 'retweet_count', 'favorite_count']
    keyword_list = ['구의 증명', '사라진 여자들', '김미경의 마흔 수업']
    # twit_df = pd.DataFrame()
    twit_list = []

    for keyword in keyword_list:
        q = f'"{keyword}"'
        statuses = twitter_crawler.fetch_tweets(q, 100)
        rst_list = twitter_crawler.get_values_from_statuses(statuses, keyword, search_list)

        if rst_list:

            for item in rst_list:
                twit_list.append(item)

            # twit_list.append(rst_list)
            # df = pd.DataFrame.from_records(rst_list)
            # df.insert(0, 'title', keyword)
            # print(df)
            # twit_df.append(df)

    twitter_crawler.export_to_csv(twit_list, 'weekly_tweets')






















# print(status.text)  # tweet 내용
# print(status.created_at)  # 게시 일자
# print(status.retweet_count)  # retweet된 횟수
# print(status.favorite_count)  # 좋아요 받은 횟수
# print(type(status))

# with open('try.json', 'w') as outfile:
#     json_str = json.dumps({'salary': statuses})
#
#     json.dump(statuses, outfile)

# json_str = json.dumps(status._json, ensure_ascii=False)

# with open('try2.json', 'w') as outfile:
#     # json_str = json.dumps({'salary': statuses})
#     # json.dump(json_str, outfile)
#     outfile.write(json_str, encoding='utf-8-sig')


a=0