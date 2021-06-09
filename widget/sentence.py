import yaml
import requests
from utils.log import log
import time

class SentenceWidget(object):
    def __init__(self, config):
        self.type = config.get("type", "").split()
        self.type_query_str = "".join(["&c="+i for i in self.type])
        self.max_length = config.get("max_length", 15)
        self.host = "https://v1.hitokoto.cn"

        self.sentence_info = None
        self.update_cycle = config.get("update_cycle", 30)
        self.update_count = -1

    def update_sentence(self):
        r = requests.get("{}?{}&max_length={}".format(self.host, self.type_query_str, self.max_length))
        assert r.status_code == 200
        result = r.json()

        log("\33[0;32;1m", "Success", "Get sentence from hitokoto")
        self.old_sentence_info = self.sentence_info
        self.sentence_info = [result["hitokoto"], result["from"]]

        return self.old_sentence_info != self.sentence_info

    def update_all(self):
        self.update_count += 1
        if self.update_count % self.update_cycle == 0:
            self.update_count = 0
            updated1 = self.update_sentence()
            return updated1
        else:
            return False

    def render(self, screen):
        pass

if __name__ == "__main__":
    f = open("configs/config.yml")
    config = yaml.load(f)
    s = SentenceWidget(config["sentence"])

    for i in range(20):
        print(s.get_sentence())
        time.sleep(2)