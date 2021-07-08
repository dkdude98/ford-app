from flask import Flask
from flask import render_template
import asyncio
from aiohttp import ClientSession
import myq
from flask import Blueprint
from . import db

main = Blueprint('main', __name__)

#app = Flask(__name__)

#def clever_function():
#    return u'HELLO'

# @app.route("/")
# def index():
# 	return render_template("sign-in.html")

@main.route('/')
def index():
    return render_template("sign-in.html")

@main.route('/profile')
def profile():
    return 'Profile'