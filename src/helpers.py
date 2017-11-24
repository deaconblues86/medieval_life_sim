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
from src.constants import (
    image_dir,
    def_dir,
    audio_dir,
    speed,
    )

blends = {
    "mult": BLEND_MULT,
    "add": BLEND_ADD,
    "sub": BLEND_SUB,
    "max": BLEND_MAX,
    "min": BLEND_MIN
}


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


def load_image(name, color=None, blendtype=None):
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
        if not blendtype:
            blendtype = BLEND_MULT
        image.fill(color, None, blends[blendtype])

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


def check_move_bounds(scrolling, bounds, x_direction, y_direction, relation_to_bounds='surrounds'):
    if x_direction or y_direction:
        if isinstance(scrolling, pygame.Rect):
            rect_to_move = scrolling
            # m = scrolling.move(x_direction*speed, y_direction*speed)

        else:
            rect_to_move = scrolling.rect
            # m = scrolling.rect.move(x_direction*speed, y_direction*speed)

        possibilities = []
        m = rect_to_move.move(x_direction*speed, y_direction*speed)
        if x_direction and y_direction:
            possibilities = {
                (x_direction, 0): rect_to_move.move(x_direction*speed, 0),
                (0, y_direction): rect_to_move.move(0, y_direction*speed)
                }

        if relation_to_bounds == "surrounds":
            if m.contains(bounds):
                scrolling = m, (x_direction, y_direction)
            else:
                try:
                    scrolling = [p for p in possibilities if possibilities[p].contains(bounds)]
                    scrolling = (possibilities[scrolling[0]], scrolling[0])
                except IndexError:
                    return False, (x_direction, y_direction)

        elif relation_to_bounds == "within":
            if bounds.contains(m):
                scrolling = m, (x_direction, y_direction)
            else:
                try:
                    scrolling = [p for p in possibilities if bounds.contains(possibilities[p])]
                    scrolling = (possibilities[scrolling[0]], scrolling[0])
                except IndexError:
                    return False, (x_direction, y_direction)

        elif relation_to_bounds == "exclusion":
            if bounds.contains(m):
                return False, (x_direction, y_direction)
            scrolling = m, (x_direction, y_direction)

        return scrolling


def calculate_grid(zone_rect):
    return [(x, y) for x in range(40, zone_rect.right, 80) for y in range(40, zone_rect.bottom, 80)]
