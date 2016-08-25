"""Help me Relocate"""
from jinja2 import StrictUndefined
#from sqlalchemy import func

from flask import Flask, render_template, request, redirect, flash, session, jsonify

from flask_debugtoolbar import DebugToolbarExtension
#from xml.dom.minidom import parse, parseString

from model import connect_to_db, db, School, User, Neighborhood, Images, CostOfLiving, PriceItems, Crime, Favorites 
from pyzipcode import ZipCodeDatabase


from helper import get_global_zipcodeObject, find_zipcode_from_input, get_city_images, get_schools, row2dict 
from helper import find_nearest_city, get_city_summary, hash_password

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


@app.route("/show_city")
def show_city_data():
    #import pdb; pdb.set_trace()

    input_string = request.args.get("zipcode")

    ZIPCODE = find_zipcode_from_input(input_string)
    zipcode = ZIPCODE.zip
    if zipcode is not None:   
        is_neighborhood_in_db = Neighborhood.query.filter_by(neighborhood_id=zipcode).first()
        #check if neighborhood is already in DB 
        if is_neighborhood_in_db is None:
            #call function from helper to get images    
            images = get_city_images()  
            image_urls = [image['src'] for image in images]
            
            zipcodeObject = get_global_zipcodeObject()
            city = zipcodeObject.city
            state = zipcodeObject.state
            #call function from helper to get summary, climate
            summary, climate = get_city_summary()
            #make neighborhood instance and store in DB
            neighborhood = Neighborhood(neighborhood_id=zipcode, summary=summary, climate=climate, city=city, state=state)
            db.session.add(neighborhood)
            db.session.commit()
            #store each image url in DB
            if len(images) > 0:
                for image in images:
                    picture = Images(neighborhood_id=zipcode, image_url=image["src"])
                    db.session.add(picture)
                    db.session.commit()
        
        else:
           
            #Fetch the data for zipcode from database 
            neighborhood = Neighborhood.query.filter_by(neighborhood_id=zipcode).first()
            city = neighborhood.city
            state = neighborhood.state
            summary = neighborhood.summary
            climate = neighborhood.climate
            images = Images.query.filter_by(neighborhood_id=zipcode).all()
            image_urls = [image.image_url for image in images]
            
    else:
        redirect("/")

    return render_template("show_city_info.html", city=city, state=state, images=image_urls, summary=summary, climate=climate)


@app.route("/add-to-favorites", methods=["POST"])
def add_to_favorites():
    #import pdb; pdb.set_trace()
    iD = request.form.get("id")

    #check if user is logged in 
    if 'user_id' in session.keys(): 
        user_id = session["user_id"] 
        ZIPCODE = get_global_zipcodeObject()
        zipcode = ZIPCODE.zip
        city = ZIPCODE.city
       
        #check to see if favorite is already in DB
        is_fav_in_db = Favorites.query.filter_by(neighborhood_id=zipcode).first()
        
        if is_fav_in_db is None:
            #favorite instance to sotre in DB
            favorite = Favorites(user_id=user_id, neighborhood_id=zipcode)
            db.session.add(favorite)
            db.session.commit()
            flash("%s %s is addded as your Favorite" % (city, zipcode))
            return jsonify(id=iD)

    return jsonify(status="success", id=iD)


@app.route("/show_school")
def show_school_details():
    """shows up to 200 schools within 5 miles of zipcode"""
    #import pdb; pdb.set_trace()
    ZIPCODE = get_global_zipcodeObject()
    zipcode = ZIPCODE.zip
    #zip_lat_lon = {'lat': ZIPCODE.latitude, 'lon': ZIPCODE.longitude}
    school = School.query.filter_by(neighborhood_id=zipcode).first()
    if school is None:
        schoolObjects = get_schools()
        for schoolObject in schoolObjects:
            schoolObject.neighborhood_id = zipcode
            db.session.add(schoolObject)
            db.session.commit()
    else:
        schoolObjects = School.query.filter_by(neighborhood_id=zipcode).all()

    #return render_template("school_details.html", zip_lat_lon=zip_lat_lon, schoolObjects=schoolObjects)
    return render_template("schools_on_map.html", schoolObjects=schoolObjects)


@app.route("/school_map_data")
def show_schools_on_map():

    ZIPCODE = get_global_zipcodeObject()
    zipcode = ZIPCODE.zip
    kwargs = {'neighborhood_id': zipcode, 'school_type': 'public'}
    schoolObjects = School.query.filter_by(**kwargs).all()
    schools_list = [row2dict(schoolObject) for schoolObject in schoolObjects]
    schools = {'schools': schools_list}
    return jsonify(schools)


@app.route("/cost_of_living/")
def show_cost_of_living():
    """calculate cost of living for city"""
    
    city = find_nearest_city()

    ZIPCODE = get_global_zipcodeObject()
    zipcode = ZIPCODE.zip
    cost_of_living = CostOfLiving.query.filter_by(neighborhood_id=zipcode).first()
    if cost_of_living is None:     
        resp = requests.get("http://numbeo.com/api/city_prices?api_key=%s&city_id=%s" % (API_KEY_NUMBEO, city['city_id']))
        resp = resp.json()
        prices = resp['prices']
        resp_indexes = requests.get("http://numbeo.com/api/indices?api_key=%s&city_id=%s" % (API_KEY_NUMBEO, city['city_id']))
        resp_indexes = resp_indexes.json()
        resp_indexes['neighborhood_id'] = zipcode
        cost_of_living = CostOfLiving(neighborhood_id=resp_indexes.get('neighborhood_id'),
                                      pollution_index=resp_indexes.get('pollution_index'),
                                      traffic_time_index=resp_indexes.get('traffic_time_index'),
                                      groceries_index=resp_indexes.get('groceries_index'),
                                      hotel_price_index=resp_indexes.get('hotel_price_index'),                                      
                                      cpi_index=resp_indexes.get('cpi_index'),
                                      restaurant_price_index=resp_indexes.get('restaurant_price_index'),
                                      property_price_to_income_ratio=resp_indexes.get('property_price_to_income_ratio'),
                                      health_care_index=resp_indexes.get('health_care_index'),
                                      safety_index=resp_indexes.get('safety_index'), 
                                      crime_index=resp_indexes.get('crime_index'), 
                                      cpi_and_rent_index=resp_indexes.get('cpi_and_rent_index'),
                                      rent_index=resp_indexes.get('rent_index'),
                                      traffic_inefficiency_index=resp_indexes.get('traffic_inefficiency_index'),
                                      purchasing_power_incl_rent_index=resp_indexes.get('purchasing_power_incl_rent_index'),
                                      raffic_co2_index=resp_indexes.get('raffic_co2_index'),
                                      traffic_index=resp_indexes.get('traffic_index')
                                      )  

        db.session.add(cost_of_living)
        db.session.commit()          
        #price items
        cost_id = cost_of_living.cost_id
    	for price_dict in prices:
    		price_item = PriceItems(cost_id=cost_id,
    								item_id=price_dict.get('item_id'),
    								item_name=price_dict.get('item_name'),
    								average_price=price_dict.get('average_price'),
    								lowest_price=price_dict.get('lowest_price'),
    								highest_price=price_dict.get('highest_price')
    							    )

    		db.session.add(price_item)
    		db.session.commit()
    else:
    	prices=[]
    	cost_id = cost_of_living.cost_id
    	resp_indexes_object = CostOfLiving.query.filter_by(neighborhood_id=zipcode).first() 
    	resp_indexes = row2dict(resp_indexes_object)
    
       	priceObjects = PriceItems.query.filter_by(cost_id=cost_id).all()   
       
       	for priceObject in priceObjects:
       		price = row2dict(priceObject)
       		prices.append(price)
       
    return render_template("cost_of_living.html", prices=prices, indexes=resp_indexes)


# @app.route("/cost_of_living")
# def show_cost_of_living_chart():
#     """bar chart for cost of living"""
#     ZIPCODE = get_global_zipcodeObject()
#     zipcode = ZIPCODE.zip
#     resp_indexes_object = CostOfLiving.query.filter_by(neighborhood_id=zipcode).first()
#     resp_indexes = row2dict(resp_indexes_object)
    




@app.route("/crime_rate")
def show_crime_rate():
    """show crime rate for the city"""
    
    city = find_nearest_city()
    ZIPCODE = get_global_zipcodeObject()
    zipcode = ZIPCODE.zip
    crime_rate = Crime.query.filter_by(neighborhood_id=zipcode).first()
    if crime_rate is None:

        resp = requests.get("http://numbeo.com//api/city_crime?api_key=%s&city_id=%s" % (API_KEY_NUMBEO, city['city_id']))
        crime_data = resp.json()
        crime_data['neighborhood_id'] = zipcode
      	crime_rate = Crime(neighborhood_id=crime_data.get('neighborhood_id'),
	                       crime_increasing=crime_data.get('crime_increasing'),
	                       contributors=crime_data.get('contributors'),
	                       city_id=crime_data.get('city_id'),
	                       worried_mugged_robbed=crime_data.get('worried_mugged_robbed'),
	                       worried_home_broken=crime_data.get('worried_home_broken'),
	                       problem_property_crimes=crime_data.get('problem_property_crimes'),
	                       worried_things_car_stolen=crime_data.get('worried_things_car_stolen'),
	                       level_of_crime=crime_data.get('level_of_crime'),
	                       worried_insulted=crime_data.get('worried_insulted'),
	                       problem_drugs=crime_data.get('problem_drugs'),
	                       worried_attacked=crime_data.get('worried_attacked'),
	                       problem_violent_crimes=crime_data.get('problem_violent_crimes'),
	                       worried_skin_ethnic_religion=crime_data.get('worried_skin_ethnic_religion'),
	                       safe_alone_night=crime_data.get('safe_alone_night'),
	                       safe_alone_daylight=crime_data.get('safe_alone_daylight'),
	                       yearLastUpdate=crime_data.get('yearLastUpdate'),
	                       index_crime=crime_data.get('index_crime'),
	                       name=crime_data.get('name'),
	                       monthLastUpdate=crime_data.get('monthLastUpdate'),
	                       problem_corruption_bribery=crime_data.get('problem_corruption_bribery'),
	                       index_safety=crime_data.get('index_safety'),
	                       worried_car_stolen=crime_data.get('worried_car_stolen')
                		  )

        db.session.add(crime_rate)
        db.session.commit()
    else:
        crime_data = Crime.query.filter_by(neighborhood_id=zipcode).first()
        crime_data = row2dict(crime_data)
    	
    return render_template("crime_rate.html")


@app.route('/crime-chart-data')
def give_chart_data():
    #import pdb; pdb.set_trace()
    import math
    ZIPCODE = get_global_zipcodeObject()
    zipcode = ZIPCODE.zip
    crime_data = Crime.query.filter_by(neighborhood_id=zipcode).first()
    crime_data = row2dict(crime_data)

    del crime_data['city_id']
    del crime_data['neighborhood_id']
    del crime_data['crime_id']
    del crime_data['name']
    del crime_data['yearLastUpdate']
    del crime_data['monthLastUpdate']
    del crime_data['index_safety']
    del crime_data['contributors']
    del crime_data['index_crime']
    del crime_data['safe_alone_night']
    del crime_data['safe_alone_daylight']
    for crime in crime_data:

        value = float(crime_data[crime])
        crime_data[crime] = math.ceil(value * 100)/100
        #print "CRIME VALUES!!!!!!!", crime_data[crime]
    #---------------------------------------   
    # To do later. For changing the keys to better names.
    # d = {'x':1, 'y':2, 'z':3}
    # d1 = {'x':'a', 'y':'b', 'z':'c'}
    # new_dict = dict((d1[key], value) for (key, value) in d.items())   
    #-----------------------------------------
    return jsonify(crime_data)    


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""
    #import pdb; pdb.set_trace()
    # Get form variables
    email = request.form.get("email")
    password = request.form.get("password")
    password_hashed = hash_password(password)
    zipcode = request.form.get("zipcode")
    zipcode = int(zipcode)

    new_user = User(email=email, password=password_hashed, zipcode=zipcode)

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
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("You are not registered. Please register and then Login")
        return render_template("register_form.html")

    if user.password != hash_password(password):
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
