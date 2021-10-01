import datetime
from utils import time as ut
import yaml
import pygame

from widget.base import BaseWidget
from utils.log import log
from ui.gradient import gradientRect
from ui.text import blit_multiline_text


class ClassTableWidget(BaseWidget):
    def __init__(self, config):
        super(ClassTableWidget, self).__init__(config)

        self.begin = datetime.datetime.strptime(config.get("begin_date"), "%Y-%m-%d")

        self.table = config.get("table", [])
        self.table = [[] if v is None else v for (k,v) in self.table.items()]

        self.class_info = None
        self.update_cycle = config.get("update_cycle", 1440) * 60
        self.last_update =0

    def update_class(self):
        try: 
            today = datetime.datetime(ut.getYear(), ut.getMonth(), ut.getDay())
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

            log("green", "Request", "ClassTableWidget - get class info successfully.")
            return self.old_class_info != self.class_info
        except Exception as e:
            log("red", "Error", "ClassTableWidget.update_class - {}.".format(e))
            return False

    def update_all(self, now):
        if now-self.last_update >= self.update_cycle:
            self.last_update = now
            updated1 = self.update_class()
            return updated1
        else:
            return False

    def render(self, window):
        anchor_y = 300
        anchor_x = 25
        x, y = anchor_x, anchor_y

        font1 = window.get_font("苹方黑体-中粗-简")
        font2 = window.get_font("苹方黑体-细-简")

        # icon
        icon = pygame.image.load("resources/Icon/class48.png")
        icon_rect = icon.get_rect()
        icon_rect.center = (anchor_x+24, anchor_y+24)
        window.screen.blit(icon, icon_rect)

        # 标题
        title_surf, title_rect = font1.render("今日课程", (255,255,255), size=32)
        window.screen.blit(title_surf, (x+64, y+14))
        x = anchor_x+6
        y = anchor_y+46

        # 分割线
        line = gradientRect((350, 2), (255,255,255), (0,0,0))
        window.screen.blit(line, (x, y))
        x -= 6
        y += 16
        
        # 课程信息
        if self.class_info == "无课程":
            count = 1
        else:
            count = len(self.class_info)
        pygame.draw.rect(window.screen, (155,155,155), (x,y, 350, 14+32*count), 2)
        x += 9

        if self.class_info == "无课程":
            class_string = "今日不播"
            text_surf, text_rect = font2.render(class_string, (255,255,255), size=24)
            window.screen.blit(text_surf, (x, y+12))
        else:
            classes = [c["name"] for c in self.class_info]
            rooms = [c["room"] for c in self.class_info]
            r = [c["range"] for c in self.class_info]
            blit_multiline_text(window.screen, classes, font2, 24, (x, y+12), (255,255,255))
            blit_multiline_text(window.screen, r, font2, 20, (x+190, y+17), (140,140,140), lineheight=32)
            blit_multiline_text(window.screen, rooms, font2, 20, (x+250, y+15), (140,140,140), lineheight=32)      


if __name__ == "__main__":
    fp = open("configs/config.yml")
    config = yaml.load(fp)
    ct = ClassTableWidget(config["class_table"])
    ct.update_class()
        