from flask import render_template
from app import app

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


