import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import cross_val_score
from sklearn.model_selection import GridSearchCV
import numpy as np

def create_model_pkl():
	""" 
	This function creates a random forest model that is used for predictions in the web application.
	It tunes among a few hyperparameters that were found to be optimal given this dataset.
	"""
	fullData = pd.read_csv("../../data/interim/" + "CrimesMergedWithWeather.csv")
	fullData.rename(columns={"Description":"Crime_Count"}, inplace = True)
	Y = fullData["Crime_Count"]
	X = fullData[["Zipcode","MeanAppTemp","PrecipIntensity","PrecipProb"]]

	#Only include final set of hyperparameters for tuning
	param_grid3 = {
                'n_estimators': [850, 950, 1050],
                 'max_depth': [9, 10, 11]
              	
            }


    bestModelRF3 = GridSearchCV(rf, cv=5, param_grid = param_grid3)

    bestModelRF3.fit(X,Y) # Fit to the current data to obtain best model

    #Save picked model object to App so app can load it
    with open("../../../../App/RandomForestModel.pkl', 'wb') as f:
    	pickle.dump(bestModelRF3, f)



if __name__ == '__main__':
	create_model_pkl()
