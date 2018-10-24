# -*- coding:utf-8 -*-
from mymodule import Mypickle
from connect import database
from connect import twitter
from operator import itemgetter
from mymodule import Myyaml
import numpy as np
import itertools
import json
import os
import sys
import random
import utils
import graph_old as graph
#from selenium import webdriver
#import webbrowser

'''global variable'''
path = "../query/"
json_path = "../password/config.json"


def recommendation(queryID, pattern, seeds, seeds_score):
  config = json.load(open(json_path, 'r'))
  query_database = config["query_database"]
  database_type = config["database"]
  get_num = config["get_num"]

  next_pattern = pattern
  match_users = []


  if database_type=="now": import graph
  else: import graph_old as graph

  for i in range(15,40):
      pattern = str(i)
      match_list, match_seeds = graph.get_match(pattern, seeds)
      if len(match_list) == 0: continue
      if len(database.select("SELECT userID from {0} where queryID = \'{1}\' and pattern = \'{2}\'".format(query_database, queryID, pattern))) >= 20: continue
      if len(match_list) != 1:
          af_match_list = ranking(pattern, match_list, match_seeds, seeds_score)
      else: af_match_list = match_list
      personal_check(pattern, af_match_list, match_seeds ,seeds_score)

  sys.exit()

  return next_pattern, seeds, seeds_score


def ranking(pattern, match_list, match_seeds, seeds_score):
  config = json.load(open(json_path, 'r'))
  parameter = config["parameter"]
  get_num = config["get_num"]
  score_type = config["score_type"]

  a = [0]*10

  seeds = seeds_score.keys()
  path_score = {}
  ranking_list = []
  count = 0
  if len(match_list) < get_num: get_num = len(match_list)-1


  for k,v in seeds_score.items():
    path_score[k] = v[pattern][0]

  for u in match_list:
      if score_type == "max":
          ss = [path_score[seed] for seed in match_seeds[u]]
          s = max(ss)
      elif score_type == "or":
          s = 1.0
          for seed in match_seeds[u]: s = s*(1-path_score[seed])
          s = 1.0-s
      elif score_type == "and":
          s = 1.0
          for seed in match_seeds[u]: s *= path_score[seed]
      elif score_type == "G":
          s = 0.0
          for seed in match_seeds[u]: s += path_score[seed]
          s = (len(match_seeds[u]) * parameter) + ((1-parameter) * s) / len(match_seeds[u])

      a[int(s)-1] += 1
      if count < get_num:
          ranking_list.append([u,s])
          count+=1
      else:
          if count == get_num:
              np_list = np.array(ranking_list)
              i = np_list.argmin(0)[1]
              count = get_num + 1
          if float(np_list[i][1]) < s:
              np_list[i] = [u,s]
              i = np_list.argmin(0)[1]

  vs = np_list.tolist()
  vs.sort(key=lambda x:x[1])
  vs.reverse()
  return vs



def personal_check(pattern, match_list, match_seeds ,seeds_score):
  config = json.load(open(json_path, 'r'))
  query_database = config["query_database"]
  queryID = config["queryID"]
  check = config["result"]
  match_users = []

  for user in match_list:
    if len(database.select('SELECT * from {0} where userID = \'{1}\' AND queryID = \'{2}\' AND pattern = \'{3}\''.format(query_database, user[0], queryID, pattern))) != 0: continue
    ans = ""
    prev = database.select('SELECT result from {0} where userID = \'{1}\''.format(query_database, user[0]))
    if len(prev) != 0:
        ans = prev[0][0]
        print("userID : {0}\nresult : {1}\n\n".format(user[0],ans))

    else:
        responce = twitter.show(user[0])
        if responce.status_code != 200:
          print("Error code: %d" %(responce.status_code))
          continue

        ress = json.loads(responce.text)
        if ress["lang"] != 'ja' or ress["protected"] == 'true': continue
        print("pattern : {0}\nscore : {1}\nmatch_seeds : {2}".format(pattern,user[1],match_seeds[user[0]]))
        print("\n\nhttps://twitter.com/intent/user?user_id=" + user[0])
        print("screen_name:{0}\nuserID:{1}\nusername:{2}\nprofile:{3}\n".format(ress["screen_name"],user[0],ress["name"],ress["description"]))

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
          database.insert(query_database, (str(int(ID[0][0]) + 1), user[0], queryID, check[input_flag], pattern))
          break
      else: print("input again!!")

    Mypickle.save(path, seeds_score, "seeds_score_" + query_database + "_" + queryID)


    murakami = len(database.select("SELECT userID from {0} where queryID = \'{1}\' and pattern = \'{2}\'".format(query_database, queryID, pattern)))
    if murakami >= 20: break
    else: print("pattern : {0}\n{1} complite!!\n".format(pattern, murakami))
