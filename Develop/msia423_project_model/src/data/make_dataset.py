# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import pickle



def interim():
    """ Runs data processing scripts to turn raw data from (../../data/raw) and (../../data/external) into
        semi-cleaned data ready to be fully processed (saved in ../../data/interim).
        Also stores series of zip codes used in web-app front end in a dropdown
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    #Reading in the files
    crimeDFs = [] 
    for i in range(2011,2019): #Fixed given we are using this file naming convention directly obtained from Chicago Open data portal
        crimeDFs.append(pd.read_csv("../data/raw/Crimes_-_" + str(i)+ ".csv", header = 0))

    fullDF = pd.concat(crimeDFs) #Combining into single dataframe
    del crimeDFs
    fullDF = fullDF[fullDF["Ward"].notnull()] # Dropping the 29 rows with missing Ward
    
    #Changing ward to zipcode
    fullDF.Ward = fullDF.Ward.astype("int")
    wardDF = pd.read_csv("../../data/raw/Ward_Offices.csv")
    wardDFtrim = wardDF[["WARD", "ZIPCODE"]]
    wardDFtrim = wardDFtrim.rename(index = str, columns = {"WARD":"Ward", "ZIPCODE":"Zipcode"})
    updatedDF = fullDF.merge(wardDFtrim, on = "Ward", how = "left" )

    #Store series of zipcodes in App/, so it can populate drop-down
    allZips = updatedDF.Zipcode.unique()
    with open('../../../../App/AllZipCodes.pkl', 'wb') as f:
        pickle.dump(allZips, f)

    #Store interim data in data/interim within develop
    updatedDF.to_csv("../data/interim/" + "OriginalMergedZipcode.csv", index = False)


def final():
    """ Runs data processing scripts to turn interim data from (../../data/interim) and (../../data/external) into
        cleaned data ready to be analyzed (saved in ../../data/processed).
    """
    ungroupedDF = pd.read_csv("../../data/interim/OriginalMergedZipcode.csv")
    ungroupedDF = ungroupedDF.drop("Updated On", 1)
    ungroupedDF = ungroupedDF[ungroupedDF["Domestic"] != True]
    excludeList = ["DECEPTIVE PRACTICE", "PROSTITUTION", "LIQUOR LAW VIOLATION", 
              "GAMBLING", "NON-CRIMINAL", "NON - CRIMINAL", "NON-CRIMINAL (SUBJECT SPECIFIED)"]
    ungroupedDF = ungroupedDF[~ungroupedDF["Primary Type"].isin(excludeList)]

    ungroupedDF["Date"] = ungroupedDF["Date"].str.slice(stop= 10)
    ungroupedDF["Date"] = pd.to_datetime(ungroupedDF["Date"], format="%m/%d/%Y")


    #Reading in the weather history files
    path = '../../data/external'
    weatherDFs = []
    for filename in os.listdir(path):
        weatherDFs.append(pd.read_csv("filename", header = 0))
    fullWeatherDF = pd.concat(weatherDFs)

    fullWeatherDF["Date"] = pd.to_datetime(fullWeatherDF["Date"], format="%m/%d/%Y")
    groupedDF = ungroupedDF.groupby(by = ["Date", "Zipcode"])["Description"].count()
    groupedDF = groupedDF.reset_index()
    groupedDF= groupedDF.merge(fullWeatherDF, on= "Date") 
    groupedDF.to_csv("../data/processed/" + "CrimesMergedWithWeather.csv", index = False)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
    final()


