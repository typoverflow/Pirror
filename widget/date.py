from utils.log import log
import time
from utils.time import *
import sxtwl

class DateWidget(object):
    YMC = [u"十一", u"十二", u"正", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十" ]
    RMC = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十", u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九", u"二十", u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", u"廿九", u"三十", u"卅一"]
    GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    JIEQI =  ["", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑","白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"]
    
    def __init__(self, config):
        self.date_info = None
        # self.time_info = None
        self.lunar_info = None
        self.lunar = sxtwl.Lunar()

        self.update_cycle = config.get("update_cycle", 1440)
        self.update_count = 0


    # def update_time_info(self):
    #     self.old_time_info = self.time_info
    #     self.time_info = time.strftime("%H:%M", time.localtime())
    #     return self.old_time_info != self.time_info
    
    def update_date_info(self):
        self.old_date_info = self.date_info
        self.date_info = "{}年{}月{}日 {}".format(
            getYear(), 
            getMonth(), 
            getDay(), 
            getWeekdayString(True)
        )
        return self.old_date_info != self.date_info

    def update_lunar_info(self):
        self.old_lunar_info = self.lunar_info
        solar_day = time.localtime()
        lunar_day = self.lunar.getDayBySolar(solar_day.tm_year, solar_day.tm_mon, solar_day.tm_mday)
        self.lunar_info = "{}{}年 {}{}月{}  {}".format(
            DateWidget.GAN[lunar_day.Lyear2.tg], 
            DateWidget.ZHI[lunar_day.Lyear2.dz], 
            "闰" if lunar_day.Lleap else "", 
            DateWidget.YMC[lunar_day.Lmc], 
            DateWidget.RMC[lunar_day.Ldi], 
            DateWidget.JIEQI[lunar_day.jqmc]
        )

        return self.old_lunar_info != self.lunar_info
    
    def update_all(self):
        self.update_count += 1
        if self.update_count % self.update_cycle == 0:
            self.update_count = 0
            # updated1 = self.update_time_info()
            updated1 = self.update_date_info()
            updated2 = self.update_lunar_info()
            return updated1 or updated2
        else:
            return False

    def render(self, screen):
        pass

if __name__ == "__main__":
    c = DateWidget()
    # c.update_time_info()
    c.update_date_info()
    c.update_lunar_info()
    print(c.date_info, c.lunar_info)
        
