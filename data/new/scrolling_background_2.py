# Source - https://stackoverflow.com/a
# Posted by Rabbid76
# Retrieved 2025-11-29, License - CC BY-SA 4.0

import pygame
from pygame import *
import os

pygame.init()

WIDTH, HEIGHT = 472, 708
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# Load background image
BG = pygame.image.load(os.path.join('images', 'BG.jpg'))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


class Background(object):
    def __init__(self, win, image):
        self.win = win
        self.image = image
        self.bgY = 0  # Only need one Y offset with modulo trick

    def draw(self):
        h = self.image.get_height()

        # Draw 3 stacked images so scrolling always covers the screen
        self.win.blit(self.image, (0, self.bgY - h))
        self.win.blit(self.image, (0, self.bgY))
        self.win.blit(self.image, (0, self.bgY + h))

        pygame.display.update()

    def bg_movement(self):
        keys = pygame.key.get_pressed()
        h = self.image.get_height()

        # Move up
        if keys[K_w]:
            self.bgY = (self.bgY + 2) % h

        # Move down
        if keys[K_s]:
            self.bgY = (self.bgY - 2) % h


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