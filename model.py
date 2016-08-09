import heapq
import time
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


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

        return "<User user_id=%s zipcode=%s>" % (self.user_id, self.zipcode)


class City(db.Model):
    """city information"""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String(80))
    zipcode = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed"""
        return "<City city_name=%s zipcode=%s>" % (self.city_name, self.zipcode)


















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
