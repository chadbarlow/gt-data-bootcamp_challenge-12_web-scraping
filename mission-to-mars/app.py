from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# prevent cached responses
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# clear db 
mongo.db.drop_collection("mars_db")

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
