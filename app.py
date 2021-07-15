# main.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask import Flask
from flask import render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required, current_user, logout_user
import requests
import ford_data
import myq
import asyncio
from flask_table import Table, Col

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Declare your table
class ItemTable(Table):
    device_id = Col('ID')
    online = Col('Online')
    device_state = Col('State')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['TEMPLATES_AUTO_RELOAD'] = True
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy(app)
vin = ""

db.metadata.clear()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    ford_email = db.Column(db.String(100))
    ford_password = db.Column(db.String(100))
    ford_vin = db.Column(db.String(17))
    myq_email = db.Column(db.String(100))
    myq_password = db.Column(db.String(100))
    garage_lat = db.Column(db.Float(10))
    garage_lng = db.Column(db.Float(10))

db.metadata.clear()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    ford_email = db.Column(db.String(100))
    ford_password = db.Column(db.String(100))
    ford_vin = db.Column(db.String(17))
    myq_email = db.Column(db.String(100))
    myq_password = db.Column(db.String(100))
    garage_lat = db.Column(db.Float(10))
    garage_lng = db.Column(db.Float(10))

db.create_all()

if __name__ == "main":
    app.run(debug=True)

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('sign-in.html')

@app.route('/profile')
@login_required
def profile():
    done = loop.run_until_complete(myq.main('dak190@pitt.edu','dkdude123?'))
    print(done)

    items = [dict(device_id=done[0][0], online=done[0][1],device_state=str(done[0][2]).title())]
    table = ItemTable(items, classes=['table table-hover'])
    # Print the html
    # print(table.__html__())

    if current_user.garage_lat != None:
        reverse = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(current_user.garage_lat) + ","+ str(current_user.garage_lng) +"&key=AIzaSyAoTPPfyEHD_hjOW42BYq0NafmEe0j9d_o").json()
        reverse_geolocation = reverse.get("results")[0].get("formatted_address")
    else:
        reverse_geolocation=""

    if current_user.ford_vin != None:
        r= ford_data.nhsta(current_user.ford_vin)
    else:
        r=["","","","","",""]

    if r[0] != 'Ford':
        r=["","","","","",""]

    return render_template("blank.html",name=current_user.name,car_vin=r[5],car_make=r[0],car_year=r[2],car_model=r[1],driver_type=r[3],fuel_type=r[4],reverse_geo=reverse_geolocation,garage_table=table.__html__())

@app.route('/profile',  methods=['POST'])
@login_required
def map_post():

    lat = request.form.get('lat')
    lng = request.form.get('lng')

    user=(User.query.filter_by(email=current_user.email)).update({'garage_lat':lat,'garage_lng':lng})
    db.session.commit()

    # if current_user.garage_lat != None:
    #     reverse = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(current_user.garage_lat) + ","+ str(current_user.garage_lng) +"&key=AIzaSyAoTPPfyEHD_hjOW42BYq0NafmEe0j9d_o").json()
    #     reverse_geolocation = reverse.get("results")[0].get("formatted_address")

    # if current_user.ford_vin != None:
    #     r= ford_data.nhsta(current_user.ford_vin)
    # else:
    #     r=["","","","","",""]

    # if r[0] != 'Ford':
    #     r=["","","","","",""]

    return redirect(url_for("profile"))

@app.route('/save_ford',  methods=['POST'])
@login_required
def save_ford_post():
    fordemail=request.form.get('ford-email')
    fordpassword=request.form.get('ford-password')
    vin=request.form.get('vin')

    user=(User.query.filter_by(email=current_user.email)).update({'ford_email':fordemail,'ford_password':fordpassword, 'ford_vin':vin})
    db.session.commit()

    # if current_user.garage_lat != None:
    #     reverse = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(current_user.garage_lat) + ","+ str(current_user.garage_lng) +"&key=AIzaSyAoTPPfyEHD_hjOW42BYq0NafmEe0j9d_o").json()
    #     reverse_geolocation = reverse.get("results")[0].get("formatted_address")

    # if current_user.ford_vin != None:
    #     r= ford_data.nhsta(vin)
    # else:
    #     r=["","","","","",""]

    # if r[0] != 'Ford':
    #     r=["","","","","",""]

    return redirect(url_for("profile"))

@app.route('/login')
def login():
    return render_template("sign-in.html")

@app.route('/save_ford')
def save_ford():
    return render_template("blank.html")

@app.route('/signup')
def signup():
    return render_template('sign-up.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#####################################################################

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),ford_email=None,ford_password=None,ford_vin=None)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page
    
    login_user(user, remember=remember)
    return redirect(url_for('profile'))

######################################################################

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))