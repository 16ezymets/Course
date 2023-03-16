import sys
from sprites import *

FPS = 60
TIMESTEP = 1 / FPS
TITLE = "Perfect Gas"
f1 = pygame.font.SysFont('arial', 20)

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
        h = 0
        for line in stat:
            text = f1.render(line, True, (150, 255, 150))
            screen.blit(text, (1225, h))
            h += 20
        # Обновление экрана
        pygame.display.flip()
        #stat_text = " ".join(stat)
        #pygame.display.set_caption(TITLE + '  ' + stat_text)


if __name__ == "__main__":
    main()

