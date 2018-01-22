import pygame
import os
import random
from functools import reduce
from src.helpers import (
    load_image
    )
from src.constants import (
    font_file,
    SCREENRECT,
    speed,)


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


# WIP:  base_object is expected rather than Sprite.  Requires proper set up of message window (art, etc)
class message_window(pygame.sprite.Sprite):
    def __init__(self, message):
        super().__init__()
        # self.image = load_image(cursor_image, -1)
        self.image = pygame.Surface((600, 40))
        self.image.fill((100, 50, 0))
        self.rect = self.image.get_rect(center=SCREENRECT.midbottom)
        self.rect = self.rect.move((20, 0))

        self.font = pygame.font.Font(os.path.join(font_file), 20)
        self.color = pygame.Color('white')

        self.message = self.font.render(message, 0, self.color)
        self.image.blit(self.message, self.rect.center)
        self.timer = 100

    def update(self, *args):
        self.timer -= 1
        if self.timer == 0:
            self.kill()


class interact_window(pygame.sprite.Sprite):
    def __init__(self, target, options=None, image=None):
        super().__init__()
        # self.image = load_image(cursor_image, -1)
        self.target = target
        self.image = pygame.Surface((200, 150))
        self.rect = self.image.get_rect()

        self.font = pygame.font.Font(os.path.join(font_file), 20)
        self.color = pygame.Color('white')
        self.selection = pygame.Color('yellow')

        # Need to better define options vs interactions -- I believe they'll be different
        if options:
            self.interactions = {x.name: x for x in options}
            self.interactions["quit"] = True
            self.options = [x.name for x in options]
            self.options.append("quit")
        else:
            self.interactions = getattr(target, "interactions", {})
            self.interactions["quit"] = True
            self.options = []
            for i in self.interactions:
                self.options.append(i)
            print(self.interactions, self.options)

        self.offset = 0
        self.update(None)

    def update(self, key_press):
        if key_press == "down":
            self.offset += 1
        elif key_press == "up":
            self.offset -= 1
        elif key_press == "select":
            return self.interactions[self.options[self.offset]]

        if self.offset < 0:
            self.offset = 0

        pos = 0
        self.offset = min(self.offset, len(self.options) - 1)
        self.image.fill((100, 50, 0))

        for x in range(max(min(self.offset, len(self.options) - 3), 0), min(self.offset + 3, len(self.options))):
            color = self.color
            if x == self.offset:
                color = self.selection

            option = self.font.render(self.options[x], 0, color)
            self.image.blit(option, (10, (pos * 50) + 12))
            pos += 1


class base_sprite(pygame.sprite.Sprite):
    """ Accepts image, and optional color/blend arg """
    def __init__(self, pos, image_index=None, **components):
        super().__init__()
        images = components.get("images")
        colors = components.get("colors")
        blends = components.get("blends")
        if not image_index:
            image_index = random.randint(0, len(images) - 1)

        img = images[image_index] if images else "None"
        img_color = colors[random.randint(0, len(colors) - 1)] if colors else None
        img_blend = blends[random.randint(0, len(blends) - 1)] if blends else None
        self.name = img
        self.image = load_image(*(img, img_color, img_blend))
        self.rect = self.image.get_rect(center=pos)

        if components.get("interactions"):
            self.interactions = components.get("interactions")

    def update(self, *args):
        self._move(*args)

    def _move(self, x_direction, y_direction, scolling):
        if scolling:
            self.rect.move_ip(x_direction*speed, y_direction*speed)


class base_object(pygame.sprite.AbstractGroup):
    comp_meta = [
        "link_images",
        "image_range"
        ]

    def __init__(self, pos, **kwargs):
        super().__init__()
        image_index = None
        components = kwargs["components"]
        if components.get("link_images"):
            try:
                image_index = random.randint(0, components["image_range"] - 1)
            except KeyError:
                image_index = None
        self.add([base_sprite(pos, image_index, **components[comp]) for comp in components if comp not in self.comp_meta])
        self.get_rect()

        self.name = kwargs.get("name", "Unknown")
        if kwargs.get("interactions"):
            self.interactions = kwargs.get("interactions")
        self.inventory = []

    def get_rect(self):
        self.rect = reduce(lambda x, y: x.union(y), [s.rect for s in self.sprites()])
        return self.rect

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

    def kill(self):
        for s in self.sprites():
            s.kill()


class drifting_object(base_object):
    def __init__(self, pos, **kwargs):
        super().__init__(pos, **kwargs)
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
    def __init__(self, pos, **kwargs):
        super().__init__(pos, **kwargs)
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
        self.get_rect()
