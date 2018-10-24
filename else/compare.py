# -*- coding:utf-8 -*-
from connect import database
from connect import twitter
from mymodule import Mail
import graph
import json
import sys
import itertools
import urllib.parse


'''global variable'''
get_num = 30

methods = ["friend", "follower", "mutual", "tweet" , "profile"]
path_index = {"friend" : "1", "follower" : "2", "mutual" : "7"}
judg_dic = {"true" : "2", "false" : "0", "half" : "1"}

def input_database(judg, queryID, user):

  ID = database.select("SELECT MAX(ID) from query where queryID = \'" + queryID + "\'")[0][0]
  if ID is None: ID = 0
  database.insert("query", (ID + 1, user, queryID, judg_dic[judg]))
  print("{0} people checked!!".format(ID + 1))



def ranking(seeds, match_list, match_seeds):

  ranking_list = []
  combinations = []

  for t in range(len(seeds), 0, -1):
    temp = list(itertools.combinations(seeds, t))
    for te in temp: combinations.append(list(te))

  while(len(combinations) > 0):
    c = combinations.pop(0)
    for match in match_list[:]:
      if len(set(c).symmetric_difference(match_seeds[match])) == 0:
        ranking_list.append(match)
        match_list.remove(match)
    if len(c) == len(seeds): print("best combinations : {0}".format(len(ranking_list)))

  return ranking_list


def tweet(keyword, count):

  match_list = []
  tweets = []

  responce = twitter.tweets(keyword, count)

  limit = int(responce.headers['x-rate-limit-remaining']) if 'x-rate-limit-remaining' in responce.headers else 0
  if responce.status_code != 200:
    if (responce.status_code == 401) or (responce.status_code == 404): return None
    print("Error code: %d" %(responce.status_code))
    Mail.sendmail("Error code: %d" %(responce.status_code))
    sys.exit()

  ress = json.loads(responce.text)["statuses"]
  for res in ress:
      match_list.append(res["user"]["id_str"])
      tweets.append(res['text'])

  return match_list, tweets


def user(keyword, count):

  match_list = []
  tweets = []
  if count // 20 == 0: pages = 1
  elif count // 20 > 0 and count % 20 == 0: pages = count // 20
  else: pages = (count // 20) + 1

  keyword = urllib.parse.quote(keyword)

  for i in range(pages):

    responce = twitter.users(keyword, i+1, 20)

    limit = int(responce.headers['x-rate-limit-remaining']) if 'x-rate-limit-remaining' in responce.headers else 0
    if responce.status_code != 200:
      if (responce.status_code == 401) or (responce.status_code == 404): return None
      print("Error code: %d" %(responce.status_code))
      Mail.sendmail("Error code: %d" %(responce.status_code))
      sys.exit()

    ress = json.loads(responce.text)
    for res in ress:
      if len(match_list) < count: match_list.append(res["id_str"])

  return match_list


if __name__ == "__main__":

  while(1):
    print("input queryID")

    queryID = input('>>> ')

    if len(database.select("SELECT * from query where queryID = \'" + queryID + "\'")) != 0: break
    else: print("\ninput again!!\n\n")

  SQL = database.select("SELECT userID from query where queryID = \'" + queryID + "\'" + "and ID = \'0\'")

  seeds = [s[0] for s in SQL]

  print("seeds : {0}".format(seeds))

  match_user = []


  while(1):
    print("input using comparative method : {0}".format(methods))

    method = input('>>> ')

    if method in methods[:3]: break
    elif method in methods[3:]:
      print("input number of users")
      count = int(input('>>> '))
      print("input keyword")
      keyword = input('>>> ')
      break
    else: "\ninput again!!\n\n"

  while(1):
    print("input using database : old or new")

    d = input('>>> ')

    if d == "new":
      d_flag = True
      break
    elif d == "old":
      d_flag = False
      break
    else: "\ninput again!!\n\n"


  if method in methods[:-2]:
    if d_flag == False: import graph_old as graph
    match_list, match_seeds = graph.get_match(path_index[method], seeds)
    match_user_profile = []
    #match_list = ranking(seeds, match_list, match_seeds)
  elif method == "tweet":
    match_list, _ = tweet(keyword, count)
  #elif:
  #  match_list = user(keyword, method)

  queryID = method + "_" + queryID

  print("len(match_list) = {0}".format(len(match_list)))

  for user in match_list:

    if len(database.select("SELECT * from query where queryID = \'" + queryID + "\'" + "and userID = \'" + user + "\'")) != 0: continue

    responce = twitter.show(user)
    if responce.status_code != 200:
      print("Error code: %d" %(responce.status_code))
      sys.exit()

    ress = json.loads(responce.text)
    if ress["lang"] != 'ja': continue
    print("\n\nhttps://twitter.com/intent/user?user_id=" + user)
    print("screen_name:{0}\nuserID:{1}\nusername:{2}\nprofile:{3}\n".format(ress["screen_name"],user,ress["name"],ress["description"]))
    if method == "tweet": print("tweets\n{0}".format(_[match_list.index(user)]))

    while(1):
      print("\ninput : {0} or skip".format(judg_dic.keys()))
      judg = input('>>>  ')
      if judg == 'skip': break

      if judg in judg_dic:
        if len(database.select("SELECT * from query where queryID = \'" + queryID + "\'" + "and userID = \'" + user + "\'")) == 0:
          input_database(judg, queryID, user)
        break
      else: print("\ninput again!!\n\n")

    if judg == "true":
      match_user.append(user)
      print("now match_user : {0}".format(match_user))

    if len(match_user) == get_num: break

  print("end comparative method!!")
