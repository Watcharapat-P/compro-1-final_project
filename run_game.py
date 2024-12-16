import turtle
import random
from main_menu import Menu

class Target:
    def __init__(self, shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy):
        self.target = turtle.Turtle()
        self.target.speed(0)
        self.target.shape(shape)
        self.target.color(color)
        self.target.penup()
        self.target.goto(x, y)
        self.bullet = turtle.Turtle()
        self.bullet.speed(0)
        self.bullet.shape(b_shape)
        self.bullet.color(b_color)
        self.bullet.penup()
        self.bullet.goto(b_x, b_y)
        self.bullet.dy = b_dy
        self.bullet.state = "ready"


class BossTarget(Target):
    def __init__(self, shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy):
        super().__init__(shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy)
        self.target.shapesize(stretch_wid=3, stretch_len=3)
        self.health = 2


class Player(Target):
    def __init__(self, shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy):
        super().__init__(shape, color, x, y, b_shape, b_color, b_x, b_y, b_dy)
        self.target.setheading(90)
        self.hp = 10


class ShooterGame:
    def __init__(self):
        self.win = turtle.Screen()
        self.win.title("Shooter Game")
        self.win.bgcolor("black")
        self.win.setup(width=600, height=600)
        self.win.tracer(0)

        self.player = Player(shape="triangle", color="white", x=0, y=-250,
                             b_shape="circle", b_color="yellow",
                             b_x=0, b_y=-400, b_dy=20)
        self.boss = BossTarget(shape="square", color="purple", x=random.randint(-290, 290),
                               y=random.randint(100, 250), b_shape="circle", b_color="orange", b_x=0, b_y=400, b_dy=-10)
        self.targets = [Target(shape="square", color="red", x=random.randint(-290, 290),
                               y=random.randint(100, 250), b_shape="circle", b_color="blue", b_x=0, b_y=400, b_dy=-10) for _ in range(5)]

        self.score = 0
        self.score_display = turtle.Turtle()
        self.score_display.speed(0)
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(0, 260)
        self.update_score()

        self.hp_display = turtle.Turtle()
        self.hp_display.speed(0)
        self.hp_display.color("white")
        self.hp_display.penup()
        self.hp_display.hideturtle()
        self.hp_display.goto(-200, 260)
        self.update_hp()

        self.win.listen()
        self.win.onkeypress(self.player_left, "Left")
        self.win.onkeypress(self.player_right, "Right")
        self.win.onkeypress(self.fire_player_bullet, "space")

        self.update()
        self.win.mainloop()

    def update_score(self):
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}", align="center", font=("Arial", 24, "normal"))

    def update_hp(self):
        self.hp_display.clear()
        self.hp_display.write(f"HP: {self.player.hp}", align="center", font=("Arial", 24, "normal"))

    def player_left(self):
        x = self.player.target.xcor()
        if x > -280:
            x -= 20
        self.player.target.setx(x)

    def player_right(self):
        x = self.player.target.xcor()
        if x < 280:
            x += 20
        self.player.target.setx(x)

    def fire_player_bullet(self):
        if self.player.bullet.state == "ready":
            self.player.bullet.goto(self.player.target.xcor(), self.player.target.ycor() + 10)
            self.player.bullet.state = "fired"

    def fire_target_bullet(self, target):
        if target.bullet.state == "ready":
            target.bullet.goto(target.target.xcor(), target.target.ycor() - 10)
            target.bullet.state = "fired"

    def fire_boss_bullet(self):
        if self.boss.bullet.state == "ready":
            self.boss.bullet.goto(self.boss.target.xcor(), self.boss.target.ycor() - 10)
            self.boss.bullet.state = "fired"

    def update(self):
        self.win.update()

        if self.player.bullet.state == "fired":
            self.player.bullet.sety(self.player.bullet.ycor() + self.player.bullet.dy)
        if self.player.bullet.ycor() > 290:
            self.player.bullet.goto(0, -400)
            self.player.bullet.state = "ready"

        for target in self.targets:
            if self.player.bullet.distance(target.target) < 20:
                self.player.bullet.goto(0, -400)
                self.player.bullet.state = "ready"
                target.target.goto(random.randint(-290, 290), random.randint(100, 250))
                self.score += 10
                self.update_score()

        if self.player.bullet.distance(self.boss.target) < 30:
            self.boss.health -= 1
            self.player.bullet.goto(0, -400)
            self.player.bullet.state = "ready"
            self.score += 50
            self.update_score()
            if self.boss.health == 0:
                self.boss.target.goto(random.randint(-290, 290), random.randint(100, 250))
                self.boss.health = 2

        for target in self.targets:
            if random.randint(1, 100) > 98:
                self.fire_target_bullet(target)
            if target.bullet.state == "fired":
                target.bullet.sety(target.bullet.ycor() + target.bullet.dy)
            if target.bullet.ycor() < -290:
                target.bullet.goto(0, 400)
                target.bullet.state = "ready"
            if target.bullet.distance(self.player.target) < 20:
                self.player.hp -= 1
                self.update_hp()
                target.bullet.goto(0, 400)
                target.bullet.state = "ready"
                if self.player.hp == 0:
                    self.game_over()

        if random.randint(1, 100) > 98:
            self.fire_boss_bullet()
        if self.boss.bullet.state == "fired":
            self.boss.bullet.sety(self.boss.bullet.ycor() + self.boss.bullet.dy)
        if self.boss.bullet.ycor() < -290:
            self.boss.bullet.goto(0, 400)
            self.boss.bullet.state = "ready"
        if self.boss.bullet.distance(self.player.target) < 20:
            self.player.hp -= 1
            self.update_hp()
            self.boss.bullet.goto(0, 400)
            self.boss.bullet.state = "ready"
            if self.player.hp == 0:
                self.game_over()

        self.win.ontimer(self.update, 20)

    def game_over(self):
        self.player.target.hideturtle()
        for target in self.targets:
            target.target.hideturtle()
        self.boss.target.hideturtle()
        self.score_display.goto(0, 0)
        self.score_display.write("GAME OVER", align="center", font=("Arial", 36, "normal"))
        self.win.update()
        turtle.done()

Menu()
