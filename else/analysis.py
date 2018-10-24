# -*- coding:utf-8 -*-
from connect import database
from mymodule import Mypickle
import os
import numpy as np

path_com = {
1:[1],
2:[2],
3:[3],
4:[4],
5:[5],
6:[6],
7:[1,2],
8:[2,3],
9:[1,3],
10:[3,5],
11:[3,6],
12:[2,4],
13:[1,4],
14:[4,5],
15:[4,6],
16:[2,5],
17:[1,5],
18:[2,6],
19:[1,6],
20:[1,2,3],
21:[1,2,4],
22:[1,2,5],
23:[1,2,6],
24:[3,4,5,6],
25:[2,3,5],
26:[1,3,5],
27:[2,3,6],
28:[1,3,6],
29:[2,4,5],
30:[1,4,5],
31:[2,4,6],
32:[1,4,6],
33:[1,2,3,5],
34:[1,2,3,6],
35:[1,2,4,5],
36:[1,2,4,6],
37:[2,3,4,5,6],
38:[1,3,4,5,6],
39:[1,2,3,4,5,6]
}



def check(node):

  for k, v in node.items():
    if len(v) != 0: return True
  return False



def set_check(node, opponent, p_dic, path_set):

  users = {}

  for k, v in node.items():
    if k == "friend" or k == "follower": continue
    for i, u in enumerate(v[:]):
      if u[1] == opponent:
        if u[0] not in users: users[u[0]] = path_set
        if p_dic[k]  not in users[u[0]]: users[u[0]].append(p_dic[k])
        v = [a for a in v if u != a]


  return users.values()



if __name__ == "__main__":

  while(1):
    print("input queryID")

    queryID = input('>>> ')

    if len(database.select("SELECT * from query where queryID = \'" + queryID + "\'")) != 0: break
    else: print("\ninput again!!\n\n")

  while(1):
    print("input using database : old or new")

    d = input('>>> ')

    if d == "new":
      import graph
      break
    elif d == "old":
      import graph_old as graph
      break
    else: "\ninput again!!\n\n"

  SQL_seeds = database.select("SELECT userID from query where queryID = \'" + queryID + "\'" + "and ID = \'0\'")
  SQL_match = database.select("SELECT userID from query where queryID LIKE \'%" + queryID + "%\'" + "and result =  \'2\'")


  seeds = [s[0] for s in SQL_seeds]
  match = list(set([s[0] for s in SQL_match]))

  node2node = {} #{userID:{friend:...,follower:...,friend2friend:...,friend2follower:...,follower2friend:...,follower2follower:...,}}
  nodeofflags = {}

  path = "../query/analysis/"
  pickle_path = "../pickle/positive/"
  doc_name = queryID + "_node2node"
  if os.path.exists(path + doc_name + ".pickle"): node2node = Mypickle.load(path, doc_name)
  print(len(node2node))

  print("seeds : {0}".format(seeds))
  print("match : {0}".format(match))

  for user in seeds + match:

    if user in node2node.keys(): continue

    node2node[user] = {}
    if user not in nodeofflags: nodeofflags[user] = [True, True]

    print("\nuser : {0} start".format(user))

    if nodeofflags[user][0] and nodeofflags[user][1]:
      friends, followers = graph.update("all", user, user)
      node2node[user]["friend"] = friends
      node2node[user]["follower"] = followers
      nodeofflags[user][0] = False
      nodeofflags[user][1] = False
    elif nodeofflags[user][0] == False and nodeofflags[user][1] == False:
      friends = node2node[user]["friend"]
      followers = node2node[user]["follower"]
    elif nodeofflags[user][0] == False:
      followers = graph.update("followers_only", user)
      node2node[user]["follower"] = followers
      nodeofflags[user][1] = False
      friends = node2node[user]["friend"]
    else:
      friends = graph.update("friends_only", user)
      node2node[user]["friend"] =friends
      nodeofflags[user][0] = False
      followers = node2node[user]["follower"]

    print("friend follower finish")

    node2node[user]["friend2friend"] = []
    node2node[user]["friend2follower"] = []

    for friend in friends:
      friend2friend, friend2follower = graph.update("all", friend, user)
      ans_friend = list((set(friend2friend) & set(seeds + match)) - set([user]))
      ans_follower = list((set(friend2follower) & set(seeds + match)) - set([user]))
      for i in ans_friend: node2node[user]["friend2friend"].append([friend, i])
      for i in ans_follower: node2node[user]["friend2follower"].append([friend, i])

      if (friend in seeds + match):

        if friend not in nodeofflags: nodeofflags[friend] = ["True", "True"]

        if nodeofflags[friend][0] == True:
          node2node[friend]["friend"] = friend2friend
          nodeofflags[friend][0] = False

        if nodeofflags[friend][1] == True:
          node2node[friend]["follower"] = friend2follower
          nodeofflags[friend][1] = False


    print("friends finish")

    node2node[user]["follower2friend"] = []
    node2node[user]["follower2follower"] = []

    for follower in followers:
      follower2friend, follower2follower = graph.update("all", follower, user)
      ans_friend = list((set(follower2friend) & set(seeds + match)) - set([user]))
      ans_follower = list((set(follower2follower) & set(seeds + match)) - set([user]))
      for i in ans_friend: node2node[user]["follower2friend"].append([follower, i])
      for i in ans_follower: node2node[user]["follower2follower"].append([follower, i])

      if (follower in seeds + match):

        if follower not in nodeofflags: nodeofflags[follower] = ["True", "True"]

        if nodeofflags[follower][0] == True:
          node2node[follower]["friend"] = follower2friend
          nodeofflags[follower][0] = False

        if nodeofflags[follower][1] == True:
          node2node[follower]["follower"] = follower2follower
          nodeofflags[follower][1] = False

    print("followers finish")


    ans_friend = list((set(friends) & set(seeds + match)) - set([user]))
    ans_follower = list((set(followers) & set(seeds + match)) - set([user]))
    node2node[user]["friend"] = []
    node2node[user]["follower"] = []
    for i in ans_friend: node2node[user]["friend"].append(i)
    for i in ans_follower: node2node[user]["follower"].append(i)
    print(ans_friend)
    print(ans_follower)

    print("friend : {0}\nfollower : {1}\nfriend2friend : {2}\nfriend2follower : {3}\n follower2friend : {4}\nfollower2follower : {5}\n".format(len(node2node[user]["friend"]),len(node2node[user]["follower"]),len(node2node[user]["friend2friend"]), len(node2node[user]["friend2follower"]), len(node2node[user]["follower2friend"]), len(node2node[user]["follower2follower"])))

    Mypickle.save("../query/analysis/", node2node, queryID + "_node2node")

  graph_count = [0] * 39
  p_dic = {"friend":1, "follower":2, "friend2follower":3, "follower2friend":4, "friend2friend":5, "follower2follower":6}

  for user in (seeds + match):

    node = node2node[user] #dic

    print("{0} : start!!".format(user))
    while(check(node)):

      while(len(node["friend"]) != 0 or len(node["follower"]) != 0):

        path_set = []

        if len(node["friend"]) != 0:
          opponent = node["friend"].pop(0)
          path_set.append(1)
          if opponent in node["follower"]:
            path_set.append(2)
            node["follower"].pop(node["follower"].index(opponent))
        elif len(node["follower"]) != 0:
          opponent = node["follower"].pop(0)
          path_set.append(2)

        Path_set = set_check(node, opponent, p_dic, path_set)
        #print("1 or 2 in set : {0}".format(path_set))
        #print("graph_count old : {0}".format(graph_count))

        for p in Path_set:
          for k, com in path_com.items():
            if len(list(set(com) - set(p))) == 0:
              graph_count[k-1] += 1

        #print("graph_count now : {0}".format(graph_count))

      for v in node.values():
        for q in v:
          opponent = q[1]
          break

      Path_set = set_check(node, opponent, p_dic, [])
      #print("1 or 2 not in set : {0}".format(path_set))
      #print("graph_count old : {0}".format(graph_count))


      for p in Path_set:
        for k, com in path_com.items():
          if len(list(set(com) - set(p))) == 0:
            graph_count[k-1] += 1

      for k,vs in node.items():
        if len(vs) == 0: continue
        while(1):
          vv = np.array(node[k])
          vv = list(vv[:,-1:])
          for i, v  in enumerate(vv):
            if opponent == v[0]:
              node[k].pop(i)
              break
          break



      #print("graph_count now : {0}".format(graph_count))

  with open("../query/analysis/" + queryID + "_graph_count.pickle", mode='wb') as p:
    pickle.dump(graph_count, p)
  print("analysis finish!!")
  print(graph_count)
