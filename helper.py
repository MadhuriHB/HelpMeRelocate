ZIPCODE = None

from pyzipcode import ZipCodeDatabase
import bs4
import urllib2
from bs4 import BeautifulSoup
from model import connect_to_db, db, School
from xml.dom.minidom import parse, parseString
import requests
import os
from model import Images
from states import get_state_full_name
#API_KEY = os.environ.get("API_KEY")
API_KEY_GS = os.environ.get("api_key_gs")
API_KEY_NUMBEO = os.environ.get("API_KEY_NUMBEO")


def get_global_zipcodeObject():
    return ZIPCODE 


def find_zipcode_from_input(input_string):
    
    global ZIPCODE
    ZIPCODE = None

    zcdb = ZipCodeDatabase() 

    input_string.strip()
    if input_string.isnumeric():
        ZIPCODE = zcdb[input_string]

    else:
        zipcodeList = zcdb.find_zip(input_string)
        if zipcodeList is not None and len(zipcodeList) >= 1:
            ZIPCODE = zipcodeList[0]
        else: 
            return None
    #print "This is ZIPCODE", ZIPCODE.zip
    return ZIPCODE


def get_city_images():
    #import pdb; pdb.set_trace()
    
    images = []
    #print "This is ZIPCODE in IMAGES ", ZIPCODE.zip
    lat = ZIPCODE.latitude
    lon = ZIPCODE.longitude
   
    min_lat = float(lat) - 0.01
    min_lon = float(lon) - 0.01
    max_lat = float(lat) + 0.01
    max_lon = float(lon) + 0.01
    # print "LATITUDE ", lat
    # print "LONGITUDE!!!!!!!!!!", lon
    resp = requests.get(
        "http://www.panoramio.com/map/get_panoramas.php?set=public&from=0&to=10&minx=%s&miny=%s&maxx=%s&maxy=%s&size=medium&mapfilter=true"
        % (min_lon, min_lat, max_lon, max_lat))
    resp = resp.json()
    photos = resp['photos']
    photoUrls = []
    
    for photo in photos:
        url = photo['photo_url']       
        photoUrls.append(url)
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, "html.parser")
        image = soup.find(id="main-photo_photo", src=True)
        images.append(image)

    return images


def get_city_summary():
    """ get summary and climate from wikipedia """
    #import pdb; pdb.set_trace()
    # Wikipedia is a wrapper on wikipedia API 
    import wikipedia

    global ZIPCODE
    city = ZIPCODE.city
    state_abbr = ZIPCODE.state
    state_full_name = get_state_full_name(state_abbr)
    # page = wikipedia.page(city + " " + state)
    # summary = page.summary
    
    results = wikipedia.search(city+" "+state_full_name, results=5, suggestion=False)
    first_page = results[0]
    wiki_page = wikipedia.page(first_page)
    summary = wiki_page.summary
    climate = wiki_page.section("Climate")
    
    return [summary, climate]
    

def get_school_rating(tempSchoolObject):
    #import pdb; pdb.set_trace()
    #from django.utils.encoding import smart_str, smart_unicode
    #putting resp in smart_str from django also works but .format.encode used below is the easy way
    
    state = tempSchoolObject.state
    gsid = tempSchoolObject.gsid
    
    #import pdb; pdb.set_trace()
    
    resp = requests.get("http://api.greatschools.org/school/tests/%s/%s?key=%s" % (state, gsid, API_KEY_GS))  
    #resp = resp.text
    resp = resp.text
    #Parse the api response string using xml_dom
    
    xml_dom = parseString(u'{}'.format(resp).encode('utf-8'))

    #xml_dom = parseString(smart_str(resp))

    rank_Elements = xml_dom.getElementsByTagName("rank")
    rank_Element = rank_Elements[0]
    # check if element is not None before using
    if rank_Element: 
        rank_children = rank_Element.childNodes
        for rank_child in rank_children:
            if rank_child.nodeName == "score":
                score = rank_child.firstChild.data
                tempSchoolObject.score = score 
            else:
                tempSchoolObject.score = None
    return tempSchoolObject


def get_schools():
    #get schools for the zipcode
    #from django.utils.encoding import smart_str, smart_unicode
    #import pdb; pdb.set_trace()
    global ZIPCODE
    state = ZIPCODE.state
    zipcode = ZIPCODE.zip
    #Api call to get school information
    resp = requests.get("http://api.greatschools.org/schools/nearby?key=%s&state=%s&zip=%s" % (API_KEY_GS, state, zipcode))
    
    resp = resp.text
   

    #Parse the api response string using xml_dom
    #Make the resp accept the unicode characters
    xml_dom = parseString(u'{}'.format(resp).encode('utf-8'))
    #xml_dom = parseString(smart_str(resp))

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
        tempSchoolObject = School(gsid=node_dict.get("gsId"), name=node_dict.get("name"), school_type=node_dict.get("type"),
                                  grade_range=node_dict.get("gradeRange"), city=node_dict.get("city"),
                                  state=node_dict.get("state"), address=node_dict.get("address"),
                                  phone=node_dict.get("phone"), website=node_dict.get("website"),
                                  latitude=node_dict.get("lat"), longitude=node_dict.get("lon"),
                                  parent_rating=node_dict.get("parentRating"),
                                  overview_link=node_dict.get("overviewLink"), 
                                  ratings_link=node_dict.get("ratingsLink"),
                                  reviews_link=node_dict.get("reviewsLink"))
        
        # call function to get great school rating for each school

        tempSchoolObject1 = get_school_rating(tempSchoolObject)     
        schoolObjects.append(tempSchoolObject1)
    
    return schoolObjects 


def find_nearest_city():
    """finds the nearest big city for the user city
       to find cost of living
    """
    #import pdb; pdb.set_trace   

    ZIPCODE = get_global_zipcodeObject()
    from geopy.distance import vincenty
    
    myCitylat = ZIPCODE.latitude
    myCitylon = ZIPCODE.longitude
    
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

        #city lat and long from citiobject that we are comparing
        isNearCity = (cityObject['latitude'], cityObject['longitude']) 
        
        #geopy function vincenty to calculate the distance
        distance = vincenty(myCity, isNearCity).miles  
        if distance < nearestDistance:
            nearestDistance = distance
            nearestCityObject = cityObject
   
    return nearestCityObject


def row2dict(row):
    dictionary = {}
    for column in row.__table__.columns:
        dictionary[column.name] = str(getattr(row, column.name))

    return dictionary


def hash_password(password):
    import hashlib
    hash1 = hashlib.md5(password)
    hashed = hash1.hexdigest()
    return hashed














