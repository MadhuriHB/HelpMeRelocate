"""Help me Relocate"""
from jinja2 import StrictUndefined

from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from xml.dom.minidom import parse, parseString

from model import connect_to_db, db, School
from pyzipcode import ZipCodeDatabase
#import geopy

#import urllib
import urllib2
from bs4 import BeautifulSoup


import requests
import os


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


@app.route('/show_city')
def show_city_info():
    """find the city and state for the zipcode input"""
    zipcode = request.args.get("zipcode")
    zipcode = zcdb[zipcode]
       
    return render_template("show_city_info.html", zipcode=zipcode)


@app.route("/show_city/<int:zipcode>")
def show_city_images(zipcode):
    zipcode = zcdb[zipcode]
    lat = zipcode.latitude
    lon = zipcode.longitude
    min_lat = float(lat) - 0.01
    min_lon = float(lon) - 0.01
    max_lat = float(lat) + 0.01
    max_lon = float(lon) + 0.01
    print "LATITUDE ", lat
    print "LONGITUDE!!!!!!!!!!", lon
    resp = requests.get(
        "http://www.panoramio.com/map/get_panoramas.php?set=public&from=0&to=10&minx=%s&miny=%s&maxx=%s&maxy=%s&size=medium&mapfilter=true"
        % (min_lon, min_lat, max_lon, max_lat))
    resp = resp.json()
    photos = resp['photos']
    photoUrls = []
    images = []
    for photo in photos:
        url = photo['photo_url']
        photoUrls.append(url)
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")
        image = soup.find(id="main-photo_photo", src=True)
        images.append(image)
        #print "Image is here!!!!!!!!!!!!", image

    #print "These are the url_list !!!!!!!!!!!!!", photoUrls
    return render_template("show_map.html", images=images)


@app.route("/show_school/<int:zipcode>")
def show_school_ratings(zipcode):
    """Returns up to 200 schools within 5 miles of ZIP Code 94105 in California"""
    #api_key = "x6qgjcxx3xltlqmxlx3mxqxx"
    zipcode = zcdb[zipcode]
    # latitude = zipcode.latitude
    # longitude = zipcode.longitude
    #city = zipcode.city
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


def find_nearest_city(zipcode):
    """finds the nearest big city for the user city
       to find cost of living
    """
    
    from geopy.distance import vincenty
    zipcode = zcdb[zipcode]
    myCity = zipcode.city
    #myState = zipcode.state
    myCitylat = zipcode.latitude
    myCitylon = zipcode.longitude
    
    #stores all city objects in US 
    cityObjects = []

    # get all cities from numbeo api call 
    resp = requests.get("http://numbeo.com/api/cities?api_key="+API_KEY_NUMBEO)
   
    resp = resp.json()

    for city_dict in resp.values()[0]:
        # get cities from US only
        if city_dict['country'] == 'United States':  
            cityObjects.append(city_dict)

    nearestCityObject = None
    nearestDistance = 1000

    #city for the zipcode that user entered
    myCity = (myCitylat, myCitylon)

    for cityObject in cityObjects:

        #city lat and long from citiobject that we are comapring
        isNearCity = (cityObject['latitude'], cityObject['longitude']) 
        
        #geopy function vincenty to calculate the distance
        distance = vincenty(myCity, isNearCity).miles  
        if distance < nearestDistance:
            nearestDistance = distance
            nearestCityObject = cityObject

    #print nearestCityObject      

    return nearestCityObject


@app.route("/cost_of_living/<int:zipcode>")
def show_cost_of_living(zipcode):
    """calculate cost of living for city"""
    #import pdb; pdb.set_trace()
    city = find_nearest_city(int(zipcode))
    print "This is city object!!!!!!!", city
    resp = requests.get("http://numbeo.com/api/city_prices?api_key=%s&city_id=%s" % (API_KEY_NUMBEO, city['city_id']))
    resp = resp.json()
    prices = resp['prices']

    return render_template("cost_of_living.html", prices)


@app.route("/crime_rate/<int:zipcode>")
def show_crime_rate(zipcode):
    """show crime rate for the city"""
    #import pdb; pdb.set_trace()
    city = find_nearest_city(zipcode)
    resp = requests.get("http://numbeo.com//api/city_crime?api_key=%s&city_id=%s" % (API_KEY_NUMBEO, city['city_id']))
    crime_data = resp.json()

    return render_template("crime_rate.html", crime_data=crime_data)



if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0', debug=True)
