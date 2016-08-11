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
    pass
    resp = requests.get("http://www.panoramio.com/map/get_panoramas.php?set=public&from=0&to=20&minx=-34&miny=-118&maxx=34&maxy=118&size=medium&mapfilter=true")
    print "This is the response!!!!!!!!!!!!!", resp.json()

    return render_template("show_map.html", zipcode=zipcode)


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

    #Api call to get school information
    resp = requests.get("http://api.greatschools.org/schools/nearby?key=%s&state=%s&zip=%s" % (API_KEY_GS, state, zip1))
      
    resp = resp.text
    
    #Parse the api response string using xml_dom
    xml_dom = parseString(resp)

    #Get a list of objects with tagname school
    xml_school_list = xml_dom.getElementsByTagName('school')
    
    node_dict = {}
    
    #create empty school object list
    schoolObjects = []

    for xmlSchool in xml_school_list:
        sChildNodes = xmlSchool.childNodes
           
        for childnode in sChildNodes:
            name = childnode.nodeName
            if childnode.hasChildNodes():
                node_dict[name] = childnode.childNodes[0].toxml()           
            else:
                node_dict[name] = childnode.toxml()

        #Temporary school object for each school         
        tempSchoolObject = School(gsid=node_dict.get("gsId"), name=node_dict.get("name"), schoolType=node_dict.get("type"),
                                  gradeRange=node_dict.get("gradeRange"), city=node_dict.get("city"),
                                  state=node_dict.get("state"), address=node_dict.get("address"),
                                  phone=node_dict.get("phone"), website=node_dict.get("website"),
                                  latitude=node_dict.get("lat"), longitude=node_dict.get("lon"),
                                  parentRating=node_dict.get("parentRating"),
                                  overviewLink=node_dict.get("overviewLink"), 
                                  ratingsLink=node_dict.get("ratingsLink"),
                                  reviewsLink=node_dict.get("reviewsLink"))
    
        schoolObjects.append(tempSchoolObject)
            
    return render_template("school_details.html", schoolObjects=schoolObjects)

    # """ FIX ME. Try later if u have more time"""
    #     # API call to get profile for each school 
    #     # xml_SchoolProfile = requests.get(
    #     #     "http://api.greatschools.org/schools/%s/%s?key=%s" 
    #     #     % (state, gsid, API_KEY_GS))       


if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', debug=True)
