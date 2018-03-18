#import requests
import time
import json
import config
import datetime
import pandas as pd
import os
import api_pull_functions

#Chicago coordinates


def GetForecast():
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
	                       "PrecipIntensity": resp["daily"]["data"][j]["precipProbability"]})
	weatherForecast = pd.DataFrame(datlist)
	return weatherForecast.iloc[[1]]

