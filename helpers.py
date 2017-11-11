import pygame
import os
import json
import random

from pygame.locals import (
    BLEND_MULT,
    BLEND_ADD,
    BLEND_SUB,
    BLEND_MAX,
    BLEND_MIN
    )

from constants import (
    image_dir,
    def_dir,
    audio_dir,
    ZONERECT,
    SCREENRECT,
    speed,
    )


def load_json(name):
    fullname = os.path.join(def_dir, name)
    content = json.loads(open(fullname).read())
    return content


def load_json_def(name):
    content = load_json(name)
    default = content.get("default", {})
    if default:
        del content["default"]
    return content, default


def extract_from_dict(req_type, content, default):
    create = default
    create.update(content[req_type])
    return create


def extract_random_from_dict(content, default):
    types = [x for x in content]
    index = random.randint(0, len(types) - 1)
    create = default
    create.update(content[types[index]])
    return create


def load_image(name, color=None, blendtype=BLEND_MULT):
    fullname = os.path.join(image_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as e:
        print(f"Cannot load image: {name}")
        raise SystemExit

    image = image.convert_alpha()
    if color is not None:
        colors = load_json_def("colors.json")[0]
        color = tuple(colors.get(color, [0, 0, 0]))
        image.fill(color, None, blendtype)

    return image


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer:
        print(f"Mixer Not enabled")
        return NoneSound()
    fullname = os.path.join(audio_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as e:
        print(f"Cannot load sound: {name}")
        raise SystemExit

    return sound


def scroll_zone(x_direction, y_direction):
    global ZONERECT
    if x_direction or y_direction:
        m = ZONERECT.move(x_direction*speed, y_direction*speed)
        if not m.contains(SCREENRECT):
            return False
        ZONERECT = m

        print(ZONERECT.left, ZONERECT.right, ZONERECT.top, ZONERECT.bottom)
        print(SCREENRECT.left, SCREENRECT.right, SCREENRECT.top, SCREENRECT.bottom)
        return True
