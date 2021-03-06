from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd
from get_forecast import GetForecast
from get_prediction import LoadModel, GetCrimePrediction
from MsiaApp import application, db, engine
import numpy as np 

"""Flask module

This module runs the final flask application when everything else is ready, including HTML pages, model pkl,
series of zipcodes, and functions to get predictions from the model, as well as the database.
The app is hosted on 0.0.0.0

"""

#Load zip codes to populate dropdown.
with open("AllZipCodes.pkl", "rb") as allzips:
	zipcodes = pickle.load(allzips)
zipcodelist = list(zipcodes)
zipcodelist = sorted(zipcodelist)

RFregressor = LoadModel()

app = Flask(__name__)

@app.route("/")
@app.route("/Home", methods=['POST'])
def homepg():
	if request.method == 'POST': #In case user presses back button.
		return render_template("HomePage_Testing.html", zipcodes = zipcodelist)
	else:
		return render_template("HomePage_Testing.html", zipcodes = zipcodelist)

@app.route("/result", methods= ['POST'])
def resultpg():
	
	X = pd.read_sql_query("select * from weather;", engine) # Pull forecast data from RDS database.
	X["MeanAppTemp"] = X["MeanAppTemp"].astype(np.float64)
	X["PrecipProb"] = X["PrecipProb"].astype(np.float64)
	X["PrecipIntensity"] = X["PrecipIntensity"].astype(np.float64)
	
	if request.method == 'POST':
		zipselected = request.form.get("Zipcode") #Store user input data from home page.
		X["Zipcode"] = int(pd.Series([zipselected]).values) 
		X = X[["Zipcode","MeanAppTemp","PrecipIntensity","PrecipProb"]]
		
		predicted = GetCrimePrediction(RFregressor, X) #Get prediction from model.


	return render_template("Results.html", zipcode = zipselected, meantemp = round(X.iloc[0]['MeanAppTemp'],2),
							 precipint = X.iloc[0]["PrecipIntensity"], precipprob = X.iloc[0]["PrecipProb"],
							 predictionres = int(round(predicted[0])))

if __name__ == "__main__":
	app.run(host="0.0.0.0")

