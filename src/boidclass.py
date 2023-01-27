import random

from drawable import DrawableCircle, DrawableWithTrail

class Boid2(DrawableWithTrail, DrawableCircle):
    def _generate_random_direction(self) -> float:
        return random.random()*2 * 1 if random.randint(-5,5) > 0 else -1

    def __init__(self, id, radius, x, y,  max_x, max_y, color=None):
        DrawableWithTrail.__init__(self, id, x, y, max_x, max_y, color)
        DrawableCircle.__init__(self, id, radius, x, y, max_x, max_y, color)

        self.vx = self._generate_random_direction()
        self.vy = self._generate_random_direction()

        self.dx = 0
        self.dy = 0

        self._VISUAL_RANGE=125
        self._CENTERING_FACTOR=0.005
        self._MAX_SPEED_X=5
        self._MAX_SPEED_Y=5

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

    def cap_speed(self):
        direction_x = self.vx / abs(self.vx)
        direction_y = self.vy / abs(self.vy)
        if abs(self.vx) > self._MAX_SPEED_X:
            self.vx = self._MAX_SPEED_X * direction_x
        if abs(self.vy) > self._MAX_SPEED_Y:
            self.vy = self._MAX_SPEED_Y * direction_y

    def move(self, others):
        self.cohesion(others)
        self.separation(others)
        self.alignment(others)
        self.cap_speed()
        # Update position
        x, y = self.x, self.y
        x += self.vx
        y += self.vy

        self.dx = x - self.x
        self.dy = y - self.y
        self.x, self.y = x, y
        self.bounce()

    def distance(self, other):
        from math import sqrt
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def cohesion(self, others): #-> tuple[float,float]:
        centerX = 0
        centerY = 0
        numNeighbors = 0
        for boid in others:
            if self.distance(boid) < self._VISUAL_RANGE:
                centerX += boid.x
                centerY += boid.y
                numNeighbors += 1
        if numNeighbors > 0:
            centerX /= numNeighbors
            centerY /= numNeighbors

            self.vx += (centerX - self.x) * self._CENTERING_FACTOR
            self.vy += (centerY - self.y) * self._CENTERING_FACTOR

    def separation(self,others):
        _MINDISTANCE = 100
        _AVOIDFACTOR = 0.05
        moveX = 0
        moveY = 0
        for other in others:
            if other.id != self.id:
                distance = self.distance(other)
                if distance < _MINDISTANCE:
                    moveX += (self.x - other.x) / distance
                    moveY += (self.y - other.y) / distance

        self.vx += moveX*_AVOIDFACTOR
        self.vy += moveY*_AVOIDFACTOR

    def alignment(self, others):
        avgVx = 0
        avgVy = 0
        numNeighbors = 0

        for other in others:
            if self.distance(other) < self._VISUAL_RANGE:
                avgVx += other.vx
                avgVy += other.vy
                numNeighbors += 1
        if numNeighbors > 0:
            avgVx /= numNeighbors
            avgVy /= numNeighbors

            self.vx += (avgVx - self.vx) * self._CENTERING_FACTOR
            self.vy += (avgVy - self.vy) * self._CENTERING_FACTOR


    def __repr__(self) -> str:
        return f"boid {self.id:5d}: ({self.x:4.2f}, {self.y:4.2f}), speed: ({self.vx:2.2f},{self.vy:2.2f}), color={self.color:4s}"
