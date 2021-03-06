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
import asyncio
from flask_table import Table, Col
from aiohttp import ClientSession
import pymyq
import re

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Declare your table
class ItemTable(Table):
    checkbox = Col('')
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
    id = db.Column(db.Integer, primary_key=True)
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
    garage_id = db.Column(db.String(100))

db.metadata.clear()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    garage_id = db.Column(db.String(100))

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

    table=''

    if current_user.myq_email != None:
        try:
            done = loop.run_until_complete(main(current_user.myq_email,current_user.myq_password))
            items = []
            i = 0
            for idx in done:
                items.append(dict(checkbox='',device_id=done[i][0], online=done[i][1],device_state=str(done[i][2]).title()))
                i+=1

            table = ItemTable(items, classes=['table table-hover'])
            table = str(table.__html__())
            table = re.sub(r'(<td></td>)', r'<td><input type="checkbox" name="check1" /></td>', table)
        except:
           table='Invalid MyQ Credentials. Please try again.'
        
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

    return render_template("dashboard.html",name=current_user.name,car_vin=r[5],car_make=r[0],car_year=r[2],car_model=r[1],driver_type=r[3],fuel_type=r[4],reverse_geo=reverse_geolocation,garage_table=table)

@app.route('/profile',  methods=['POST'])
@login_required
def map_post():

    lat = request.form.get('lat')
    lng = request.form.get('lng')

    user=(User.query.filter_by(email=current_user.email)).update({'garage_lat':lat,'garage_lng':lng})
    db.session.commit()

    return redirect(url_for("profile"))

@app.route('/save_ford',  methods=['POST'])
@login_required
def save_ford_post():
    fordemail=request.form.get('ford-email')
    fordpassword=request.form.get('ford-password')
    vin=request.form.get('vin')

    user=(User.query.filter_by(email=current_user.email)).update({'ford_email':fordemail,'ford_password':generate_password_hash(fordpassword, method='sha256'), 'ford_vin':vin})
    db.session.commit()

    return redirect(url_for("profile"))

@app.route('/save_myq',  methods=['POST'])
@login_required
def save_myq_post():
    myqemail=request.form.get('myq-email')
    myqpassword=request.form.get('myq-password')

    user=(User.query.filter_by(email=current_user.email)).update({'myq_email':myqemail,'myq_password':myqpassword})
    db.session.commit()

    return redirect(url_for("profile"))

@app.route('/save_garage',  methods=['POST'])
@login_required
def save_garage_post():

    if request.form.get('check1') == 'on':
        done = loop.run_until_complete(main(current_user.myq_email,current_user.myq_password))
        user=(User.query.filter_by(email=current_user.email)).update({'garage_id':done[0][0]})
        db.session.commit()

    return redirect(url_for("profile"))

@app.route('/save_all',  methods=['POST'])
@login_required
def save_all():

    URL = "https://60f0f45738ecdf0017b0f981.mockapi.io/users"
    data = {'id':current_user.id,'email':current_user.email,'ford_email': current_user.ford_email, 'ford_password':generate_password_hash(current_user.ford_password, method='sha256'),'ford_vin':current_user.ford_vin,'myq_email':current_user.myq_email,'myq_password':current_user.myq_password,'garage_lat':current_user.garage_lat,'garage_lng':current_user.garage_lat,'garage_id':current_user.garage_id}
    r = requests.delete(URL + "/" + str(current_user.id))
    r = requests.post(url = URL, data = data)

    return redirect(url_for("profile"))

@app.route('/login')
def login():
    return render_template("sign-in.html")

@app.route('/save_ford')
def save_ford():
    return render_template("dashboard.html")

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

######################################################################

async def main(email, password) -> None:
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
      myq = await pymyq.login(email, password, websession)

      # Return only garage devices:
      devices = myq.covers
      garages=[None]*(len(devices))
      if len(devices) != 0:
        for idx, device_id in enumerate(
          device_id
          for device_id in devices):
            device = devices[device_id]
            garages[idx] = [device.device_id,device.online,device.state]
            #await device.close()
      return garages