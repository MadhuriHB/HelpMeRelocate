import heapq
import time
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

class Neighborhood(db.Model):
    """ Neighborhood information"""

    __tablename__ = "neighborhood"
    
    neighborhood_id = db.Column(db.String(10), primary_key=True, nullable=False)
    #neighborhood_image = 

    #map
    #image



class School(db.Model):
    """User sign in details"""
    __tablename__ = "schools"

    gsid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    schoolType = db.Column(db.String(64), nullable=True)
    gradeRange = db.Column(db.String(64), nullable=True)
    parentRating = db.Column(db.String(15), nullable=True)
    city = db.Column(db.String(15), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(64), nullable=False)
    website = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.String(64), nullable=False)
    longitude = db.Column(db.String(64), nullable=False)
    overviewLink = db.Column(db.Text, nullable=True)
    ratingsLink = db.Column(db.Text, nullable=True)
    reviewsLink = db.Column(db.Text, nullable=True)

    neighborhood_id = db.Column(db.Integer, db.ForeignKey(Neighborhood.neighborhood_id), nullable=False)

    neighborhood = db.relationship("Neighborhood", backref="schools")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<School gs_id=%s zipcode=%s name=%s>" % (self.gs_id, self.zipcode, self.name)


class CostOfLiving(db.Model):
    """ Cost of living index and price list for each city"""
#one to one relationship with Neighborhood
    __tablename__ = "costOfLiving"


    neighborhood = db.relationship("Neighborhood", db.backref("costOfLiving", uselist=False))


class PriceList(db.Model):
    """ Average price list """
# one to many relationship with Neighborhood

    __tablename__ = "priceList"
    neighborhood = db.relationship("Neighborhood", backref="priceList")


class Crime(db.Model):
    """crime index """
# one to one relationship with Neighborhood    
    __tablename__ = "crimeRate"

    crime_increasing = db.Column(db.String(20), nullable=True)
    contributors = db.Column(db.String(20), nullable=True) 
    city_id = db.Column(db.String(20), nullable=True) 
    worried_mugged_robbed = db.Column(db.String(20), nullable=True)  
    worried_home_broken = db.Column(db.String(20), nullable=True) 
    problem_property_crimes = db.Column(db.String(20), nullable=True)  
    worried_things_car_stolen = db.Column(db.String(20), nullable=True) 
    level_of_crime = db.Column(db.String(20), nullable=True) 
    worried_insulted = db.Column(db.String(20), nullable=True) 
    problem_drugs = db.Column(db.String(20), nullable=True) 
    worried_attacked = db.Column(db.String(20), nullable=True) 
    problem_violent_crimes = db.Column(db.String(20), nullable=True) 
    worried_skin_ethnic_religion = db.Column(db.String(20), nullable=True) 
    safe_alone_night = db.Column(db.String(20), nullable=True) 
    safe_alone_daylight = db.Column(db.String(20), nullable=True) 
    yearLastUpdate = db.Column(db.String(20), nullable=True) 
    index_crime = db.Column(db.String(20), nullable=True) 
    name = db.Column(db.String(20), nullable=True) 
    monthLastUpdate = db.Column(db.String(20), nullable=True) 
    problem_corruption_bribery = db.Column(db.String(20), nullable=True) 
    index_safety = db.Column(db.String(20), nullable=True) 
    worried_car_stolen = db.Column(db.String(20), nullable=True) 

    neighborhood_id = db.Column(db.Integer, db.ForeignKey(Neighborhood.neighborhood_id), nullable=False)
    neighborhood = db.relationship("Neighborhood", db.backref("crime_rate", uselist=False))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Crime city=%s crime_index=%s safety_index=%s>" % (self.name, self.index_crime, self.index_safety)

class User(db.Model):
    """User sign in details"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s zipcode=%s>" % (self.user_id, self.email, self.zipcode)

        
class Favorites(db.Model):
    """ specific user's Favorite neighborhoods"""
   #Association table between User and Neighborhood  
    fav_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey(User.user_id),
                        nullable=False)
    neighborhood_id = db.Column(db.Integer,
                                db.ForeignKey('neighborhood.neighborhood_id'),
                                nullable=False)

    def __repr__(self):
        return "<Favorites neighborhood_id=%s user_id=%s >" % (self.neighborhood_id, self.user_id)
 

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///relocation'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
