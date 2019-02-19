from FlaskSite import database
from datetime import datetime


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(60), unique=True, nullable=False)
    image_file = database.Column(database.String(20), nullable=False, default='default.jpg')
    password = database.Column(database.String(60), nullable=False)
    posts = database.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(80), nullable=False)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    content = database.Column(database.Text, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
