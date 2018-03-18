from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd
from get_forecast import GetForecast
from get_prediction import LoadModel, GetCrimePrediction
from MsiaApp import application, db, engine 

with open("AllZipCodes.pkl", "rb") as allzips:
	zipcodes = pickle.load(allzips)
zipcodelist = list(zipcodes)
zipcodelist = sorted(zipcodelist)

RFregressor = LoadModel()

#weatherForecast = GetForecast()

#Default for testing
#weatherForecast = pd.DataFrame({"Date": [pd.to_datetime("3/20/2018", format = "%m/%d/%Y")],
#								"MeanAppTemp": [53.5], "PrecipIntensity":[0.0],"PrecipProb":[0.5]})

#predictor
#X = weatherForecast


app = Flask(__name__)

@app.route("/")
@app.route("/Home", methods=['POST'])
def homepg():
	if request.method == 'POST':
		return render_template("HomePage_Testing.html", zipcodes = zipcodelist)
	else:
		return render_template("HomePage_Testing.html", zipcodes = zipcodelist)

@app.route("/result", methods= ['POST'])
def resultpg():
	#global X
	X = pd.read_sql_query("select * from weather;", engine)
	print(X)
	if request.method == 'POST':
		zipselected = request.form.get("Zipcode")
		X["Zipcode"] = int(pd.Series([zipselected]).values) #Temporary BS measure for testing
		X = X[["Zipcode","MeanAppTemp","PrecipIntensity","PrecipProb"]]
		print(X)
		predicted = GetCrimePrediction(RFregressor, X)


	return render_template("Results.html", zipcode = zipselected, meantemp = round(X.iloc[0]['MeanAppTemp'],2),
							 precipint = X.iloc[0]["PrecipIntensity"], precipprob = X.iloc[0]["PrecipProb"],
							 predictionres = int(round(predicted[0])))

if __name__ == "__main__":
	app.run(host="0.0.0.0")

