import pygame
from atom import Atom
from box import Border

from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, a: Atom):
        pygame.sprite.Sprite.__init__(self)
        self.a = a
        r = max(MIN_DRAW_RADIUS, self.a.r / SCALE)
        d = 2*r
        self.image = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, a.color, [0, 0, d, d])
        self.rect = self.image.get_rect()
        self.rect.center = (self.a.position.x / SCALE, self.a.position.y / SCALE)

    def update(self):
        self.rect.center = (self.a.position.x / SCALE, self.a.position.y / SCALE)


class BorderSprite(pygame.sprite.Sprite):
    def __init__(self, b: Border):
        pygame.sprite.Sprite.__init__(self)
        self.b = b
        self.image = pygame.Surface((ATOM_R*2, (HEIGHT / SCALE)))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.center = (-ATOM_R, HEIGHT / SCALE / 2)

    def update(self):
        self.image = pygame.Surface((self.b.position.x / SCALE, (HEIGHT / SCALE) + ATOM_R / SCALE))
        self.rect.center = (0, HEIGHT / SCALE / 2)
        self.image.fill(GRAY)


class StatScreen(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x + width / 2, y + height / 2)
