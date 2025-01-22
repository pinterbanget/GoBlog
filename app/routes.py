from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/hello')
def hello():
    return "Hello, who are you?"

@app.route('/user/<username>')
def show_user_profile(username):
    return f'Hi there {username}!'


