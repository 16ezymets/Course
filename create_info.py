from sprites import *

f1 = pygame.font.SysFont('arial', 20)


def create_info():
    pix = 0
    stat = app.hot_stat()
    # ввод скорости стенки
    for i in range(len(stat)):
        text1 = f1.render(stat[i], True, (150, 255, 150))
        screen.blit(text1, (width + 7, 0 + pix))
        pix += 40