from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pickle
import joblib


def LoadModel():
	with open("RandomForestModel.pkl", "rb") as rfmod:
		RFModel	= pickle.load(rfmod)

	#RFModel = pickle.load("RFModel_comp.pkl")
	return RFModel


def GetCrimePrediction(rfmodel,X):
	prediction = rfmodel.predict(X.iloc[0].values.reshape(1,-1))
	return prediction
	 


