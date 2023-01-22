import pygame
from objects import Atom, Box, Vector2d
from app import App


circle = pygame.image.load('Circle.bmp')
circle.set_colorkey((255, 255, 255))
circle_rect = circle.get_rect()
# Загрузка изображения


class Sprite(pygame.sprite.Sprite):
    def __init__(self, a: Atom):
        pygame.sprite.Sprite.__init__(self)
        self.a = a
        self.image = circle
        self.rect = self.image.get_rect()
        self.rect.center = (a.position.x, a.position.y)

    def update(self):
        self.rect.center = (self.a.position.x, self.a.position.y)


d = 10
app = App()
box = Box(Vector2d(900, 600))
WIDTH = box.size.x + d / 2
HEIGHT = box.size.y + d / 2
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Perfect Gas")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Основное для PyGame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
# Параметры PyGame

all_sprites = pygame.sprite.Group()
a0 = Sprite(app.atoms[0])
a1 = Sprite(app.atoms[1])
all_sprites.add(a0, a1)
all_sprites.update()
