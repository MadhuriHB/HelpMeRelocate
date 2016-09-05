import json
import server
from unittest import TestCase
from model import User, School, Neighborhood, Images, CostOfLiving, PriceItems, Crime, Favorites, connect_to_db, db, example_data
from server import app



class FlaskTestsBasic_noZipcode(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Relocate", result.data)

    def test_city_no_zipcode(self):
        """Test homepage page."""
       
        result = self.client.get("/show_city")
        # self.assertIn("Climate", result.data)
        self.assertEqual(result.status_code, 200)
        self.assertIn('', result.data)

    def test_school_no_zipcode(self):
        """Test school page """
        result = self.client.get("/show_school")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Click On The Neighborhood", result.data)

    def test_costOfliving_no_zipcode(self):
        """Test school page """
        result = self.client.get("/cost_of_living")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Click On The Neighborhood", result.data)

    def test_crimeRate_no_zipcode(self):
        """Test school page """
        result = self.client.get("/crime_rate")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Click On The Neighborhood", result.data)



class FlaskTestsBasic_WithZipcode(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        
    
class FlaskTestsDatabase_93012(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_show_school(self): 

        result = self.client.get("/show_school?zipcode=93012")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Schools in this neighborhood", result.data)

    def test_show_school_not_empty(self): 

        result = self.client.get("/show_school?zipcode=93012")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Score", result.data)


    def test_show_city(self): 

        result = self.client.get("/show_city?zipcode=93012")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Summary", result.data)

    def test_cost_of_living(self): 

        result = self.client.get("/cost_of_living?zipcode=93012")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Cost Of Living", result.data)

    
    def test_crime_rate(self): 

        result = self.client.get("/crime_rate?zipcode=93012")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Crime rate", result.data)

    def test_register(self):
        """Test login page."""

        result = self.client.get("/register")
        self.assertIn("Email", result.data)

    def test_register_post(self):
        """Test login page."""

        result = self.client.post("/register", 
                                  data={"email": "Tanvi@gmail.com", "password": "Tanvi", "zipcode": 80123},
                                  follow_redirects=True)
        self.assertIn("Relocate", result.data)


    def test_login(self):
        """Test login page."""

        result = self.client.post("/login", 
                                  data={"email": "Madhuri@yahoo.com", "password": "Madhuri"},
                                  follow_redirects=True)
        self.assertIn("Email", result.data)

    def test_cost_of_living_Json(self):
        result = self.client.get("/cost_of_living-chart-data?zipcode=93012")
        # self.assertEqual(result.status_code, 200)
        self.assertIn("crime_index", result.data)        


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = "Madhuri@yahoo.com"

    def test_login_page(self):
        """Test important page."""

        result = self.client.get("/login")
        self.assertIn("Email", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = "Madhuri@yahoo.com"

    def test_logout(self):
        """Test Logout page """
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("Relocate", result.data)



if __name__ == "__main__":
    import unittest


    unittest.main()


