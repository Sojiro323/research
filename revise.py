from connect import database
from connect import twitter
from mymodule import Mypickle
import utils
import os
import json

DIR = '../pickle/positive_old/'
path = "../query/"


def tuple2list(tp):
  return [t[0] for t in tp]

def init_pickle(seed):
    for i in range(1,8):
        #if os.path.isfile(DIR + seed + '_' + str(i) + '.pickle') == False or os.path.isfile(DIR + seed + '_' + str(i) + '_app.pickle') == False:#friend
            target = Mypickle.load(DIR, seed + '_' + str(i) + '_app')
            target = tuple2list(target)
            Mypickle.save(DIR, target, seed + '_' + str(i) + '_app')

#init_pickle("149340795")

seeds_score = Mypickle.load(path, 'seeds_score_australia_or_new')
score_list = {}
for seed_k, seed_v in seeds_score.items():
    print(seed_k)
    for path_k  in sorted(seed_v.keys()):
         #if path_k == "16":
         print(path_k,seed_v[path_k])
         if path_k not in score_list: score_list[path_k] = 0
         score_list[path_k] += seed_v[path_k][0]/len(seeds_score) * 1.0

print("sum list")
for k  in sorted(score_list.keys()):
    print(k,score_list[k])
