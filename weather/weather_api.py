import os
import requests

from dotenv import load_dotenv
from typing import Union


class WeatherAPI():
  api_key = None

  def __init__(self, api_key: str=None) -> None:
    self.api_key = api_key if api_key else self.load_weather_key_from_env()

  def load_weather_key_from_env(self) -> str:
    load_dotenv()
    return os.environ.get('WEATHER_API_KEY')
    
  def __make_request(self, url: str) -> requests.models.Response:
    response = None
    try:
      response = requests.get(url)  
    except Exception as e:
       pass

    return response
     
  def get_current_weather(self, 
                          city: str, 
                          units: str='metric', 
                          lang: str='pt_br'
                          ) -> Union[float, str]:
    # Set up
    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units={units}&lang={lang}"
    temperature = 0.0
    weather = ''
    
    # Make request
    response = self.__make_request(current_weather_url)

    # Handle response
    if response.status_code == 200:
      data = response.json()
      temperature = data["main"]["temp"]
      weather = data["weather"][0]["description"]
    else:
      print("Error:", response.status_code, response.text)
    
    return (temperature, weather)

  def get_weather_forecast(self, 
                           city: str,
                           units: str='metric',
                           lang: str='pt_br'
                           ) -> list[dict]:
    weather_forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units={units}&lang={lang}"

    # Set up
    forecast_list = []

     # Make request
    response = self.__make_request(weather_forecast_url)

    # Handle response
    if response.status_code == 200:
      data = response.json()
      forecast_list = data["list"]
    else:
      print("Error:", response.status_code, response.text)

    return forecast_list

  def get_five_days_forecast(self, city: str) -> str:
    # Set up
    forecast_text = ''

    # Getting forecast data for next 5 days
    forecast_list = self.get_weather_forecast(city)
    
    # Handling errors
    if not forecast_list:
      print("Error: No forecast data found")
      return ''

    # Initial statement
    forecast_data = self.get_forecast_data(forecast_list[0])
    forecast_text += f"{round(forecast_data['temperature'])}°C e {forecast_data['weather']} em {city} em " \
                     f"{forecast_data['day']}/{forecast_data['month']}."

    # Get current date
    current_day = forecast_data['date'] 

    # Get temperature and date from forecast list
    temperature_by_date = {}
    for forecast in forecast_list:
      forecast_data = self.get_forecast_data(forecast)

      date, temperature = forecast_data['date'], forecast_data['temperature']
      
      # Skiping temperature from current date
      if date == current_day:
        continue

      # Checking new dates for new keys creation in the dictionary
      if date not in temperature_by_date:
        temperature_by_date[date] = [temperature]
        continue

      # Store temperature
      temperature_by_date[date].append(temperature)

    # Calcuting mean tempetarure and formating date (DD/MM) for the next 5 days
    days_temperature = []
    for date, temperatures in temperature_by_date.items():
      mean_temperature = sum(temperatures) / len(temperatures)
      year, month, day = date.split('-')
      days_temperature.append(f"{round(mean_temperature)}°C em {day}/{month}")

    #Generating output
    forecast_text += f" Média para os próximos dias: {', '.join(days_temperature)}."

    return forecast_text

  def get_forecast_data(self, forecast: dict) -> dict:
    forecast_data = {}
    temperature = forecast["main"]["temp"]
    date = forecast["dt_txt"]
    weather = forecast["weather"][0]["description"] 
    date, hour = date.split(' ')
    year, month, day = date.split('-')
    
    forecast_data['temperature'] = temperature
    forecast_data['weather'] = weather
    forecast_data['date'] = date
    forecast_data['year'] = year
    forecast_data['month'] = month
    forecast_data['day'] = day
    
    return forecast_data