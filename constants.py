from atom import Atom


#  параметры газа
Atom.m = 10**(-24)

#Atom.r = 0.4
#ATOM_COUNT = 1000

#Atom.r = 5
#ATOM_COUNT = 300

Atom.r = 16
ATOM_COUNT = 50

BOX_SPEED = 20
MAX_SPEED = 200
RED_PART = 20

#  параметры бокса (экрана)
WIDTH = 1200
HEIGHT = 800
SCALE = 0.001   # 1 mm per point
DEPTH = 1       # in meters

STAT_MOVE_COUNT = 300
# чем больше STAT_MOVE_COUNT, тем точнее вычесление давления
