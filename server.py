"""Help me Relocate"""
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, flash, session, jsonify

from flask_debugtoolbar import DebugToolbarExtension
from xml.dom.minidom import parse, parseString

from model import connect_to_db, db, School, User
from pyzipcode import ZipCodeDatabase


from helper import get_global_zipcodeObject, find_zipcode_from_input, get_city_images, get_schools
from helper import find_nearest_city, get_city_summary

import requests
import os

import model


app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


zcdb = ZipCodeDatabase()
# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ.get("API_KEY")
API_KEY_GS = os.environ.get("api_key_gs")
API_KEY_NUMBEO = os.environ.get("API_KEY_NUMBEO")


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("index.html")


@app.route("/show_city")
def show_city_images():
   # import pdb; pdb.set_trace()

    input_string = request.args.get("zipcode")

    if find_zipcode_from_input(input_string):
        
        #call function from helper to get images    
        images = get_city_images()                 
        zipcodeObject = get_global_zipcodeObject()
        city = zipcodeObject.city
        state = zipcodeObject.state
        #call function from helper to get summary
        summary, climate = get_city_summary()
    else:
        redirect("/")

    return render_template("show_city_info.html", city=city, state=state, images=images, summary=summary, climate=climate)


@app.route("/add-to-favorites", methods=["POST"])
def add_to_favorites():
    city = request.form.get("id")

    # put this in a "favorites" table?
    # favorite
    favorite = Favorites()

    return jsonify(status="success", id=city)




@app.route("/show_school")
def show_school_ratings():
    """Returns up to 200 schools within 5 miles of zipcode"""
    
    schoolObjects = get_schools()
    
    return render_template("school_details.html", schoolObjects=schoolObjects)

    


@app.route("/cost_of_living/")
def show_cost_of_living():
    """calculate cost of living for city"""
    #import pdb; pdb.set_trace()

    city = find_nearest_city()
  
    resp = requests.get("http://numbeo.com/api/city_prices?api_key=%s&city_id=%s" % (API_KEY_NUMBEO, city['city_id']))
    resp = resp.json()
    prices = resp['prices']
    #keys = ['item_id', u'item_name', u'average_price', u'lowest_price', u'highest_price']
    resp_indexes = requests.get("http://numbeo.com/api/indices?api_key=%s&city_id=%s" % (API_KEY_NUMBEO, city['city_id']))
    resp_indexes = resp_indexes.json()

    return render_template("cost_of_living.html", prices=prices, indexes=resp_indexes)



@app.route("/crime_rate")
def show_crime_rate():
    """show crime rate for the city"""
    
    city = find_nearest_city()
    resp = requests.get("http://numbeo.com//api/city_crime?api_key=%s&city_id=%s" % (API_KEY_NUMBEO, city['city_id']))
    crime_data = resp.json()

    return render_template("crime_rate.html", crime_data=crime_data)




@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    #age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("You are not registered. Please register and then Login")
        return render_template("register_form.html")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You are now Logged in")
    return redirect("/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")



if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', debug=True)
