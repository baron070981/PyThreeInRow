import pygame as pg
from random import randint
import os

from elements import *
from spaces import *
from utils import *

os.system("clear && clear")

pg.init()
clock = pg.time.Clock()

WIDTH_WIN = 900
HEIGHT_WIN = 760

GS_WIDTH = WIDTH_WIN * 0.88
GS_HEIGHT = HEIGHT_WIN * 0.69
GS_Y = HEIGHT_WIN * 0.25
GS_X = HEIGHT_WIN * 0.07

bg_src = './src/background.png'

screen = pg.display.set_mode((WIDTH_WIN, HEIGHT_WIN))
pg.display.set_caption("Три в ряд")

bg_space = Space(bg_src, WIDTH_WIN, HEIGHT_WIN)
gamespace = GameSpace((0,0,0,0), GS_WIDTH, GS_HEIGHT, (GS_X, GS_Y))


def main():
    running = True

    while running:
        clock.tick(30)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            
            # обработка нажатия левой кнопки мыши
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                ...

        screen.fill((55, 55, 55))
        screen.blit(bg_space.image, (0,0))
        
        gamespace.draw(screen)
        gamespace.draw_rect(screen)
        

        pg.display.flip()

        clock.tick(40)
    pg.quit()






if __name__ == '__main__':
    ...
    main()






