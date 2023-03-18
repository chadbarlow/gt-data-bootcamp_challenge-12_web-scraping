
# Use MongoDB with Flask templating to create a new HTML page that
# displays all of the information that was scraped from the URLs above.

# Start by converting your Jupyter notebook into a Python script
# called scrape_mars.py with a function called scrape that will
# execute all of your scraping code from above and return one
# Python dictionary containing all of the scraped data.

# Next, create a route called /scrape that will import your
# scrape_mars.py script and call your scrape function.

# Store the return value in Mongo as a Python dictionary.
# Create a root route / that will query your Mongo database and pass
# the mars data into an HTML template to display the data.

# Create a template HTML file called index.html that will take the
# mars data dictionary and display all of the data in the appropriate
# HTML elements. Use the following as a guide for what the final product
# should look like, but feel free to create your own design.

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars_db = mongo.db.mars_db.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars_db=mars_db)

# set our path to /scrape


@app.route("/scrape")
def scraper():
    # create a listings database
    mars_db = mongo.db.mars_db
    # call the scrape function in our scrape_phone file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape()
    # update our listings with the data that is being scraped.
    mars_db.replace_one({}, mars_data, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)


# # Automates browser actions
# from splinter import Browser

# # Parses the HTML
# from bs4 import BeautifulSoup
# import pandas as pd

# # For scraping with Chrome
# from webdriver_manager.chrome import ChromeDriverManager


# def scrape():
#     # Setup splinter
#     # browser = init_browser()
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=False)

#     # Set an empty dict for listings that we can save to Mongo
#     listings = {}

#     # The url we want to scrape
#     url = "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch"

#     # Call visit on our browser and pass in the URL we want to scrape
#     browser.visit(url)

#     # Let it sleep for 1 second
#     time.sleep(1)

#     # Return all the HTML on our page
#     html = browser.html

#     # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
#     soup = BeautifulSoup(html, "html.parser")

#     # Build our dictionary for the headline, price, and neighborhood from our scraped data
#     listings["headline"] = soup.find("a", class_="title").get_text()
#     listings["price"] = soup.find("h4", class_="price").get_text()
#     listings["reviews"] = soup.find("p", class_="pull-right").get_text()

#     # Quit the browser
#     browser.quit()

#     # Return our dictionary
#     return listings
