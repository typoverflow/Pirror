import requests
from requests_oauthlib.oauth2_session import OAuth2Session
import yaml
import os
import time
import datetime

from utils.log import log
from ui.gradient import gradientRect
from ui.text import blit_multiline_text

os.environ["OAUTHLIB_INSECURE_TRANSPORT"]   = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"]    = "1"
os.environ["OAUTHLIB_IGNORE_SCOPE_CHANGE"]  = "1"

class TodoListWidget(object):
    def __init__(self, config):
        self.provider = config.get("provider", {})
        if self.provider == {}:
            raise ValueError("To do list provider not set!")
        self.update_cycle = config.get("update_cycle", 30)*60

        config = config.get(self.provider, {})

        if self.provider == "microsoft":
            self.client_id      = config.get("client_id", "")
            self.client_secret  = config.get("client_secret", "")
            self.redirect_uri   = config.get("redirect_uri", "")
            self.scope          = config.get("scopes", "")
            self.auth_host      = "https://login.microsoftonline.com/common/oauth2/v2.0"
            self.api_host       = "https://graph.microsoft.com/v1.0"
        else: 
            raise NotImplementedError("Provider for todo list widget is not supported yet!")

        # self.fetch_token()
        self.fetch_refresh_token()

        self.tasks_info = None
        self.last_update = 0

    def fetch_refresh_token(self):
        try: 
            self.oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
            authorization_url, _ = self.oauth.authorization_url(self.auth_host + "/authorize")

            log("\n\033[0;33;1m", "Authorize", "ToDoListWidget - 在浏览器中打开下面的URL，并在授权后将重定向的URL复制粘贴进入终端内")
            print(authorization_url)
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
            log("\33[0;33;1m", "Authorize", "ToDoListWidget - Microsoft To Do API authorized. ")
        except Exception as e:
            log("\33[0;31;1m", "Error", "ToDoListWidget.fetch_refresh_token - {}.".format(e))

    def get_token(self):
        try: 
            # check expiration
            if (time.time() - self.token_create_time) > self.token_expire_time:
                new_tokens = self.oauth.refresh_token(self.auth_host + "/token", self.refresh_token, client_id=self.client_id, client_secret=self.client_secret)
                self.refresh_token      = new_tokens["refresh_token"]
                self.access_token       = new_tokens["access_token"]
                self.token_expire_time  = new_tokens["expires_in"] - 600
                self.token_create_time  = time.time()
                log("\33[0;33;1m", "Authorize", "ToDoListWidget - Microsoft To Do access token refreshed successfully.")

            return self.access_token
        except Exception as e:
            log("\33[0;31;1m", "Error", "ToDoListWidget.get_token - {}.".format(e))
        

    def update_tasks(self):
        try: 
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
                    info = {
                        "lid": lid, 
                        "lname": lname, 
                        "tid": _["id"], 
                        "title": _["title"], 
                        "body": _["body"], 
                        "status": _["status"], 
                        "importance": _["importance"], 
                        "lastModifiedDateTime": _["lastModifiedDateTime"], 
                        "completedDateTime": _.get("completedDateTime", "")
                    }
                    tasks.append(info)
            
            self.old_tasks_info = self.tasks_info
            self.tasks_info = tasks

            log("\33[0;32;1m", "Request", "ToDoListWidget - get tasks info successfully.")
            return self.old_tasks_info != self.tasks_info
        except Exception as e:
            log("\33[0;31;1m", "Error", "ToDoListWidget.update_tasks - {}.".format(e))

    def update_all(self, now):
        if now - self.last_update >= self.update_cycle:
            self.last_update = now
            updated1 = self.update_tasks()
            return updated1
        else:
            return False

    def render(self, window):
        anchor_x = 25
        anchor_y = window.height - 36
        
        x = anchor_x
        y = anchor_y

        # “干点正事吧”标题文字
        title_surf, title_rect = window.get_font("苹方黑体-细-简").render("Derek，干点正事吧！", (255,255,255), size=24)
        window.screen.blit(title_surf, (x, y))
        y -= 14

        # 分割线
        line = gradientRect((350, 2), (255, 255, 255), (0,0,0))
        window.screen.blit(line, (x, y))
        y -= 16

        # 已完成任务列表
        font = window.get_font("苹方黑体-细-简")
        starred = ["★ "+t["title"] for t in self.tasks_info if t["status"] == "notStarted" and t["importance"] == "high"]
        unfinished = ["□ "+t["title"] for t in self.tasks_info if t["status"] == "notStarted" and t["importance"] != "high"]
        finished = [["×  "+t["title"], t["completedDateTime"]["dateTime"], t["completedDateTime"]["timeZone"]] for t in self.tasks_info if t["status"] == "completed"]
        finished = list(filter(lambda x: (datetime.datetime.today()-datetime.datetime.strptime(x[1].split("T")[0]+"T"+x[2], "%Y-%m-%dT%Z")).days <= 4, finished))
        finished = [t[0] for t in finished]
        x, y = blit_multiline_text(window.screen, starred, font, 24, (x,y), (255,255,255), down=False)
        x, y = blit_multiline_text(window.screen, unfinished, font, 24, (x,y), (255,255,255), down=False)
        font.underline = True
        font.underline_adjustment = -0.3
        x, y = blit_multiline_text(window.screen, finished, font, 24, (x,y), (150,150,150), down=False)
        font.underline = False


if __name__ == "__main__":
    f = yaml.load(open("configs/config.yml"))["todo_list"]
    t = TodoListWidget(f)
    t.get_tasks()
