from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Ryan'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/user/<username>')
def show_user_profile(username):
    return f'Hi there {username}!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Login', form=form)

