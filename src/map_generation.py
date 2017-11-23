import random
import pygame
from src.helpers import (
    load_json_def,
    extract_random_from_dict,
    extract_from_dict
    )
from src.resources import (
    drifting_object,
    base_object,
    player_object
    )
from src.constants import (
    ZONERECT,
    SCREENRECT
    )


def spawn_zone():
    spawn_grid = [(x, y) for x in range(40, ZONERECT.right, 80) for y in range(40, ZONERECT.bottom, 80)]

    characters, char_default = load_json_def("characters.json")
    trees, tree_default = load_json_def("trees.json")
    create = extract_random_from_dict(characters, char_default)
    test = drifting_object(pos=spawn_grid[0], **create)

    sprites = []
    for x in range(10):
        pos = spawn_grid.pop(random.randint(0, len(spawn_grid)-1))
        tree = base_object(pos=pos, **trees["evergreen"])
        sprites.append(tree)
    for x in range(10):
        # balls.append(base_object(pos=(random.randint(0, ZONERECT.right), random.randint(0, ZONERECT.bottom)), **extract_from_dict("ball", characters, char_default)))
        pos = spawn_grid.pop(random.randint(0, len(spawn_grid)-1))
        create = extract_random_from_dict(characters, char_default)
        sprites.append(base_object(pos=pos, **create))

    sprites.append(test)
    allsprites = pygame.sprite.RenderPlain(sprites)

    # Adding player last
    p = extract_from_dict("player", characters, char_default)
    player = player_object(pos=SCREENRECT.center, **p)

    allsprites.add(player)

    return allsprites, player
