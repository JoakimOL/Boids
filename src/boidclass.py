from drawable import DrawableCircle, DrawableWithTrail

class Boid2(DrawableWithTrail, DrawableCircle):
    def __init__(self, id, radius, x, y,  max_x, max_y, color=None):
        DrawableWithTrail.__init__(self, id, x, y, max_x, max_y, color)
        DrawableCircle.__init__(self, id, radius, x, y, max_x, max_y, color)

        self.vx = 1
        self.vy = 1

        self.dx = 0
        self.dy = 0

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
        return f"boid {self.id:5d}: ({self.x:4.2f}, {self.y:4.2f}), speed: ({self.vx:2.2f},{self.vy:2.2f}), color={self.color:4s}"
