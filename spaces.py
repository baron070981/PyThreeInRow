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
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def draw_rect(self, screen):
        pg.draw.rect(screen, (255, 50, 50), self.rect, width=1)


class GameSpace(Space):

    def __init__(self, source, width, height, pos=(0, 0), group=None):
        super().__init__(source, width, height, pos=pos)

        self.rows = 0
        self.columns = 0
        self.all_sprites = []
        self.elements_matrix: elements.Element = []
        self.ids_matrix = []
        self.sources = dict()
        self.spare_elements = set()
        self.positions = dict()
        self.last_time = pg.time.get_ticks()
    
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
        surplus_width = self.width - useful_space_width - paddings_width_space
        
        paddings_height_space = (self.rows + 2) * padding
        useful_space_height = self.rows * size
        surplus_height = self.height - useful_space_height - paddings_height_space
        return surplus_height // 2 + padding + size // 2, surplus_width // 2 + padding + size // 2


        
    def create_empty_matrix(self, rows, columns, padding=1):
        ...

    def fill_matrix(self, sources:dict):
        """
        sources: {name: path or tuple}
        """
        ...

    def delete_elements(self, *elements:elements.Element):
        ...
    



if __name__ == "__main__":
    ...








    


