"""Help me Relocate"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, City, User, db
from pyzipcode import ZipCodeDatabase
zcdb = ZipCodeDatabase()
import requests
import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ.get("API_KEY")


@app.route('/')
def index():
    """Homepage."""

    return render_template("index.html")


@app.route('/show_city')
def show_city_info():
    """find the city and state for the zipcode input"""
    zipcode = request.args.get("zipcode")
    zipcode = zcdb[zipcode]
       
    return render_template("show_city_info.html", zipcode=zipcode)


@app.route("/show_city/<int:zipcode>")
def show_city_on_map(zipcode):
    zipcode = zcdb[zipcode]
    latitude = zipcode.latitude
    longitude = zipcode.longitude
    resp = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=50&key=%s" % (latitude, longitude, API_KEY))
    
    reference_str = resp.json()['results'][0]['reference']
    # print reference_str
    # print API_KEY
    payload = {'photoreference': reference_str, 'maxheight': '400', 'key': API_KEY}

    photo_resp = requests.get("https://maps.googleapis.com/maps/api/place/photo", params=payload)
    print photo_resp.text
   
    # import pdb; pdb.set_trace()

    return render_template("show_map.html", zipcode=zipcode)


if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', debug=True)
