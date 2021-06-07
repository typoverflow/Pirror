import yaml

with open("configs/config.yml", "r") as f:
    config = yaml.load(f)

print(config["weather"])

import requests
import json

# r = requests.post("https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id=8cc39a0e-7e91-44bf-8834-072dfa640b30&response_type=code&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&response_mode=form_post&scope=offline_access%20user.read%20mail.read&state=12345", 
# json.dumps())

# https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
# client_id=8cc39a0e-7e91-44bf-8834-072dfa640b30
# &response_type=code
# &redirect_uri=http%3A%2F%2Flocalhost%2Fmyapp%2F
# &response_mode=query
# &scope=offline_access%20user.read%20mail.read
# &state=12345



client_id = "8cc39a0e-7e91-44bf-8834-072dfa640b30"
client_secret = "H)_k26v!SL0im5_btBC*0NU#aj_T8+f5"
scope=r"offline_access%20user.read%20mail.read"

from oauthlib.oauth2 import MobileApplicationClient
from requests_oauthlib import OAuth2Session

# oauth = OAuth2Session(client=MobileApplicationClient(client_id=client_id), scope=scope)
# # url, state = oauth.authorization_url("https://dida365.com/oauth/authorize")
# url, state = oauth.authorization_url("https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize")



# r = oauth.get("https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize")
# oauth.token_from_fragment(r.url)

def get_sign_in_url():
      # Initialize the OAuth client
  aad_auth = OAuth2Session(client_id,
    scope=scope)

  sign_in_url, state = aad_auth.authorization_url("https://login.microsoftonline.com/common/oauth2/v2.0/authorize", prompt='login')

  return sign_in_url, state

u, s = get_sign_in_url()
u