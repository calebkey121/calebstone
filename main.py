import pygame
import os
import GameManager
import settings


WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT),pygame.FULLSCREEN, pygame.RESIZABLE)
pygame.display.set_caption("Calebstone")

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("avatars", "backgrounds", "ricardo.png")), (settings.WIDTH, settings.HEIGHT))

def main ():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    #game info
    game = GameManager()


    def redraw_window():
        WIN.blit(BACKGROUND, (0, 0))

        #player dividing borders 
        pygame.draw.line(WIN, (255,255,255), (settings.WIDTH / 2, 0), ((settings.WIDTH / 2, settings.HEIGHT)), 5)
        #pygame.draw.line(WIN, (255,255,255), (0, settings.HEIGHT * 2 / 3), ((settings.WIDTH, settings.HEIGHT * 2 / 3)), 5)

        game._player1.draw(WIN)
        game._player1.draw_army(WIN) # side 1 = true
        game._player2.draw(WIN)
        game._player2.draw_army(WIN) # side 1 = false ie side 2

        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                

if __name__ == "__main__":
    main()