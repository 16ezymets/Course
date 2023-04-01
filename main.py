
import pygame
from animate import animate

FPS = 60
TIMESTEP = 1 / FPS
TITLE = "Perfect Gas"


def main():
    pygame.display.set_caption(TITLE)
    animate(FPS, TIMESTEP)


if __name__ == "__main__":
    main()
