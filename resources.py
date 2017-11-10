import pygame
from helpers import (
    load_image
    )


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
    def __init__(self, *image_args):
        super().__init__()
        self.image = load_image(*image_args)
        self.rect = self.image.get_rect()

    def update(self):
        self._move()

    def _move(self):
        self.rect.move_ip(1, 0)
        if self.rect.right > 1024:
            self.rect.left = 0


class base_object(pygame.sprite.AbstractGroup):
    def __init__(self, image, **kwargs):
        super().__init__()
        if not isinstance(image, list):
            image = [image]

        self.add([base_sprite(*i) for i in image])
