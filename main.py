import sys
from sprites import *

FPS = 30
TIMESTEP = 1 / FPS

def animate():
    running = True
    # Процесс
    while running:
        # FPS
        clock.tick(FPS)
        # Закрытие Окна
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
        app.run(TIMESTEP)
        # Поле
        screen.fill(BLACK)
        # Спрайты
        all_sprites.update()
        all_sprites.draw(screen)
        # Обновление экрана
        pygame.display.flip()


if __name__ == "__main__":
    animate()


