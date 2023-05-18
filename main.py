
from app import App
from sprites import *
from settings import *


def main():
    title = "Perfect Gas"
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption(title)

    app = App()
    width = app.box.size.x + ATOM_R
    height = app.box.size.y + ATOM_R
    screen = pygame.display.set_mode((width + STAT_WIDTH, height))

    # Sprites creating
    stats_screen = StatScreen(width, 0, STAT_WIDTH, height)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BorderSprite(app.box.borders[0]), stats_screen, [Sprite(a) for a in app.atoms])
    all_sprites.update()

    # выделить в объект
    fps = 60
    timestep = 1 / fps
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
        app.step(timestep)
        # Screen
        screen.fill(BLACK)
        # Sprites
        all_sprites.update()
        all_sprites.draw(screen)
        fill_info(app, font, screen, width)
        # Screen updating
        pygame.display.flip()
        clock.tick(fps)


LINE_HEIGHT = 40
LEFT_OFFSET = 7


def fill_info(app, font, screen, width):
    pix = 0
    stat = app.hot_stat()
    # ввод скорости стенки
    for i in range(len(stat)):
        text1 = font.render(stat[i], True, STAT_TEXT_COLOR)
        screen.blit(text1, (width + LEFT_OFFSET, pix))
        pix += LINE_HEIGHT


if __name__ == "__main__":
    main()
