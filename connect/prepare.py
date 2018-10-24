# -- coding: utf-8 --

def load_pass():
    import yaml
    f = open('../password/database.yml', 'r+')
    password = yaml.load(f)
    return password

def init():
    import MySQLdb as sql
    #import pymysql as sql
    #sql.install_as_MySQLdb()
    
    password = load_pass()
    return sql.connect(user=password['database_user'],
        host=password['ip'],
        password=password['database_password'],
        db=password['dbname'])
