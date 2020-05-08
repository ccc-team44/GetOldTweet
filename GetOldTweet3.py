import GetOldTweets3 as oldTweet
import couchdb
import json


# fetch old tweets based on criterion
def get_oldTweets(query, geo_code, since_time, until_time):
    print(query, geo_code, since_time, until_time)
    search_criteria = oldTweet.manager.TweetCriteria().setQuerySearch(query).setNear(geo_code).setWithin(
        '50km').setSince(since_time).setUntil(until_time)
    tweets = oldTweet.manager.TweetManager.getTweets(search_criteria)
    return tweets


def set_database(name):
    try:
        host = 'http://admin:1111@127.0.0.1:5984'
        couch = couchdb.Server(host)
    except Exception as e:
        print('error', e)
    try:
        database = couch[name]
        return database
    except:
        print("Creating database", name)
        database = couch.create(name)
        return database


# save tweet to database
def save_tweet(name, data):
    database = set_database(name)
    try:
        database.save(data)
    except Exception as e:
        print('error,', e)


def to_database(tweets, city, admin, country):
    for each in tweets:
        tweet_dict = {'id': each.id, 'date': str(each.date), 'geo': each.geo, 'hashtags': each.hashtags, 'text': each.text,
                      'retweets': each.retweets, 'city': city, 'admin': admin, 'country': country}
        name = '%s_tweets' % admin.lower()
        save_tweet(name, tweet_dict)


def main():
    with open('au.json', 'r') as json_file:
        geo_code = json.load(json_file)
        geo_code = geo_code[2:3]
    since_time, until_time = '2019-09-01', '2020-04-30'
    queries = ['aupol', 'scomo', 'Scott Morrison']

    for city in geo_code:
        city_geo = '%s, %s' % (city['lat'], city['lng'])
        for query in queries:
            old_tweets = get_oldTweets(query, city_geo, since_time, until_time)
            print(len(old_tweets))
            to_database(old_tweets, city['city'], city['admin'], city['country'])


if __name__ == '__main__':
    main()
