import pygame
from app import App
from atom import *


MIN_DRAW_RADIUS = 2
STAT_WIDTH = 350


app = App()
width = app.box.size.x + Atom.r
height = app.box.size.y + Atom.r
screen = pygame.display.set_mode((width + STAT_WIDTH, height))
