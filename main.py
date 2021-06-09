VER = "Version: v1.0.0"
import pygame
import sys
import random
import os
import time, datetime
import yaml

import pygame
from pygame.locals import *

from widget import weather, todo_list, class_table, sentence, date
import utils.time as ut

class ScreenConfig(object):
        self.fps = config.get("FPS", 30)
        self.width = config.get("width", 1080)
        self.height = config.get("height", 1920)

def initialize_widgets(global_config):
    ret = []
    widgets = [k for (k, v) in global_config.get("widgets", {}).items() if v==True]
    for w in widgets:
        if w == "class_table":
            ret.append(class_table.ClassTableWidget(global_config.get("class_table")))
        elif w == "weather":
            ret.append(weather.WeatherWidget(global_config.get("weather")))
        elif w == "todo_list":
            ret.append(todo_list.TodoListWidget(global_config.get("todo_list")))
        elif w == "sentence":
            ret.append(sentence.SentenceWidget(global_config.get("sentence")))
        elif w == "date":
            ret.append(date.DateWidget(global_config.get("date")))
        else:
            raise NotImplementedError("Widget {} has not been implemented yet".format(w))
    return ret

def trigger_update_and_render(widgets, screen):
    for widget in widgets:
        widget.update_all()
        widget.render(screen)

def show_time(screen):
    pass



if __name__ == "__main__":
    # 加载全局配置
    with open("configs/config.yml", "r") as fp:
        global_config = yaml.load(fp, yaml.SafeLoader)

    # 生成屏幕配置
    screen_config = ScreenConfig(global_config.get("screen", {}))

    #初始化pygame对象
    pygame.init()
    screen = pygame.display.set_mode(size=(screen_config.width, screen_config.height))
    pygame.display.set_caption("Pirror")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    # 生成widget
    widgets = initialize_widgets(global_config)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        # 低频组件的update和渲染
        if ut.getSec() == 0:
            updated = False
            for widget in widgets:
                updated = widget.update_all() or updated
            if updated:
                screen.blit(background, (0, 0))
                for widget in widgets:
                    widget.render(screen)
        
        screen.blit(background_time_area, (0, 0))
        show_time(screen)
        clock.tick(screen_config.fps)

        pygame.display.update()
            







    
    