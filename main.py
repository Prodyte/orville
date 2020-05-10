import time
import os
import random
import turtle

turtle.speed(0)

turtle.bgcolor("#404552")
turtle.title("Orville")
turtle.bgpic("orville.gif")
turtle.ht() #hides turtle

turtle.setundobuffer(1) #saves memory
turtle.tracer(0)

class Sprite(turtle.Turtle):
    def __init__(self, shapesize, color, startx, starty):
        turtle.Turtle.__init__(self, shape = shapesize)
        self.speed(0)
        self.penup()
        self.color(color)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)
    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
           (self.xcor() <= (other.xcor() + 20)) and \
           (self.ycor() >= (other.ycor() - 20)) and \
           (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False

class Player(Sprite):
    def __init__(self, shapesize, color, startx, starty):
        Sprite.__init__(self, shapesize, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4
        self.lives = 3

    def left(self):
        self.lt(45)

    def right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1


class Enemy(Sprite):
    def __init__(self, shapesize, color, startx, starty):
        Sprite.__init__(self, shapesize, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0,360))

class Ally(Sprite):
    def __init__(self, shapesize, color, startx, starty):
        Sprite.__init__(self,shapesize, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)

class Missile(Sprite):
    def __init__(self, shapesize, color, startx, starty):
        Sprite.__init__(self, shapesize, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            os.system("aplay laser.mp3&")
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "firing":
            self.fd(self.speed)

        if self.xcor() < -290 or self.xcor() > 290 or \
           self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score : " + str(self.score)
        self.pen.penup()
        self.pen.write(msg, font=("Arial", 16, "normal"))


game = Game()
game.draw_border()

game.show_status()

player = Player("triangle", "white", 0, 0)
#enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
#ally = Ally("square", "blue", 0, 0)
#keyboard bindings

enemies = []
for i in range(6):
    enemies.append(Enemy("circle", "red", -100, 0))

allies = []
for i in range(6):
    allies.append(Ally("square", "blue", -100, 0))

turtle.onkey(player.left, "Left")
turtle.onkey(player.right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()
#game loop
while True:
    turtle.update()
    time.sleep(0.02)
    player.move()
    missile.move()
    for enemy in enemies:
        enemy.move()
        if player.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 1
            game.show_status()
         #missile and enemy
        if missile.is_collision(enemy):
            os.system("aplay explosion.mp3&")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            game.score += 1
            game.show_status()

    for ally in allies:
        ally.move()

        if missile.is_collision(ally):
            os.system("aplay explosion&")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            game.score -= 1
            game.show_status()


        #missile and enemy
        if missile.is_collision(enemy):
            os.system("aplay explosion.mp3&")
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            game.score += 1
            game.show_status()
delay = input("Press enter to finish. ")
