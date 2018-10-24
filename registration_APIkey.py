from connect import database
import os
import yaml
# coding: utf-8

limit = {"friends":15, "followers":15, "lookup":900, "show":900, "users":900,"tweets":180}

def register_api():
    MAX = database.select("select MAX(id) from api_limit")[0][0]
    keys = os.listdir('../password/twitterAPI/')

    f = open('../password/API_database.yml', 'r+')
    api_names = yaml.load(f)['api_name']

    for key in keys:
      if 'yml' not in key: continue
      ID = key.split(".")[0]
      if int(ID) > MAX:
        for api_name in api_names:
          print("INSERT INTO api_limit VALUES (\'{0}\',\'{1}\',{2},\'{3}\')".format(ID,api_name,limit[api_name],'2018-01-01 00:00:00'))
          database.select("INSERT INTO api_limit VALUES (\'{0}\',\'{1}\',{2},\'{3}\')".format(ID,api_name,limit[api_name],'2018-01-01 00:00:00'))

register_api()
