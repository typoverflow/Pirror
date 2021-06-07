from oauthlib.oauth2.rfc6749 import tokens
import requests
from requests.api import head
from requests_oauthlib.oauth2_session import OAuth2Session
import yaml
import json
from utils.log import printc, log
import os
import time

os.environ["OAUTHLIB_INSECURE_TRANSPORT"]   = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"]    = "1"
os.environ["OAUTHLIB_IGNORE_SCOPE_CHANGE"]  = "1"

class TodoList(object):
    def __init__(self, config):
        self.client_id      = config.get("client_id", "")
        self.client_secret  = config.get("client_secret", "")
        self.redirect_uri   = config.get("redirect_uri", "")
        self.scope          = config.get("scopes", "")
        self.auth_host      = "https://login.microsoftonline.com/common/oauth2/v2.0"
        self.api_host       = "https://graph.microsoft.com/v1.0"

        # self.fetch_token()
        self.fetch_refresh_token()

    def fetch_refresh_token(self):
        self.oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
        authorization_url, _ = self.oauth.authorization_url(self.auth_host + "/authorize")

        log("\n\033[0;33;1m", "Authorize", "在浏览器中打开下面的URL，并在授权后将重定向的URL复制粘贴进入终端内")
        print(authorization_url)
        # code = input("重定向的URL为:\n").split("?")[1].split("&")[0].split("=")[1]
        res_url = input("重定向的URL为:\n")

        tokens = self.oauth.fetch_token(self.auth_host + "/token", 
            client_secret=self.client_secret, 
            authorization_response=res_url, 
            scope=self.scope, 
        )

        self.refresh_token      = tokens["refresh_token"]
        self.access_token       = tokens["access_token"]
        self.token_expire_time  = tokens["expires_in"] - 600
        self.token_create_time  = time.time()

    def get_token(self):
        # check expiration
        if (time.time() - self.token_create_time) > self.token_expire_time:
            new_tokens = self.oauth.refresh_token(self.auth_host + "/token", self.refresh_token, client_id=self.client_id, client_secret=self.client_secret)
            self.refresh_token      = new_tokens["refresh_token"]
            self.access_token       = new_tokens["access_token"]
            self.token_expire_time  = new_tokens["expries_in"] - 600
            self.token_create_time  = time.time()

        return self.access_token
        

    def get_tasks(self):
        token = self.get_token()
        headers = {
            "Authorization": "Bearer {}".format(token)
        }
        tasks = []

        r = requests.get(self.api_host + "/me/todo/lists", headers=headers)
        assert r.status_code == 200
        lids = list(map(lambda x: (x["id"], x["displayName"]), r.json()["value"]))

        for lid, lname in lids:
            r= requests.get(self.api_host + "/me/todo/lists/{}/tasks".format(lid), headers=headers)
            assert r.status_code == 200
            for _ in r.json()["value"]:
                tasks.append({
                    "lid": lid, 
                    "lname": lname, 
                    "tid": _["id"], 
                    "title": _["title"], 
                    "body": _["body"], 
                    "status": _["status"], 
                    "importance": _["importance"], 
                    "lastModifiedDatetime": _["lastModifiedDatetime"]
                })
        
        self.tasks = tasks
        return tasks


if __name__ == "__main__":
    f = yaml.load(open("configs/config.yml"))["todo_list"]
    t = TodoList(f)
    t.get_tasks()
