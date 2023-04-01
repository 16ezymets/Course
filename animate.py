import sys
from create_sprites import *
from create_info import *


def animate(fps: int, timestep: float | int):
    running = True
    while running:
        # FPS
        clock.tick(fps)
        # Window closing
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
        app.step(timestep)
        # stat = app.hot_stat()
        # Screen
        screen.fill(BLACK)
        # Sprites
        all_sprites.update()
        all_sprites.draw(screen)
        create_info()
        # Screen updating
        pygame.display.flip()
        clock.tick(fps)
