from fastapi import FastAPI, HTTPException
from weather.weather_api import WeatherAPI
from twitter.twitter_api import TwitterAPI
from starlette.responses import HTMLResponse

app = FastAPI()
weather_api = WeatherAPI()
twitter_api = TwitterAPI()


@app.get("/", response_class=HTMLResponse)
def home():
  # HTML content for the home page
  content = """
  <html>
  <head>
      <title>Welcome to the API</title>
  </head>
  <body>
      <h1>Welcome to the API</h1>
      <p>This is the home page of the API.</p>
      <p>Check out the <a href="/docs">API documentation</a> for more information.</p>
  </body>
  </html>
  """
  return content


@app.get("/gen-PIN")
def tweet_weather():
  try:
    twitter_api.get_request_token()
    twitter_api.gen_authorization_PIN()
    return {'message': 'PIN generated'}

  except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))


@app.post("/tweet-weather")
def tweet_weather(city: str, authotization_pin: str):
  try:
    forecast = weather_api.get_five_days_forecast(city)
    twitter_api.get_access_token(authotization_pin)
    twitter_api.make_request({'text':forecast})
    return {'message': 'Tweet sent successfully'}

  except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
  