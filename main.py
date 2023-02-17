import sys
from sprites import *

FPS = 30
TIMESTEP = 1 / FPS
TITLE = "Perfect Gas"

def main():
    pygame.display.set_caption(TITLE)
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
        stat = app.hot_stat()
        # Поле
        screen.fill(BLACK)
        # Спрайты
        all_sprites.update()
        all_sprites.draw(screen)
        # Обновление экрана
        pygame.display.flip()
        pygame.display.set_caption(TITLE + '  ' + stat)


if __name__ == "__main__":
    main()

