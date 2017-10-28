# config
import os

db_path = os.path.join(os.environ.get('HOME', os.environ.get('USERPROFILE')), 'db', 'example.db')


class Configuration(object):
    DATABASE = {
        'name': db_path,
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = False
    SECRET_KEY = 'shhh86468486h'
