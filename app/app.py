import os
from flask import Flask
# flask-peewee bindings
from flask_peewee.db import Database
from config import ppoi_secret

# from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Configuration')

db = Database(app)
