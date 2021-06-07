# -*- coding:utf-8 -*-
import time
weekday_map = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']

def getTimeString():
    return time.strftime("%H:%M", time.localtime())

def getDateString():
    return time.strftime("%b/%d", time.localtime())

def getWeekdayString(zh=False):
    if not zh:
        return time.strftime("%a", time.localtime())
    else:
        id = time.localtime().tm_wday
        return weekday_map[id]

def getYear():
    return time.localtime().tm_year

def getMonth():
    return time.localtime().tm_mon

def getDay():
    return time.localtime().tm_mday

def getHour():
    return time.localtime().tm_hour

def getMinute():
    return time.localtime().tm_min

def getSec():
    return time.localtime().tm_sec

def getWday():
    return time.localtime().tm_wday