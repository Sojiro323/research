from requests_oauthlib import OAuth1Session
from requests.exceptions import ConnectionError
import datetime
import time
from . import database


def create_oath_session(api_name):

    ID = limit_check(api_name)
    import yaml
    f = open('../password/twitterAPI/' + str(ID) + '.yml', 'r+')
    oath_key_dict = yaml.load(f)
    oath = OAuth1Session(
    oath_key_dict["consumer_key"],
    oath_key_dict["consumer_secret"],
    oath_key_dict["access_token"],
    oath_key_dict["access_token_secret"]
    )

    return oath, ID

def show(user_ID):

    url = "https://api.twitter.com/1.1/users/show.json?"
    params = {
        "user_id": user_ID
        }
    oath, ID = create_oath_session("show")
    try:
        responce = oath.get(url, params = params)
        insert2database(ID, "show", responce)
    except ConnectionError as e:
        return show(user_ID)
    return responce


def lookup(users_ID):
    url = "https://api.twitter.com/1.1/users/lookup.json?"
    params = {
        "user_id": users_ID,
        "stringify_ids": "true"
        }
    oath, ID = create_oath_session("lookup")
    try:
        responce = oath.post(url, params = params)
        insert2database(ID, "lookup", responce)
    except ConnectionError as e:
        return lookup(users_ID)
    return responce



def followers(userID):

    url = "https://api.twitter.com/1.1/followers/ids.json?"
    params = {
        "user_id": userID,
        "stringify_ids": "true"
        }
    oath, ID = create_oath_session("followers")
    try:
        responce = oath.get(url, params = params)
        #responce = oath.post(url, params = params)
        insert2database(ID, "followers", responce)
    except ConnectionError as e:
        return followers(userID)
    return responce


def friends(userID):
    url = "https://api.twitter.com/1.1/friends/ids.json?"
    params = {
        "user_id": userID,
        "stringify_ids": "true"
        }
    oath, ID = create_oath_session("friends")
    try:
        responce = oath.get(url, params = params)
        #responce = oath.post(url, params = params)
        insert2database(ID, "friends", responce)
    except ConnectionError as e:
        return friends(userID)
    return responce


def tweets(keyword, count):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
        "q": keyword,
        "lang": "ja",
        "result_type": "mixed",
        "count": count,
        "result_type":"mixed"
        }
    oath, ID = create_oath_session("tweets")
    try:
        responce = oath.get(url, params = params)
        insert2database(ID, "tweets", responce)
    except ConnectionError as e:
        return tweet(userID)
    return responce


def users(keyword, page, count):
    url = "https://api.twitter.com/1.1/users/search.json?"
    params = {
        "q": keyword,
        "page": page,
        "count": count
        }
    oath, ID = create_oath_session("users")
    try:
        responce = oath.get(url, params = params)
        insert2database(ID, "users", responce)
    except ConnectionError as e:
        return tweet(userID)
    return responce


def insert2database(ID, api_name, responce):
    limit = responce.headers['x-rate-limit-remaining'] if 'x-rate-limit-remaining' in responce.headers else 0
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    database.update('api_limit', ((ID, str(limit), now, api_name)))


def limit_check(api_name):

    SQLs = database.select('select id, limited, last_use from api_limit where api_name = \'' + api_name + '\'')

    now = time.strftime('%Y-%m-%d %H:%M:%S')
    now_time = datetime.datetime(int(now[0:4]),int(now[5:7]),int(now[8:10]),int(now[11:13]),int(now[14:16]),int(now[17:19]))

    ID = ""

    for SQL in SQLs:
        limit = SQL[1]
        last_use = SQL[2]
        last_time = datetime.datetime(int(last_use[0:4]),int(last_use[5:7]),int(last_use[8:10]),int(last_use[11:13]),int(last_use[14:16]),int(last_use[17:19]))
        delta = now_time - last_time
        if int(limit) > 0 or delta.total_seconds() > 900:
            ID = SQL[0]
            break

    if ID == "":
        print("start sleep")
        SQLs = database.select('select id, last_use from api_limit where api_name = \'' + api_name + '\'')
        recent = datetime.datetime(2020,1,1,00,00,00)
        for SQL in SQLs:
          use = SQL[1]
          temp = datetime.datetime(int(use[0:4]),int(use[5:7]),int(use[8:10]),int(use[11:13]),int(use[14:16]),int(use[17:19]))
          if recent > temp:
            recent = temp
            ID = SQL[0]
        delta = (now_time - recent).total_seconds()
        if delta > 900: return ID
        print("delta.total_seconds : {0}".format(delta))
        time.sleep(900 - delta)

    return ID


def join_params(params_list,*,count = 0):

    lookup = ""

    if count == 0:
        for param in params_list:
            lookup = lookup + "," + param
        lookup = lookup[1:]
        return lookup


    counts = [0,0]
    return_list = []

    for param in params_list:
        lookup = lookup + "," + param
        counts[0]+= 1
        if counts[0] == count:
            lookup = lookup[1:]
            return_list.append(lookup)
            counts[0] = 0
            counts[1]+= 1
            lookup = ""

    if len(params_list) < count: return [lookup]
    if return_list[-1] == "": return_list.pop()

    return return_list
