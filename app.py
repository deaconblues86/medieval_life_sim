import pygame
from functools import reduce
from src.helpers import (
    load_image,
    check_move_bounds
    )
from src.resources import (
    cursor,
    base_object,
    interact_window
    )
from src.map_generation import (
    spawn_zone
)
from src.constants import (
    SCREENRECT,
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

    allsprites, player = spawn_zone()

    # Clock controls frame rate
    clock = pygame.time.Clock()

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
                target_objs = list(set([base for x in target for base in allsprites.sprites()[x].groups() if isinstance(base, base_object)]))
                # Creating selection of interactable Sprites in location
                window = interact_window(None, options=target_objs)
                allsprites.add(window)
                interacting = True

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
                window.kill()

            choice = window.update(key_press)
            if choice:
                window.kill()
                print(choice, target)
                interacting = False
                # If choice was what to interact with, continue interacting
                if isinstance(choice, base_object):
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
