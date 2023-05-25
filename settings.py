ANIMATION = True

MIN_DRAW_RADIUS = 2
STAT_WIDTH = 350

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 64, 64)
BLUE = (100, 100, 255)
STAT_TEXT_COLOR = (150, 255, 150)


#  параметры бокса (экрана)
WIDTH = 1200
HEIGHT = 800
SCALE = 1  # 1 m per point
DEPTH = 1       # in meters
EXTREME_WIDTH = 150
extreme_volume = HEIGHT * EXTREME_WIDTH * SCALE * SCALE * DEPTH

#  параметры газа
ATOM_M = 1.7**(-24)
H_SPEED = 2 * 10**3  # m/s

ATOM_R = 0.4
ATOM_COUNT = 1000

# ATOM_R = 5
# ATOM_COUNT = 300

ATOM_R = 16
ATOM_COUNT = 30

BOX_SPEED = 50 // SCALE  # скорость в точках
MAX_SPEED = 2 * H_SPEED // SCALE  # скорость в точках
RED_PART = 20

STAT_MOVE_COUNT = 300
# чем больше STAT_MOVE_COUNT, тем точнее вычесление давления

R = 8.314_462  # универсальная газовая постоянная
K = 1.380_649 * 10**-23   # постоянная Больцмана
NA = 6.022_140_76 * 10**23  # число Авогардо
