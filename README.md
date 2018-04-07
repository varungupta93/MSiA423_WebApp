# Chicago Crime Forecast Web-App
Repository for Web Application created for MSiA423-Analytics Value Chain at Northwestern University

## Project Overview
For this project, a web application was built that takes a user's Zipcode of interest, combines that with weather data and provides a forecast of the number of crimes in that neighbourhoods the next day.
Crimes do not include domestic crimes, financial fraud, licencing failures, narcotics possession, and a number of other categories that typically would not make a difference to the average visitor. These categories were filtered out from the data before training the model.

Sphinx documentation can be found in Develop/build.

## Data Sources and Reproduction of Raw data:
Chicago Crime Data (Change year for each year)
https://data.cityofchicago.org/Public-Safety/Crimes-2017/d62x-nvdr

Store data from 2011 to 2018, using the auto-provided filenames, in Develop/msia423_project_model/data/raw

Weather Data - Sign up for API Key:
https://darksky.net/dev

Once you have your key, save it in Develop/msia423_project_model/src/data/config.py with the variable name api_k.
Set preferences in configyaml.yml in the same directory. Within your API limits, pull weather data for the given number of days till the final date required, and store it in the csv using the path given in the YAML file. Be sure that this path points to Develop/msia423_project_model/data/external.

Run Develop/msia423_project_model/src/data/pull_api_hist.py, within API limits and modifying the yaml before each pull to pull the correct data and prevent any overwrites.


## Reproduce final data after obtaining raw
Run Develop/msia423_project_model/src/data/make_dataset.py. Both functions need to run. (Make sure your config file was set up in the previous step)

The final data to be used will be found in Develop/msia423_project_model/data/processed/


### Model Used:
A random forest model was used, with hyperparameters tuned to minimize SSE/RMSE. The reasoning behind going with tree models was that the relationship between weather and crime while interesting is certainly not linear, and that trees are great at handling categoricals with a large number of levels (They sort of treat numerical variables in a similar way).

## Reproduction of model:
With all your data saved correctly, run Develop/msia423_project_model/src/model/train_model.py


## Reproduction of app:

### Set up config
In a file named config.py, stored in App/, store your dark sky API key, and your RDS connection parameter in this format:

```
api_k = "your_api_key"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://awsuername:awspassword@rdslink.com:Port#/Dbname"
```

### Deploy Model
First set up the virtual environment
At the level of "ec2-user/home", which is represented as "~""
```
$ sudo yum install python36
$ mkdir venv
$ cd venv
$ virtualenv -p /usr/bin/python3.6 python36
$ source /home/ec2-user/venv/python36/bin/activate
$ pip install -r requirements.txt
```

Return to ~
Then run the file to create the db:
```
$ cd MSiA423_WebApp/App
$ python create_db.py
```

Set up the cron-job to update the RDS whenever you like. The line is stored in Cron_command.txt, but timings to update weather forecast can be adjusted as the developer sees fit. The current command in the repo pulls the forecast from the API and updates data every 4 hours.

```
$ crontab -e
```

Finally run the command:
```
$ nohup python Flask_Initial.py &
```
The web app can be accessed at the public link for your server.
(http://ec2-18-188-134-206.us-east-2.compute.amazonaws.com:5000/)