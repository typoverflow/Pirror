import os
from datetime import datetime
import time
from utils import time as ut

begin=datetime.datetime(2021,3,1)
today=datetime.datetime(ut.getYear(),ut.getMonth(),ut.getDay())
interval = today-begin
weekcount = interval.days // 7 + 1

class ClassTable(object):
    def __init__(self, config):
        self.begin = datetime.strptime(config.get("begin_date"), "%Y-%m-%d")
        self.today = datetime(ut,ut.getYear(), ut.getMonth(), ut.getDay())
        self.interval = self.today - self.begin
        self.weekcount = interval.days // 7 + 1

        self.table = config.get("table", [])

    def get_class(self, idx, weekday):
        if self.table == []:
            return {"name": "无课程信息"}
        if len(self.table[weekday]) < idx:
            return {"name": "无课程"}
        if self.table[weekday][idx]["start"] <= self.weekcount <= self.table[weekday][idx]["end"]:
            return self.table[weekday][idx]
        else:
            return {"name": "无课程"}
        