from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a0c7dfa745210394922b8d487c1f70d4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

database = SQLAlchemy(app)

from FlaskSite import routes