import pygame
from functools import reduce
from helpers import (
    load_image
    )
from constants import(
    SCREENRECT,
    ZONERECT,
    speed)


class cursor(pygame.sprite.Sprite):
    """Makes a cursor that follows the mouse"""
    def __init__(self, cursor_image='cursor.bmp'):
        super().__init__()
        self.image = load_image(cursor_image, -1)
        self.rect = self.image.get_rect()
        self.clicking = 0

    def update(self):
        "move the cursor based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.clicking:
            self.rect.move_ip(5, 10)

    def click(self, target):
        "returns true if the cursor collides with the target"
        if not self.clicking:
            self.clicking = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unclick(self):
        self.clicking = 0


class base_sprite(pygame.sprite.Sprite):
    """ Accepts image, and optional color/blend arg """
    def __init__(self, pos, *image_args, **kwargs):
        super().__init__()
        self.name = image_args[0]
        self.image = load_image(*image_args)
        self.rect = self.image.get_rect(center=pos)

    def update(self, *args):
        self._move(*args)

    def _move(self, x_direction, y_direction, scolling):
        if scolling:
            self.rect.move_ip(x_direction*speed, y_direction*speed)


class base_object(pygame.sprite.AbstractGroup):
    def __init__(self, pos, image, **kwargs):
        super().__init__()
        if not isinstance(image, list):
            image = [image]
        self.add([base_sprite(pos, *i, **kwargs) for i in image])
        self.update_self()

    def update_self(self):
        self.rect = reduce(lambda x, y: x.union(y), [s.rect for s in self.sprites()])

    def contains(self, obj):
        if isinstance(obj, pygame.Rect):
            if all([s.rect.contains(obj) for s in self.sprites()]):
                return True
            else:
                return False
        elif isinstance(obj, base_object):
            if all(map(lambda x: x[0].rect.contains(x[1].rect), zip(self.sprites(), obj.sprites()))):
                return True
            else:
                return False


class drifting_object(base_object):
    def __init__(self, pos, image, **kwargs):
        super().__init__(pos, image)
        self.speed = 1
        for s in self.sprites():
            s.update = self.update

    def update(self, *args):
        self._move()

    def _move(self):
        for s in self.sprites():
            s.rect.move_ip(self.speed, 0)
            if s.rect.right > SCREENRECT.right:
                s.rect.left = 0


class player_object(base_object):
    def __init__(self, pos, image, **kwargs):
        super().__init__(pos, image)
        self.speed = kwargs["speed"]
        # for s in self.sprites():
        #     s.update = self.update

    # Apparently this updates actually called?  REFACTOR:  Better than calling update on every spite in base_objects
    # def update(self, *args):
    #     pass

    def move(self, x_direction, y_direction):
        # Moves player character sprites based on input
        # True up platyer_object rect afterwards
        for s in self.sprites():
            s.rect.move_ip(x_direction*self.speed, y_direction*self.speed)
            s.rect = s.rect.clamp(SCREENRECT)
        self.update_self()
