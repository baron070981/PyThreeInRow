import pygame as pg
from random import randint
import os

from elements import *
from spaces import *
from utils import *

os.system("clear && clear")

pg.init()

WIDTH_WIN = 900
HEIGHT_WIN = 760

screen = pg.display.set_mode((WIDTH_WIN, HEIGHT_WIN))
pg.display.set_caption("Три в ряд")
clock = pg.time.Clock()





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

        screen.fill((255, 255, 255))
        
        
        

        pg.display.flip()

        clock.tick(40)
    pg.quit()






if __name__ == '__main__':
    ...
    main()






