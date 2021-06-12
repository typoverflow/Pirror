VER = "v1.0.0"

import pygame
import sys
import os
import time
import yaml
from skimage import io, transform
import numpy as np

import pygame
import pygame.freetype
from pygame.locals import *

import widget
import utils.time as ut
from utils.log import log

class Window(object):
    def __init__(self, config):
        self.fps = config.get("FPS", 30)
        self.width = config.get("width", 900)
        self.height = config.get("height", 1600)

        background_path = config.get("background", None)
        if background_path is None:
            self.background = np.zeros((self.width, self.height, 3))
        else:
            self.background = io.imread(background_path)
            self.background = transform.resize(self.background, (self.height, self.width), anti_aliasing=True)
        self.background_time_area = self.background[0:400, 0:180 , :]
        
        self.background = pygame.surfarray.make_surface(self.background)
        self.background_time_area = pygame.surfarray.make_surface(self.background_time_area)

        self.fonts = dict()
        for font in os.listdir("./resources/Fonts"):
            path = os.path.join("./resources/Fonts", font)
            self.fonts[font.split(".")[0]] = pygame.freetype.Font(path)

        self.screen = pygame.display.set_mode(size=(self.width, self.height))
        pygame.display.set_caption("Pirror")
        # pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

    def get_font(self, font):
        return self.fonts.get(font)


def initialize_widgets(global_config):
    ret = []
    widgets = [k for (k, v) in global_config.get("widgets", {}).items() if v==True]
    for w in widgets:
        if w == "class_table":
            ret.append(widget.ClassTableWidget(global_config.get("class_table")))
        elif w == "weather":
            ret.append(widget.WeatherWidget(global_config.get("weather")))
        elif w == "todo_list":
            ret.append(widget.TodoListWidget(global_config.get("todo_list")))
        elif w == "sentence":
            ret.append(widget.SentenceWidget(global_config.get("sentence")))
        elif w == "date":
            ret.append(widget.DateWidget(global_config.get("date")))
        else:
            raise NotImplementedError("Widget {} has not been implemented yet".format(w))
    return ret

def trigger_update_and_render(widgets, screen):
    for widget in widgets:
        widget.update_all()
        widget.render(screen)

def show_time(window):
    font = window.get_font("sarasa-mono-cl-regular")

    time_string = ut.getTimeString()
    time_surf, time_rect = font.render(time_string, (255,255,255), size=128)
    window.screen.blit(time_surf, (60, 80))

def show_version(window):
    font = window.get_font("sarasa-mono-cl-italic")

    ver_string = "Powered by Pirror {}".format(VER)
    ver_surf, ver_rect = font.render(ver_string, (255,255,255), size=18)
    window.screen.blit(ver_surf, (window.width-10*len(ver_string), window.height-22))



if __name__ == "__main__":
    pygame.init()

    # 加载全局配置
    with open("configs/config.yml", "r") as fp:
        global_config = yaml.load(fp, yaml.SafeLoader)

    # 生成屏幕
    window = Window(global_config.get("window", {}))

    # 生成widgets
    widgets = initialize_widgets(global_config)

    while 1:
        # handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # updates and rendering for widgets
        now = time.time()
        updated = False
        for widget in widgets:
            updated = widget.update_all(now) or updated
        if updated:
            window.screen.blit(window.background, (0, 0))
            for widget in widgets:
                widget.render(window)
            log("\33[0;34;1m", "Render", "Screen - Re-rendering the whole screen.")
        
        # blit time and version info to screen
        window.screen.blit(window.background_time_area, (0, 0))
        show_time(window)
        show_version(window)
        # window.clock.tick(window.fps)
        pygame.display.update()
        pygame.time.delay(10000)
        # time.sleep(1000000000)
