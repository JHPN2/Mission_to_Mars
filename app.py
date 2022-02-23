# Importing denpendencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" # <-- tells Python that our app will
                                                               #     connect to Mongo using a URI

mongo = PyMongo(app) # <-- the URI

# Defining the routes
@app.route("/")
def index():
   mars = mongo.db.mars.find_one() # <-- uses PyMongo to find the "mars" collection in our database,
                                   #     which we will create when we convert our Jupyter scraping 
                                   #     code to Python Script
   return render_template("index.html", mars=mars) # <-- tells Flask to return an HTML template 
                                                   #     using an index.html file

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()