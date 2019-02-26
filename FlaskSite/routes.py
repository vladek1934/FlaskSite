from flask import render_template, flash, url_for, redirect, request
from FlaskSite.forms import RegForm, LoginForm, AlterAccountForm
from FlaskSite.models import User, Post
from FlaskSite import app, database, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        database.session.add(user)
        database.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.rememberpass.data)
            next_page = request.args.get('next')
            flash('Welcome', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    prof_form = AlterAccountForm()
    if prof_form.validate_on_submit():
        current_user.username = prof_form.username.data
        current_user.email = prof_form.email.data
        current_user.password = bcrypt.generate_password_hash(prof_form.password.data).decode('utf-8')
        database.session.commit()
        flash('The update is successful', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        prof_form.username.data = current_user.username
        prof_form.email.data = current_user.email
    image = url_for('static', filename='profile_photos/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image, form=prof_form)
