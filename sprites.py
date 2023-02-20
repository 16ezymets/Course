import pygame
from atom import *
from app import App


MIN_DRAW_RADIUS = 2


class Sprite(pygame.sprite.Sprite):
    def __init__(self, a: Atom):
        pygame.sprite.Sprite.__init__(self)
        self.a = a
        r = max(MIN_DRAW_RADIUS, self.a.r)
        d = 2*r
        self.image = pygame.Surface((d, d), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, a.color, [0, 0, d, d])
        self.rect = self.image.get_rect()
        self.rect.center = (self.a.position.x, self.a.position.y)

    def update(self):
        self.rect.center = (self.a.position.x, self.a.position.y)


# Основное для PyGame
app = App()
pygame.init()
clock = pygame.time.Clock()
width = app.box.size.x + Atom.r
height = app.box.size.y + Atom.r
screen = pygame.display.set_mode((width, height))

# Создание спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add([Sprite(a) for a in app.atoms])
all_sprites.update()
