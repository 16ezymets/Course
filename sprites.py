
from screen_settings import *


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


class StatScreen(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x + width // 2, y + height // 2)
