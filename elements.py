from pathlib import Path
from random import choice
import math

import pygame as pg


class Element(pg.sprite.Sprite):

    def __init__(self, source, width, height, pos=(0, 0), name=None, matrix_pos=None):
        super().__init__()
        self.width = width
        self.height = height
        self.name = name
        self.matrix_pos = matrix_pos
        if isinstance(source, (str, Path)):
            self.original_image = pg.image.load(str(source)).convert_alpha()
            self.original_image = pg.transform.scale(self.original_image, (width, height))
        elif isinstance(source, tuple):
            self.original_image = pg.Surface((width, height))
            self.original_image.fill(source)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.scale_k = 0
        self.last_time = pg.time.get_ticks()
        self.selected = False
    
    def equal(self, value):
        """сравнение двух элементов по их именам"""
        if self.name is None or value.name is None:
            raise ValueError('Не определены имена в Element')
        return self.name == value.name

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def draw_rect(self, screen):
        """вспомогательный метод для отрисовки границ self.rect"""
        pg.draw.rect(screen, (250, 250, 50), self.rect, width=2)

    def set_image(self, path:str|Path):
        """установка изображения из файла"""
        self.original_image = pg.image.load(str(path)).convert_alpha()
        self.original_image = pg.transform.scale(self.original_image, (self.width, self.height))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.pos)
    
    def reset(self):
        """сброс некоторых параметров и флагов до начального значения"""
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.pos)
        self.selected = False
        self.scale_k = 0

    def animate_select(self, ticks=50):
        """анимацмя выбранного элемента"""
        if not self.selected: return
        now_time = pg.time.get_ticks()
        if now_time - self.last_time >= ticks:
            self.last_time = now_time
            w, h = self.original_image.get_size()
            scale_vals = [0, -1, -2, -3, -4, -5, -5, -4, -3, -2, -1, 0]
            index = self.scale_k % len(scale_vals)
            self.scale_k += 1
            if self.scale_k >= len(scale_vals): self.scale_k = 0
            value = scale_vals[index]
            w += value
            h += value
            self.image = pg.transform.scale(self.original_image, (w, h))
            self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)




if __name__ == "__main__":
    ...






