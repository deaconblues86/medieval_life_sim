import sys
import pygame
import json
import time
import random

from helpers import (
    load_image,
    load_json_def,
    extract_random_from_dict
    )


characters, char_default = load_json_def("characters.json")
print(char_default)

pygame.init()

size = width, height = 1024, 768

screen = pygame.display.set_mode(size)

ball = load_image("ball.gif")
background = load_image("background.jpg")
ballrect = ball.get_rect()

# Quick Demo 1
# speed = [2, 2]
# while 1:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()

#     ballrect = ballrect.move(speed)
#     if ballrect.left < 0 or ballrect.right > width:
#         speed[0] = -speed[0]
#     if ballrect.top < 0 or ballrect.bottom > height:
#         speed[1] = -speed[1]

#     screen.fill(black)
#     screen.blit(ball, ballrect)
#     pygame.display.flip()
#     time.sleep(0.01)


class GameObject():
    def __init__(self, image, height, speed, **kwargs):
        self.speed = speed
        if not isinstance(image, list):
            image = [image]

        self.image = [load_image(*i) for i in image]
        self.pos = [i.get_rect() for i in self.image]

    def move(self):
        self.pos = [pos.move(self.speed, 0) for pos in self.pos]
        if self.pos[0].right > 1024:
            for pos in self.pos:
                pos.left = 0


# Bliting over surface
# screen.blit(background, (0, 0))        # draw the background
# position = ball.get_rect()
# screen.blit(ball, position)          # draw the player
# pygame.display.update()                # and show it all
# for x in range(100):                   # animate 100 frames
#     screen.blit(background, position, position)  # erase
#     position = position.move(2, 0)     # move player
#     screen.blit(ball, position)      # draw new player
#     pygame.display.update()            # and show it all
#     pygame.time.delay(100)             # stop the program for 1/10 second


# Bliting over surface with objects
screen.blit(background, (0, 0))        # draw the background
objects = []
for x in range(10):                    # create 10 objects</i>
    create = extract_random_from_dict(characters, char_default)
    o = GameObject(**create)
    # o = GameObject(ball, x*40, random.randint(1, 40))
    objects.append(o)

while 1:
    # Check for events to quit
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()
    # blits background over current obj location
    for o in objects:
        screen.blit(background, o.pos[0], o.pos[0])
    # blits obj to new location after move
    for o in objects:
        o.move()
        for i in range(len(o.image)):
            screen.blit(o.image[i], o.pos[i])

    # Writes updates to display
    pygame.display.update()
    pygame.time.delay(100)
