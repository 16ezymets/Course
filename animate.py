import sys
from create_sprites import *
from create_info import *

k = 0
def animate(fps: int, timestep: float | int):
    running = True
    while running:
        global k
        k += 1
        # FPS
        clock.tick(fps)
        # Window closing
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
        # print(app.box.borders[0].position)
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
