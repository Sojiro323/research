# -*- coding:utf-8 -*-
from mymodule import Myyaml
from connect import database
from mymodule import Mypickle
import graph_old
import utils
import recommend
import json
import os

def tuple2list(tp):
  return [t[0] for t in tp]

### Execute
if __name__ == "__main__":

  config = json.load(open("../password/config.json", 'r'))
  seeds = config["seeds"]
  path = config["path"]
  get_num = config["get_num"]
  parameter = config["parameter"]
  query_database = config["query_database"]
  queryID = config["queryID"]
  path_pattern = Myyaml.load("path")["path_com"]["39"]

  seeds_list = seeds
  start_num = len(seeds_list)

  print("queryID is {0}\n".format(queryID))
  now_seeds = database.select("select userID from {0} where queryID = \'{1}\' and (result=\'2\' or result=\'None\')".format(query_database, queryID))
  continue_seeds = database.select("select userID from {0} where queryID = \'{1}\'".format(query_database, queryID))

  #check continue
  if len(continue_seeds) > len(seeds) or os.path.exists(os.path.join(config["path"], "seeds_score_" + query_database + "_" + queryID + ".pickle")):
    seeds_list = tuple2list(now_seeds)
    seeds_score = Mypickle.load(path, "seeds_score_" + query_database + "_" + queryID)
    for seed in seeds_list:
        if seed not in seeds_score:
            graph_old.init_pickle(seed)
            utils.init_score(config, seed, seeds_score)
  #fast try
  else:
    import random
    #next_pattern = random.choice(path_pattern)
    #next_pattern = random.choice(path_pattern[0:6])
    for seed in seeds_list:database.insert(query_database, (0, seed, queryID, "None", "No"))

    for seed in seeds_list: graph_old.init_pickle(seed)

    seeds_score = utils.set_score(config, seeds)
    Mypickle.save(path, seeds_score, "seeds_score_" + query_database + "_" + queryID)

  _, next_pattern, seeds_score = utils.passcheck_continue(config,"0", seeds_score)
  while(1):
      next_pattern, seeds_list, seeds_score = recommend.recommendation(config, next_pattern, seeds_list, seeds_score)
      if int(database.select("SELECT MAX(ID) from {0} where queryID = \'{1}\'".format(query_database, queryID))[0][0]) >= get_num+len(seeds): break

  print("finish work!!!")
  #recommend.visualize(seeds_list[start_num:])
