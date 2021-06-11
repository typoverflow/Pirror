import yaml
import requests
import time

from utils.log import log
from ui.text import blit_text_in_middle

class SentenceWidget(object):
    def __init__(self, config):
        self.type = config.get("type", "").split()
        self.type_query_str = "".join(["&c="+i for i in self.type])
        self.max_length = config.get("max_length", 15)
        self.host = "https://v1.hitokoto.cn"

        self.sentence_info = None
        self.update_cycle = config.get("update_cycle", 30)*60
        self.last_update = 0

    def update_sentence(self):
        r = requests.get("{}?{}&max_length={}".format(self.host, self.type_query_str, self.max_length))
        assert r.status_code == 200
        result = r.json()

        self.old_sentence_info = self.sentence_info
        self.sentence_info = [result["hitokoto"], result["from"]]
        
        log("\33[0;32;1m", "Request", "SentenceWidget - get sentence for the day successfully.")
        return self.old_sentence_info != self.sentence_info

    def update_all(self, now):
        if now - self.last_update >= self.update_cycle:
            self.last_update = now
            updated1 = self.update_sentence()
            return updated1
        else:
            return False

    def render(self, window):
        anchor_y = window.height*2/3
        anchor_x = 0
        x, y = anchor_x, anchor_y

        font = window.get_font("苹方黑体-细-简")
        text = self.sentence_info[0]
        if text[-1] in {"。", ".", "，"}:
            text = text[:-1]
        text = "「"+text+"」"
        quote = self.sentence_info[1]
        quote = "《"+quote+"》"
        _, y = blit_text_in_middle(window.screen, text, font, 30, window.width, y, (255,255,255))
        y += 30

        _, y = blit_text_in_middle(window.screen, quote, font, 24, window.width, y, (180,180,180))


if __name__ == "__main__":
    f = open("configs/config.yml")
    config = yaml.load(f)
    s = SentenceWidget(config["sentence"])

    for i in range(20):
        print(s.get_sentence())
        time.sleep(2)