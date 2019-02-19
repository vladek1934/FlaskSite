from flask import render_template, flash, url_for, redirect
from FlaskSite.forms import RegForm, LoginForm
from FlaskSite.models import User, Post
from FlaskSite import app

posts = [
    {
        'author': 'Caesar',
        'title': '1',
        'content': '100 tenge',
        'date_posted': 'March 20, 2012'
    },
    {
        'author': 'Caesar',
        'title': '2',
        'content': '200 tenge',
        'date_posted': 'january 20, 2018'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'admin':
            flash('Welcome', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed', 'danger')
    return render_template('login.html', title='Login', form=form)
