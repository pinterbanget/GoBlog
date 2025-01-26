import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, SignUpForm
from app.models import User
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'title': 'Beautiful day in Portland!',
            'body': 'Today was beautiful broskis. I went to the park and saw a squirrel!'
        },
        {
            'author': {'username': 'Susan'},
            'title': 'The Avengers movie',	
            'body': 'The Avengers movie was so cool! No Way Home still sucks tho #idc'
        },
        {
            'author': {'username': 'Ryan'},
            'title': 'My first post',
            'body': 'This is my first post on this website. I hope you all enjoy it!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/user/<username>')
def show_user_profile(username):
    return f'Hi there {username}!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)