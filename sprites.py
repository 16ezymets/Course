
from box import Border
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


class Piston(pygame.sprite.Sprite):
    def __init__(self, border: Border):
        pygame.sprite.Sprite.__init__(self)
        self.border = border
        self.x = border.position.x
        self.y = border.position.y
        self.velocity = border.velocity.x if (border.velocity.x is not None) else border.velocity.y
        self.image = pygame.Surface((self.x, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        if self.x is not None:
            self.rect.center = (self.x // 2, height // 2)
        else:
            self.rect.center = (self.y // 2, width)

    def update(self):
        if self.x is not None:
            self.rect.center = (self.x // 2 + self.border.velocity.x, height // 2)
        else:
            self.rect.center = (width, self.x + self.border.velocity.y)

