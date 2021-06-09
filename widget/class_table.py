import os
from datetime import date, datetime
import time
from utils import time as ut
import yaml


class ClassTableWidget(object):
    def __init__(self, config):
        self.begin = datetime.strptime(config.get("begin_date"), "%Y-%m-%d")
        # self.today = datetime(ut,ut.getYear(), ut.getMonth(), ut.getDay())
        # self.interval = self.today - self.begin
        # self.weekcount = interval.days // 7 + 1

        self.table = config.get("table", [])

        self.class_info = None
        self.update_count = 0

    def update_class(self):
        today = datetime(ut.getYear(), ut.getMonth(), ut.getDay())
        interval = today - self.begin
        weekcount = interval.days // 7 + 1
        self.old_class_info = self.class_info
        if self.table == []:
            self.class_info = "无课程"
        if ut.getWday() >= len(self.table):
            self.class_info = "无课程"
        else:
            classes = self.table[ut.getWday()]
            classes = list(filter(lambda x: x["start"] <= weekcount <= x["end"], classes))
            if len(classes) == 0:
                self.class_info = "无课程"
            else: 
                self.class_info = classes

        return self.old_class_info != self.class_info

    def update_all(self, cycle):
        self.update_count += 1
        if self.update_count % cycle == 0:
            self.update_count = 0
            updated1 = self.update_class()
            return updated1

if __name__ == "__main__":
    fp = open("configs/config.yml")
    config = yaml.load(fp)
    ct = ClassTableWidget(config["class_table"])
    ct.update_class()
        