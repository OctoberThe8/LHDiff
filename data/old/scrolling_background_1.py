# Source - https://stackoverflow.com/q
# Posted by TheDarkObjective
# Retrieved 2025-11-29, License - CC BY-SA 4.0

import pygame
from pygame import *
import os

pygame.init()

WIDTH, HEIGHT = 472, 708

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

BG = pygame.image.load(os.path.join('images', 'BG.jpg'))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

class Background(object):
    def __init__(self, win, image):
        self.win = win
        self.image = image
        self.bgY = 0
        self.bgY2 = BG.get_height()
        self.bgY3 = BG.get_height() * -1

    def draw(self):
        self.win.blit(self.image, (0, self.bgY))
        self.win.blit(self.image, (0, self.bgY2))
        self.win.blit(self.image, (0, self.bgY3))
        pygame.display.update()

    def bg_movement(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.bgY += 2
            self.bgY2 += 2
            self.bgY3 += 2
        if keys[K_s]:
            self.bgY -= 2
            self.bgY2 -= 2
            self.bgY3 -= 2
        if self.bgY < self.image.get_height() * -1:
            self.bgY = self.image.get_height()
        if self.bgY2 < self.image.get_height() * -1:
            self.bgY2 = self.image.get_height()
        if self.bgY3 < self.image.get_height() * -1:
            self.bgY3 = (self.image.get_height() * -1)

player = Background(WIN, BG)

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        player.draw()
        player.bg_movement()

    pygame.quit()

if __name__ == '__main__':
    main()
