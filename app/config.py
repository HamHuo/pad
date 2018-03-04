# config
import os

db_path = os.path.join(os.environ.get('HOME', os.environ.get('USERPROFILE')), 'db', 'example.db')

sec = os.getenv('website_secret')


class Configuration(object):
    DATABASE = {
        'name': db_path,
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = False
    SECRET_KEY = sec
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    # TEMPLATES_AUTO_RELOAD = True
