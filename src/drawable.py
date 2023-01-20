import random

class Drawable():
    def __init__(self, id, x, y, max_x, max_y, color = None):
        self.id = id
        self.color = f"#{random.randint(2,15):1x}{random.randint(2,15):1x}{random.randint(2,15):1x}" if color is None else color

        self.MAXX = max_x
        self.MAXY = max_y

        self.x = x
        self.y = y

    def get_bounds(self):
        pass


class DrawableCircle(Drawable):
    def __init__(self, id, radius, x, y,  max_x, max_y, color=None):
        super().__init__(id, x, y, max_x, max_y, color)

        self.radius = radius

    def get_bounds(self):
        return (self.x - self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)

class DrawableWithTrail(Drawable):
    class Trail():
        def __init__(self, x, y, length=50):
            self._length = length
            self.trail = [(x,y) for _ in range(self._length)]
            self.ptr = 0

        def add_point(self,x,y):
            self.trail[self.ptr] = (x,y)
            self.ptr = (self.ptr + 1) % self._length
            return self.trail[self.ptr]

    def __init__(self, id, x, y,  max_x, max_y, color=None):
        super().__init__(id, x, y, max_x, max_y, color)
        self.trail = self.Trail(x,y)

    def update_trail(self,x,y):
        return self.trail.add_point(x,y)
