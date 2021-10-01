
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

def blit_text_in_middle(screen, text, font, size, width, y, color, x_range=None):
    # en_width = font.render("测", color, size=size)[1].width
    # zh_width = font.render("t", color, size=size)[1].width
    if x_range:
        x_left, x_right = x_range
    else:
        x_left, x_right = (0, width)
    text_surf, text_rect = font.render(text, color, size=size)
    text_rect.center = ((x_left+x_right)/2, y)
    screen.blit(text_surf, text_rect)

    return width, y+text_rect.height+10
    
def screen_len(text):
    ret = 0
    for c in text:
        if not "a"<=c<="z" and not "A" <= c <= "z":
            ret += 2
        else:
            ret += 1
    return ret


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((920, 920))
    font = freetype.Font("./resources/Fonts/苹方黑体-中粗-简.ttf")
    # font.underline_adjustment = -0.3
    # font.underline = True
    # x,y=blit_multiline_text(screen, ["「」「」是不是", "....,,，，。。是不是是不是"], font, 24, (10, 200), (255,255,255), down=False)
    blit_text_in_middle(screen, "「艰难困苦，玉汝于成。」", font, 24, 920, 460, (255,255,255))
    # font.render_to(screen, (x,y),"使\u0336得\u0336", (255,255,255), size=24)
    pygame.display.update()
    time.sleep(1000000)