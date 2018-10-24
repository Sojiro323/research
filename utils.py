import random
import json
from mymodule import Myyaml
from mymodule import Mypickle
from connect import database
import graph_old

def tuple2list(tp):
  return [t[0] for t in tp]

def set_score(config, seeds):
  start_score = config["start_score"]


  seeds_score = {}

  path_pattern = Myyaml.load("path")["path_com"]["39"]
  precision_score = {p:list(start_score) for p in path_pattern}  #[precision, good, bad]

  for user in seeds:
      print("set score : {0}".format(user))
      user_score = {}
      user_score["precision"] = dict(precision_score)
      temp = list(seeds)
      temp.remove(user)
      print("initscore : molecule")
      user_score["molecule"] = get_molecule(user, temp)
      print("initscore : denominator")
      user_score["denominator"] = get_denominator(user)
      #user_score["denominator"] = get_denominator(user, len(temp))
      user_score["score"] = get_score(config, user_score)
      user_score["find"] = {p:list([]) for p in path_pattern}

      seeds_score[user] = user_score

  return seeds_score

def init_score(config, user, seeds_score):
  start_score = config["start_score"]

  path_pattern = Myyaml.load("path")["path_com"]["39"]
  user_score = {}
  count = len(seeds_score)

  precision_score = {}
  print("update old seeds molecule")
  for seed_k,seed_v in seeds_score.items():
    seeds = list(seeds_score.keys())
    seeds.remove(seed_k)
    seed_k_molecule = get_molecule(seed_k, [user])
    for m_k,m_v in seed_k_molecule.items():
        if int(m_v[0]) == 1:
            seeds_score[seed_k]["molecule"][m_k][0] = ((len(seeds_score[seed_k]["molecule"][m_k])-1)*1.0)/(len(seeds)+1)
            seeds_score[seed_k]["molecule"][m_k].append(user)
            seeds_score[seed_k]["score"] = get_score(config, seeds_score[seed_k])
    for path_k, path_v in seed_v["precision"].items():
        if path_k not in precision_score:
            precision_score[path_k] = list(start_score)
            precision_score[path_k][0] = 0
        precision_score[path_k][0] += path_v[0]*1.0/count

  user_score["precision"] = dict(precision_score)
  seeds = list(seeds_score.keys())
  print("initscore : molecule")
  user_score["molecule"] = get_molecule(user, seeds)
  print("initscore : denominator")
  #user_score["denominator"] = get_denominator(user, len(seeds))
  user_score["denominator"] = get_denominator(user)
  user_score["score"] = get_score(config, user_score)
  user_score["find"] = {p:list([]) for p in path_pattern}

  seeds_score[user] = user_score


  return seeds_score

def get_molecule(user, seeds, count=100):
    molecule = {str(i):[0,0] for i in range(1,40)}
    user_friends = database.select('select friendID from friend_graph where userID = \'' + user + '\'')
    user_friends = tuple2list(user_friends)
    user_followers = database.select('select followerID from follower_graph where userID = \'' + user + '\'')
    user_followers = tuple2list(user_followers)

    for seed in seeds:
        print(seed)
        p = []
        check_path = set([])
        if seed in user_friends and seed in user_followers: p+=["1","2"]
        elif seed in user_friends: p+=["1"]
        elif seed in user_followers: p+=["2"]

        target_friends = database.select('select friendID from friend_graph where userID = \'' + seed + '\'')
        target_friends = set(tuple2list(target_friends))
        target_followers = database.select('select followerID from follower_graph where userID = \'' + seed + '\'')
        target_followers = set(tuple2list(target_followers))
        if len(set(user_friends)|set(user_followers)) > len(target_friends|target_followers): nodes = list(set(target_friends)|set(target_followers))
        else: nodes = list(set(user_friends)|set(user_followers))
        for node in nodes:
            p_t = p
            if node in user_friends and node in target_friends: p_t.append("3")
            if node in user_followers and node in target_followers: p_t.append("4")
            if node in user_friends and node in target_followers: p_t.append("5")
            if node in user_followers and node in target_friends: p_t.append("6")
            for k,v in Myyaml.load("path")["basic_path_com"].items():
                if set(v) == set(p_t):
                    molecule[k][1]+=1
                    check_path.add(k)

        for l in list(check_path):
            molecule[l][0]+=1
            molecule[l].append(seed)

    for k,v in molecule.items():
        if v[0] != 0: molecule[k][0] = v[0]/len(seeds)
        else : molecule[k][0] = 1.0/(count*2)

    return molecule


def get_denominator(user, count=100):
    ans = set([])

    DIR = '../pickle/positive_old/'
    for i in range(1,40):
        t = Mypickle.load(DIR, user + '_' + str(i))
        if isinstance(t, list): ans = ans|set(t)
        else: ans = ans|set(t.keys())

    seeds = random.sample(list(ans), count)
    del ans
    return get_molecule(user, seeds)

def get_precision(precision, denominator):
    count = 0
    ans = 0.0
    for i in range(1,40): count+=denominator[str(i)][1]
    for i in range(1,40): ans += (precision[str(i)][0]*denominator[str(i)][1]*1.0)/count

    return ans


def get_score(config, user_score):
    start_score = config["start_score"]
    dic = {}
    precision = get_precision(user_score["precision"], user_score["denominator"])
    for i in range(1,40):
        if user_score["precision"][str(i)][1] == start_score[1] and user_score["precision"][str(i)][2] == start_score[2] and user_score["precision"][str(i)][3] == start_score[3]:
            dic[str(i)] = (precision*user_score["molecule"][str(i)][0])/user_score["denominator"][str(i)][0]

        else:
            dic[str(i)] = user_score["precision"][str(i)][0]
    return dic

"""
def update_pattern(pattern, match_seeds, target_user):

  path_com = Myyaml.load("path")["path_com"]
  add_pattern = []
  for k,v in path_com.items():
    if k == pattern: continue
    if pattern in v: add_pattern.append(k)
  return add_pattern_check(pattern, add_pattern,match_seeds, target_user)
"""

def update_score(config, flag, p_com, seeds_score, userID):

  #match_seeds = list(set(match_seeds))
  #print("UPDATE SCORE : {0}".format(match_seeds))
  for seed, seed_score in seeds_score.items():
      for i,v in seed_score["precision"].items():
          pat = seed+"_"+str(i)
          if pat in p_com:
              if flag == "true":
                  seeds_score[seed]["precision"][i][1] += 1
                  seeds_score[seed]["find"][i].append(userID)
              elif flag == "false": seeds_score[seed]["precision"][i][3] += 1
              else: seeds_score[seed]["precision"][i][2] += 1
              seeds_score[seed]["precision"][i][0] = (seeds_score[seed]["precision"][i][1] * 1.0 + seeds_score[seed]["precision"][i][2] * 0.5) / (seeds_score[seed]["precision"][i][1] + seeds_score[seed]["precision"][i][2] + seeds_score[seed]["precision"][i][3])
      seeds_score[seed]["score"] = get_score(config, seeds_score[seed])
  return seeds_score

def update_pattern(seeds, target_user):
    l = []
    for seed in seeds:
        print("update pattern check : {0}".format(seed))
        for i in range(1,40):
            users, _ = graph_old.get_match([[seed,str(i)]])
            del _
            if target_user in users: l.append(seed+"_"+str(i))
    return l

def add_pattern_check(pattern, add_pattern, match_seeds, target_user):
    add_dic={}
    basic_pass_com = Myyaml.load("path")["basic_path_com"]
    for seed in match_seeds:
        add_dic[seed] = [pattern]
        for p in add_pattern:
            #if target_user in eval('basic_pass'+str(p))(seed): add_dic[seed].append(p)
            if target_user in graph_old.approximate_path(seed, basic_pass_com[p]):
                print("True")
                add_dic[seed].append(p)
            else: print("False")
    return add_dic

def check_pickle_rest(config, seed, pattern):
    DIR = '../pickle/positive_old/'
    query_database = config["query_database"]
    queryID = config["queryID"]

    min_needs = Myyaml.load("path")["path_com"][str(pattern)]
    min_needs.remove(str(pattern))
    if min_needs is None: min_needs = []
    max_needs = []
    for k,v in Myyaml.load("path")["path_com"].items():
      if k == pattern: continue
      if pattern in v: max_needs.append(k)

    users = graph_old.different_approximate_path(pattern, seed, min_needs, max_needs)
    for user in users:
        if len(database.select('SELECT * from {0} where userID = \'{1}\' AND queryID = \'{2}\''.format(query_database, user, queryID))) == 0: return True
    print("{0} is finish (seed:{1}) len{2}".format(pattern, seed, len(users)))
    return False

def passcheck_continue(config, pattern, seeds_score, thres_num = 2.0):

  """
  score_list = {}
  for seed_k, seed_v in seeds_score.items():
    for path_k, path_v in seed_v.items():
      if path_k not in score_list: score_list[path_k] = 0
      score_list[path_k] += path_v[0]/len(seeds_score) * 1.0

  max_val = max(score_list.values())
  path_pattern = list(score_list.keys())
  keys_of_max_val = [key for key in score_list if score_list[key] == max_val]

  print("now graph pattern score\n {0}\n\n".format(score_list))

  if pattern in keys_of_max_val and len(keys_of_max_val) != len(path_pattern):
    next_pattern = pattern
  elif len(keys_of_max_val) == len(path_pattern):
    next_pattern = random.choice(path_pattern)
  else:
    next_pattern = random.choice(list(keys_of_max_val))

  if next_pattern == pattern: return False, next_pattern
  else: return True, next_pattern
  """

  ans_list = []
  thres = len(seeds_score)*thres_num
  ranking_list=[]
  conti_count = 0.0
  for seed_k, seed_v in seeds_score.items():
    for path_k, path_v in seed_v["score"].items():
        ranking_list.append([seed_k,path_k,path_v])

  ranking_list.sort(key=lambda x:x[2])
  ranking_list.reverse()
  #print(len(ranking_list))
  for i, r in enumerate(ranking_list):
      #if r[2] >= 1.0: ans_list.append([r[0],r[1]])
      if len(ans_list) >= thres: break
      else:
          if check_pickle_rest(config, r[0], r[1]): ans_list.append([r[0],r[1]])
          else: seeds_score[r[0]]["score"][str(r[1])] = 0.0


  print("ranking_check\nold_ranking:{0}\nnew_ranking:{1}".format(pattern, ans_list))
  return True, ans_list, seeds_score


def visualize(answer_list):

  print("visualize")
  print(answer_list)
