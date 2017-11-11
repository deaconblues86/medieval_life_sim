from pygame.rect import Rect

image_dir = "img"
def_dir = "defs"
audio_dir = "audio"
screen_size = (1024, 768)
speed = 4

SCREENRECT = Rect(0, 0, screen_size[0], screen_size[1])

# These extended into screen - no buffer needed
EDGE_TOP = Rect(0, 0, screen_size[0], screen_size[1] / 3)
EDGE_LEFT = Rect(0, 0, screen_size[0] / 3, screen_size[1])

# These extended off screen - including buffer to comp for math
EDGE_BOTTOM = Rect(0, 2 * (screen_size[1] / 3), screen_size[0], (screen_size[1] / 3) + 10)
EDGE_RIGHT = Rect(2 * (screen_size[0] / 3), 0, (screen_size[0] / 3) + 10, screen_size[1])

PLAYERBOUNDS = [EDGE_RIGHT, EDGE_LEFT, EDGE_BOTTOM, EDGE_TOP]
print(PLAYERBOUNDS)
ZONERECT = Rect(0, 0, 1600, 1600)
