import requests
import datetime
import pandas as pd

"""
.. module:: api_pull_functions
   :platform: Unix, Windows
   :synopsis: This module contain helper functions to pull historical weather data from the Dark Sky API, used by the pull_api_hist module.

.. moduleauthor:: Varun Gupta <varungupta2018@u.northwestern.edu>

"""

def pull_darksky(startdate, enddate, api_k, latitude, longitude):
	"""Uses the passed parameters to pull the historical weather data for the range specified and return the pulled dictionaries in a list.
	:param startdate: The first date for which historical data is pulled.
	:param enddate: The last date for which historical data is pulled.
	:param api_k: The user's Dark Sky API key.
	:param latitude: The latitude for location for which weather data is required. (Fixed for Chicago in this project)
	:param longitude: The longitude for the location for which weather data is required. (Fixed for Chicago in this project)
	:return: A list of responses returned from the API. Responses are JSON format which is dict in Python.
	"""
	day_datetime = startdate
	ctr = 0 #to be depracated
	responses = [] #list to store responses from API
	while day_datetime <= enddate: #iteratively request from the API for every date in range. (Free API tier currently 1000 call limit)
	    dayiter = str(int(day_datetime.timestamp())) #string date format for current date on loop.
	    ctr = ctr + 1
	    url = str("https://api.darksky.net/forecast/"+ api_k + "/"+ latitude + 
	           "," + longitude + ","+ str(dayiter) + "?exclude=currently,minutely,flags,hourly")
	    
	    response = requests.get(url).json()
	    responses.append(response)
	    day_datetime = day_datetime + datetime.timedelta(days = 1)
	    
	    
	return responses



def RespToHistoricalDat(responses):
	"""Uses the passed parameters to pull the historical weather data for the range specified and return the pulled dictionaries in a list.
	:param responses: List of responses returned from the dark sky API, via function pull_darksky.
	:return: A pandas dataframe containing the weather data in the format required for this project.
	"""
	datlist = []
	for resp in responses:
	    
	    datlist.append({"Date": datetime.datetime.fromtimestamp(resp["daily"]["data"][0]["time"]).strftime("%m/%d/%Y"),
	                       "MeanAppTemp": (resp["daily"]["data"][0]["apparentTemperatureLow"] +
	                                      resp["daily"]["data"][0]["apparentTemperatureHigh"])/2,
	                       "PrecipProb": resp["daily"]["data"][0]["precipProbability"],
	                       "PrecipIntensity": resp["daily"]["data"][0]["precipProbability"]})
	weatherDat = pd.DataFrame(datlist)
	return weatherDat

