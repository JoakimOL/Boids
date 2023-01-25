import tkinter
from tkinter.ttk import Label
from boid import Boid
from boidclass import Boid2
import random
import uuid

class DrawableWindow():
    def __init__(self, width, height, delay=16):
        self.root = tkinter.Tk()
        self.width, self.height = width, height
        self.delay = delay

        self.root.bind('<q>', self.quit)
        self.root.bind('<space>', self.toggle_running)

        # this is only used to draw the trails
        self.photo = tkinter.PhotoImage(width=width, height=height)

        self.canvas = tkinter.Canvas(self.root, width=width, height=height, bg='#000')
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<1>', self.handle_mouse_click)

        self.start_label = Label(self.canvas,
                                 text="press space to start",
                                 background="#000",
                                 foreground="#F00",
                                 justify=tkinter.CENTER,
                                 padding=500)
        self.start_label.pack()

        self.boids = []
        self.other_objects = []
        self.drawn_objects = {}

        self.paused = True

    def start(self):
        self.root.mainloop()

    def resize(self, width, height):
        print(f"resizing to {width}x{height}")
        self.canvas.configure(width=width, height=height)

    def handle_resize_event(self, event):
        self.resize(event.width,event.height)

    def handle_mouse_click(self, event):
        self.add_boid(Boid2(uuid.uuid4().int, 5, event.x, event.y, self.width, self.height))
        print(event)

    def toggle_running(self, _):
        self.start_label.destroy()
        self.paused = not self.paused
        if not self.paused:
            self.update()

    def update(self):
        if self.paused:
            return
        for boid in self.boids:
            boid.move()
            x = int(boid.x)
            y = int(boid.y)
            oldest = boid.update_trail(x,y)
            self.photo.put(boid.color, (x,y))
            self.photo.put("#000", oldest)
            self.canvas.move(self.drawn_objects[boid.id], boid.dx, boid.dy)
            self.canvas.event_add
            print(boid)
            print(f"number of boids: {len(self.boids)}", end="\r")
        self.root.after(self.delay, self.update)

    def motion(self, event):
        self.mousex,self.mousey = event.x, event.y
        # print(f"({self.mousex},{self.mousey})")


    def quit(self, _):
        print("Goodbye")
        exit(0)

    def add_boid(self, boid):
        self.boids.append(boid)
        self.make_drawable(boid)

    def make_drawable(self, drawable):
        drawn = self.canvas.create_oval(drawable.get_bounds(), outline=drawable.color, fill=drawable.color)
        self.drawn_objects[drawable.id] = drawn




if __name__ == "__main__":
    WIDTH = 1000
    HEIGHT = 1000
    window = DrawableWindow(WIDTH,HEIGHT)
    boids = [Boid2(id=x,
                  radius=5,
                  x=random.randint(0,WIDTH),
                  y=random.randint(0,HEIGHT),
                  max_x=WIDTH,
                  max_y=HEIGHT) for x in range(0,10)]
    for boid in boids:
        window.add_boid(boid)
    window.start()
