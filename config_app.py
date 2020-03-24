import os

# export DATABASE_URL=your postgresql database

owner_list = []  # list of owners` telegram ids


class Config:
    sender_executor = 'python'
    sender_file = 'sender_test.py'
    interval = 2.0
    wait_before_send = 10.0


class DbConfig:
    destination_table = 'fh_table'
    identifier = 'id'
    group_name = 'group_name'
    message = 'message'
    DATABASE_URL = os.environ['DATABASE_URL']
