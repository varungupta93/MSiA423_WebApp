import requests
import time
import datetime
import json
import config
import pandas as pd


#Chicago coordinates


def GetForecast():
	""" Function t o pull the current weather forecast for Chicago from the Dark Sky API, and return the next day's forecast as
		a single row data frame.
	:return: Single row pandas dataframe with the next days weather forecast for Chicago
	"""
	latitude = "41.8781" #Fixed for this purpose. Can be kept externally or in config if ever likely to be changed.
	longitude = "-87.6298"
	url = str("https://api.darksky.net/forecast/"+ config.api_k + "/"+ latitude + 
           "," + longitude + "?exclude=currently,minutely,flags,hourly")
	response = requests.get(url).json()
	datlist = []
	resp = response
	for j in range(4):  #For today and next 3 days
	    datlist.append({"Date": datetime.datetime.fromtimestamp(resp["daily"]["data"][j]["time"]).strftime("%m/%d/%Y"),
	                       "MeanAppTemp": (resp["daily"]["data"][j]["apparentTemperatureLow"] +
	                                      resp["daily"]["data"][j]["apparentTemperatureHigh"])/2,
	                       "PrecipProb": resp["daily"]["data"][j]["precipProbability"],
	                       "PrecipIntensity": resp["daily"]["data"][j]["precipIntensity"]})
	weatherForecast = pd.DataFrame(datlist)
	return weatherForecast.iloc[[1]]

