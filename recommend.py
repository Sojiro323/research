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


def recommendation(config, pattern, seeds, seeds_score):
  query_database = config["query_database"]
  database_type = config["database"]
  get_num = config["get_num"]

  if database_type=="now": import graph
  else: import graph_old as graph

  match_list, match_seeds = graph.get_match(pattern)
  print('all match_list_lengh : {0}\n\n'.format(len(match_list)))

  if len(match_list) == 0:
    _, next_pattern, seeds_score  = utils.passcheck_continue(pattern, seeds_score, thres_num = 3.0)
    #sys.exit()
    #next_pattern = random.choice(list(seeds_score[seeds[0]].keys()))
  else:
    match_list = ranking(config, pattern, match_list, match_seeds, seeds_score)
    match_users, next_pattern, seeds_score = personal_check(config, pattern, match_list, match_seeds ,seeds_score)
    seeds = seeds + match_users

    #print("\npatern next_pattern (seeds:{0}): now:{1}\nnext:{2}".format(len(seeds), pattern, next_pattern))


  return next_pattern, seeds, seeds_score


def ranking(config, pattern, match_list, match_seeds, seeds_score):
  parameter = config["parameter"]
  get_num = config["get_num"]
  score_type = config["score_type"]
  query_database = config["query_database"]
  queryID = config["queryID"]

  seeds = seeds_score.keys()
  path_score = {}
  ranking_list = []
  count = 0
  max_u = []
  max_s = 0
  max_u_2 = []
  max_s_2 = 0

  old_user = graph.tuple2list(database.select('SELECT userID from {0} where queryID = \'{1}\''.format(query_database, queryID)))

  if len(match_list) < get_num: get_num = len(match_list)-1

  for p in pattern:
      if seeds_score[p[0]]["score"][p[1]] > 1.0: path_score[p[0]+"_"+p[1]] = 1.0
      else: path_score[p[0]+"_"+p[1]] = seeds_score[p[0]]["score"][p[1]]

  for u in match_list:
      if u in old_user: continue
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
          #s = (len(match_seeds[u]) * parameter) + ((1-parameter) * s) / len(match_seeds[u])
          s = (len(match_seeds[u]) * parameter) + ((1-parameter) * s)

      if max_s < s:
          max_u_2 = max_u
          max_s_2 = max_s
          max_s = s
          max_u = [u]
      elif max_s == s:max_u.append(u)

  print("max score users : ", len(max_u))
  vs = []
  for u in max_u:vs.append([u,max_s])
  for u in max_u_2:vs.append([u,max_s_2])

  return vs

  """if count < get_num:
          ranking_list.append([u,s])
          count+=1
          print(u,s)
      else:
          if count == get_num:
              np_list = np.array(ranking_list)
              i = np_list.argmin(0)[1]
              count = get_num + 1
          if float(np_list[i][1]) < s:
              np_list[i] = [u,s]
              i = np_list.argmin(0)[1]
              print(s,u)

  vs = np_list.tolist()
  vs.sort(key=lambda x:x[1])
  vs.reverse()
  return vs"""





def personal_check(config, pattern, match_list, match_seeds ,seeds_score):
  next_pattern = pattern
  query_database = config["query_database"]
  queryID = config["queryID"]
  check = config["result"]
  match_users = []

  for user in match_list:
    if len(database.select('SELECT * from {0} where userID = \'{1}\' AND queryID = \'{2}\''.format(query_database, user[0], queryID))) != 0:
        print("checked once")
        continue
    ans = ""
    prev = database.select('SELECT result from {0} where userID = \'{1}\''.format(query_database, user[0]))
    print("pattern : {0}\nmatch_seeds : {1}\nscore : {2}\n".format(pattern,match_seeds[user[0]],user[1]))
    if len(prev) != 0:
        ans = prev[0][0]
        print("userID : {0}\nresult : {1}\n\n".format(user[0],ans))

    else:
        responce = twitter.show(user[0])
        if responce.status_code != 200:
          print("Error code: %d" %(responce.status_code))
          continue

        ress = json.loads(responce.text)
        #if ress["lang"] != 'ja' or ress["protected"] == 'true': continue
        print("https://twitter.com/intent/user?user_id=" + user[0])
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
          database.insert(query_database, (str(int(ID[0][0]) + 1), user[0], queryID, check[input_flag], "0"))
          break
      else: print("input again!!")

    print("{0} people checked!!\n\n".format(int(ID[0][0])+1))
    #p_com = utils.update_pattern(seeds_score.keys(), user[0])
    p_com = match_seeds[user[0]]
    #print("match pattern is\n{0}".format(p_com))
    seeds_score = utils.update_score(config, input_flag, p_com, seeds_score, user[0])

    if input_flag == "true":
      graph.init_pickle(user[0])
      seeds_score = utils.init_score(config, user[0], seeds_score)
      match_users.append(user[0])

    Mypickle.save(path, seeds_score, "seeds_score_" + query_database + "_" + queryID)

    continue_flag, next_pattern, seeds_score = utils.passcheck_continue(config, pattern, seeds_score)
    if continue_flag is True or (continue_flag is False and input_flag == "true"): break

  return match_users, next_pattern, seeds_score
