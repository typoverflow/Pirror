VER = "Version: v1.0.0"
import pygame
import sys
import random
import os
import time, datetime
import yaml

import pygame
from pygame.locals import *

from widget import weather, todo_list, class_table, sentence

class ScreenConfig(object):
    def __init__(self, config):
        self.fps = config.get("FPS", 30)
        self.width = config.get("width", 1080)
        self.height = config.get("height", 1920)




if __name__ == "__main__":
    with open("configs/config.yml", "r") as fp:
        global_config = yaml.load(fp, yaml.SafeLoader)

    sc = ScreenConfig(global_config.get("screen", {}))

    pygame.init()
    screen = pygame.display.set_mode(size=(sc.width, sc.height))
    pygame.display.set_caption("Pirror")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    
    