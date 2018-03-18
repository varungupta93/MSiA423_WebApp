from MsiaApp import db
from MsiaApp.models import Weather
import datetime
from get_forecast import GetForecast

"""Ingestion module

This module is meant to be called to ingest data and place it into db. Once an API is used
the module can be extended with a function that calls the API and puts the data into the db.

Functionality presumes that the db has already been created. 

"""

def seed_db():
    """Seed a preexisting db with dat

    Returns:

    """
    db.session.query(Weather).delete()
    weatherForecast = GetForecast()
    forecast1 = Weather(Date=weatherForecast.iloc[0]['Date'],
    					MeanAppTemp = weatherForecast.iloc[0]["MeanAppTemp"],
    					PrecipProb = weatherForecast.iloc[0]["PrecipProb"],
    					PrecipIntensity = weatherForecast.iloc[0]["PrecipIntensity"] )
    db.session.add(forecast1)
    db.session.commit()


if __name__ == "__main__":
    seed_db()
