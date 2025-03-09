import pygame as pg
from random import randint
import os

from elements import *
from spaces import *
from utils import *

os.system("clear && clear")

pg.init()

WIDTH = 440
HEIGHT = 760

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()


avokado = './images/avokado.png'
avokadot = './images/avokado_t.png'
limon = './images/limon.png'
klubnika = './images/klubnika.png'
klubnikat = './images/klubnika_t.png'
fon = './images/fon.png'
settings_img = './images/settings.png'
key_img = './images/key.png'
avokado_img = './images/mascot01.png'
klubnika_img = './images/mascot2.png'
level_img = './images/level.png'
progress_img = './images/uroven.png'
status_img = './images/status.png'

sources = {'avokado':avokado, 'limon':limon, 'klubnika':klubnika}

fon = pg.image.load(fon).convert_alpha()
fon = pg.transform.scale(fon, (WIDTH, HEIGHT))

gamespace = GameSpace((0,0,0,0), WIDTH*0.93, HEIGHT*0.66, (15, HEIGHT//3//3*2+20))
gamespace.create_empty_matrix(5, 4, 15)
gamespace.fill_matrix(sources)

topleft_gs = gamespace.rect.topleft
topright_gs = gamespace.rect.topright

settings_spr = elements.Decoration(settings_img, 40, 40, (40, HEIGHT - 40))
key_spr = elements.Decoration(key_img, 40, 40, (WIDTH-40, HEIGHT - 40))
avokado_spr = elements.Decoration(avokado_img, 80, 80//0.58, (topleft_gs[0]+56, topleft_gs[1]-15))
klubnika_spr = elements.Decoration(klubnika_img, 110, 110//0.77, (topright_gs[0]-56, topright_gs[1]-5))
level_spr = elements.Decoration(level_img, WIDTH*0.62, HEIGHT*0.1, (WIDTH//2, HEIGHT*0.2))
progress_spr = elements.Decoration(progress_img, WIDTH*.66, HEIGHT*0.07, (WIDTH//2, HEIGHT*0.1))
status_spr = elements.Decoration(status_img, WIDTH*.8, HEIGHT*0.05, (WIDTH//2, HEIGHT*0.03))


def main():
    running = True
    selected_items: list[elements.Element] = []
    animated_swap_list: list[elements.Element] = []
    swap_list: list[elements.Element] = []
    animated_delete_list: list[elements.Element] = []
    delete_list: list[elements.Element] = []

    while running:
        clock.tick(30)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            
            # обработка нажатия левой кнопки мыши
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if pg.mouse.get_focused():
                    mouse_pos = pg.mouse.get_pos() # позиция мыши
                    # пребор в цикле спрайтов из группы
                    for el in gamespace.group_el:
                        if el.rect.collidepoint(mouse_pos): # проверка что позиция мыши совпадает со спрайтом
                            el.state = not el.state
                            if el.state and el not in selected_items and not animated_delete_list:
                                if len(selected_items) == 0:
                                    # добавление в список элемента если список пуст
                                    selected_items.append(el)
                                elif len(selected_items) == 1:
                                    prev = selected_items.pop() # получаю предыдущий выбранный элемент
                                    prev_pos = prev.pos # его позиция в окне
                                    el_pos = el.pos # позиция текущего элемента
                                    # получение кортежа индексов соседних элементов
                                    neighbors = gamespace.get_neighbors(*el.matrix_pos)
                                    # сбрасыаю параметры обоих элементов
                                    el.reset() 
                                    prev.reset()
                                    # если позиции (в Element.matrix_pos) предыдущего элемента нет в кортеже
                                    # индексов
                                    if prev.matrix_pos not in neighbors:
                                        ...
                                    else: 
                                        if not prev.MOVE_STATE and not el.MOVE_STATE and not animated_swap_list:
                                            prev.MOVE_STATE = True # включаю флаг, что элемент будет перемещаться
                                            el.MOVE_STATE = True
                                            # создаю генераторы анимации перемещения элементов
                                            prev_move = prev.animated_move(el_pos)
                                            el_move = el.animated_move(prev_pos)
                                            # добавляю их в список
                                            animated_swap_list.append(prev_move)
                                            animated_swap_list.append(el_move)
                            else:
                                el.reset()
                                el.MOVE_SATE = False
                                if el in selected_items: selected_items.remove(el)


        screen.fill((255, 255, 255))
        screen.blit(fon, (0, 0))
        gamespace.draw(screen)
        settings_spr.draw(screen)
        key_spr.draw(screen)
        status_spr.draw(screen)
        progress_spr.draw(screen)
        level_spr.draw(screen)
        avokado_spr.draw(screen)
        klubnika_spr.draw(screen)
        
        gamespace.add_element_to_first_row()
        DELETES = len(animated_delete_list) > 0

        # увеличение размера элемента при наведении курсора
        mouse_pos = pg.mouse.get_pos() # позиция курсора
        for el in gamespace.group_el:
            if not el.MOVE_STATE and not DELETES:
                foc = el.rect.collidepoint(mouse_pos)
                el.scale_focuse(1, foc)

        # анимация выбранного элемента
        for el in selected_items:
            if not el.MOVE_STATE and not DELETES:
                el.animated_select(.75, 8)
        
        # анимация обмена местами выбранных элементов
        if len(animated_swap_list) == 2 and not DELETES:
            gen1, gen2 = animated_swap_list
            try:
                x, el1 = next(gen1) # переход к следующей итерации
            except:
                el.MOVE_STATE = False
                animated_swap_list.remove(gen1)
                swap_list.append(el1)
            try:
                x, el2 = next(gen2)
            except:
                el.MOVE_STATE = False
                animated_swap_list.remove(gen2)
                swap_list.append(el2)
        elif len(animated_swap_list) == 1 and not not DELETES:
            gen = animated_swap_list[0]
            try:
                x, el = next(gen)
            except:
                el.MOVE_STATE = False
                animated_swap_list.remove(gen)
                swap_list.append(el)

        # удаление отработавших генераторов и взаимная замена параметоров элементов
        if len(swap_list) == 2 and not DELETES:
            gamespace.swap(*swap_list)
            swap_list = []
        
        # проверка на совпадающие подряд элементы и анимация их удаления
        if gamespace.is_not_empty() and not animated_delete_list:
            row_el, col_el = gamespace.get_identical_elements()
            animated_delete_list.extend(row_el)
            animated_delete_list.extend(col_el)
        elif animated_delete_list:
            for el in animated_delete_list:
                is_del = el.animated_delete(15)
                if not is_del: delete_list.append(el)
            gamespace.delete_elements(*delete_list)
            for el in delete_list:
                animated_delete_list.remove(el)
            delete_list = []
        else:
            # заполнение пустых клеток путем заполнения вышестоящим элементом
            gamespace.fill_empty_sections()


        gamespace.group_el.update()
        gamespace.group_el.draw(screen)
        

        pg.display.flip()

        clock.tick(40)
    pg.quit()






if __name__ == '__main__':
    ...
    main()






