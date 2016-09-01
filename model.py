# import heapq
# import time
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


class Neighborhood(db.Model):
    """ Neighborhood information"""

    __tablename__ = "neighborhoods"
    
    neighborhood_id = db.Column(db.Integer, primary_key=True, nullable=False)
    city = db.Column(db.String(50))    
    state = db.Column(db.String(50))
    summary = db.Column(db.Text, nullable=True)
    climate = db.Column(db.Text, nullable=True)

    crime = db.relationship("Crime")
    images = db.relationship("Images")


class Images(db.Model):
    """save image urls"""
    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey(Neighborhood.neighborhood_id), nullable=False)

    neighborhood = db.relationship("Neighborhood")


class School(db.Model):
    """User sign in details"""
    __tablename__ = "schools"

    school_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    gsid = db.Column(db.Integer)
    name = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Float, nullable=True)
    school_type = db.Column(db.String(200), nullable=True)
    grade_range = db.Column(db.String(200), nullable=True)
    parent_rating = db.Column(db.String(15), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    website = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    overview_link = db.Column(db.Text, nullable=True)
    ratings_link = db.Column(db.Text, nullable=True)
    reviews_link = db.Column(db.Text, nullable=True)

    neighborhood_id = db.Column(db.Integer, db.ForeignKey(Neighborhood.neighborhood_id), nullable=False)

    neighborhood = db.relationship("Neighborhood", backref="schools")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<School gsid=%s city=%s name=%s>" % (self.gsid, self.city, self.name)


class CostOfLiving(db.Model):
    """ Cost of living index and price list for each city"""
    #one to one relationship with Neighborhood
    __tablename__ = "cost_of_living"

    cost_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    neighborhood_id = db.Column(db.Integer, db.ForeignKey(Neighborhood.neighborhood_id), nullable=False)
    pollution_index = db.Column(db.String(20), nullable=True)
    traffic_time_index = db.Column(db.String(20), nullable=True)
    groceries_index = db.Column(db.String(20), nullable=True)
    hotel_price_index = db.Column(db.String(20), nullable=True)
    cpi_index = db.Column(db.String(20), nullable=True)
    restaurant_price_index = db.Column(db.String(20), nullable=True)
    property_price_to_income_ratio = db.Column(db.String(20), nullable=True)
    health_care_index = db.Column(db.String(20), nullable=True)
    safety_index = db.Column(db.String(20), nullable=True)
    crime_index = db.Column(db.String(20), nullable=True)
    cpi_and_rent_index = db.Column(db.String(20), nullable=True)
    rent_index = db.Column(db.String(20), nullable=True)
    traffic_inefficiency_index = db.Column(db.String(20), nullable=True)
    purchasing_power_incl_rent_index = db.Column(db.String(20), nullable=True)
    raffic_co2_index = db.Column(db.String(20), nullable=True)
    traffic_index = db.Column(db.String(20), nullable=True)

    neighborhood = db.relationship("Neighborhood", uselist=False, backref="cost_of_living")


class PriceItems(db.Model):
    """ Average price list """
# one to many relationship with Neighborhood

    __tablename__ = "price_items"

    price_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cost_id = db.Column(db.Integer, db.ForeignKey(CostOfLiving.cost_id), nullable=False)
    item_id = db.Column(db.Integer)
    item_name = db.Column(db.Text, nullable=True)
    average_price = db.Column(db.Float, nullable=True)
    lowest_price = db.Column(db.Float, nullable=True)
    highest_price = db.Column(db.Float, nullable=True)
   
    cost_of_living = db.relationship("CostOfLiving", backref="price_list")


class Crime(db.Model):
    """crime index """
# one to one relationship with Neighborhood    
    __tablename__ = "crime_rate"

    crime_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    crime_increasing = db.Column(db.String(120), nullable=True)
    contributors = db.Column(db.String(120), nullable=True) 
    city_id = db.Column(db.String(120), nullable=True) 
    worried_mugged_robbed = db.Column(db.String(120), nullable=True)  
    worried_home_broken = db.Column(db.String(120), nullable=True) 
    problem_property_crimes = db.Column(db.String(120), nullable=True)  
    worried_things_car_stolen = db.Column(db.String(120), nullable=True) 
    level_of_crime = db.Column(db.String(120), nullable=True) 
    worried_insulted = db.Column(db.String(120), nullable=True) 
    problem_drugs = db.Column(db.String(120), nullable=True) 
    worried_attacked = db.Column(db.String(120), nullable=True) 
    problem_violent_crimes = db.Column(db.String(120), nullable=True) 
    worried_skin_ethnic_religion = db.Column(db.String(120), nullable=True) 
    safe_alone_night = db.Column(db.String(120), nullable=True) 
    safe_alone_daylight = db.Column(db.String(120), nullable=True) 
    yearLastUpdate = db.Column(db.String(100), nullable=True) 
    index_crime = db.Column(db.String(100), nullable=True) 
    name = db.Column(db.String(100), nullable=True) 
    monthLastUpdate = db.Column(db.String(100), nullable=True) 
    problem_corruption_bribery = db.Column(db.String(100), nullable=True) 
    index_safety = db.Column(db.String(100), nullable=True) 
    worried_car_stolen = db.Column(db.String(100), nullable=True) 

    neighborhood_id = db.Column(db.Integer, db.ForeignKey(Neighborhood.neighborhood_id), nullable=False)

    neighborhood = db.relationship("Neighborhood")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Crime city=%s crime_index=%s safety_index=%s>" % (self.name, self.index_crime, self.index_safety)


class User(db.Model):
    """User sign in details"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

    favorite = db.relationship("Neighborhood",
                               secondary="favorites",
                               backref="user")
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s zipcode=%s>" % (self.user_id, self.email, self.zipcode)

        
class Favorites(db.Model):
    """ specific user's Favorite neighborhoods"""
   #Association table between User and Neighborhood  
    fav_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey(User.user_id),
                        nullable=False)
   
    neighborhood_id = db.Column(db.Integer,
                                db.ForeignKey(Neighborhood.neighborhood_id),
                                nullable=False)
 
    user = db.relationship("User", backref="favorites")
    neighborhood = db.relationship("Neighborhood", backref="favorites")

    def __repr__(self):
        return "<Favorites neighborhood_id=%s user_id=%s >" % (self.neighborhood_id, self.user_id)
 

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///relocate'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
