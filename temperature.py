import prefect
from prefect import flow, task
from prefect.tasks import task_input_hash
import requests
import json
import os
import datetime

WEATHER_INFO_DIR = os.environ["WEATHER_INFO_DIR"]
API_KEY = os.environ["OPEN_WEATHER_API_KEY"]
OPEN_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Most likely there will not be a lot of difference in the weather in 30 mins
# 30 mins cache expiration is reasonalble


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=datetime.timedelta(minutes=30))
def get_weather_info(zipcode):
    '''
    Extracts the weather data from openweathermap api for a given zip code and returns response

    Parameters: 
        zipcode - str
    Returns:
        weather_info - dict
    '''

    try:
        response = requests.get(
            url=f"{OPEN_WEATHER_URL}?zip={zipcode},us&appid={API_KEY}")
    except requests.exceptions.RequestException as e:
        flow_logger = prefect.get_run_logger()
        flow_logger.error(f"API error while retrieving weather info: {str(e)}")
        raise

    weather_info = response.json()

    # API response has the temperature in Kelvin, so needs to be converted to Fahrenheit
    if 'main' in weather_info:
        weather_info['main']['temp'] = round((
            weather_info['main']['temp'] - 273.15) * 9/5 + 32, 2)

    return weather_info


@task
def save_weather_info(zipcode, weather_info):
    '''
    Saves the weather data into a file.
    File name format = weather_info_<zipcode>_<yyyymmddhhmmss>.json

    Parameters:
        zipcode - str
        weather_info - dict

    Returns:
        filename
    '''

    curr_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{WEATHER_INFO_DIR}\weather_info_{zipcode}_{curr_date}.json"

    try:
        with open(filename, "w") as file_handle:
            json.dump(weather_info, file_handle)
    except PermissionError as e:
        flow_logger = prefect.get_run_logger()
        flow_logger.error(
            f"File permission error while saving weather data: {str(e)}")
        raise
    except OSError as e:
        flow_logger = prefect.get_run_logger()
        flow_logger.error(f"OS Error while saving weather data: {str(e)}")
        raise

    return filename


@task
def get_temperature(weather_info):
    '''
    Parses the weather results to determine the temperature and returns it.

    Parameters:
        weather_info - dict

    Returns:
        temperature 
    '''

    return weather_info['main']['temp'] if 'main' in weather_info else None


@flow(name="Weather Info")
def weather_flow(zipcode):
    '''
    This is a flow function that validates the zipcode and calls tasks (functions) to extract and save weather info and returns the temperature.

    Parameters:
        zipcode - str
    Returns:
        temperature in Fahrenheit
    '''

    # Just a bare minimum validation to make sure the zipcode is 5 digits long and it is only made of digits
    # Better would be to validate with zipcode validator api.

    if len(zipcode) == 5 and zipcode.isdigit():
        weather_info = get_weather_info(zipcode)
        save_weather_info(zipcode, weather_info)
        temperature = get_temperature(weather_info)
    else:
        raise ValueError("Invalid zipcode")

    return temperature


# This code will run when the script is run directly.
if __name__ == "__main__":

    while True:
        zipcode = input("Enter 5 digit zipcode (q to quit): ")
        if len(zipcode) == 5 and zipcode.isdigit():
            print(weather_flow(zipcode))
            break

        if zipcode == 'q':
            break
