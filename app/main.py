# main.py
from flask import Blueprint, render_template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.run(debug=True)

db.init_app(app)

@app.route('/')
def index():
    return render_template('sign-in.html')

@app.route('/profile')
def profile():
    return 'Profile'

@app.route('/login')
def login():
    return render_template("sign-in.html")

@app.route('/signup')
def signup():
    return render_template('sign-up.html')

@app.route('/logout')
def logout():
    return 'Logout'