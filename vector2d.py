class Vector2d:
    def __init__(self, x: float, y: float):
        self.x = float(x) if x is not None else None
        self.y = float(y) if y is not None else None

    def __mul__(self, other):
        if not isinstance(other, float | int):
            return NotImplemented
        return Vector2d(self.x * other, self.y * other)

    def __add__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        return Vector2d(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        return Vector2d(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        if not isinstance(other, Vector2d):
            return NotImplemented
        self.x -= other.x
        self.y -= other.y
        return self

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def dist_2(self, other):
        return (other.x-self.x)**2 +(other.y-self.y)**2

    def dist_2_xy(self, x, y):
        return (x-self.x)**2 +(y-self.y)**2

