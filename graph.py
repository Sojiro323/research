from connect import database
from connect import twitter
from mymodule import Mypickle
import os
import json

DIR = '../pickle/positive/'

def get_match(pattern, seeds):

  print("now : pattern{0}".format(pattern))

  from mymodule import Myyaml
  path_pattern = Myyaml.load("path")["path_com"]["39"]
  needs = Myyaml.load("path")["basic_path_com"][pattern]

  print("needs:{0}".format(needs))

  target_list = []
  target_seeds = {}

  for seed in seeds:
    print("graph {0}".format(seed))
    f = True
    for need in needs:
      if os.path.isfile(DIR + seed + '_' + need + '.pickle') == False:
          f = False
          break

    if f:
      print("all pickle")
      match_list = []
      for i, need in enumerate(needs):
        if i == 0: match_list = Mypickle.load(DIR, seed + '_' +need)
        su = Mypickle.load(DIR, seed + '_' +need)
        print("pickle length : {0}".format(len(su)))
        match_list = list(set(match_list) & set(su))

    else:
      print("else")
      if pattern == path_pattern[0]:#friend
        match_list = basic_pass1(seed)

      elif pattern == path_pattern[1]:#follower
        match_list = basic_pass2(seed)

      elif pattern == path_pattern[2]:#com_friend
        match_list = basic_pass3(seed)

      elif pattern == path_pattern[3]:#com_follower
        match_list = basic_pass4(seed)

      elif pattern == path_pattern[4]:#friend_friend
        match_list = basic_pass5(seed)

      elif pattern == path_pattern[5]:#follower_follower
        match_list = basic_pass6(seed)

      elif pattern == path_pattern[6]:#mutual
        match_list = basic_pass7(seed)

      elif pattern == path_pattern[7]:#8
        match_list = basic_pass8(seed)

      elif pattern == path_pattern[8]:#9
        match_list = basic_pass9(seed)

      elif pattern == path_pattern[9]:#10
        match_list = basic_pass10(seed)

      elif pattern == path_pattern[10]:#11
        match_list = basic_pass11(seed)

      elif pattern == path_pattern[11]:#12
        match_list = basic_pass12(seed)

      elif pattern == path_pattern[12]:#13
        match_list = basic_pass13(seed)

      elif pattern == path_pattern[13]:#14
        match_list = basic_pass14(seed)

      elif pattern == path_pattern[14]:#15
        match_list = basic_pass15(seed)

      elif pattern == path_pattern[15]:#16
        match_list = basic_pass16(seed)

      elif pattern == path_pattern[16]:#17
        match_list = basic_pass17(seed)

      elif pattern == path_pattern[17]:#18
        match_list = basic_pass18(seed)

      elif pattern == path_pattern[18]:#19
        match_list = basic_pass19(seed)

      elif pattern == path_pattern[19]:#20
        match_list = basic_pass20(seed)

      elif pattern == path_pattern[20]:#21
        match_list = basic_pass21(seed)

      elif pattern == path_pattern[21]:#22
        match_list = basic_pass22(seed)

      elif pattern == path_pattern[22]:#23
        match_list = basic_pass23(seed)

      elif pattern == path_pattern[23]:#24
        match_list = basic_pass24(seed)

      elif pattern == path_pattern[24]:#25
        match_list = basic_pass25(seed)

      elif pattern == path_pattern[25]:#26
        match_list = basic_pass26(seed)

      elif pattern == path_pattern[26]:#27
        match_list = basic_pass27(seed)

      elif pattern == path_pattern[27]:#28
        match_list = basic_pass28(seed)

      elif pattern == path_pattern[28]:#29
        match_list = basic_pass29(seed)

      elif pattern == path_pattern[29]:#30
        match_list = basic_pass30(seed)

      elif pattern == path_pattern[30]:#31
        match_list = basic_pass31(seed)

      elif pattern == path_pattern[31]:#32
        match_list = basic_pass32(seed)

      elif pattern == path_pattern[32]:#33
        match_list = basic_pass33(seed)

      elif pattern == path_pattern[33]:#34
        match_list = basic_pass34(seed)

      elif pattern == path_pattern[34]:#35
        match_list = basic_pass35(seed)

      elif pattern == path_pattern[35]:#36
        match_list = basic_pass36(seed)

      elif pattern == path_pattern[36]:#37
        match_list = basic_pass37(seed)

      elif pattern == path_pattern[37]:#38
        match_list = basic_pass38(seed)

      elif pattern == path_pattern[38]:#39
        match_list = basic_pass39(seed)

      else:
        print("key error : {0}".format(pattern))
    print("match_list : {0}\n\n".format(len(match_list)))
    target_list = list((set(target_list) | set(match_list)))
    target_seeds = match(seed, match_list, target_seeds)

  return target_list, target_seeds


def match(seed, match_list, match_seeds):

  if len(match_list) == 0:
    return match_seeds

  for match in match_list:
    if match not in match_seeds: match_seeds[match] = []
    match_seeds[match] += [seed]

  return match_seeds

def up(goal, userID):

  friends = []
  followers = []
  flag = database.check(userID)

  if goal == 'friends_only':
    if flag == 'followers_only':
      friends = use_API(userID, 'friends')
      if friends is not None: database.select('UPDATE checked_list SET state = \'all\' WHERE userID = \'{0}\''.format(userID))
    elif flag == '***':
      friends = use_API(userID, 'friends')
      if friends is not None: database.select('UPDATE checked_list SET state = \'friends_only\' WHERE userID = \'{0}\''.format(userID))
    elif flag == 'friends_only' or flag == 'all':
      friends = database.select('SELECT followerID FROM follow_graph WHERE userID = \'{0}\''.format(userID))
      friends = tuple2list(friends)

    if friends is None: return []
    return friends

  else:
    if flag == 'friends_only':
      followers = use_API(userID, 'followers')
      if followers is not None: database.select('UPDATE checked_list SET state = \'all\' WHERE userID = \'{0}\''.format(userID))
    elif flag == '***':
      followers = use_API(userID, 'followers')
      if followers is not None: database.select('UPDATE checked_list SET state = \'followers_only\' WHERE userID = \'{0}\''.format(userID))
    elif flag == 'followers_only' or flag == 'all':
      followers = database.select('SELECT userID FROM follow_graph WHERE followerID = \'{0}\''.format(userID))
      followers = tuple2list(followers)

    if followers is None: return []
    return followers

def update(goal, userID, seed):

  friends = []
  followers = []
  flag = database.check(userID)

  if userID == seed:
    if goal == 'all':
      if os.path.isfile(DIR + seed + '_1' + '.pickle'):
          friends = Mypickle.load(DIR, seed + '_1')
      else:
          friends = up('friends_only', userID)
      if os.path.isfile(DIR + seed + '_2' + '.pickle'):
          followers = Mypickle.load(DIR, seed + '_2')
      else:
          followers = up('followers_only', userID)
      return friends, followers
    elif goal == 'friends_only':
      if os.path.isfile(DIR + seed + '_1' + '.pickle'): return Mypickle.load(DIR, seed + '_1')
    else:
      if os.path.isfile(DIR + seed + '_2' + '.pickle'): return Mypickle.load(DIR, seed + '_2')



  if goal == 'all':
    if flag == '***':
      friends = use_API(userID, 'friends')
      if friends is not None: database.select('UPDATE checked_list SET state = \'friends_only\' WHERE userID = \'{0}\''.format(userID))
      followers = use_API(userID, 'followers')
      if followers is not None: database.select('UPDATE checked_list SET state = \'all\' WHERE userID = \'{0}\''.format(userID))
    elif flag == 'followers_only':
      friends = use_API(userID, 'friends')
      followers = database.select('SELECT userID FROM follow_graph WHERE followerID = \'{0}\''.format(userID))
      followers = tuple2list(followers)
      if friends is not None: database.select('UPDATE checked_list SET state = \'all\' WHERE userID = \'{0}\''.format(userID))
    elif flag == 'friends_only':
      followers == use_API(userID, 'followers')
      friends = database.select('SELECT followerID FROM follow_graph WHERE userID = \'{0}\''.format(userID))
      friends = tuple2list(friends)
      if followers is not None: database.select('UPDATE checked_list SET state = \'all\' WHERE userID = \'{0}\''.format(userID))
    elif flag == "all":
      friends = database.select('SELECT followerID FROM follow_graph WHERE userID = \'{0}\''.format(userID))
      friends = tuple2list(friends)
      followers = database.select('SELECT userID FROM follow_graph WHERE followerID = \'{0}\''.format(userID))
      followers = tuple2list(followers)

    if friends is None or followers is None: return [], []
    return friends, followers

  elif goal == 'friends_only':
    if flag == 'followers_only':
      friends = use_API(userID, 'friends')
      if friends is not None: database.select('UPDATE checked_list SET state = \'all\' WHERE userID = \'{0}\''.format(userID))
    elif flag == '***':
      friends = use_API(userID, 'friends')
      if friends is not None: database.select('UPDATE checked_list SET state = \'friends_only\' WHERE userID = \'{0}\''.format(userID))
    elif flag == 'friends_only' or flag == 'all':
      friends = use_API(userID, 'friends')
      friends = database.select('SELECT followerID FROM follow_graph WHERE userID = \'{0}\''.format(userID))
      friends = tuple2list(friends)

    if friends is None: return []
    return friends

  elif goal == 'followers_only':
    if flag == 'friends_only':
      followers = use_API(userID, 'followers')
      if followers is not None: database.select('UPDATE checked_list SET state = \'all\' WHERE userID = \'{0}\''.format(userID))
    elif flag == '***':
      followers = use_API(userID, 'followers')
      if followers is not None: database.select('UPDATE checked_list SET state = \'followers_only\' WHERE userID = \'{0}\''.format(userID))
    elif flag == 'followers_only' or flag == 'all':
      followers = database.select('SELECT userID FROM follow_graph WHERE followerID = \'{0}\''.format(userID))
      followers = tuple2list(followers)

    if followers is None: return []
    return followers

def check_lang(userID):

    language = database.select("SELECT language FROM checked_list WHERE userID = \'{0}\'".format(userID))
    if len(language) == 0:
        responce = twitter.show(userID)
        if responce.status_code != 200:
            if responce.status_code == 401:
                sql = 'INSERT INTO checked_list (userID, state) VALUES (\'{0}\', \'protected \')'.format(userID)
                database.select(sql)
            elif responce.status_code == 404:
                sql = 'INSERT INTO checked_list (userID, state) VALUES (\'{0}\', \'NotFound \')'.format(userID)
                database.select(sql)
            return False
        else:
            ress = json.loads(responce.text)
            language = ress["lang"]
            followers_count = ress["followers_count"]
            friends_count = ress["friends_count"]
            sql = 'INSERT INTO checked_list VALUES (\'{0}\',\'***\',\'{1}\',\'{2}\',\'{3} \')'.format(userID,language,str(friends_count),str(followers_count))
            database.select(sql)
    else: language = language[0][0]

    if language == 'ja': return True
    else: return False


def use_API(userID, api):

  values = []
  if not check_lang(userID): return None
  print("{0} using {1} API".format(userID,api))

  return_list = acsessAPI(userID, api)
  if return_list is None: return None
  if len(return_list) == 0: return []

  if api == 'friends':
    inserted = database.select('SELECT followerID FROM follow_graph WHERE userID = \'{0}\''.format(userID))
    inserted = tuple2list(inserted)
    for i, friend in enumerate(return_list):
      if friend in inserted: continue
      #sql = 'INSERT IGNORE INTO follow_graph VALUES (\'{0}\',\'{1}\')'.format(userID,friend)
      #database.select(sql)
      values.append("(\'{0}\',\'{1}\')".format(userID,friend))
      if i % 1000 == 0:
          sq =','.join(values)
          database.select("INSERT IGNORE INTO follow_graph VALUES " + sq  )
          values = []
  if len(values) != 0:
      if len(values) != 1:sq =','.join(values)
      else: sq = values[0]
      database.select("INSERT IGNORE INTO follow_graph VALUES " + sq )

  else:
    inserted = database.select('SELECT userID FROM follow_graph WHERE followerID = \'{0}\''.format(userID))
    inserted = tuple2list(inserted)
    for i,follower in enumerate(return_list):
      if follower in inserted: continue
      #sql = 'INSERT IGNORE INTO follow_graph VALUES (\'{0}\',\'{1}\')'.format(follower,userID)
      #database.select(sql)
      values.append("(\'{0}\', \'{1}\')".format(follower,userID))
      if i % 1000 == 0:
          sq =','.join(values)
          database.select("INSERT IGNORE INTO follow_graph VALUES " + sq )
          values = []
  if len(values) != 0:
      if len(values) != 1:sq =','.join(values)
      else: sq = values[0]
      database.select("INSERT IGNORE INTO follow_graph VALUES " + sq )

  print("get use length : {0}".format(len(return_list)))
  return return_list


def acsessAPI(userID, api):

    return_list = []

    if api == "followers":responce = twitter.followers(userID)
    else:responce = twitter.friends(userID)

    if responce.status_code != 200:
      return None

    IDs = json.loads(responce.text)
    return_list = [ID for ID in IDs['ids']]

    print('{0} \'s return list : \n {1}'.format(userID, len(return_list)))
    return return_list


def tuple2list(tp):
  return [t[0] for t in tp]


def basic_pass1(seed):

  match_list = []

  friends = update("friends_only",seed, seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'): Mypickle.save(DIR, friends, seed + '_1')

  return friends

def basic_pass2(seed):

  match_list = []

  followers = update("followers_only",seed, seed)
  if not os.path.isfile(DIR + seed + '_2.pickle'): Mypickle.save(DIR, followers, seed + '_2')

  return followers


def basic_pass3(seed):

  match_list = []

  friends = update("friends_only",seed ,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')

  for friend in friends:
    followers = update("followers_only",friend, seed)
    match_list = list(set(match_list) | set(followers))

  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, match_list, seed + '_3')
  return match_list



def basic_pass4(seed):

  match_list = []


  followers = update("followers_only",seed, seed)
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    friends = update("friends_only",follower, seed)
    match_list = list(set(match_list) | set(friends))

  if not os.path.isfile(DIR + seed + '_4.pickle'):  Mypickle.save(DIR, match_list, seed + '_4')
  return match_list



def basic_pass5(seed):

  match_list = []


  friends = update("friends_only",seed, seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')

  for friend in friends:
    friends_2 = update("friends_only",friend,seed)
    match_list = list(set(match_list) | set(friends_2))

  if not os.path.isfile(DIR + seed + '_5.pickle'):  Mypickle.save(DIR, match_list, seed + '_5')
  return match_list


def basic_pass6(seed):

  match_list = []


  followers = update("followers_only",seed,seed)
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2 = update("followers_only",follower,seed)
    match_list = list(set(match_list) | set(followers_2))


  if not os.path.isfile(DIR + seed + '_6.pickle'):  Mypickle.save(DIR, match_list, seed + '_6')
  return match_list

def basic_pass7(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')
  match_list = list(set(followers) & set(friends))

  return match_list

def basic_pass8(seed):

  match_list = []
  frfo = []


  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for friend in friends:
    friends2followers = update("followers_only",friend,seed)
    frfo = list(set(friends2followers) | set(frfo))
    ans = list(set(followers) & set(friends2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, frfo, seed + '_3')
  return match_list

def basic_pass9(seed):

  match_list = []
  frfo = []

  friends = update("friends_only", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')

  for friend in friends:
    friends2followers = update("followers_only",friend,seed)
    frfo = list(set(friends2followers) | set(frfo))
    ans = list(set(friends) & set(friends2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, frfo, seed + '_3')
  return match_list

def basic_pass10(seed):

  match_list = []
  frfr = []
  frfo = []

  friends = update("friends_only", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')

  for friend in friends:
    friends2friends, friends2followers = update("all",friend,seed)
    frfo = list(set(friends2followers) | set(frfo))
    frfr = list(set(friends2friends) | set(frfr))
    ans = list(set(friends2friends) & set(friends2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_5.pickle'):  Mypickle.save(DIR, frfr, seed + '_5')
  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, frfo, seed + '_3')
  return match_list

def basic_pass11(seed):

  match_list = []

  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))
  mutual = list(set(mutual) - set(seed))

  for m in mutual:
    ans = update("followers_only", m,seed)
    match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass12(seed):

  match_list = []
  fofr = []

  followers = update("followers_only", seed,seed)
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2friends = update("friends_only",follower,seed)
    fofr = list(set(followers2friends) | set(fofr))
    ans = list(set(followers) & set(followers2friends))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_4.pickle'):  Mypickle.save(DIR, fofr, seed + '_4')
  return match_list

def basic_pass13(seed):

  match_list = []
  fofr = []

  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2friends = update("friends_only",follower,seed)
    fofr = list(set(followers2friends) | set(fofr))
    ans = list(set(friends) & set(followers2friends))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_4.pickle'):  Mypickle.save(DIR, fofr, seed + '_4')
  return match_list

def basic_pass14(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))
  mutual = list(set(mutual) - set(seed))

  for m in mutual:
    ans = update("friends_only", m,seed)
    match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass15(seed):

  match_list = []
  fofo = []
  fofr = []

  followers = update("followers_only", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, followers, seed + '_1')

  for follower in followers:
    followers2friends, followers2followers = update("all",follower,seed)
    fofr = list(set(followers2friends) | set(fofr))
    fofo = list(set(followers2followers) | set(fofo))
    ans = list(set(followers2friends) & set(followers2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_4.pickle'):  Mypickle.save(DIR, fofr, seed + '_4')
  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, fofo, seed + '_3')
  return match_list

def basic_pass16(seed):

  match_list = []
  frfr = []

  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for friend in friends:
    friends2friends = update("friends_only",friend,seed)
    frfr = list(set(friends2friends) | set(frfr))
    ans = list(set(followers) & set(friends2friends))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_5.pickle'):  Mypickle.save(DIR, frfr, seed + '_5')
  return match_list

def basic_pass17(seed):

  match_list = []
  frfr = []

  friends = update("friends_only", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')

  for friend in friends:
    friends2friends = update("friends_only",friend,seed)
    frfr = list(set(friends2friends) | set(frfr))
    ans = list(set(friends) & set(friends2friends))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_5.pickle'):  Mypickle.save(DIR, frfr, seed + '_5')
  return match_list

def basic_pass18(seed):

  match_list = []
  fofo = []

  followers = update("followers_only", seed,seed)
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2followers = update("followers_only",follower,seed)
    fofo = list(set(followers2followers) | set(fofo))
    ans = list(set(followers) & set(followers2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, fofo, seed + '_3')
  return match_list

def basic_pass19(seed):

  match_list = []
  fofo = []


  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2followers = update("followers_only",follower,seed)
    fofo = list(set(followers2followers) | set(fofo))
    ans = list(set(follower) & set(friends) & set(followers2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_6.pickle'):  Mypickle.save(DIR, fofo, seed + '_6')
  return match_list

def basic_pass20(seed):

  match_list = []
  frfo = []

  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for friend in friends:
    friends2followers = update("followers_only",friend,seed)
    frfo = list(set(friends2followers) | set(frfo))
    ans = list(set(followers) & set(friend) & set(friends2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, frfo, seed + '_3')
  return match_list

def basic_pass21(seed):

  match_list = []
  fofr = []

  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2friends = update("friends_only",follower,seed)
    fofr = list(set(followers2friends) | set(fofr))
    ans = list(set(friends) & set(followers) & set(followers2friends))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_4.pickle'):  Mypickle.save(DIR, fofr, seed + '_4')
  return match_list

def basic_pass22(seed):

  match_list = []
  frfr = []

  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for friend in friends:
    friends2friends = update("friends_only",friend,seed)
    frfr = list(set(friends2friends) | set(frfr))
    ans = list(set(followers) & set(friends) & set(friends2friends))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_5.pickle'):  Mypickle.save(DIR, frfr, seed + '_5')
  return match_list

def basic_pass23(seed):

  match_list = []
  fofo = []

  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2followers = update("followers_only",follower,seed)
    fofo = list(set(followers2followers) | set(fofo))
    ans = list(set(friends) & set(followers) & set(followers2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_6.pickle'):  Mypickle.save(DIR, fofo, seed + '_6')
  return match_list

def basic_pass24(seed):

  match_list = []

  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))

  for m in mutual:
    mutual2friends, mutual2followers = update("all", m,seed)

    ans = list(set(mutual2friends) & set(mutual2followers))

    match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass25(seed):

  match_list = []
  frfr = []
  frfo = []

  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'): Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for friend in friends:
    friends2friends, friends2followers = update("all",friend,seed)
    frfr = list(set(friends2friends) | set(frfr))
    frfo = list(set(friends2followers) | set(frfo))
    ans = list(set(followers) & set(friends2followers) & set(friends2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_5.pickle'):  Mypickle.save(DIR, frfr, seed + '_5')
  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, frfo, seed + '_3')
  return match_list

def basic_pass26(seed):

  match_list = []
  frfr = []
  frfo = []

  friends = update("friends_only", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')

  for friend in friends:
    friends2friends, friends2followers = update("all",friend,seed)
    frfr = list(set(friends2friends) | set(frfr))
    frfo = list(set(friends2followers) | set(frfo))
    ans = list(set(friends) & set(friends2friends) & set(friends2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_5.pickle'):  Mypickle.save(DIR, frfr, seed + '_5')
  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, frfo, seed + '_3')
  return match_list

def basic_pass27(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))

  for m in mutual:
    mutual2followers = update("followers_only", m,seed)

    ans = list(set(mutual2followers) & set(followers))

    match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass28(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))

  for m in mutual:
    mutual2followers = update("followers_only", m,seed)

    ans = list(set(mutual2followers) & set(friends))

    match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass29(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))

  for m in mutual:
    mutual2friends = update("friends_only", m,seed)

    ans = list(set(mutual2friends) & set(followers))

    match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass30(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))

  for m in mutual:
      mutual2friends = update("friends_only", m,seed)

      ans = list(set(mutual2friends) & set(friends))

      match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass31(seed):

  match_list = []
  fofr = []
  fofo = []

  followers = update("followers_only", seed,seed)
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2friends, followers2followers = update("all",follower,seed)
    fofr = list(set(followers2friends) | set(fofr))
    fofo = list(set(followers2followers) | set(fofo))
    ans = list(set(followers2friends) & set(followers2followers) & set(followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_4.pickle'):  Mypickle.save(DIR, fofr, seed + '_4')
  if not os.path.isfile(DIR + seed + '_6.pickle'):  Mypickle.save(DIR, fofo, seed + '_6')
  return match_list

def basic_pass32(seed):

  match_list = []
  fofr = []
  fofo = []

  friends, followers = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2friends, followers2followers = update("all",follower,seed)
    fofr = list(set(followers2friends) | set(fofr))
    fofo = list(set(followers2followers) | set(fofo))
    ans = list(set(followers2friends) & set(followers2followers) & set(friends))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_4.pickle'):  Mypickle.save(DIR, fofr, seed + '_4')
  if not os.path.isfile(DIR + seed + '_6.pickle'):  Mypickle.save(DIR, fofo, seed + '_6')
  return match_list

def basic_pass33(seed):

  match_list = []
  frfr = []
  frfo = []

  friends, followers  = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for friend in friends:
    friends2friends, friends2followers = update("all",friend,seed)
    frfr = list(set(friends2friends) | set(frfr))
    frfo = list(set(friends2followers) | set(frfo))
    ans = list(set(followers) & set(friends) & set(friends2followers) & set(friends2followers))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_5.pickle'):  Mypickle.save(DIR, frfr, seed + '_5')
  if not os.path.isfile(DIR + seed + '_3.pickle'):  Mypickle.save(DIR, frfo, seed + '_3')
  return match_list

def basic_pass34(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))

  for m in mutual:
    mutual2followers = update("followers_only", m,seed)

    ans = list(set(mutual2followers) & set(mutual))

    match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass35(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))

  for m in mutual:
    mutual2friends = update("friends_only", m,seed)

    ans = list(set(mutual2friends) & set(mutual))

    match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass36(seed):

  match_list = []
  fofo = []
  fofr = []

  friends, followers = update("all", seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  for follower in followers:
    followers2friends, followers2followers = update("all",follower,seed)
    fofr = list(set(followers2friends) | set(fofr))
    fofo = list(set(followers2followers) | set(fofo))
    ans = list(set(followers2friends) & set(followers2followers) & set(followers) & set(friends))
    match_list = list(set(match_list) | set(ans))

  if not os.path.isfile(DIR + seed + '_4.pickle'):  Mypickle.save(DIR, fofr, seed + '_4')
  if not os.path.isfile(DIR + seed + '_6.pickle'):  Mypickle.save(DIR, fofo, seed + '_6')
  return match_list

def basic_pass37(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))

  for m in mutual:
    mutual2friends, mutual2followers = update("all", m,seed)

    ans = list(set(mutual2friends) & set(mutual2followers) & set(followers))

    match_list = list(set(match_list) | set(ans))

  return match_list

def basic_pass38(seed):

    match_list = []


    friends, followers = update("all",seed,seed)
    if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
    if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

    mutual = list(set(followers) & set(friends))

    for m in mutual:
      mutual2friends, mutual2followers = update("all", m,seed)

      ans = list(set(mutual2friends) & set(mutual2followers) & set(friends))

      match_list = list(set(match_list) | set(ans))

    return match_list

def basic_pass39(seed):

  match_list = []


  friends, followers = update("all",seed,seed)
  if not os.path.isfile(DIR + seed + '_1.pickle'):  Mypickle.save(DIR, friends, seed + '_1')
  if not os.path.isfile(DIR + seed + '_2.pickle'):  Mypickle.save(DIR, followers, seed + '_2')

  mutual = list(set(followers) & set(friends))

  for m in mutual:
    mutual2friends, mutual2followers = update("all", m,seed)

    ans = list(set(mutual2friends) & set(mutual2followers) & set(mutual))

    match_list = list(set(match_list) | set(ans))

  return match_list

def join_dic(dics):
  ans = {}
  for dic in dics:
    for k, v in dic.items():
      if k not in ans: ans[k] = []
      ans[k] += v

  for k, v in ans.items():
    ans[k] = list(set(v))

  return {k:list(set(v)) for k,v in ans.items()}
