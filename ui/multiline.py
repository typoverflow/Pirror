
from pygame import surface
import pygame
from pygame import freetype
import time


def blit_multiline_text(screen, text, font, size, pos, color, down=True, lineheight=None):
    _, __ = font.render("test", color, size=size)
    lineheight = __.height*(1+1/1.2) if lineheight is None else lineheight

    x, y = pos[0], pos[1] if down else pos[1]-__.height
    flag = 1 if down else -1
    for line in text:
        line_surface, line_rect = font.render(line, color, size=size)
        screen.blit(line_surface, (x, y))
        y += flag*lineheight
    
    if down:
        return x, y
    else:
        return x, y+__.height

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((920, 920))
    font = freetype.Font("./resources/Fonts/苹方黑体-中粗-简.ttf")
    font.underline_adjustment = -0.3
    font.underline = True
    x,y=blit_multiline_text(screen, ["☒☑☐", "完成了"], font, 24, (10, 200), (255,255,255), down=False)
    # font.render_to(screen, (x,y),"使\u0336得\u0336", (255,255,255), size=24)
    pygame.display.update()
    time.sleep(1000000)