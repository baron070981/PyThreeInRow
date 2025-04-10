import pygame as pg
from random import randint
import os
from pathlib import Path

from elements import *
from spaces import *
import utils
from records import *

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

TEXT_COLOR1 = (255, 255, 255)
TEXT_COLOR2 = (255, 30, 30)
GS_COLOR = (252, 252, 252, 110)

ROOT = Path(__file__).parent
SRC = ROOT / 'src'
SMILES = SRC / 'smiles'
ADL = SRC / 'pshik_animate'
FONT_PTH = SRC / 'fonts'

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

animate_delete_list = [
    ADL/'pshik1.png',ADL/'pshik1.png',ADL/'pshik2.png',ADL/'pshik2.png',
    ADL/'pshik3.png',ADL/'pshik3.png',ADL/'pshik4.png',ADL/'pshik4.png',
    ADL/'pshik5.png',ADL/'pshik6.png',ADL/'pshik7.png',ADL/'pshik8.png',
    ADL/'pshik9.png',ADL/'pshik10.png'
]

element_src = {
    'radost': radost,
    'zzz': zzz,
    'nyam': nyam,
    'hohot': hohot,
    'gnev': gnev,
    'balbes': balbes,
    'pechal': pechal,
    'krutoy': krutoy,
    'ulybka': ulybka,
    'udivlenie': udivlenie,
}


screen = pg.display.set_mode((WIDTH_WIN, HEIGHT_WIN))
pg.display.set_caption("Три в ряд")

bg_space = Space(bg_src, WIDTH_WIN, HEIGHT_WIN)
gamespace = GameSpace(GS_COLOR, GS_WIDTH, GS_HEIGHT, (GS_X, GS_Y))
# gamespace = GameSpace((150, 150, 50, 180), GS_WIDTH, GS_HEIGHT, (GS_X, GS_Y))
rows = 8
columns = 9
pad = 15
element_size = gamespace.get_element_size(rows, columns, pad)
top, left = gamespace.get_first_paddings(element_size, pad)

gamespace.create_empty_matrix(rows, columns, pad)
gamespace.fill_matrix(element_src)



def main():
    running = True
    animate = False
    swap_list = []
    scores = 0 # очки
    record = 0 # рекорд очков за кол-во ходов
    limit = 30 # макс кол-во ходов
    count_limit_steps = 30 # счетчик сделанных ходов
    record = get_record()
    RECORD = False
    new_record_text = "Новый рекорд:  :-("

    font = pg.font.Font(FONT_PTH / "DejaVuSans-Bold.ttf", 28)

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            
            # обработка нажатия левой кнопки мыши
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mpos = pg.mouse.get_pos()
                for el in gamespace.el_group:
                    if el.collidepoint(mpos) and not gamespace.delete_elements_group:
                        el.selected = not el.selected
                        if el.selected:
                            gamespace.add_selected(el, 2)
                            if len(gamespace.selected_elements) == 2:
                                els = gamespace.selected_elements.sprites()
                                gamespace.selected_elements.remove(*els)
                                el1, el2 = els
                                el1.reset()
                                el2.reset()
                                n = utils.get_neighbors((gamespace.rows,gamespace.columns), el1.matrix_pos[0], el1.matrix_pos[1])
                                if el2.matrix_pos in n:
                                    el1.MOVE_STATE = True
                                    el2.MOVE_STATE = True
                                    el1.target_pos = el2.rect.center
                                    el2.target_pos = el1.rect.center
                                    gamespace.swap_elements_group.add(el1, el2)
                                    count_limit_steps -= 1 if count_limit_steps > 0 else 0
                                else:
                                    el2.selected = True
                                    gamespace.add_selected(el2)
                        
                        elif not el.selected:
                            el.reset()
                            gamespace.selected_elements.remove(el)


        screen.fill((55, 55, 55))
        screen.blit(bg_space.image, (0,0))
        
        gamespace.draw(screen)
        gamespace.draw_rect(screen)

        if not gamespace.delete_elements_group:
            equals = utils.get_identical_elements(gamespace.elements_matrix, Element.equal)
            if equals:
                del_elements = gamespace.get_elements(*equals)
                gamespace.delete_elements_group.add(*del_elements)
                gamespace.delete_elements()
                for el in gamespace.delete_elements_group:
                    el.is_deleted = True

        if len(gamespace.swap_elements_group) > 0:
            gamespace.swap_elements()

        # gamespace.el_group.draw(screen)

        if not gamespace.delete_elements_group:
            for el in gamespace.selected_elements:
                el.animate_select(100)
            
        if not gamespace.delete_elements_group:
            gamespace.fill_empty_sections()


        for el in gamespace.delete_elements_group:
            if count_limit_steps > 0:
                scores += el.animate_delete(animate_delete_list, 50)
            else:
                el.animate_delete(animate_delete_list, 50)
                if scores > record and not RECORD:
                    RECORD = True
                    record = scores
                    write_record(record)
        

        if count_limit_steps == 0 and RECORD:
            new_record_text = f"Новый рекорд:  {record}"

        gamespace.el_group.draw(screen)

        score_surface = font.render(f"Очки: {scores}", True, TEXT_COLOR1)
        color = TEXT_COLOR1 if count_limit_steps > 5 else TEXT_COLOR2
        step_surface = font.render(f"Ходы: {count_limit_steps}", True, color)
        last_record_surface = font.render(f"Старый рекорд: {record}", True, TEXT_COLOR1)
        new_record_surface = font.render(new_record_text, True, TEXT_COLOR1)
        screen.blit(score_surface, (50, 33))
        screen.blit(step_surface, (300, 33))
        screen.blit(last_record_surface, (540, 18))
        screen.blit(new_record_surface, (540, 50))

        pg.display.flip()

        clock.tick(FPS)
    pg.quit()






if __name__ == '__main__':
    ...
    main()






