import pygame
import random
from functools import reduce
from helpers import (
    load_image,
    load_sound,
    load_json_def,
    extract_from_dict,
    extract_random_from_dict,
    check_move_bounds
    )
from resources import (
    cursor,
    base_sprite,
    base_object,
    player_object,
    drifting_object,
    interact_window
    )
from constants import (
    SCREENRECT,
    PLAYERBOUNDS,
    ZONERECT
    )


def main():
    global ZONERECT

    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
    pygame.display.set_caption('Medieval Life Sim')
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
    trees, tree_default = load_json_def("trees.json")
    create = extract_random_from_dict(characters, char_default)
    test = drifting_object(pos=(100, 0), **create)

    balls = []
    tree = base_object(pos=SCREENRECT.center, **trees["evergreen"])
    balls.append(tree)
    for x in range(10):
        # balls.append(base_object(pos=(random.randint(0, ZONERECT.right), random.randint(0, ZONERECT.bottom)), **extract_from_dict("ball", characters, char_default)))
        create = extract_random_from_dict(characters, char_default)
        balls.append(base_object(pos=(random.randint(0, ZONERECT.right), random.randint(0, ZONERECT.bottom)), **create))

    # RenderPlain creates Sprite Group for chimp and mouse
    allsprites = pygame.sprite.RenderPlain((test,))
    allsprites.add(balls)
    print(allsprites.sprites())
    # Clock controls frame rate
    clock = pygame.time.Clock()

    # Adding player last
    p = extract_from_dict("player", characters, char_default)
    player = player_object(pos=SCREENRECT.center, **p)

    allsprites.add(player)

    interacting = False
    while True:
        clock.tick(100)
        # Handling Exit events separately
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        # Clean up screen and watch for events
        allsprites.clear(screen, background)
        keystate = pygame.key.get_pressed()

        # Checking for and handling interactions
        if not interacting and keystate[pygame.K_SPACE]:
            target = player.rect.collidelistall(allsprites.sprites())
            if target is not None:
                # Creating selection of interactable Sprites in location
                window = interact_window(None, options=[allsprites.sprites()[x] for x in target])
                allsprites.add(window)
                interacting = True

                # target = allsprites.sprites()[target]
                # window = interact_window(target)
                # allsprites.add(window)

        if interacting:
            pygame.event.wait()
            key_press = None
            if keystate[pygame.K_DOWN]:
                key_press = "down"
            elif keystate[pygame.K_UP]:
                key_press = "up"
            elif keystate[pygame.K_RETURN]:
                key_press = "select"
            elif keystate[pygame.K_ESCAPE]:
                key_press = "exit"
                interacting = False

            choice = window.update(key_press)
            if choice:
                window.kill()
                print(choice, target)
                interacting = False
                # If choice was what to interact with, continue interacting
                if isinstance(choice, base_sprite):
                    target = choice
                    window = interact_window(choice)
                    allsprites.add(window)
                    interacting = True

        # if not interacting, operating under normal conditions
        if not interacting:
            x_direction = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
            y_direction = keystate[pygame.K_DOWN] - keystate[pygame.K_UP]

            view_x_direction = -1 * (keystate[pygame.K_d] - keystate[pygame.K_a])
            view_y_direction = -1 * (keystate[pygame.K_s] - keystate[pygame.K_w])

            scrolling = False
            req_move = (x_direction, y_direction)
            best_move = view_move = (view_x_direction, view_y_direction)
            if view_x_direction or view_y_direction:
                scrolling, best_move = check_move_bounds(ZONERECT, SCREENRECT, *(view_move))
                if scrolling:
                    ZONERECT = scrolling

            allsprites.update(*best_move, scrolling)
            player.move(*req_move)

        allsprites.draw(screen)
        pygame.display.flip()
        # pygame.display.update(dirty)

    pygame.quit()


if __name__ == "__main__":
    main()
