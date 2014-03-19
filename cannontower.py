# -*- coding: utf-8 -*-

import pygame
from objects import *
from pygame.locals import *

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Cannon Tower')
    pygame.mouse.set_visible(0)

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0 , 0))

    aim = Aim()
    cannonball = Cannonball((0, 0))

    allsprites = pygame.sprite.RenderPlain(aim, cannonball)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()

    mainloop = True

    # Event loop
    while mainloop:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                mainloop = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mainloop = False
            if event.type == MOUSEBUTTONDOWN:
                target = pygame.mouse.get_pos()
                cannonball.fly(target)

        allsprites.update()
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
