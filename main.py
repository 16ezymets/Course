import pygame
from sprites import *

FPS = 50
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
                running = False
        app.run(TIMESTEP)
        # Поле
        screen.fill(BLACK)
        # Спрайты
        all_sprites.update()
        all_sprites.draw(screen)
        # Обновление экрана
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    animate()


