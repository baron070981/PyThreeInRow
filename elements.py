from pathlib import Path
from random import choice
from math import *

import pygame as pg


class Element(pg.sprite.Sprite):

    number_selected = 0

    def __init__(self, source, width, height, pos=(0, 0), name=None, matrix_pos:tuple|None=None, weight=0):
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
        self.target_pos = pos
        self.scale_k = 0
        self.last_time_delete = pg.time.get_ticks()
        self.last_time_select = pg.time.get_ticks()
        self.last_time_swap_move = pg.time.get_ticks()
        self.selected = False
        self.delete_animate_count = 0
        self.is_deleted = False
        self.weight = 1 # кол-во очков которое может дать элемент
        self.MOVE_STATE = False
    
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
        self.MOVE_STATE = False

    def animate_select(self, ticks=50):
        """анимацмя выбранного элемента"""
        if not self.selected: return
        now_time = pg.time.get_ticks()
        if now_time - self.last_time_select >= ticks:
            self.last_time_select = now_time
            w, h = self.original_image.get_size()
            scale_vals = [0, -2, -4, -6, -8, -10, -10, -8, -6, -4, -2, 0]
            index = self.scale_k % len(scale_vals)
            self.scale_k += 1
            if self.scale_k >= len(scale_vals): self.scale_k = 0
            value = scale_vals[index]
            w += value
            h += value
            self.image = pg.transform.scale(self.original_image, (w, h))
            self.rect = self.image.get_rect(center=self.pos)

    def animate_delete(self, animate_images:list, tick_limit=100):
        """
        анимация удаления
        """
        if self.is_deleted:
            now_time = pg.time.get_ticks()
            if now_time - self.last_time_delete >= tick_limit:
                self.last_time_delete = now_time
                filename = animate_images[self.delete_animate_count%len(animate_images)]
                img = pg.image.load(filename).convert_alpha()
                img = pg.transform.scale(img, (self.width, self.height))
                self.image = img.copy()
                self.rect = self.image.get_rect(center=self.pos)
                self.delete_animate_count += 1
            if self.delete_animate_count >= len(animate_images):
                self.is_deleted = False
                self.rect.center = (10, -10)
                self.matrix_pos = (None, None)
                self.delete_animate_count = 0
                if self.alive():
                    self.kill()
                return self.weight
            return 0

    def move(self, target_pos, step=1):
        tx, ty = target_pos # целевая позиция
        x, y = self.rect.center # текущая позиция
        dist = pg.Vector2(x, y).distance_to(pg.Vector2(tx, ty))
        vect = pg.Vector2(x, y).move_towards(pg.Vector2(tx, ty), step)
        return vect.x, vect.y

    def animated_swap_move(self, target_pos, tick_limit=50, step=3):
        """
        target_pos:tuple[int, int] - x, y
        """
        if self.MOVE_STATE:
            now_time = pg.time.get_ticks()
            if now_time - self.last_time_swap_move < tick_limit:
                return True
            else:
                self.last_time_swap_move = now_time
            tx, ty = target_pos # целевая позиция
            x, y = self.move(target_pos, step)
            self.rect.center = x, y
            if int(x) == tx and int(y) == ty:
                self.MOVE_STATE = False
                self.target_pos = self.rect.center
                self.pos = self.rect.center
                return False
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collidepoint(self, point):
        return self.rect.collidepoint(point)
    
    def swap(self, other):
        self.matrix_pos, other.matrix_pos = other.matrix_pos, self.matrix_pos

if __name__ == "__main__":
    ...






