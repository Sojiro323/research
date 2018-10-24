#!/usr/bin/env python
# -*- coding:utf-8 -*-
from connect import database
from mymodule import Mypickle
import graph
import time
import os


'''global'''
path = "../pickle/"
'''end global'''



### Functions
def main():
    seeds = ['75007332','1316932982','261467131']
    #check init or restart
    if os.path.exists(path + "que_fo.pickle"):
      que,done = load_pickle(path, ["que_fo","done_fo"])

    else:
      que =  seeds
      que.reverse()
      done = []


    while(1):

      user = que.pop()
      print("user start : {0}".format(user))
      followers = graph.update('followers_only',user,'nnn')

      for ad_fo in followers:
        flag = database.check(ad_fo)
        lang = graph.check_lang(ad_fo)
        if not lang: continue
        if (flag != "protected" and flag != 'NotFound') and ad_fo not in done:
          que.insert(0,ad_fo)

      print(len(que))
      done.insert(0,user)


      Mypickle.save(path, que, "que_fo")
      Mypickle.save(path, done, "done_fo")


def load_pickle(files):

    load_files = Mypickle.load(path,files)

    return load_files[0], load_files[1]



### Execute
if __name__ == "__main__":
  main()
