import requests
from requests_oauthlib.oauth2_session import OAuth2Session
import yaml
import json
from utils.log import printc, log

class TodoList(object):
    def __init__(self, config):
        self.client_id      = config.get("client_id", "")
        self.client_secret  = config.get("client_secret", "")
        self.redirect_uri   = "https://www.baidu.com"
        self.scope          = "tasks:read"
        self.host           = "https://api.dida365.com"

        self.fetch_token()

    def fetch_token(self):
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
        authorization_url, _ = oauth.authorization_url("https://dida365.com/oauth/authorize")

        log("\n\033[0;33;1m", "Authorize", "在浏览器中打开下面的URL，并在授权后将重定向的URL复制粘贴进入终端内")
        print(authorization_url)
        code = input("重定向的URL为:\n").split("?")[1].split("&")[0].split("=")[1]

        r = requests.post("https://dida365.com/oauth/token", params={
            "client_id": self.client_id, 
            "client_secret": self.client_secret, 
            "code" : code, 
            "grant_type": "authorization_code", 
            "scope": self.scope,
            "redirect_uri": self.redirect_uri
        })
        self.token = r.json()["access_token"]

    def get_tasks(self):

        r = requests.get(self.host+"/open/v1/project/60bd8d9b4eafd122d7b8c925/task/0", headers={
            "Authorization": "Bearer {}".format(self.token)
        })
        r

if __name__ == "__main__":
    f = yaml.load(open("configs/config.yml"))["todo_list"]
    t = TodoList(f)
    t.get_tasks()
