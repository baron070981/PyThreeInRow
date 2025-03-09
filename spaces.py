from random import randint, choice
from pathlib import Path

from rich import print, inspect
import pygame as pg

import elements


class GameSpace(pg.sprite.Sprite):

    def __init__(self, source, width, height, pos=(0, 0), group=None):
        super().__init__()
        self.width = width
        self.height = height
        self.pos = pos
        self.group_el = group if group is not None else pg.sprite.Group()
        if isinstance(source, (str, Path)):
            self.original_image = pg.image.load(str(source)).convert_alpha()
            self.original_image = pg.transform.scale(self.original_image, (width, height))
        elif isinstance(source, tuple):
            self.original_image = pg.Surface((width, height)).convert_alpha()
            self.original_image.fill(source)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=pos)

        self.all_sprites = []
        self.elements_matrix: elements.Element = []
        self.ids_matrix = []
        self.sources = dict()
        self.spare_elements = set()
        self.positions = dict()
        self.last_time = pg.time.get_ticks()
    
    def get_element_size(self, rows, columns, padding=1):
        total_pad_x = (columns + 1) * padding # 25
        total_pad_y = (rows + 1) * padding # 30
        useful_width = self.width - total_pad_x # 395
        useful_height = self.height - total_pad_y # 476
        size_from_width = useful_width // columns # 98
        size_from_height = useful_height // rows # 95
        height_to_width = self.width - (size_from_height * columns + total_pad_x) # 
        width_to_height = self.height - (size_from_width * rows + total_pad_y)
        if height_to_width >= 0 and width_to_height >= 0:
            return min(height_to_width, width_to_height)
        # if size_from_height > size_from_width:
        #     correct_padding = self.width - ()
        return min(size_from_height, size_from_width)
        
    def create_empty_matrix(self, rows, columns, padding=1):
        w = h = self.get_element_size(rows, columns, padding)
        print(self.width, w, self.height, h)
        x = self.rect.x + w // 2 + padding
        y = self.rect.y + w // 2 + padding
        for i in range(rows):
            r = []
            for j in range(columns):
                self.positions[(i,j)] = (x, y)
                el = elements.Element((100,100,100), w, h, (x, y), matrix_pos=(i,j))
                r.append(el)
                self.group_el.add(el)
                x += w + padding
            x = self.rect.x + w // 2 + padding
            y += h + padding
            self.elements_matrix.append(r)

    def fill_matrix(self, sources:dict):
        """
        sources: {name: path or tuple}
        """
        self.sources.update(sources)
        names = list(self.sources.keys())
        for el in self.group_el:
            name = choice(names)
            src = self.sources[name]
            el.set_image(src)
            el.name = name

    def delete_elements(self, *elements:elements.Element):
        for el in elements:
            i, j = el.matrix_pos
            if i is None or j is None:
                continue
            el.kill()
            self.elements_matrix[i][j] = None
            el.rect.center = (10, -10)
            el.matrix_pos = (None, None)
            self.spare_elements.add(el)
    
    def add_element_to_first_row(self):
        for i, el in enumerate(self.elements_matrix[0]):
            if el is None:
                el = self.spare_elements.pop()
                self.add_element(el, (0, i))

    def get_column_up(self, row, column) -> tuple[list[elements.Element], list[tuple[int, int]]]:
        """
        возвращает список элементов столбца и их индексы
        """
        coords = list(map(lambda x: (x, column), range(0, row)))[::-1]
        elements = list(map(lambda x: self.elements_matrix[x[0]][x[1]], coords))
        return elements, coords
    
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

    def is_not_empty(self):
        return all(map(lambda x: all(x), self.elements_matrix))

    def add_element(self, el, matrix_pos):
        i, j = matrix_pos
        name = choice([*self.sources.keys()])
        src = self.sources[name]
        el.set_image(src)
        el.name = name
        el.rect.center = self.positions.get((i, j))
        el.pos = self.positions.get((i, j))
        self.group_el.add(el)
        self.elements_matrix[i][j] = el
        el.matrix_pos = i, j

    def get_identical_elements(self):
        row_elements = set()
        for i, row in enumerate(self.elements_matrix):
            for j, col in enumerate(row[:-2]):
                if any(map(lambda x: x is None, row[j:j+3])):
                    continue
                if all(map(lambda x: col.equal(x), row[j+1:j+3])):
                    row_elements.add(col)
                    row_elements.add(row[j+1])
                    row_elements.add(row[j+2])
        
        col_elements = set()
        for i in range(len(self.elements_matrix[0])):
            coords = [*map(lambda x: (x, i), range(len(self.elements_matrix)))]
            for j in range(len(coords)-2):
                r,c = coords[j]
                el = self.elements_matrix[r][c]
                next_elements = [*map(lambda x: self.elements_matrix[x[0]][x[1]], coords[j+1:j+3])]
                # next_elements = map(lambda x, y: self.elements_matrix[x][y], coords[j+1:j+3])
                if None in next_elements or el is None: continue
                if all(map(lambda x: el.equal(x), next_elements)):
                    col_elements.add(el)
                    col_elements.add(next_elements[0])
                    col_elements.add(next_elements[1])
        
        return row_elements, col_elements

    def get_neighbors(self, row, column):
        top, right, bottom, left = [None]*4
        top = None if row == 0 else (row-1, column)
        right = None if column == len(self.elements_matrix[0])-1 else (row, column+1)
        bottom = None if row == len(self.elements_matrix)-1 else (row+1, column)
        left = None if column == 0 else (row, column-1)
        indexes = tuple(filter(lambda x: x, [top, right, bottom, left]))
        return indexes

    def swap(self, el1:elements.Element, el2:elements.Element):
        matr_pos1 = el1.matrix_pos
        pos1 = self.positions.get(matr_pos1)

        matr_pos2 = el2.matrix_pos
        pos2 = self.positions.get(matr_pos2)

        el1.matrix_pos = matr_pos2
        el2.matrix_pos = matr_pos1

        el1.pos = pos2
        el1.image = el1.original_image.copy()
        el1.rect = el1.image.get_rect(center=pos2)
        self.elements_matrix[matr_pos2[0]][matr_pos2[1]] = el1

        el2.pos = pos1
        el2.image = el2.original_image.copy()
        el2.rect = el2.image.get_rect(center=pos1)
        self.elements_matrix[matr_pos1[0]][matr_pos1[1]] = el2

    def update_matrix_pos(self):
        for i, row in enumerate(self.elements_matrix):
            for j, el in enumerate(row):
                el.matrix_pos = (i, j)
 
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)
    
    def draw_rect(self, screen):
        pg.draw.rect(screen, (255, 50, 50), self.rect, width=1)
    



if __name__ == "__main__":
    ...
    m = [
        [1,2,3,4],
        [5,2,3,4],
        # [None, None, None, None],
        [7,2,3,4],
    ]
    print(all(map(lambda x: all(x), m)))


