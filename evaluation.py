# -*- coding:utf-8 -*-
from connect import database
import plot
import os
import math
import pickle
import csv
import json

'''global variable'''


def get_ideal(config):

    query_database = config["query_database"]
    get_num = config["get_num"]

    TRUE = []
    HALF = []
    FALSE = []
    ideal_list = []
    ideal_list_binary = []

    querys = database.select("SELECT DISTINCT queryID from {0}".format(query_database))
    for query in querys:
        q = query[0]
        if "unknown" in q: continue
        true = database.select("SELECT userID from {0} where queryID = \'{1}\' and result = '2'".format(query_database, q))
        half = database.select("SELECT userID from {0} where queryID = \'{1}\' and result = '1'".format(query_database, q))
        false = database.select("SELECT userID from {0} where queryID = \'{1}\' and result = '0'".format(query_database, q))

        for t in true:
            if t[0] not in TRUE: TRUE.append(t[0])
        for t in half:
            if t[0] not in HALF: HALF.append(t[0])
        for t in false:
            if t[0] not in FALSE: FALSE.append(t[0])

    ideal_list = [2]*len(TRUE) + [1]*len(HALF) + [0]*len(FALSE)
    ideal_list_binary = [1]*len(TRUE) + [0]*(len(ideal_list)-len(TRUE))
    return ideal_list[:get_num], ideal_list_binary[:get_num]


def nDCG(queryID,ideal,config):

    query_database = config["query_database"]

    rec_list = []
    ans_list = []
    SQL = database.select("SELECT ID, result from {0} where queryID = \'{1}\' and result <> 'None' order by ID".format(query_database, queryID))
    for user in SQL:
      if int(user[0]) <= len(ideal): rec_list.append(user[1])
    if len(rec_list) < len(ideal):rec_list+=[0]*(len(ideal)-len(rec_list))
    molecule = DCG(rec_list)
    denominator = DCG(ideal)

    for m,d in zip(molecule, denominator): ans_list.append(m/d)

    return ans_list, rec_list

def nDCG_binary(queryID,ideal,config):
    query_database = config["query_database"]

    rec_list = []
    ans_list = []
    SQL = database.select("SELECT ID, result from {0} where queryID = \'{1}\' and result <> 'None' order by ID".format(query_database, queryID))
    for user in SQL:
      if int(user[0]) <= len(ideal):
          if user[1] == "1": rec_list.append("0")
          elif user[1] == "2": rec_list.append("1")
          else: rec_list.append(user[1])
    if len(rec_list) < len(ideal):rec_list+=[0]*(len(ideal)-len(rec_list))
    molecule = DCG(rec_list)
    denominator = DCG(ideal)
    for m,d in zip(molecule, denominator): ans_list.append(m/d)

    return ans_list, rec_list

def DCG(users):

  ans = []

  for i, user in enumerate(users):
      if len(ans) == 0: ans.append((2**int(user)-1)/math.log2(1+(i+1)))
      else: ans.append(ans[i-1] + (2**int(user)-1)/math.log2(1+(i+1)))

  return ans


def AP(rec_list,k):

  ans = 0.0
  p_index = []
  for i, user in enumerate(rec_list):
    if i == k:break
    if int(user) == 2 or int(user) == 1:
      p_index.append(i)
      ans += len(p_index) / (i+1) * 1.0

  if len(p_index) == 0: ans = 0
  else: ans = ans /len(p_index) * 1.0

  return ans, p_index


if __name__ == "__main__":

  config = json.load(open("../password/config_evaluate.json", 'r'))
  ideal_list,ideal_list_binary = get_ideal(config)
  print("ideal_list : \n{0}".format(ideal_list))
  ks = [i+1 for i in range(config["get_num"])]

  plot_name = []
  plot_score = {}

  for q in config["querys"]:

      '''calucrate score'''
      nDCG_score, rec_list = nDCG(q,ideal_list,config)
      #nDCG_score, rec_list = nDCG_binary(q,ideal_list_binary,config)
      for qu in config["qs"].keys():
          if qu in q:
              plot_score[config["qs"][qu]] = nDCG_score
              plot_name.append(config["qs"][qu])



  plot.image(plot_score,ks,config["img_name"],plot_name,config["title"],config["xlabel"],config["ylabel"])

  for k,v in plot_score.items():
      print("{0}\n10:{1}\n30:{2}\n50:{3}\n100:{4}\n".format(k,v[9],v[29],v[49],v[99]))
