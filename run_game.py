import turtle
import random

class Target:
    def __init__(self, shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy):
        target = turtle.Turtle()
        target.speed(0)
        target.shape(shape)
        target.color(color)
        target.penup()
        target.goto(x, y)
        self.target = target
        bullet = turtle.Turtle()
        bullet.speed(0)
        bullet.shape(b_shape)
        bullet.color(b_color)
        bullet.penup()
        bullet.goto(b_x, b_y)
        bullet.dy = b_dy
        bullet.state = "ready"
        self.bullet = bullet


class BossTarget(Target):
    def __init__(self, shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy):
        Target.__init__(self, shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy)
        self.target.shapesize(stretch_wid=3, stretch_len=3)
        self.health = 2


class Player(Target):
    def __init__(self, shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy):
        Target.__init__(self, shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy)
        self.target.setheading(90)


class GameInstance:
    def __init__(self):
        win = turtle.Screen()
        win.title("Shooter Game")
        win.bgcolor("black")
        win.setup(width=600, height=600)
        win.tracer(0)
        self.win = win
        self.p1 = Player(shape="triangle", color="white", x=0, y=-250,
                         b_shape="circle", b_color="yellow",
                         b_x=0, b_y=-400, b_dy=20)
        self.b1 = BossTarget(shape="square", color="purple", x=random.randint(-290, 290),
                             y=random.randint(100, 250), b_shape="circle", b_color="orange", b_x=0, b_y=400, b_dy=-10)
        self.targets = []
        for _ in range(5):
            self.targets.append(Target(shape="square", color="red", x=random.randint(-290, 290),
                                       y=random.randint(100, 250),
                                       b_shape="circle", b_color="blue",
                                       b_x=0, b_y=400, b_dy=-10))

    def player_left(self):
        x = self.p1.target.xcor()
        if x > -280:
            x -= 20
        self.p1.target.setx(x)

    def player_right(self):
        x = self.p1.target.xcor()
        if x < 280:
            x += 20
        self.p1.target.setx(x)

    def fire_player_bullet(self):
        if self.p1.bullet.state == "ready":
            self.p1.bullet.goto(self.p1.target.xcor(), self.p1.target.ycor() + 10)
            self.p1.bullet.state = "fired"

    # Function for targets to shoot bullets
    def fire_target_bullet(self, t):
        if t.bullet.state == "ready":
            t.bullet.goto(t.target.xcor(), t.target.ycor() - 10)
            t.bullet.state = "fired"

    # Function for boss to shoot bullets
    def fire_boss_bullet(self, b):
        if b.bullet.state == "ready":
            b.bullet.goto(b.target.xcor(), b.target.ycor() - 10)
            b.bullet.state = "fired"

    def update(self):
        self.win.update()

        # Move the player's bullet
        if self.p1.bullet.state == "fired":
            self.p1.bullet.sety(self.p1.bullet.ycor() + self.p1.bullet.dy)

        # Check if the player's bullet has gone off the screen
        if self.p1.bullet.ycor() > 290:
            self.p1.bullet.goto(0, -400)
            self.p1.bullet.state = "ready"

        # Check for collisions with normal targets
        for target in self.targets:
            if self.p1.bullet.distance(target.target) < 20:
                target.target.goto(random.randint(-290, 290), random.randint(100, 250))
                self.p1.bullet.goto(0, -400)
                self.p1.bullet.state = "ready"
                print("Target hit!")

        # Check for collisions with boss target
        if self.p1.bullet.distance(self.b1.target) < 30:
            self.b1.health -= 1
            self.p1.bullet.goto(0, -400)
            self.p1.bullet.state = "ready"
            print("Boss hit!")
            if self.b1.health == 0:
                self.b1.target.goto(random.randint(-290, 290), random.randint(100, 250))
                self.b1.health = 2

        # Move the targets
        for target in self.targets:
            target.target.sety(target.target.ycor() - 0.5)  # Move the targets slower

            # Check if the target has gone off the screen
            if target.target.ycor() < -290:
                target.target.goto(random.randint(-290, 290), random.randint(100, 250))

            # Randomly fire bullets from targets
            if random.randint(1, 100) > 98:  # 2% chance to fire each frame
                self.fire_target_bullet(target)

            if target.bullet.state == "fired":
                target.bullet.sety(target.bullet.ycor() + target.bullet.dy)

            # Check if the target's bullet has gone off the screen
            if target.bullet.ycor() < -290:
                target.bullet.goto(0, 400)
                target.bullet.state = "ready"

            # Check for collisions with the player
            if target.bullet.distance(self.p1.target) < 20:
                print("Player hit!")
                target.bullet.goto(0, 400)
                target.bullet.state = "ready"

        # Move the boss
        self.b1.target.sety(self.b1.target.ycor() - 0.1)  # Move the boss slower

        # Check if the boss has gone off the screen
        if self.b1.target.ycor() < -290:
            self.b1.target.goto(random.randint(-290, 290), random.randint(100, 250))

        # Randomly fire bullets from the boss
        if random.randint(1, 100) > 95:  # 5% chance to fire each frame
            self.fire_boss_bullet(self.b1)

        # Move the boss's bullet
        if self.b1.bullet.state == "fired":
            self.b1.bullet.sety(self.b1.bullet.ycor() + self.b1.bullet.dy)

        # Check if the boss's bullet has gone off the screen
        if self.b1.bullet.ycor() < -290:
            self.b1.bullet.goto(0, 400)
            self.b1.bullet.state = "ready"

        # Check for collisions with the player
        if self.b1.bullet.distance(self.p1.target) < 20:
            print("Player hit!")
            self.b1.bullet.goto(0, 400)
            self.b1.bullet.state = "ready"

        # Schedule the next update
        self.win.ontimer(self.update, 20)

    def start_game(self):
        self.win.listen()
        self.win.onkeypress(self.player_left, "Left")
        self.win.onkeypress(self.player_right, "Right")
        self.win.onkeypress(self.fire_player_bullet, "space")

        self.update()
        self.win.mainloop()


# Create game instance and start the game
game = GameInstance()
game.start_game()