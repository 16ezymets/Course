import pygame
from objects import Atom
from app import App


Atom.r = 16
WHITE = (255, 255, 255)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, a: Atom):
        pygame.sprite.Sprite.__init__(self)
        self.a = a
        d = 2*a.r
        self.image = pygame.Surface((d, d))
        self.image = pygame.Surface((0, 0))     #  круги пока рисуются прямо в update()
        self.image.fill(WHITE)
        self.rect = pygame.Rect(a.position.x - a.r, a.position.y - a.r, d, d)
        self.rect.center = (self.a.position.x, self.a.position.y)
        self.rect.size = (Atom.r, Atom.r)

    def update(self):
        self.rect.center = (self.a.position.x, self.a.position.y)
        pygame.draw.circle(screen, WHITE, self.rect.center, self.a.r)


# Основное для PyGame
app = App()
pygame.init()
clock = pygame.time.Clock()
width = app.box.size.x + Atom.r
height = app.box.size.y + Atom.r
screen = pygame.display.set_mode((width, height))

# Параметры PyGame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Создание спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add([Sprite(a) for a in app.atoms])
all_sprites.update()
