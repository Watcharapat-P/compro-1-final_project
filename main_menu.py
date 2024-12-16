import turtle
import run_game

class TextBox:
    def __init__(self, width=0, height=0, text='', state=0, command=None):
        self.x, self.y = turtle.pos()
        self.width = width
        self.height = height
        self.text = text
        self.state = state
        self.command = command

    def draw(self):
        turtle.penup()
        if self.state == 0:
            turtle.goto(self.x + self.width/2, self.y + self.height)
            turtle.pensize(5)
            turtle.pendown()
            turtle.setheading(270)
            turtle.forward(self.height)
            turtle.right(90)
            turtle.forward(self.width)
            turtle.right(90)
            turtle.forward(self.height)
            turtle.right(90)
            turtle.forward(self.width)
            turtle.penup()
            turtle.goto(self.x, self.y + self.height/3)
            turtle.write(self.text, font=("Arial", 24, "bold"), align="center")
        elif self.state == 1:
            turtle.goto(self.x + self.width/2, self.y + self.height)
            turtle.fillcolor("#F0F8FF")
            turtle.begin_fill()
            turtle.pensize(5)
            turtle.pendown()
            turtle.setheading(270)
            turtle.forward(self.height)
            turtle.right(90)
            turtle.forward(self.width)
            turtle.right(90)
            turtle.forward(self.height)
            turtle.right(90)
            turtle.forward(self.width)
            turtle.end_fill()
            turtle.penup()
            turtle.goto(self.x, self.y + self.height/3)
            turtle.write(self.text, font=("Arial", 24, "bold"), align="center")


class Menu:
    def __init__(self):
        self.button_list = []
        turtle.speed(0)
        turtle.hideturtle()
        turtle.penup()
        turtle.bgcolor("#E0FFFF")
        turtle.goto(0, 300)
        turtle.write("Triangle Shoot", font=("Arial", 36, "bold"), align="center")
        turtle.penup()
        turtle.goto(-200, -200)
        play_button = TextBox(width=200, height=100, text='Play Game', state=1, command=self.play_game)
        self.button_list.append(play_button)
        turtle.goto(200, -200)
        exit_button = TextBox(width=200, height=100, text='Exit', state=0, command=self.exit_game)
        self.button_list.append(exit_button)
        for button in self.button_list:
            button.draw()
        turtle.listen()
        turtle.onkeypress(self.change_button, 'Right')
        turtle.onkeypress(self.change_button, 'Left')
        turtle.onkeypress(self.select_button, 'Return')
        turtle.mainloop()

    def change_button(self):
        for i in range(len(self.button_list)):
            if self.button_list[i].state == 1 and i != len(self.button_list)-1:
                self.button_list[i].state = 0
                self.button_list[i+1].state = 1
                self.redraw()
                break
            elif self.button_list[i].state == 1 and i == len(self.button_list)-1:
                self.button_list[i].state = 0
                self.button_list[0].state = 1
                self.redraw()
                break

    def select_button(self):
        for button in self.button_list:
            if button.state == 1:
                if button.command:
                    button.command()

    def redraw(self):
        turtle.clear()
        turtle.speed(0)
        turtle.hideturtle()
        turtle.goto(0, 300)
        turtle.write("Triangle Shoot", font=("Arial", 36, "bold"), align="center")
        turtle.penup()
        for button in self.button_list:
            button.draw()

    def play_game(self):
        turtle.clear()
        run_game.ShooterGame()

    def exit_game(self):
        turtle.bye()
