from mymodule import Mypickle
from connect import database

import sys

DIR = '../pickle/positive_old/'
'''
temp_list = Mypickle.load(DIR, '2563168410_3_app')
print(len(temp_list))
print(sys.getsizeof(temp_list))
Mypickle.save(DIR, temp_list, 'test')'''

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

followers = update('followers_only', '415194234','2563168410')
print(len(followers))
for follower in followers:
    followers_2 = update("followers_only",follower,'2563168410')
