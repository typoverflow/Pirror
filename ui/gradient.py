import pygame
from pygame import color
import time

def gradientRect(shape, left_colour, right_colour):
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, shape)
    return colour_rect

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((920, 920))
    line = gradientRect((350, 2), (255, 255, 255, 255), (0,0,0))
    screen.blit(screen, (10,10))
    # font = freetype.Font("./resources/Fonts/苹方黑体-中粗-简.ttf")
    # blit_multiline_text(screen, ["没有完成", "完成了"], font, 24,(10, 200), (255,255,255), down=False)
    pygame.display.update()
    time.sleep(1000000)