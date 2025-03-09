from pathlib import Path
from random import choice

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
        self.state = False
        self.angle = 0
        self.direct_rotate = 1
        self.MOVE_STATE = False
    
    def equal(self, value):
        if self.name is None or value.name is None:
            raise ValueError('Не определены имена в Element')
        return self.name == value.name

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def set_random_image(self, *sources:str|Path|tuple):
        src = choice(sources)
        self.set_image(src)
    
    def draw_rect(self, screen):
        pg.draw.rect(screen, (200, 50, 50), self.rect, width=2)
    
    def set_image(self, src):
        if isinstance(src, (str, Path)):
            self.original_image = pg.image.load(str(src)).convert_alpha()
            self.original_image = pg.transform.scale(self.original_image, (self.width, self.height))
        elif isinstance(src, tuple):
            self.original_image = pg.Surface((self.width, self.height))
            self.original_image.fill(src)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def animated_select(self, step, angle):
        if self.state:
            if self.direct_rotate == 1 and self.angle < angle:
                self.angle += step
            if self.angle >= angle and self.direct_rotate == 1:
                self.direct_rotate = -1
                self.angle = angle
            if self.direct_rotate == -1 and self.angle > -angle:
                self.angle -= step
            if self.direct_rotate == -1 and self.angle <= -angle:
                self.direct_rotate = 1
                self.angle = -angle
            self.image = pg.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        else:
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(center=self.pos)
            self.angle = 0
            self.direct_rotate = 1

    def reset(self):
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.direct_rotate = 1
        self.state = False

    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)
    
    def scale_focuse(self, scale, is_focuse=False):
        if is_focuse:
            w, h = self.width, self.height
            self.image = pg.transform.scale(self.original_image, (w+6, h+6))
        else:
            self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def animated_move(self, target_pos):
        step = 15
        if self.MOVE_STATE:
            while True:
                tx, ty = target_pos
                x, y = self.rect.center
                if abs(x - tx) >= step:
                    x += -step if x > tx else step if x < tx else 0
                else:
                    x = tx
                if abs(y - ty) >= step:
                    y += -step if y > ty else step if y < ty else 0
                else:
                    y = ty
                self.image = self.original_image.copy()
                self.rect = self.image.get_rect()
                self.rect.center = (x, y)
                self.pos = (x, y)
                if x != tx or y != ty:
                    yield self.rect.center, self
                else:
                    self.MOVE_STATE = False
                    return

    def animated_delete(self, step=1):
        w, h =  self.image.get_size()
        w -= step
        # h -= step
        if w <= step // 2 + 1: return False
        self.image = pg.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(center=self.pos)
        return True


class Decoration(pg.sprite.Sprite):

    def __init__(self, source, width, height, pos=(0, 0)):
        super().__init__()
        self.width = width
        self.height = height
        if isinstance(source, (str, Path)):
            self.original_image = pg.image.load(str(source)).convert_alpha()
            self.original_image = pg.transform.scale(self.original_image, (width, height))
        elif isinstance(source, tuple):
            self.original_image = pg.Surface((width, height))
            self.original_image.fill(source)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos


    def draw(self, screen):
        screen.blit(self.image, self.rect)



if __name__ == "__main__":
    ...






