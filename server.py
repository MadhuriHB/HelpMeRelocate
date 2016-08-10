"""Help me Relocate"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from xml.dom.minidom import parse, parseString

from model import connect_to_db, db, School
from pyzipcode import ZipCodeDatabase

import requests
import os
import untangle

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
zcdb = ZipCodeDatabase()


# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
API_KEY = os.environ.get("API_KEY")
API_KEY_GS = os.environ.get("api_key_gs")


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
    resp = resp.json()
    # direct_image_url = resp.json()['results'][5]['photos'][0]['html_attributions']
    # reference_str = resp.json()['results'][5]['photos'][0]['photo_reference']

    photos_to_show = []

   
    for result in resp['results']:
        photos = result.get("photos")
        if photos:
            photos_to_show.append(photos[0]['photo_reference'])

    payload = {'photoreference': photos_to_show[0], 'maxheight': '400', 'key': API_KEY}

    photo_resp = requests.get("https://maps.googleapis.com/maps/api/place/photo", params=payload)
    
    import pdb; pdb.set_trace()
    print photo_resp.content


    return render_template("show_map.html", zipcode=zipcode, photos_to_show=photo_resp)


@app.route("/show_school/<int:zipcode>")
def show_school_ratings(zipcode):
    """Returns up to 200 schools within 5 miles of ZIP Code 94105 in California"""
    #api_key = "x6qgjcxx3xltlqmxlx3mxqxx"
    zipcode = zcdb[zipcode]
    # latitude = zipcode.latitude
    # longitude = zipcode.longitude
    city = zipcode.city
    state = zipcode.state
    zip1 = zipcode.zip


    
    resp = requests.get("http://api.greatschools.org/schools/nearby?key=%s&state=%s&zip=%s" % (API_KEY_GS, state, zip1))
    
  
    resp = resp.text
    
    #Parse the api response string using xml_dom
    xml_dom = parseString(resp)

    #Get a list of objects with tagname school
    xml_school_list = xml_dom.getElementsByTagName('school')

    #create empty school object list
    schoolObjects = []
    for xmlSchool in xml_school_list:
        #for each school, find the dataif len(xmlSchool.childNodes) > 20:
        i = 0
        while i < len(xmlSchool.childNodes):

            gsid = xmlSchool.childNodes[0].childNodes[0].toxml()
            name = xmlSchool.childNodes[1].childNodes[0].toxml()
            type_of_school = xmlSchool.childNodes[2].childNodes[0].toxml()
            grade_range = xmlSchool.childNodes[3].childNodes[0].toxml()
            rating = xmlSchool.childNodes[5].childNodes[0].toxml()
            city = xmlSchool.childNodes[7].childNodes[0].toxml()
            state = xmlSchool.childNodes[8].childNodes[0].toxml()
            address = xmlSchool.childNodes[12].childNodes[0].toxml()
            phone = xmlSchool.childNodes[13].childNodes[0].toxml()
            website = xmlSchool.childNodes[15].childNodes[0].toxml()
            latitude = xmlSchool.childNodes[17].childNodes[0].toxml()
            longitude = xmlSchool.childNodes[18].childNodes[0].toxml()
            gsSchoolOverviewLink = xmlSchool.childNodes[19].childNodes[0].toxml()
            gsRatinglink = xmlSchool.childNodes[20].childNodes[0].toxml()

            #Create temporary School instance for each school and append it to a list 
            tempSchoolObject = School(gsid=gsid, name=name, schoolType=type_of_school,
                                      grade_range=grade_range, rating=rating,
                                      city=city, state=state, address=address,
                                      phone=phone, website=website,
                                      latitude=latitude, longitude=longitude,
                                      gsSchoolOverviewLink=gsSchoolOverviewLink,
                                      gsRatinglink=gsRatinglink)

            schoolObjects.append(tempSchoolObject)
            
    #import pdb; pdb.set_trace()

    """ FIX ME. Try later if u have more time"""
        # API call to get profile for each school 
        # xml_SchoolProfile = requests.get(
        #     "http://api.greatschools.org/schools/%s/%s?key=%s" 
        #     % (state, gsid, API_KEY_GS))
       

    return render_template ("school_details.html", schoolObjects=schoolObjects)



if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', debug=True)
