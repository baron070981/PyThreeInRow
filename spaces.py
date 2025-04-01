from random import randint, choice
from pathlib import Path

from rich import print, inspect
import pygame as pg

import elements
from errors import *


class Space(pg.sprite.Sprite):

    def __init__(self, source, width, height, pos=(0, 0)):
        super().__init__()
        self.width = width
        self.height = height
        self.pos = pos
        if isinstance(source, (str, Path)):
            self.original_image = pg.image.load(str(source)).convert_alpha()
            self.original_image = pg.transform.scale(self.original_image, (width, height))
        elif isinstance(source, tuple):
            self.original_image = pg.Surface((width, height)).convert_alpha()
            self.original_image.fill(source)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.spare_elements: list[elements.Element] = []
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def draw_rect(self, screen):
        pg.draw.rect(screen, (255, 50, 50), self.rect, width=1)


class GameSpace(Space):

    def __init__(self, source, width, height, pos=(0, 0), group=None):
        super().__init__(source, width, height, pos=pos)
        
        self.el_group:pg.sprite.Group[elements.Element] = group if group is not None else pg.sprite.Group()
        self.rows = 0
        self.columns = 0
        self.elements_matrix: list[elements.Element] = [] # 2-мерный список элементов
        self.sources = dict() # словарь с путями до изображений элементов и имен. Ключи - имена, значения - пути
        self.spare_elements = set()
        # словарь в котором ключ - индексы в матрице, а ключи - позиции элементов по этим индексам
        self.positions: dict[tuple, tuple] = dict() 
        self.last_time = pg.time.get_ticks()
        self.selected_elements:pg.sprite.Group[elements.Element] = pg.sprite.Group()
        self.delete_elements_group:pg.sprite.Group[elements.Element] = pg.sprite.Group()
        self.swap_elements_group:pg.sprite.Group[elements.Element] = pg.sprite.Group()
    
    def get_element_size(self, rows:int, columns:int, padding=1):
        ...
        if self.rows != rows: self.rows = rows
        if self.columns != columns: self.columns = columns
        useful_space_width = self.width - (columns + 2) * padding
        useful_space_height = self.height - (rows + 2) * padding
        size_from_width = useful_space_width // columns
        size_from_height = useful_space_height // rows
        width_to_height = size_from_width * rows < useful_space_height
        height_to_width = size_from_height * columns < useful_space_width
        if width_to_height:
            return size_from_width
        elif height_to_width:
            return size_from_height
        raise SizeError()

    def get_first_paddings(self, size:int, padding=1):
        ...
        """
        return: tuple[int, int] - верхний и левый отступы
        """
        paddings_width_space = (self.columns + 2) * padding
        useful_space_width = self.columns * size
        surplus_width = self.width - useful_space_width - paddings_width_space + 1
        
        paddings_height_space = (self.rows + 2) * padding
        useful_space_height = self.rows * size
        surplus_height = self.height - useful_space_height - paddings_height_space + 1
        return surplus_height // 2 + padding + size // 2, surplus_width // 2 + padding + size // 2

    def create_empty_matrix(self, rows, columns, padding=1):
        """
        создание двумерного списка спрайтов без изображения и полностью прозрачными - elements_matrix
        заполнение словаря positions, где ключ - позиция элемента в матрице, а значение - позиция в окне
        добавление элементов в группу el_group
        """
        el_size = self.get_element_size(rows, columns, padding)
        top_pad, left_pad = self.get_first_paddings(el_size, padding)
        empty_element_color = (50, 50, 50, 100)
        x = left_pad + self.rect.x
        y = top_pad + self.rect.y
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                el = elements.Element(empty_element_color, el_size, el_size, (x, y), matrix_pos=(i, j))
                self.positions[(i,j)] = (x, y)
                row.append(el)
                self.el_group.add(el)
                x += el_size + padding
            x = left_pad + self.rect.x
            y += el_size + padding
            self.elements_matrix.append(row)

    def fill_matrix(self, sources:dict):
        """
        sources: {name: path or tuple}
        """
        self.sources.update(sources)
        names = list(self.sources)
        for el in self.el_group:
            name = choice(names)
            el.set_image(self.sources.get(name))
            el.name = name

    def add_selected(self, element:elements.Element, max_selected=1):
        """
        добавление в группу selected_elements и удаление лишних, ранее добавленных элементов
        """
        if not element.selected: return
        if len(self.selected_elements) > max_selected-1:
            sprites = self.selected_elements.sprites()
            del_sprites = sprites[:]
            self.selected_elements.remove(*del_sprites)
            [el.reset() for el in del_sprites]
        if element not in self.selected_elements:
            self.selected_elements.add(element)

    def get_elements(self, *indexes):
        elements = []
        for i, j in indexes:
            elements.append(self.elements_matrix[i][j])
        return elements

    def delete_elements(self):
        # print(self.delete_elements_group)
        score = 0
        for el in self.delete_elements_group:
            i, j = el.matrix_pos
            if i is None or j is None:
                continue
            self.elements_matrix[i][j] = None
            self.spare_elements.add(el)
    
    def swap_elements(self):
        # for el in self.swap_elements_group:
        #     state = el.animated_swap_move(el.target_pos, 20, 10)
        #     if not state: 
        #         self.swap_elements_group.remove(el)
        #         el.pos = el.rect.center
        el1, el2 = self.swap_elements_group.sprites()
        state1 = el1.animated_swap_move(el1.target_pos, 20, 10)
        state2 = el2.animated_swap_move(el2.target_pos, 20, 10)
        if not state1 and not state2:
            self.swap_elements_group.remove(el1, el2)
            el1.swap(el2)
            i,j = el1.matrix_pos
            self.elements_matrix[i][j] = el1
            el1.pos = self.positions[(i,j)]
            i,j = el2.matrix_pos
            self.elements_matrix[i][j] = el2
            el2.pos = self.positions[(i,j)]

    def add_element(self, el:elements.Element, matrix_pos:tuple[int, int]):
        i, j = matrix_pos
        name = choice([*self.sources.keys()])
        src = self.sources[name]
        el.set_image(src)
        el.name = name
        el.rect.center = self.positions.get((i, j))
        el.pos = self.positions.get((i, j))
        self.el_group.add(el)
        self.elements_matrix[i][j] = el
        el.matrix_pos = i, j
    
    def get_column_up(self, row, column) -> tuple[list[elements.Element], list[tuple[int, int]]]:
        """
        возвращает список элементов столбца и их индексы
        """
        coords = list(map(lambda x: (x, column), range(0, row)))[::-1]
        elements = list(map(lambda x: self.elements_matrix[x[0]][x[1]], coords))
        return elements, coords

    def add_element_to_first_row(self):
        for i, el in enumerate(self.elements_matrix[0]):
            if el is None:
                el = self.spare_elements.pop()
                self.add_element(el, (0, i))
    
    def fill_empty_sections(self):
        for i, row in enumerate(self.elements_matrix):
            self.add_element_to_first_row()
            if all(row): continue
            for j, col in enumerate(row):
                if col is None:
                    elements, coords = self.get_column_up(i, j)
                    for x, el in enumerate(elements):
                        self.elements_matrix[i-x][j] = el
                        self.elements_matrix[i-x-1][j] = None
                        el.matrix_pos = i-x, j
                        el.rect.center = self.positions.get((i-x, j))
                        el.pos = self.positions.get((i-x, j))


if __name__ == "__main__":
    ...








    


