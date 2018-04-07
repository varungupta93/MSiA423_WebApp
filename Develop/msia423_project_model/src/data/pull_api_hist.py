import time
import json
import config
import datetime
import pandas as pd
import os
import api_pull_functions
import yaml

"""
.. module:: pull_api_hist
   :platform: Unix, Windows
   :synopsis: This module pulls historical weather data for Chicago and stores it in a csv.

.. moduleauthor:: Varun Gupta <andrew@invalid.com>


"""
def SaveHistoricalWeather():
	""" This function pulls historical Chicago weather data, for a date range specified by the YAML file configyaml, and stores it in a csv.
		The csvs are stored in Develop/msia423_project_model/Data/external, unless otherwise specified in the YAML file.
	"""
	with open("configyaml.yml", 'r') as ymlfile:
		ymlcfg = yaml.load(ymlfile)

	#Chicago coordinates. Fixed for the purposes of this project
	latitude = "41.8781"
	longitude = "-87.6298"

	#Date up to which data needs to be pulled
	endday = int(configyaml["days"]["endday"])
	endmonth = int(configyaml["days"]["endmonth"])
	endyear = int(configyaml["days"]["endyear"])

	enddate = datetime.datetime(endyear,endmonth,endday) #final date to pull weather for.

	startdate = enddate - datetime.timedelta(days = ymlcfg["days"]["daystopull"]) #Capped at 1000 API calls on free tier

	responses = api_pull_functions.pull_darksky(startdate, enddate, config.api_k, latitude,longitude)

	weatherDat = api_pull_functions.RespToHistoricalDat(responses)


	pathToSave = ymlcfg["path"]["pathtosave"] #If this is changed in the YAML, modelling files need to be modified to load from the correct location

	filenum = ymlcfg["files"]["filenum"] #If saving multiple csvs, change num to prevent overwrite.

	weatherDat.to_csv(pathToSave + "WeatherHist" + str(filenum) ".csv", index= False)

if __name__ == '__main__':
	SaveHistoricalWeather()
