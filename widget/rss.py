import requests
import pandas
import yaml
import json
import pygame
import random

from widget.base import BaseWidget
from utils.log import log
from utils.url import safe_url
from ui.gradient import gradientRect
from ui.text import blit_multiline_text, blit_text_in_middle

class RSSWidget(BaseWidget):
    def __init__(self, config):
        super(RSSWidget, self).__init__(config)

        self.server_api_url = safe_url(config.get("server_api_url"))
        self.user_name = config.get("user_name")
        self.password = config.get("password")
        self.update_cycle = config.get("update_cycle", 60)*60

        self.focused_categories = config.get("focused_categories")
        self.max_entry_num = config.get("max_entry_num", 3)

        self.sid = None
        self.unread_info = None
        self.old_unread_info = None
        self.last_update = 0
    
    def try_log_in(self):
        try: 
            if self.sid is None:
                r = requests.post(
                    url = self.server_api_url, 
                    data = json.dumps({
                        "op": "login", 
                        "user": self.user_name, 
                        "password": self.password, 
                    })
                )
                assert r.status_code == 200
                
                log("green", "Request", "RSSWidget - login and get session id.")
                self.sid = json.loads(r.text)["content"]["session_id"]
            else:
                r = requests.post(
                    url = self.server_api_url, 
                    data = json.dumps({
                        "sid": self.sid, 
                        "op": "isLoggedIn", 
                    })
                )
                assert r.status_code == 200

                if json.loads(r.text)["content"]["status"]:
                    return
                else:
                    r = requests.post(
                        url = self.server_api_url, 
                        data = json.dumps({
                            "op": "login", 
                            "user": self.user_name, 
                            "password": self.password, 
                        })
                    )
                    assert r.status_code == 200
                    log("green", "Request", "RSSWidget - login and get session id.")
                    self.sid = json.loads(r.text)["contents"]["session_id"]
        except Exception as e:
            log("red", "Error", "RSSWidget.try_log_in - {}".format(e))
        
    def update_unread_info(self):
        self.try_log_in()
        try: 
            r = requests.post(
                url = self.server_api_url, 
                data = json.dumps({
                    "op": "getCategories", 
                    "sid": self.sid, 
                    "unread_only": True
                })
            )
            assert r.status_code == 200
            unread_catogories = r.json()["content"]
        except Exception as e:
            log("red", "Error", "RSSWidget.update_unread_info - Fail to get categories info: {}".format(e))
            return False

        cat_name2id = dict()
        for cat in unread_catogories:
            if cat["title"] in self.focused_categories:
                cat_name2id[cat["title"]] = cat["id"]
        
        try: 
            cat2headlines = dict()
            for cat_name, cat_id in cat_name2id.items():
                r = requests.post(
                    url = self.server_api_url, 
                    data = json.dumps({
                        "op": "getHeadlines", 
                        "sid": self.sid, 
                        "feed_id": int(cat_id),
                        "limit": self.max_entry_num, 
                        "is_cat": True
                    })
                )
                assert r.status_code == 200
                entries = r.json()["content"]
                entries = [{
                    "title": e["title"], 
                    "feed": e["feed_title"]
                } for e in entries if e["unread"]]
                cat2headlines[cat_name] = entries
        except Exception as e:
            log("red", "Error", "RSSWidget.update_unread_info - Failed to  get headlines: {}".format(e))
            return False

        # 筛选要显示的title
        unread_info = []
        for cat_name, headlines in cat2headlines.items():
            unread_info.extend(headlines[:min(self.max_entry_num, len(headlines))])
        random.shuffle(unread_info)
        unread_info = unread_info[:min(self.max_entry_num, len(unread_info))]
        unread_info = sorted(unread_info, key=lambda x:len(x["title"]+x["feed"]), reverse=True)

        # unread_info = []
        # for cat_name, headlines in cat2headlines.items():
        #     cat2headlines[cat_name] = headlines[:min(self.max_entry_num, len(headlines))]
        # tmp = dict()
        # for _ in range(self.max_entry_num):
        #     cat = random.choice(self.focused_categories)
        #     tmp[cat] = id = tmp.get(cat, -1) + 1
        #     unread_info.append(cat2headlines[cat][id])
        
        self.old_unread_info = self.unread_info
        self.unread_info = unread_info

        return self.old_unread_info != self.unread_info

    def update_all(self, now):
        if now - self.last_update >= self.update_cycle:
            self.last_update = now
            updated1 = self.update_unread_info()
            return updated1
        else:
            return False

    def render(self, window):
        anchor_x = 25
        anchor_y = window.height - 180

        x = anchor_x
        y = anchor_y

        # What's UP? 标题文字
        title_surf, title_rect = window.get_font("sarasa-mono-cl-bolditalic").render("What's UP?", (255,255,255), size=36)
        window.screen.blit(title_surf, (x, y))

        # 分割线
        x1, y1 = x,  y+title_rect.height + 15
        line = gradientRect((300, 2), (255,255,255), (0,0,0))
        window.screen.blit(line, (x1, y1))

        # entries
        x2, y2 = x1, y1+15
        titles = ["《"+i["title"]+"》   by "+i["feed"] for i in self.unread_info]
        # feeds = [i["feed"] for i in self.unread_info]
        blit_multiline_text(window.screen, titles, window.get_font("苹方黑体-细-简"), 26, (x2, y2), (255,255,255), lineheight=42)

        # blit_multiline_text(window.screen, feeds, window.get_font("苹方黑体-细-简"), 20, (x2+600, y2+4), (200,200,200), lineheight=42)



if __name__ == "__main__":
    import yaml
    config = yaml.load(open("configs/config.yml"))["rss"]
    rw = RSSWidget(config)
    rw.try_log_in()
    rw.try_log_in()
    rw.update_unread_info()