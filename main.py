VER = "Version: v1.0.0"
import pygame
import sys
import random
import os
import time, datetime
import yaml
from PIL import Image
from skimage import io, transform
import numpy as np

import pygame
import pygame.freetype
from pygame.locals import *

from widget import weather, todo_list, class_table, sentence, date
import utils.time as ut

class Window(object):
    def __init__(self, config):
        self.fps = config.get("FPS", 30)
        self.width = config.get("width", 900)
        self.height = config.get("height", 1600)

        background_path = config.get("background", None)
        if background_path is None:
            self.background = np.zeros((self.height, self.width, 3))
        else:
            self.background = io.imread(background_path)
            self.background = transform.resize(self.background, (self.height, self.width), anti_aliasing=True)
        self.background_time_area = self.background[0:400, 0:450 , :]
        
        self.background = pygame.surfarray.make_surface(self.background)
        self.background_time_area = pygame.surfarray.make_surface(self.background_time_area)

        # self.fonts = {}
        # for file in os.listdir("./resources/Fonts"):
        #     if file.endswith(".ttf"):
        #         self.fonts[file] = pygame.freetype.Font(os.path.join("./resources/Fonts", file))
        #     else:
        #         raise NotImplementedError("Font type is not supported yet.")

        self.screen = pygame.display.set_mode(size=(self.width, self.height))
        pygame.display.set_caption("Pirror")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

    def get_font(self, type, size):
        return pygame.freetype.Font(os.path.join("./resources/Fonts", type), size)


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

def show_time(window):
    font = pygame.freetype.Font("./resources/Fonts/苹方黑体-纤细-简.ttf", 116)

    time_string = ut.getTimeString()
    font.render_to(window.screen, (40, 60), time_string, (255,255,255))



if __name__ == "__main__":
    pygame.init()

    # 加载全局配置
    with open("configs/config.yml", "r") as fp:
        global_config = yaml.load(fp, yaml.SafeLoader)

    # 生成屏幕
    window = Window(global_config.get("window", {}))

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
                window.screen.blit(window.background, (0, 0))
                for widget in widgets:
                    widget.render(window)
        
        window.screen.blit(window.background_time_area, (0, 0))
        show_time(window)
        window.clock.tick(window.fps)

        pygame.display.update()
            







    
    