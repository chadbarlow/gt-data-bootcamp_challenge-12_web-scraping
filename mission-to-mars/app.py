from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import re

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# def format_table(html_table):
#     table_start = '<div class="table-responsive"><div class="table-container"><table class="table table-striped table-hover table-bordered">'
#     table_end = '</table></div></div>'
#     return table_start + re.sub('^<table>', '', re.sub('</table>$', '', html_table)) + table_end


# app.jinja_env.filters['format_table'] = format_table


@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars_db = mongo.db.mars_db.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars_db=mars_db)


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
