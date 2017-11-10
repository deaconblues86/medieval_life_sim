import pygame
from helpers import (
    load_image,
    load_sound,
    load_json_def,
    extract_random_from_dict
    )
from resources import (
    cursor,
    base_object
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Life Sim')
    pygame.mouse.set_visible(1)

    background = load_image("background.jpg")

    screen.blit(background, (0, 0))
    # Rather than updating display, simply flipping the display makes background/text visible
    pygame.display.flip()

    characters, char_default = load_json_def("characters.json")
    create = extract_random_from_dict(characters, char_default)
    test = base_object(**create)

    # RenderPlain creates Sprite Group for chimp and mouse
    allsprites = pygame.sprite.RenderPlain(test)
    print(allsprites.sprites())
    # Clock controls frame rate
    clock = pygame.time.Clock()

    while 1:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        allsprites.update()
        allsprites.clear(screen, background)
        allsprites.draw(screen)
        pygame.display.flip()
        # pygame.display.update(dirty)

    pygame.quit()

if __name__ == "__main__":
    main()
