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

    def get_sentence(self):
        r = requests.get("{}?{}&max_length={}".format(self.host, self.type_query_str, self.max_length))
        assert r.status_code == 200
        result = r.json()

        log("\33[0;32;1m", "Success", "Get sentence from hitokoto")
        return [result["hitokoto"], result["from"]]

if __name__ == "__main__":
    f = open("configs/config.yml")
    config = yaml.load(f)
    s = SentenceWidget(config["sentence"])

    for i in range(20):
        print(s.get_sentence())
        time.sleep(2)