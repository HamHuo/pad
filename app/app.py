from flask import Flask
# flask-peewee bindings
from flask_peewee.db import Database
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object('config.Configuration')

db = Database(app)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)