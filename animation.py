
from sprites import *

FPS = 60
def animate():
    running = True
    # Процесс
    while running:
        clock.tick(FPS)
        # FPS
        for close in pygame.event.get():
            if close.type == pygame.QUIT:
                running = False
        # Закрытие Окна
        app.run()
        screen.fill(BLACK)
        # Поле
        all_sprites.update()
        all_sprites.draw(screen)
        # Спрайты
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    animate()


