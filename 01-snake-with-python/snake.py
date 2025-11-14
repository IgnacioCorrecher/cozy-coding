import random
import time
import turtle
from dataclasses import dataclass

# Screen setup
GRID = 20

screen = turtle.Screen()
screen.bgcolor("black")
screen.tracer(0)
screen.setup(width=GRID * 30, height=GRID * 30)
screen.title("Snake Game")


DIR_VEC = {
    "up": (0, GRID),
    "down": (0, -GRID),
    "left": (-GRID, 0),
    "right": (GRID, 0),
}


class Snake:
    def __init__(self):
        self.head = self._make_segment()
        self.segments = []
        self.direction = random.choice(list(DIR_VEC))  # initial inertia

    @staticmethod
    def _make_segment():
        t = turtle.Turtle()
        t.speed(0)
        t.color("white")
        t.shape("square")
        t.penup()
        return t

    # Moving the snake
    def move(self):
        # In Snake move propagates from back to head
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].goto(self.segments[i - 1].pos())
        if self.segments:
            self.segments[0].goto(self.head.pos())

        dx, dy = DIR_VEC[self.direction]
        self.head.goto(self.head.xcor() + dx, self.head.ycor() + dy)

    # Set the new direction
    def set_dir(self, d):
        # In snake you can't directly move to an opposite direction
        opp = {"up": "down", "down": "up", "left": "right", "right": "left"}

        if self.direction != opp[d]:
            self.direction = d

    # Out little snake needs to grow
    def grow(self):
        last_segment = self.segments[-1] if self.segments else self.head
        new_segment = self._make_segment()
        new_segment.goto(last_segment.pos())
        self.segments.append(new_segment)


@dataclass
class Fruit:
    name: str
    color: str
    shape: str
    # points: int -> Left as an excerside to the viewer! ;D


fruits = [
    Fruit("apple", "red", "square"),
    Fruit("banana", "yellow", "circle"),
    Fruit("orange", "orange", "circle"),
    Fruit("pear", "green", "triangle"),
]


class FruitManager:
    def __init__(self, fruits):
        self.fruits = fruits
        self.current = None
        self.t = turtle.Turtle()
        self.t.penup()
        self.t.speed(0)

    def spawn(self):
        self.current = random.choice(self.fruits)

        # Make sure fruits spawn inside the playable area
        max_x = screen.window_width() // 2 - GRID
        max_y = screen.window_height() // 2 - GRID

        x = random.randrange(-max_x, max_x, GRID)
        y = random.randrange(-max_y, max_y, GRID)

        self.t.color(self.current.color)
        self.t.shape(self.current.shape)
        self.t.goto(x, y)
        self.t.showturtle()

        return self.current


# Key listeners
screen.listen()
screen.onkey(lambda: snake.set_dir("up"), "Up")
screen.onkey(lambda: snake.set_dir("down"), "Down")
screen.onkey(lambda: snake.set_dir("left"), "Left")
screen.onkey(lambda: snake.set_dir("right"), "Right")

snake = Snake()
fm = FruitManager(fruits)
fm.spawn()

# Game Loop
while True:
    screen.update()
    snake.move()

    # Collisions

    # Wall collition
    if (
        abs(snake.head.xcor() > screen.window_width() // 2)
        or abs(snake.head.ycor()) > screen.window_height() // 2
    ):
        print("Game over")
        screen.bye()
    elif snake.head.distance(fm.t) < 20:  # Grabs a fruit
        print("Gotcha!")
        snake.grow()
        fm.spawn()

    time.sleep(0.15)
