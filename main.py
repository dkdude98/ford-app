from flask import Flask
from flask import render_template
import asyncio
from aiohttp import ClientSession
import myq
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ford'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # app.run(debug=True)

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

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