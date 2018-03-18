import requests
import datetime
import pandas as pd

def pull_darksky(startdate, enddate, api_k, latitude, longitude):
	day_datetime = startdate
	ctr = 0 #to be depracated
	responses = [] #list to store responses from API
	while day_datetime <= enddate: #Need to change dates and call <1000/day to get weather for all dates.
	    dayiter = str(int(day_datetime.timestamp())) #string date format for current date on loop.
	    ctr = ctr + 1
	    url = str("https://api.darksky.net/forecast/"+ api_k + "/"+ latitude + 
	           "," + longitude + ","+ str(dayiter) + "?exclude=currently,minutely,flags,hourly")
	    
	    response = requests.get(url).json()
	    responses.append(response)
	    day_datetime = day_datetime + datetime.timedelta(days = 1)
	    
	    
	return responses



def RespToHistoricalDat(responses):
	datlist = []
	for resp in responses:
	    
	    datlist.append({"Date": datetime.datetime.fromtimestamp(resp["daily"]["data"][0]["time"]).strftime("%m/%d/%Y"),
	                       "MeanAppTemp": (resp["daily"]["data"][0]["apparentTemperatureLow"] +
	                                      resp["daily"]["data"][0]["apparentTemperatureHigh"])/2,
	                       "PrecipProb": resp["daily"]["data"][0]["precipProbability"],
	                       "PrecipIntensity": resp["daily"]["data"][0]["precipProbability"]})
	weatherDat = pd.DataFrame(datlist)
	return weatherDat

