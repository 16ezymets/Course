import pygame
from sprites import *

FPS = 60
def animate():
    running = True
    # Процесс
    while running:
        # FPS
        clock.tick(FPS)
        # Закрытие Окна
        for close in pygame.event.get():
            if close.type == pygame.QUIT:
                running = False
        app.run()
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


