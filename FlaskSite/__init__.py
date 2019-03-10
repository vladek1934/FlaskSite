from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_redis import FlaskRedis
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a0c7dfa745210394922b8d487c1f70d4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
rediska = FlaskRedis(app)

rediska.set('Accounts created today', '0')
rediska.set('Logins today', '0')
rediska.set('Added posts today', '0')
rediska.set('Last restart of the site', datetime.utcnow().strftime('%Y-%m-%d %H:%M'))




login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please login before trying to access this page'

from FlaskSite import routes

#for ubuntu virtualenv use python3.7 -m pip install x (ex flask)