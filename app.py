import pygame
import random
from helpers import (
    load_image,
    load_sound,
    load_json_def,
    extract_from_dict,
    extract_random_from_dict,
    scroll_zone
    )
from resources import (
    cursor,
    base_object,
    player_object,
    drifting_object
    )
from constants import (
    SCREENRECT,
    ZONERECT
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
    pygame.display.set_caption('Life Sim')
    pygame.mouse.set_visible(1)

    # Loading background tiles
    bgdtile = load_image('background.jpg')
    background = pygame.Surface(bgdtile.get_rect().size)
    background.blit(bgdtile, (0, 0))
    # for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    #     background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    characters, char_default = load_json_def("characters.json")
    create = extract_random_from_dict(characters, char_default)
    test = drifting_object(pos=(100, 0), **create)

    p = extract_from_dict("player", characters, char_default)
    print(SCREENRECT.center)
    player = player_object(pos=SCREENRECT.center, **p)

    balls = []
    for x in range(10):
        balls.append(base_object(pos=(random.randint(0, ZONERECT.right), random.randint(0, ZONERECT.bottom)), **extract_from_dict("ball", characters, char_default)))

    # RenderPlain creates Sprite Group for chimp and mouse
    allsprites = pygame.sprite.RenderPlain((test, player))
    allsprites.add(balls)
    print(allsprites.sprites())
    # Clock controls frame rate
    clock = pygame.time.Clock()
    print(ZONERECT.left, ZONERECT.right, ZONERECT.top, ZONERECT.bottom)
    print(SCREENRECT.left, SCREENRECT.right, SCREENRECT.top, SCREENRECT.bottom)
    while 1:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        allsprites.clear(screen, background)
        keystate = pygame.key.get_pressed()

        x_direction = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
        y_direction = keystate[pygame.K_DOWN] - keystate[pygame.K_UP]

        scrolling = scroll_zone(x_direction * -1, y_direction * -1)
        allsprites.update(x_direction * -1, y_direction * -1, scrolling)
        player.move(x_direction, y_direction)

        allsprites.draw(screen)
        pygame.display.flip()
        # pygame.display.update(dirty)

    pygame.quit()

if __name__ == "__main__":
    main()
