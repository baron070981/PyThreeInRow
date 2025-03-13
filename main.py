import pygame as pg
from random import randint
import os
from pathlib import Path

from elements import *
from spaces import *
from utils import *

os.system("clear && clear")

pg.init()
clock = pg.time.Clock()

FPS = 40
WIDTH_WIN = 900
HEIGHT_WIN = 760

GS_WIDTH = WIDTH_WIN * 0.88
GS_HEIGHT = HEIGHT_WIN * 0.69
GS_Y = HEIGHT_WIN * 0.25
GS_X = WIDTH_WIN * 0.07

ROOT = Path(__file__).parent
SRC = ROOT / 'src'
SMILES = SRC / 'smiles'

bg_src = SRC / 'background.png'
radost = SMILES / 'radost.png'
zzz = SMILES / 'zzz.png'
nyam = SMILES / 'nyamnyam.png'
hohot = SMILES / 'hohot.png'
gnev = SMILES / 'gnev.png'
balbes = SMILES / 'balbes.png'
pechal = SMILES / 'pechal.png'
krutoy = SMILES / 'krutoy.png'
ulybka = SMILES / 'ulybka.png'
udivlenie = SMILES / 'udivlenie.png'





screen = pg.display.set_mode((WIDTH_WIN, HEIGHT_WIN))
pg.display.set_caption("Три в ряд")

bg_space = Space(bg_src, WIDTH_WIN, HEIGHT_WIN)
gamespace = GameSpace((250, 250, 250, 50), GS_WIDTH, GS_HEIGHT, (GS_X, GS_Y))

element_size = gamespace.get_element_size(2, 2, 5)
top, left = gamespace.get_first_paddings(element_size, 5)
top += GS_Y
left += GS_X

test_element = Element(balbes, element_size, element_size, (left, top))

def main():
    running = True
    animate = False

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            
            # обработка нажатия левой кнопки мыши
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mpos = pg.mouse.get_pos()
                # if pg.mouse.get_focused():
                #     ...
                #     test_element.selected = not test_element.selected
                #     if not test_element.selected:
                #         test_element.reset()

        screen.fill((55, 55, 55))
        screen.blit(bg_space.image, (0,0))
        
        gamespace.draw(screen)
        gamespace.draw_rect(screen)
        
        test_element.draw(screen)
        test_element.draw_rect(screen)
        test_element.animate_select(70)
        

        pg.display.flip()

        clock.tick(FPS)
    pg.quit()






if __name__ == '__main__':
    ...
    main()






