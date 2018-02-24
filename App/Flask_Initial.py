from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pickle

with open("AllZipCodes.pkl", "rb") as allzips:
	zipcodes = pickle.load(allzips)
zipcodelist = list(zipcodes)
zipcodelist = sorted(zipcodelist)

app = Flask(__name__)


@app.route("/")
def homepg():
	return render_template("HomePage.html", zipcodes = zipcodelist)

if __name__ == "__main__":
	app.run()

