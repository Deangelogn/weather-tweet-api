import json
import os
from dotenv import load_dotenv
import webbrowser
from requests_oauthlib import OAuth1Session


class TwitterAPI():
  consumer_key = None
  consumer_secret = None
  resource_owner_key = None
  resource_owner_secret = None
  access_token = None
  access_token_secret = None

  def __init__(self):
    load_dotenv()
    self.consumer_key = os.environ.get("CONSUMER_KEY")
    self.consumer_secret = os.environ.get("CONSUMER_SECRET")
    self.oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)

  def get_request_token(self):
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    self.oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)
    try:
      fetch_response = self.oauth.fetch_request_token(request_token_url)
    except ValueError:
      print("There may have been an issue with the consumer_key or consumer_secret you entered.")
      return None, None

    self.resource_owner_key = fetch_response.get("oauth_token")
    self.resource_owner_secret = fetch_response.get("oauth_token_secret")

    return self.resource_owner_key, self.resource_owner_secret
  
  def gen_authorization_PIN(self):
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = self.oauth.authorization_url(base_authorization_url)
    print(f'ACCESS {authorization_url} AND YOUR PIN')
    webbrowser.open(authorization_url)
    
  def get_access_token(self, authorization_PIN):
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        self.consumer_key,
        client_secret=self.consumer_secret,
        resource_owner_key=self.resource_owner_key,
        resource_owner_secret=self.resource_owner_secret,
        verifier=authorization_PIN,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    self.access_token = oauth_tokens["oauth_token"]
    self.access_token_secret = oauth_tokens["oauth_token_secret"]
    
    return self.access_token, self.access_token_secret
  
  def make_request(self,  payload):
    oauth = OAuth1Session(
        self.consumer_key,
        client_secret=self.consumer_secret,
        resource_owner_key=self.access_token,
        resource_owner_secret=self.access_token_secret,
    )

    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )   
    return response
  
  def tweet(self, text):
    self.get_request_token()
    self.get_authorization()
    self.get_access_token()
    response = self.make_request({"text": text})

    if response.status_code != 201:
      print (f"It was not possible to complete the tweet due the following reasons: {response.text} ")

    print (f"Tweet sucessfully posted!")