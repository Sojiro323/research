from connect import database
from connect import twitter
from mymodule import Mypickle
from mymodule import Myyaml
import utils
import os
import json

DIR = '../pickle/positive_old/'




def get_match(pattern):

  target_list = []
  target_seeds = {}

  for i in pattern:
    seed = i[0]
    p = i[1]
    if len(pattern) != 1: print("get_match start!! (seed:{0}  pattern:{1})".format(seed, p))


    min_needs = Myyaml.load("path")["path_com"][str(p)]
    min_needs.remove(str(p))
    if min_needs is None: min_needs = []
    max_needs = []
    for k,v in Myyaml.load("path")["path_com"].items():
      if k == p: continue
      if p in v: max_needs.append(k)

    #if len(pattern) != 1: print("pattern : {0}\nmin_need : {1}\nmax_need : {2}".format(p, min_needs, max_needs))
    #else: print("pattern : {0}".format(p))


    match_list = different_approximate_path(p, seed, min_needs, max_needs)
    #print("seed : {0}\nmatch_list : {1}\n".format(seed, len(match_list)))
    target_list = list((set(target_list) | set(match_list)))
    target_seeds = match(seed+"_"+str(p), match_list, target_seeds)

  return target_list, target_seeds


def different_approximate_path(pattern, seed, min_needs, max_needs):
    if os.path.isfile(DIR +  "different_" + seed + "_" + pattern + '.pickle'):
        answer_list = Mypickle.load(DIR, "different_" + seed + "_" + pattern)
        if isinstance(answer_list, dict): return answer_list.keys()
        elif isinstance(answer_list, list): return answer_list
        else: print("load error (answer_list)")


    answer_list = eval('basic_pass'+str(pattern))(seed)
    if isinstance(answer_list, dict):
        temp_dics = []
        for max_need in max_needs:
            temp_dic = eval('basic_pass'+str(max_need))(seed)
            temp_dics.append(temp_dic)
            del temp_dic
        dics = join_dic(temp_dics)
        del temp_dics

        for k, v in dict(answer_list).items():
            if k in dics:
                answer_list[k] = list(set(v) - set(dics[k]))
                if len(answer_list[k]) == 0: del answer_list[k]

        Mypickle.save(DIR, answer_list, "different_" + seed + "_" + pattern)
        return answer_list.keys()

    elif isinstance(answer_list, list):
        for max_need in max_needs:
            temp_list = eval('basic_pass'+str(max_need))(seed)
            if isinstance(temp_list, dict): answer_list = list(set(answer_list) - set(temp_list.keys()))
            elif isinstance(temp_list, list): answer_list = list(set(answer_list) - set(temp_list))
            else: print("type error (temp_list)")

        Mypickle.save(DIR, answer_list, "different_" + seed + "_" + pattern)
        return answer_list

    else: print("type error (answer_list)")

"""
def approximate_path(seed, needs):
    answer_list = []
    for i, need in enumerate(needs):
        if i == 0: answer_list =  Mypickle.load(DIR, seed + '_' + str(need) + '_app')
        else:
          temp_list = Mypickle.load(DIR, seed + '_' + str(need) + '_app')
          answer_list = list(set(answer_list) & set(temp_list))

    return answer_list

def different_approximate_path(pattern, seed, min_needs, max_needs):
    different_list = []
    for min_need in min_needs:
        temp_list = Mypickle.load(DIR, "different_" + seed + "_" + min_need)
        different_list = list(set(different_list) | set(temp_list))
    for max_need in max_needs:
        temp_list = approximate_path(seed, Myyaml.load("path")["basic_path_com"][max_need])
        different_list = list(set(different_list) | set(temp_list))

    answer_list = list(set(approximate_path(seed, Myyaml.load("path")["basic_path_com"][pattern])) - set(different_list))
    Mypickle.save(DIR, answer_list, "different_" + seed + "_" + pattern)

    return answer_list
"""

def match(seed, match_list, match_seeds):

  if len(match_list) == 0:
    return match_seeds

  for match in match_list:
    if match not in match_seeds: match_seeds[match] = []
    match_seeds[match].append(seed)

  return match_seeds


def update(goal, userID, seed):

  friends = []
  followers = []

  if goal == "friends_only":
    friends = database.select('select friendID from friend_graph where userID = \'' + userID + '\'')
    friends = tuple2list(friends)
    return friends
  elif goal == "followers_only":
    followers = database.select('select followerID from follower_graph where userID = \'' + userID + '\'')
    followers = tuple2list(followers)
    return followers
  else:
    friends = database.select('select friendID from friend_graph where userID = \'' + userID + '\'')
    friends = tuple2list(friends)
    followers = database.select('select followerID from follower_graph where userID = \'' + userID + '\'')
    followers = tuple2list(followers)
    return friends, followers



def tuple2list(tp):
  return [t[0] for t in tp]

def init_pickle(seed):
    for i in range(1,40):
        if not os.path.isfile(os.path.join(DIR, seed+'_'+str(i)+'.pickle' )): eval('basic_pass'+str(i))(seed)

"""
def init_pickle(seed):
    sql = {1:'select distinct friendID from friend_graph where userID=\'',
            2:'select distinct followerID from follower_graph where userID=\'',
            3:'select distinct followerID from follower_graph where userID in (select friendID from friend_graph where userID=\'',
            4:'select distinct friendID from friend_graph where userID in (select followerID from follower_graph where userID=\'',
            5:'select distinct friendID from friend_graph where userID in (select friendID from friend_graph where userID=\'',
            6:'select distinct followerID from follower_graph where userID in (select followerID from follower_graph where userID=\''
}
    for i in range(1,7):
        #if os.path.isfile(DIR + seed + '_' + str(i) + '.pickle') == False or os.path.isfile(DIR + seed + '_' + str(i) + '_app.pickle') == False:#friend
        if os.path.isfile(DIR + seed + '_' + str(i) + '_app.pickle') == False:
            if i==1 or i==2:de  print("a")
f different_approximate_path(pattern, seed, min_needs, max_needs):
    different_list = []
    for min_need in min_needs:
        temp_list = Mypickle.load(DIR, "different_" + seed + "_" + min_need)
        different_list = list(set(different_list) | set(temp_list))
    for max_need in max_needs:
        temp_list = approximate_path(seed, Myyaml.load("path")["basic_path_com"][max_need])
        different_list = list(set(different_list) | set(temp_list))

    answer_list = list(set(approximate_path(seed, Myyaml.load("path")["basic_path_com"][pattern])) - set(different_list))
    Mypickle.save(DIR, answer_list, "different_" + seed + "_" + pattern)

    return answer_list
                target = database.select(sql[i] + seed + '\'')
            else:
                target = database.select(sql[i] + seed + '\')')
            target = tuple2list(target)
            Mypickle.save(DIR, target, seed + '_' + str(i) + '_app')

def intersection(dic):
    match_list = []
    for v in dic.values():
        match_list = list(set(match_list)|set(v))
    return match_list
"""

def intersections(*dics):
    first_dic = dics[0]
    dics = dics[1:]
    match_dic = {}
    for k,v in first_dic.items():
        add_list = v
        for dic in dics:
            if k not in dic: add_list = []
            else: add_list = list(set(add_list)&set(dic[k]))
        if len(add_list) != 0:
            match_dic[k] = add_list
    return match_dic


def join_dic(dics):
  ans = {}
  for dic in dics:
    for k, v in dic.items():
      if k not in ans: ans[k] = v
      else: ans[k] = ans[k] + v

  return {k:list(set(v)) for k,v in ans.items()}


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


def basic_pass3(seed):

  _3 = {}

  if not os.path.isfile(DIR + seed + '_3.pickle'):
      friends = basic_pass1(seed)
      for friend in friends:
          followers = update("followers_only",friend, seed)
          for follower in followers:
              if follower not in _3: _3[follower] = [friend]
              else: _3[follower].append(friend)
      Mypickle.save(DIR, _3, seed + '_3')
  else:
      _3 = Mypickle.load(DIR, seed + '_3')

  return _3



def basic_pass4(seed):

  _4 = {}

  if not os.path.isfile(DIR + seed + '_4.pickle'):
      followers = basic_pass2(seed)
      for follower in followers:
          friends = update("friends_only",follower, seed)
          for friend in friends:
              if friend not in _4: _4[friend] = [follower]
              else: _4[friend].append(follower)
      Mypickle.save(DIR, _4, seed + '_4')
  else:
      _4 = Mypickle.load(DIR, seed + '_4')

  return _4



def basic_pass5(seed):

  _5 = {}

  if not os.path.isfile(DIR + seed + '_5.pickle'):
      friends = basic_pass1(seed)
      for friend in friends:
          friends_2 = update("friends_only",friend,seed)
          for friend_2 in friends_2:
              if friend_2 not in _5: _5[friend_2] = [friend]
              else: _5[friend_2].append(friend)
      Mypickle.save(DIR, _5, seed + '_5')
  else:
      _5 = Mypickle.load(DIR, seed + '_5')

  return _5


def basic_pass6(seed):

  _6 = {}

  if not os.path.isfile(DIR + seed + '_6.pickle'):
      followers = basic_pass2(seed)
      for follower in followers:
          followers_2 = update("followers_only",follower,seed)
          for follower_2 in followers_2:
              if follower_2 not in _6: _6[follower_2] = [follower]
              else: _6[follower_2].append(follower)
      Mypickle.save(DIR, _6, seed + '_6')
  else:
      _6 = Mypickle.load(DIR, seed + '_6')

  return _6

def basic_pass7(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_7.pickle'):
    _1 = basic_pass1(seed)
    _2 = basic_pass2(seed)
    match_list = list(set(_1) & set(_2))
    Mypickle.save(DIR, match_list, seed + '_7')
  else:
    match_list = Mypickle.load(DIR, seed + '_7')

  return match_list


def basic_pass8(seed):

  if not os.path.isfile(DIR + seed + '_8.pickle'):
      _2 = basic_pass2(seed)
      _3 = basic_pass3(seed)
      match_dic =  {v:_3[v] for v in list(set(_2) & set(_3.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_8')
  else:
      match_dic = Mypickle.load(DIR, seed + '_8')

  return match_dic


def basic_pass9(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_9.pickle'):
      _1 = basic_pass1(seed)
      _3 = basic_pass3(seed)
      match_dic =  {v:_3[v] for v in list(set(_1) & set(_3.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_9')
  else:
      match_dic = Mypickle.load(DIR, seed + '_9')

  return match_dic


def basic_pass10(seed):

  if not os.path.isfile(DIR + seed + '_10.pickle'):
      _3 = basic_pass3(seed)
      _5 = basic_pass5(seed)
      match_dic = intersections(_5,_3)
      Mypickle.save(DIR, match_dic, seed + '_10')
  else:
      match_dic = Mypickle.load(DIR, seed + '_10')

  return match_dic


def basic_pass11(seed):

  if not os.path.isfile(DIR + seed + '_11.pickle'):
      _3 = basic_pass3(seed)
      _6 = basic_pass6(seed)
      match_dic = intersections(_3,_6)
      Mypickle.save(DIR, match_dic, seed + '_11')
  else:
      match_dic = Mypickle.load(DIR, seed + '_11')

  return match_dic


def basic_pass12(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_12.pickle'):
      _2 = basic_pass2(seed)
      _4 = basic_pass4(seed)
      match_dic =  {v:_4[v] for v in list(set(_2) & set(_4.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_12')
  else:
      match_dic = Mypickle.load(DIR, seed + '_12')

  return match_dic


def basic_pass13(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_13.pickle'):
      _1 = basic_pass1(seed)
      _4 = basic_pass4(seed)
      match_dic =  {v:_4[v] for v in list(set(_1) & set(_4.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_13')
  else:
      match_dic = Mypickle.load(DIR, seed + '_13')

  return match_dic


def basic_pass14(seed):

  if not os.path.isfile(DIR + seed + '_14.pickle'):
      _4 = basic_pass4(seed)
      _5 = basic_pass5(seed)
      match_dic = intersections(_5,_4)
      Mypickle.save(DIR, match_dic, seed + '_14')
  else:
      match_dic = Mypickle.load(DIR, seed + '_14')

  return match_dic


def basic_pass15(seed):

  if not os.path.isfile(DIR + seed + '_15.pickle'):
      _4 = basic_pass4(seed)
      _6 = basic_pass6(seed)
      match_dic = intersections(_4,_6)
      Mypickle.save(DIR, match_dic, seed + '_15')
  else:
      match_dic = Mypickle.load(DIR, seed + '_15')

  return match_dic


def basic_pass16(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_16.pickle'):
      _2 = basic_pass2(seed)
      _5 = basic_pass5(seed)
      match_dic =  {v:_5[v] for v in list(set(_2) & set(_5.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_16')
  else:
      match_dic = Mypickle.load(DIR, seed + '_16')

  return match_dic


def basic_pass17(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_17.pickle'):
      _1 = basic_pass1(seed)
      _5 = basic_pass5(seed)
      match_dic =  {v:_5[v] for v in list(set(_1) & set(_5.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_17')
  else:
      match_dic = Mypickle.load(DIR, seed + '_17')

  return match_dic


def basic_pass18(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_18.pickle'):
      _2 = basic_pass2(seed)
      _6 = basic_pass6(seed)
      match_dic =  {v:_6[v] for v in list(set(_2) & set(_6.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_18')
  else:
      match_dic = Mypickle.load(DIR, seed + '_18')

  return match_dic


def basic_pass19(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_19.pickle'):
      _1 = basic_pass1(seed)
      _6 = basic_pass6(seed)
      match_dic =  {v:_6[v] for v in list(set(_1) & set(_6.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_19')
  else:
      match_dic = Mypickle.load(DIR, seed + '_19')

  return match_dic


def basic_pass20(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_20.pickle'):
      _3 = basic_pass3(seed)
      _7 = basic_pass7(seed)
      match_dic =  {v:_3[v] for v in list(set(_7) & set(_3.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_20')
  else:
      match_dic = Mypickle.load(DIR, seed + '_20')

  return match_dic


def basic_pass21(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_21.pickle'):
      _4 = basic_pass4(seed)
      _7 = basic_pass7(seed)
      match_dic =  {v:_4[v] for v in list(set(_7) & set(_4.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_21')
  else:
      match_dic = Mypickle.load(DIR, seed + '_21')

  return match_dic


def basic_pass22(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_22.pickle'):
      _5 = basic_pass5(seed)
      _7 = basic_pass7(seed)
      match_dic =  {v:_5[v] for v in list(set(_7) & set(_5.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_22')
  else:
      match_dic = Mypickle.load(DIR, seed + '_22')

  return match_dic


def basic_pass23(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_23.pickle'):
      _6 = basic_pass6(seed)
      _7 = basic_pass7(seed)
      match_dic =  {v:_6[v] for v in list(set(_7) & set(_6.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_23')
  else:
      match_dic = Mypickle.load(DIR, seed + '_23')

  return match_dic


def basic_pass24(seed):

  if not os.path.isfile(DIR + seed + '_24.pickle'):
      _3 = basic_pass3(seed)
      _4 = basic_pass4(seed)
      _5 = basic_pass5(seed)
      _6 = basic_pass6(seed)
      match_dic = intersections(_5,_3,_4,_6)
      Mypickle.save(DIR, match_dic, seed + '_24')
  else:
      match_dic = Mypickle.load(DIR, seed + '_24')

  return match_dic


def basic_pass25(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_25.pickle'):
      _2 = basic_pass2(seed)
      _10 = basic_pass10(seed)
      match_dic =  {v:_10[v] for v in list(set(_2) & set(_10.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_25')
  else:
      match_dic = Mypickle.load(DIR, seed + '_25')

  return match_dic

def basic_pass26(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_26.pickle'):
      _1 = basic_pass1(seed)
      _10 = basic_pass10(seed)
      match_dic =  {v:_10[v] for v in list(set(_1) & set(_10.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_26')
  else:
      match_dic = Mypickle.load(DIR, seed + '_26')

  return match_dic

def basic_pass27(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_27.pickle'):
      _2 = basic_pass2(seed)
      _11 = basic_pass11(seed)
      match_dic =  {v:_11[v] for v in list(set(_2) & set(_11.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_27')
  else:
      match_dic = Mypickle.load(DIR, seed + '_27')

  return match_dic


def basic_pass28(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_28.pickle'):
      _1 = basic_pass1(seed)
      _11 = basic_pass11(seed)
      match_dic =  {v:_11[v] for v in list(set(_1) & set(_11.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_28')
  else:
      match_dic = Mypickle.load(DIR, seed + '_28')

  return match_dic


def basic_pass29(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_29.pickle'):
      _2 = basic_pass2(seed)
      _14 = basic_pass14(seed)
      match_dic =  {v:_14[v] for v in list(set(_2) & set(_14.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_29')
  else:
      match_dic = Mypickle.load(DIR, seed + '_29')

  return match_dic


def basic_pass30(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_30.pickle'):
      _1 = basic_pass1(seed)
      _14 = basic_pass14(seed)
      match_dic =  {v:_14[v] for v in list(set(_1) & set(_14.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_30')
  else:
      match_dic = Mypickle.load(DIR, seed + '_30')

  return match_dic


def basic_pass31(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_31.pickle'):
      _2 = basic_pass2(seed)
      _15 = basic_pass15(seed)
      match_dic =  {v:_15[v] for v in list(set(_2) & set(_15.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_31')
  else:
      match_dic = Mypickle.load(DIR, seed + '_31')

  return match_dic


def basic_pass32(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_32.pickle'):
      _1 = basic_pass1(seed)
      _15 = basic_pass15(seed)
      match_dic =  {v:_15[v] for v in list(set(_1) & set(_15.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_32')
  else:
      match_dic = Mypickle.load(DIR, seed + '_32')

  return match_dic

def basic_pass33(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_33.pickle'):
      _7 = basic_pass7(seed)
      _10 = basic_pass10(seed)
      match_dic =  {v:_10[v] for v in list(set(_7) & set(_10.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_33')
  else:
      match_dic = Mypickle.load(DIR, seed + '_33')

  return match_dic

def basic_pass34(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_34.pickle'):
      _7 = basic_pass7(seed)
      _11 = basic_pass11(seed)
      match_dic =  {v:_11[v] for v in list(set(_7) & set(_11.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_34')
  else:
      match_dic = Mypickle.load(DIR, seed + '_34')

  return match_dic

def basic_pass35(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_35.pickle'):
      _7 = basic_pass7(seed)
      _14 = basic_pass14(seed)
      match_dic =  {v:_14[v] for v in list(set(_7) & set(_14.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_35')
  else:
      match_dic = Mypickle.load(DIR, seed + '_35')

  return match_dic

def basic_pass36(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_36.pickle'):
      _7 = basic_pass7(seed)
      _15 = basic_pass15(seed)
      match_dic =  {v:_15[v] for v in list(set(_7) & set(_15.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_36')
  else:
      match_dic = Mypickle.load(DIR, seed + '_36')

  return match_dic

def basic_pass37(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_37.pickle'):
      _2 = basic_pass2(seed)
      _24 =basic_pass24(seed)
      match_dic =  {v:_24[v] for v in list(set(_2) & set(_24.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_37')
  else:
      match_dic = Mypickle.load(DIR, seed + '_37')

  return match_dic

def basic_pass38(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_38.pickle'):
      _1 = basic_pass1(seed)
      _24 = basic_pass24(seed)
      match_dic =  {v:_24[v] for v in list(set(_1) & set(_24.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_38')
  else:
      match_dic = Mypickle.load(DIR, seed + '_38')

  return match_dic

def basic_pass39(seed):

  match_list = []

  if not os.path.isfile(DIR + seed + '_39.pickle'):
      _7 = basic_pass7(seed)
      _24 = basic_pass24(seed)
      match_dic =  {v:_24[v] for v in list(set(_7) & set(_24.keys()))}
      Mypickle.save(DIR, match_dic, seed + '_39')
  else:
      match_dic = Mypickle.load(DIR, seed + '_39')

  return match_dic
