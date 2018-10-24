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
def main(num):
    seeds = ['75007332','1316932982','261467131']
    #check init or restart
    if os.path.exists(path + "que_" + seeds[num-1] + "_fr.pickle"):
      que_fr = load_pickle(path, "que_" + seeds[num-1] + "_fr")
      que_fo = load_pickle(path, "que_" + seeds[num-1] + "_fo")
    else:
      que_fr =  seeds[num-1]
      que_fr =  seeds[num-1]

    start_time = time.time()

    while(1):

      user = que.pop()

      print("user start : {0}".format(user))
      friend,follower = graph.update('all',user,'nnn')

      for ad_fr in friend:
        flag = database.check(ad_fr)
        if flag != "protected" and flag != 'NotFound':
          que_fr.insert(0,ad_fr)

      for ad_fo in follower:
        flag = database.check(ad_fo)
        if flag != "protected" and flag != 'NotFound':
          que_fr.insert(0,ad_fr)


      end_time = time.time()

      if end_time - start_time > 1800:
        Mypickle.save(path, que_fr, "que_" + seeds[num-1] + "_fr")
        Mypickle.save(path, que_fo, "que_" + seeds[num-1] + "_fo")
        start_time = end_time



def load_pickle(api):

    files = ['que_' + api]
    load_files = Mypickle.load(path,files)

    return load_files[0]



### Execute
if __name__ == "__main__":
  while(1):
    print("input 1,2,3")

    num = input('>>> ')

    if int(num) < 4: break
    else: "\ninput again!!\n\n"

  main(int(num))
