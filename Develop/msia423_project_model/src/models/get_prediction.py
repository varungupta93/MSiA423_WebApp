from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pickle


def LoadModel():
	"""
	Function that loads a pickle file for the tuned random forest and returns it to the calling location
	:return: Scikit-learn RandomForestRegressor object loaded from pickle file in current directory
	"""

	with open("RandomForestModel.pkl", "rb") as rfmod:
		RFModel	= pickle.load(rfmod)

	#RFModel = pickle.load("RFModel_comp.pkl")
	return RFModel


def GetCrimePrediction(rfmodel,X):
	""" Function that returns prediction on a single row data frame in the required format, using the loaded random forest
	
	:param rfmodel: Scikit-learn randomforestregressor tuned model object
	:param X: Single row pandas data frame containing the required columns for this random forest to make a prediction.
	:return: Predicted number of crimes in that location, given the weather data, as specified in the dataframe X.
	"""
	prediction = rfmodel.predict(X.iloc[0].values.reshape(1,-1))
	return prediction
	 


