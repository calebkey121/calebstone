import pygame
import os

# https://stackoverflow.com/questions/31538506/how-do-i-maximize-the-display-screen-in-pygame
# needed to get current screen info
os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()
pygame.init()
info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
WIDTH,HEIGHT = info.current_w,info.current_h
card_size = (WIDTH / 6, HEIGHT / 6)

main_font = pygame.font.SysFont("comicsans", 40)
sub_font = pygame.font.SysFont("comicsans", 30)