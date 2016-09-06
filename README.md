# Help Me Relocate
Are you relocating to a new place in the USA? Become a neighborhood detective with this app before you move. Intended to help users profile and compare neighborhoods, this app provides the user with a broad understanding of any zip code they choose using many data sources, providing a mental picture of the neighborhood.

The idea for the app came to me from my own experiences - my family and I have moved across the world and across the country multiple times. Each time, we have had to research each location using multiple websites. We wanted to check for good schools for my daughter, cost of living for the area, and the crime rate of our potential neighborhood.
Help Me Relocate is a web application that compiles this information in one location.
Users can profile the neighborhood based on zip code clicked by user on google map.

- Information about the city(About the city, Climate, Images)
- overall cost of living(house rents, prices for key items, healthcare, traffic situation, safety, pollution and much more)
- School Profile(Scores, Parent Ratings and other details)
- Crime rate


You can also:
  - Register(optional).
  - When logged in, save your favorite neighborhoods.
  - Compare them to pick the appropriate one.


> The simple design of this app is to make it easy for users to search their neighborhoods.


> Easy click on the google map to search the neighborhoods.

![Help Me Relocate Homepage](/static/images/homepage.png)

> Clear and simple page which shows images and a short info about the city and climate.

 
 ![Help Me Relocate city page](/static/images/show_city.png)


> Schools are shown on map with marker for each school showing school name, address and school score. Also, a table to access other details of school, like parent rating, website url etc.

![Help Me Relocate school page](/static/images/show_schools.png)

> Cost of living page shows a simple and clean chart which shows different indices for the neighborhood.

![Help Me Relocate cost of living page](/static/images/cost_of_living.png)

> Cost of living page also categorizes the prices for different items like Restaurants, Groceries, Clothing etc and shows them on charts so users can quickly get the idea.

![Help Me Relocate price items page](/static/images/Restaurants.png)


>Comparison page shows user's favorite neighborhoods and selecting two neighborhoods, compares them by cost of living and shows it on a bar chart. 

![Help Me Relocate Comparison page](/static/images/compare_cost.png)

>Schools are also compared for the two neighborhoods by scores and parent ratings  and shown on bubble chart.

![Help Me Relocate Comparison schools page](/static/images/compare_schools.png)

### Tech

Help Me Relocate uses following technologies:

* Python
* PostgreSQL
* SQLAlchemy
* Flask
* Javascript/jQuery
* AJAX/JSON
* Jinja2
* Chart.js
* Bootstrap
* HTML5
* CSS

### APIs Used
* Google Maps(Geocoding, Reverse Geocoding )
* Numbeo.com cost of living
* Numbeo.com Crime rate
* Numbeo.com price items
* Numbeo.com cities
* Greatschools.org
* Panoramio.com
* Wikipedia 



### Run the app
* Dependencies are listed in requirements.txt)
* Set up and activate a python virtualenv, and install all dependencies:
    * `pip install -r requirements.txt`
  * Make sure you have PostgreSQL running. Create a new database in psql named relocate
    * `createdb relocate`
	* `psql relocate`

  * Create the tables in your database:
    * `python -i model.py`
    * While in interactive mode, create tables: `db.create_all()`
  
* Now, quit interactive mode. Start up the flask server:
    * `python server.py`
    *  Go to localhost:5000 to see the web app

