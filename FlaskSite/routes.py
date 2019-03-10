from flask import render_template, flash, url_for, redirect, request
from FlaskSite.forms import RegForm, LoginForm, AlterAccountForm, NewPostForm
from FlaskSite.models import User, Post
from FlaskSite import app, database, bcrypt, rediska
from flask_login import login_user, logout_user, current_user, login_required
import secrets, os
from PIL import Image

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
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


def save_photo(form_photo):
    photo_size = (512, 512)
    resized = Image.open(form_photo)
    resized.thumbnail(photo_size)
    random_name = secrets.token_hex(6)
    f_name, f_ext = os.path.splitext(form_photo.filename)
    photo_filename = f_name + random_name + f_ext
    photo_path = os.path.join(app.root_path, 'static/profile_photos', photo_filename)
    resized.save(photo_path)
    return photo_filename


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    prof_form = AlterAccountForm()
    if prof_form.validate_on_submit():
        if prof_form.photo.data:
            new_photo = save_photo(prof_form.photo.data)
            current_user.image_file = new_photo
        current_user.username = prof_form.username.data
        current_user.email = prof_form.email.data
        if prof_form.password.data:
            current_user.password = bcrypt.generate_password_hash(prof_form.password.data).decode('utf-8')
        database.session.commit()
        flash('The update is successful', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        prof_form.username.data = current_user.username
        prof_form.email.data = current_user.email
    image = url_for('static', filename='profile_photos/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image, form=prof_form)


@app.route("/posts/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('The item has been created', 'success')
        return redirect(url_for('home'))
    return render_template('new_item.html', title='New Item', form=form)
