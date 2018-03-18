#import requests
import time
import json
import config
import datetime
import pandas as pd
import os
import api_pull_functions

#Chicago coordinates
latitude = "41.8781"
longitude = "-87.6298"


enddate = datetime.datetime(2011,1,10) #final date to pull weather for.

startdate = enddate - datetime.timedelta(days = 40)

responses = api_pull_functions.pull_darksky(startdate, enddate, config.api_k, latitude,longitude)

weatherDat = api_pull_functions.RespToHistoricalDat(responses)

#curpath = os.getcwd()
pathToSave = "../../data/external/"

weatherDat.to_csv(pathToSave + "WeatherHist10.csv", index= False)
