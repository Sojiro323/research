# -*- coding:utf-8 -*-
from mymodule import Myyaml
from connect import database
from connect import twitter
from mymodule import Mypickle
from connect import twitter
import graph_old
import utils
import recommend
import json
import os


def basic_pass1(seed):

  if not os.path.isfile(DIR + seed + '_1.pickle'):
      friends = update("friends_only",seed, seed)
      Mypickle.save(DIR, friends, seed + '_1')
  else:
      friends = Mypickle.load(DIR, seed + '_1')

  return friends

def basic_pass2(seed):

  if not os.path.isfile(DIR + seed + '_2.pickle'):
      followers = update("followers_only",seed, seed)
      Mypickle.save(DIR, followers, seed + '_2')
  else:
      followers = Mypickle.load(DIR, seed + '_2')

  return followers


def basic_pass7(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_7.pickle'):
    _1 = Mypickle.load(DIR, seed + '_1')
    _2 = Mypickle.load(DIR, seed + '_2')
    match_list = list(set(_1) & set(_2))
    Mypickle.save(DIR, match_list, seed + '_7')
  else:
    match_list = Mypickle.load(DIR, seed + '_7')

  return match_list

def basic_pass_tweet(seed):

  keyword = "オーストラリアドル"
  count = 100
  match_list = twitter.tweets(keyword, count)

  return match_list


def tuple2list(tp):
  return [t[0] for t in tp]

### Execute
if __name__ == "__main__":
  DIR = '../pickle/positive_old/'

  config = json.load(open("../password/config.json", 'r'))
  seeds = config["seeds"]
  path = config["path"]
  get_num = config["get_num"]
  parameter = config["parameter"]
  query_database = config["query_database"]
  queryID = config["queryID"]
  check = config["result"]
  path_pattern = Myyaml.load("path")["path_com"]["39"]

  seeds_list = seeds
  start_num = len(seeds_list)

  print("queryID is {0}\n".format(queryID))
  for seed in seeds_list:database.insert(query_database, (0, seed, queryID, "None", "No"))

  num =  {'friend':'1', 'follower':'2','mutual':'7','tweet':'_tweet'}
  for n in num.keys():
      if n in queryID: method = num[n]

  ans_list = []
  tweets = {}
  for seed in seeds:
      temp_list = []
      if method in 'tweet':
          responce = eval('basic_pass'+ method)(seed)
          ress = json.loads(responce.text)["statuses"]
          for res in ress:
              temp_list.append(res["user"]["id_str"])
              tweets[res["user"]["id_str"]] = res["text"]
      else:
          temp_list = eval('basic_pass'+ method)(seed)


      ans_list = list(set(ans_list)|set(temp_list))
  for user in ans_list:
    if len(database.select('SELECT * from {0} where userID = \'{1}\' AND queryID = \'{2}\''.format(query_database, user, queryID))) != 0:
        print("checked once")
        continue
    ans = ""
    prev = database.select('SELECT result from {0} where userID = \'{1}\''.format(query_database, user))
    if len(prev) != 0:
        ans = prev[0][0]
        print("userID : {0}\n\n".format(user))

    else:
        responce = twitter.show(user)
        if responce.status_code != 200:
          print("Error code: %d" %(responce.status_code))
          continue

        ress = json.loads(responce.text)
        if ress["lang"] != 'ja' or ress["protected"] == 'true': continue
        print("https://twitter.com/intent/user?user_id=" + user)
        print("screen_name:{0}\nuserID:{1}\nusername:{2}\nprofile:{3}\n".format(ress["screen_name"],user,ress["name"],ress["description"]))
        if method in 'tweet':print(tweets[user])

    #webbrowser_flag = False
    while(1):
      if len(ans) == 0:
          print("input true or false or half (help = h)")
          input_flag = input('>>>  ')
      else:
          for k,v in check.items():
              if ans == v: input_flag=k

      '''if input_flag == "h":
        driver = webdriver.Chrome("./chromedriver")
        driver.get(":)
        webbrowser_flag = True

      elif input_flag == "y" or input_flag == "n":
        y_n[user] = input_flag
        if webbrowser_flag: driver.close()
        break'''

      if input_flag in check:
          ID = database.select("SELECT MAX(ID) from {0} where queryID = \'{1}\'".format(query_database, queryID))
          database.insert(query_database, (str(int(ID[0][0]) + 1), user, queryID, check[input_flag], "0"))
          break
      else: print("input again!!")

    print("{0} people checked!!\n\n".format(int(ID[0][0])+1))
    if len(database.select('SELECT * from {0} where queryID = \'{1}\''.format(query_database, queryID))) >= get_num+len(seeds): break
