# -*- coding:utf-8 -*-
from connect import database
from mymodule import Mypickle
import os
import recommend

### Execute
if __name__ == "__main__":

  while(1):
    print("input queryID")

    queryID = input('>>> ')
    c_flag = database.select("SELECT * from query where queryID = \'" + queryID + "\'")
    if len(c_flag) != 0: break
    else: "\ninput again!!\n\n"

  
  score = Mypickle.load("../query", "seeds_score_" + queryID)
  print("queryID:{0}\n".format(queryID))

  score_list = {}
  for seed_k, seed_v in score.items():
    for path_k, path_v in seed_v.items():
      if path_k not in score_list: score_list[path_k] = 0
      score_list[path_k] += path_v[0]/len(score) * 1.0

  for i in range(1,40):
    print("graph_num:{0} \t score:{1}".format(str(i), score_list[str(i)]))

  if os.path.isfile("../query/analysis/" + queryID + '_graph_count.pickle'):
    graph = Mypickle.load("../query/analysis/", queryID + "_graph_count.pickle")
    for i in range(1,40):
      print("graph_num:{0} \t sum:{1}".format(str(i), score_list[str(i)]))
