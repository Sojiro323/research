# coding: utf-8
from sshtunnel import SSHTunnelForwarder
from . import database



def check(userID):

    with SSHTunnelForwarder(
        (password['host'], password['local_port']),
        ssh_host_key= None,
        ssh_pkey=None,
        ssh_username=password['ssh_username'],
        ssh_password=password['ssh_password'],
        remote_bind_address=(password['ip'], password['database_port'])
        ) as ssh:

            return database.check(userID)


def select(sql):

    with SSHTunnelForwarder(
        (password['host'], password['local_port']),
        ssh_host_key= None,
        ssh_pkey=None,
        ssh_username=password['ssh_username'],
        ssh_password=password['ssh_password'],
        remote_bind_address=(password['ip'], password['database_port'])
        ) as ssh:

            return database.select(sql)

def update(database, values):

    with SSHTunnelForwarder(
        (password['host'], password['local_port']),
        ssh_host_key= None,
        ssh_pkey=None,
        ssh_username=password['ssh_username'],
        ssh_password=password['ssh_password'],
        remote_bind_address=(password['ip'], password['database_port'])
        ) as ssh:

            return database.update(database, values)



def insert(database, values):

    with SSHTunnelForwarder(
        (password['host'], password['local_port']),
        ssh_host_key= None,
        ssh_pkey=None,
        ssh_username=password['ssh_username'],
        ssh_password=password['ssh_password'],
        remote_bind_address=(password['ip'], password['database_port'])
        ) as ssh:

            return database.insert(userID)

def register_api():

    with SSHTunnelForwarder(
        (password['host'], password['local_port']),
        ssh_host_key= None,
        ssh_pkey=None,
        ssh_username=password['ssh_username'],
        ssh_password=password['ssh_password'],
        remote_bind_address=(password['ip'], password['database_port'])
        ) as ssh:

            return database.register_api()
