import json
import server
from unittest import TestCase
from model import User, School, Neighborhood, Images, CostOfLiving, PriceItems, Crime, Favorites
from server import app
import helper


# class FlaskTestsBasic_noZipcode(TestCase):
#     """Flask tests."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         # Get the Flask test client
#         self.client = app.test_client()

#         # Show Flask errors that happen during tests
#         app.config['TESTING'] = True

#     def test_index(self):
#         """Test homepage page."""

#         result = self.client.get("/")
#         self.assertIn("Click On The Neighborhood", result.data)

#     def test_city_no_zipcode(self):
#         """Test homepage page."""
       
#         result = self.client.get("/show_city")
#         # self.assertIn("Climate", result.data)
#         self.assertEqual(result.status_code, 200)
#         self.assertIn('', result.data)

#     def test_school_no_zipcode(self):
#         """Test school page """
#         result = self.client.get("/show_school")
#         self.assertEqual(result.status_code, 200)
#         self.assertIn("Click On The Neighborhood", result.data)

#     def test_costOfliving_no_zipcode(self):
#         """Test school page """
#         result = self.client.get("/cost_of_living")
#         self.assertEqual(result.status_code, 200)
#         self.assertIn("Click On The Neighborhood", result.data)

#     def test_crimeRate_no_zipcode(self):
#         """Test school page """
#         result = self.client.get("/crime_rate")
#         self.assertEqual(result.status_code, 200)
#         self.assertIn("Click On The Neighborhood", result.data)



class FlaskTestsBasic_WithZipcode(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        


    # def test_ZIPCODE_object(self, input_string="93012"):
    #     result = helper.find_zipcode_from_input(input_string)
    #     # self.assertEqual(result.status_code, 200)
    #     self.assertEqual(result.city, "Camarillo")
    #     self.assertEqual(result.state, "CA")
    #     # return result
        
    # def test_show_school(self):
    #     # self.test_ZIPCODE_object()
    #     result = self.client.get("/show_school")
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn("Schools in this neighborhood", result.data)






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
        self.assertIn("Click On The Neighborhood", result.data)




if __name__ == "__main__":
    import unittest


    unittest.main()


