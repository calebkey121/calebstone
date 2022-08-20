import pygame
import os
import Hero
import settings


WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT),pygame.FULLSCREEN, pygame.RESIZABLE)
pygame.display.set_caption("Calebstone")
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("avatars", "backgrounds", "b1.jpg")), (settings.WIDTH, settings.HEIGHT))
wolf = Hero.Hero(hero="Wolf", deckList="CalebDeckList", side1=True)
bear = Hero.Hero(hero="Bear", deckList="DioDeckList", side1=False)

def redraw_window():
    WIN.blit(BACKGROUND, (0, 0))

    #player dividing borders 
    pygame.draw.line(WIN, (255,255,255), (settings.WIDTH / 2, 0), ((settings.WIDTH / 2, settings.HEIGHT)), 5)
    #pygame.draw.line(WIN, (255,255,255), (0, settings.HEIGHT * 2 / 3), ((settings.WIDTH, settings.HEIGHT * 2 / 3)), 5)

    wolf.draw(WIN)
    wolf.draw_army(WIN) # side 1 = true
    bear.draw(WIN)
    bear.draw_army(WIN) # side 1 = false ie side 2 

    pygame.display.update()

def main ():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                
                if wolf._sprite.collidepoint(pos):
                    wolf.select()
                else:
                    wolf.unselect()
                if bear._sprite.collidepoint(pos):
                    bear.select()
                else:
                    bear.unselect()
                
                

if __name__ == "__main__":
    main()