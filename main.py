from excel_inf import *
from sprites import *
from settings import *


def main():
    title = "Perfect Gas"
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption(title)

    app = App()
    width = app.box.size.x / SCALE + ATOM_R
    height = app.box.size.y / SCALE + ATOM_R
    screen = pygame.display.set_mode((width + STAT_WIDTH, height))

    # Sprites creating
    stats_screen = StatScreen(width, 0, STAT_WIDTH, height)
    all_sprites = pygame.sprite.Group()
    if FULL_ANIMATION:
        all_sprites.add(BorderSprite(app.box.borders[0]), stats_screen, [AtomSprite(a) for a in app.atoms])
    else:
        all_sprites.add(BorderSprite(app.box.borders[0]), stats_screen)
    all_sprites.update()

    # выделить в объект
    fps = 60
    timestep = 1 / fps / TIME_SCALE
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('arial', 20)

    running = True
    while running:
        # fps
        clock.tick(fps)
        # Window closing
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                break
        running = app.step(timestep) if running else False
        if ANIMATION:
            # Screen
            screen.fill(BLACK)
            # Sprites
            all_sprites.update()
            all_sprites.draw(screen)
        fill_info(app, font, screen, width, timestep)
        if ANIMATION:
            # Screen updating
            pygame.display.flip()
            clock.tick(fps)
    # for i in range(len(app.time)):
        # print(f"{app.time[i]};{app.press[i]};{app.volume};{app.temperature[i]}\n")
    if WRITE_DATA_TO_TEXTFILE:
        write_to_text_file(app)


LINE_HEIGHT = 32
LEFT_OFFSET = 7


def fill_info(app, font, screen, width, timestep):
    pix = 0
    stat = app.hot_stat(timestep)
    # ввод скорости стенки
    for i in range(len(stat)):
        text1 = font.render(stat[i], True, STAT_TEXT_COLOR)
        screen.blit(text1, (width + LEFT_OFFSET, pix))
        pix += LINE_HEIGHT


if __name__ == "__main__":
    main()
