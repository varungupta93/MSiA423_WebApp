from MsiaApp import db
from MsiaApp.models import Weather
import datetime
from get_forecast import GetForecast
import numpy

"""Ingestion module

This module is meant to be called to ingest data and place it into db. The dark sky API is called to retrieve the next
day's forecast and the function within this module then sputs the data into the db.

Functionality presumes that the db has already been created. 

"""

def seed_db():
    """Seed the prexisting db with fresh forecast data from the Dark Sky API. If app functionality is ever
    extended to support multiple date choices, the function can be modified to keep multiple dates in the db.

    """
    db.session.query(Weather).delete()
    weatherForecast = GetForecast()
    forecast1 = Weather(Date=weatherForecast.iloc[0]['Date'],
    					MeanAppTemp = weatherForecast.iloc[0]["MeanAppTemp"].item(),
    					PrecipProb = weatherForecast.iloc[0]["PrecipProb"].item(),
    					PrecipIntensity = weatherForecast.iloc[0]["PrecipIntensity"].item())
    db.session.add(forecast1)
    db.session.commit()


if __name__ == "__main__":
    seed_db()
