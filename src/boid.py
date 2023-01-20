import random

class Boid():

    class Trail():
        def __init__(self,x,y):
            self._length = 50
            self.trail = [(x,y) for _ in range(self._length)]
            self.ptr = 0

        def add_point(self,x,y):
            self.trail[self.ptr] = (x,y)
            self.ptr = (self.ptr + 1) % self._length
            return self.trail[self.ptr]

    def __init__(self, id:int, x: int, y: int, max_x, max_y):
        self.id = id
        self.x = x
        self.y = y

        self.SIZEX = 10
        self.SIZEY = 10
        self.MAXX = max_x
        self.MAXY = max_y

        self.vx = 1
        self.vy = 1

        self.dx = 0
        self.dy = 0

        self.update()
        self.color = f"#{random.randint(2,15):1x}{random.randint(2,15):1x}{random.randint(2,15):1x}"
        self.trail = self.Trail(x,y)

    def update(self):
        self._dimensions = (self.SIZEX,self.SIZEY)
        self._bounds = (self.x,
                        self.y,
                        self.x + self._dimensions[0],
                        self.y + self._dimensions[1])


    def update_trail(self,x,y):
        return self.trail.add_point(x,y)


    def bounce(self):
        if self.x < 0:
            self.x = 0
            self.vx = -self.vx
        elif self.x > self.MAXX:
            self.x = self.MAXX
            self.vx = -self.vx
        if self.y < 0:
            self.y = 0
            self.vy = -self.vy
        elif self.y > self.MAXY:
            self.y = self.MAXY
            self.vy = -self.vy


    def move(self):
        # Update position
        x, y = self.x, self.y
        x += self.vx
        y += self.vy

        self.dx = x - self.x
        self.dy = y - self.y
        self.x, self.y = x, y
        self.bounce()


    def __repr__(self) -> str:
        return f"boid {self.id:10d}: ({self.x}, {self.y}), color={self.color}"
