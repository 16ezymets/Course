from sprites import *


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
stats_screen = StatScreen(width, 0, STAT_WIDTH, height)

# Sprites creating
all_sprites = pygame.sprite.Group()
all_sprites.add([Sprite(a) for a in app.atoms], stats_screen)
all_sprites.update()
