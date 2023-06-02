# Weather Application (Prefect Flow)

This is a prefect flow that exracts weather information for a given zip code, save the data in a file in json format, parse the temperate and returns it

# Project Requirements

* Using python 3.10 and the prefect package you will create a prefect flow
* The flow should take a parameter for a zipcode
* The flow should perform the following tasks:
* Lookup the daily weather from the zipcode (any free weather api should work)
* Save a json file with the weather
* Parse the weather result to determine the temperature
* Save the temperature as a prefect flow result
* document the code as you would any project
* if required include one test for each task

# Implementation

## Tasks
### get_weather_info
This task would extract the weather info from openweather api for the zipcode that is passed in as an argument and returns the weather info in JSON format.

### save_weather_info
Save the weather info in a file in JSON format and returns the filename. 
filename format - weather_info_<zipcode>_<yyyymmddhhmmss>.json

### get_temperature
Parses the weather info returned by the API to find the temperature and returns it

## Flow
### weather_flow
Does a bare minimum validation on the zipcode passed in to the flow to make sure it is of length 5 characters and it is entirely made up of digits. Then calls the above flows to extract, save weather info and parse temperature and returns the parsed temperature.
Future enhancement: Validate zipcode against a zipcode validator api

## Setup

Git clone this repo to your machine.

```bash
git clone https://github.com/srinivas-marayallappareddy/prefect_weather_flow.git
```
Create a virtual environment

```bash
python -m venv venv
```
Activate the virtual environment

On Windows: 
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### Dependencies
Since there is only one dependent library needed for this. Requirements.txt is not created.
Install prefect library using the below command

```bash
pip install prefect
```

### Environment variables
API_KEY - This is the api key obtained from openweathermap.org  
WEATHER_INFO_DIR - Local directory where the weather data to be saved in files. 

## Usage

From command line

```bash
python temperature.py
```

Start Prefect server with the below command and check the dashboard at  http://127.0.0.1:4200

```bash
prefect server start
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
