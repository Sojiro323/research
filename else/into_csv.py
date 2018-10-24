L# coding: utf-8
import MySQLdb
import os
import yaml
import gzip

f = open('password/database.yml', 'r+')
password = yaml.load(f)

def insert(csv):

  conn = MySQLdb.connect(user=password['database_user'],
    host=password['ip'],
    password=password['database_password'],
    db=password['dbname'])
  c = conn.cursor()

  # レコードの登録
  for u in t:
      sql = "LOAD DATA LOCAL INFILE \'{0}\' INTO TABLE testtable FIELDS TERMINATED BY \',\';".format(csv)
      c.execute(sql)
      conn.commit()

  c.close()
  conn.close()


while(1):
  print("input number")

  d  = input('>>> ')

  break

path = "./" + d  +"/csv/"

files = os.listdir(path)
for f in files:
    insert(path + f)
    j = open("./" + d + "_into.txt" , 'a')
    j.write(f + '\n')
    j.close()
