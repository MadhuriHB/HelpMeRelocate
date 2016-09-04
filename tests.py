import json
import server
from unittest import TestCase
from model import User, School, Neighborhood, Images, CostOfLiving, PriceItems, Crime, Favorites
from server import app


class FlaskTestsBasic(TestCase):
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
        self.assertIn("Click On The Neighborhood", result.data)

    # def test_city(self):
    #     """Test homepage page."""
    #     # self.client = app.test_client()
    #     # app.config['TESTING'] = True
    #     result = self.client.get("/")
       
    #     self.assertIn("Climate", result.data)

    def test_school(self):
        """Test school page """
        result = self.client.get("/show_school")
        self.assertIn("Click On The Neighborhood", result.data)

    # def test_costOfliving(self):
    #     """Test school page """
    #     result = self.client.get("/cost_of_living")
    #     self.assertIn("Cost Of Living", result.data)

    # def test_crimeRate(self):
    #     """Test school page """
    #     result = self.client.get("/crime_rate")
    #     self.assertIn("Schools in this neighborhood", result.data)

    # def test_favorites(self):
    #     """Test school page """
    #     result = self.client.get("/show_favorites")
    #     self.assertIn("Your Favorite Neighborhoods", result.data)

    # def test_comparison(self):
    #     """Test comparison page """
    #     result = self.client.get("/compare")
    #     self.assertIn("Comparison", result.data)



# class FlaskTestsDatabase(TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         # Get the Flask test client
#         self.client = app.test_client()
#         app.config['TESTING'] = True

#         # Connect to test database
#         connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data
#         db.create_all()
        # example_data()

    # def tearDown(self):
    #     """Do at end of every test."""

    #     db.session.close()
    #     db.drop_all()

    # def test_departments_list(self):
    #     """Test departments page."""

    #     result = self.client.get("/departments")
    #     self.assertIn("Legal", result.data)

                
    # def test_departments_details(self):
    #     """Test departments page."""

    #     result = self.client.get("/department/fin")
    #     self.assertIn("Phone: 555-1000", result.data)


    # def test_login(self):
    #     """Test login page."""

    #     result = self.client.post("/login", 
    #                               data={"user_id": "rachel", "password": "123"},
    #                               follow_redirects=True)
    #     self.assertIn("You are a valued user", result.data)


# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_login_page(self):
#         """Test important page."""

#         result = self.client.get("/login")
#         self.assertIn("Email", result.data)


# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_logout(self):
#         """Test Logout page """
#         result = self.client.get("/logout")
#         self.assertIn("Click On The Neighborhood". result.data)




if __name__ == "__main__":
    import unittest

    unittest.main()



