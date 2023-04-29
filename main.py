
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
    all_sprites.add([Sprite(a) for a in app.atoms], BorderSprite(app.box.borders[0]), stats_screen)
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
                return
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    for b in app.box.borders:
                        b.velocity.x, b.velocity.y = 0, 0
                elif ev.key == pygame.K_RIGHT:
                    app.box.borders[0].velocity.x = BOX_SPEED
        # print(app.box.borders[0].position)
        app.step(timestep)
        # print(f'{app.atoms[0].velocity}, {app.atoms[0].position}           {app.cur_time}, {app.events[0].time}')
        # Screen
        screen.fill(BLACK)
        # Sprites
        all_sprites.update()
        all_sprites.draw(screen)
        fill_info(app, font, screen, width)
        # Screen updating
        pygame.display.flip()
        clock.tick(fps)


def fill_info(app, font, screen, width):
    pix = 0
    stat = app.hot_stat()
    # ввод скорости стенки
    for i in range(len(stat)):
        text1 = font.render(stat[i], True, STAT_TEXT_COLOR)
        screen.blit(text1, (width + 7, pix))
        pix += 40


if __name__ == "__main__":
    main()
