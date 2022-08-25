import pygame
import os

# PYGAME Setup
os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()
pygame.init()
info = pygame.display.Info() # You have to call this before pygame.display.set_mode()

# PYGAME Setup
WIDTH,HEIGHT = info.current_w,info.current_h


# Sizes
card_size = (WIDTH / 10, HEIGHT / 5)
hero_size = (WIDTH / 8, HEIGHT / 4)
text_box_width = card_size[0] * 1.5
card_border_size = 4

# Buffers
hero_zone_buffer = 15 # pixel buffer between the hero and the border
card_zone_buffer = 15 # pixel buffer between the middle of the screen and the army
card_buffer = 10 # pixel buffer between the cards themselves

endHeroZone = 2 * hero_zone_buffer + hero_size[0]

# Colors
white = (255,255,255)
black = (0,0,0)
gold = (255,255,0)
dark_grey = (30, 30, 30)
grey = (90, 90, 90)
light_grey = (200, 200, 200)
ready_color = (102,255,0)
selected_color = (0,200,255)
targeted_color = gold
health_color = (255, 25, 60)
attack_color = (255, 140, 0)

# Fonts
font_type = "comicsans"
main_font = pygame.font.SysFont(font_type, 35)
sub_font = pygame.font.SysFont(font_type, 20)
small_font = pygame.font.SysFont(font_type, 15)