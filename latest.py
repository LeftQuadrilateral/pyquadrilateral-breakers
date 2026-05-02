from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import askstring

root = Tk()
root.title("pyQuadrilateral Breakers")

canvas = Canvas(root, width=640, height=360, background = "#F8F4E8")

square1 = canvas.create_rectangle(60,60, 300,300, fill="white")
square2 = canvas.create_rectangle(340,60, 580,300, fill="white")

block1 = canvas.create_rectangle(60,160,300,200)
block2 = canvas.create_rectangle(340,160,580,200)

start_health = 500

block1_health = start_health
block2_health = start_health

health1 = canvas.create_text(180, 180, text=block1_health, anchor = "center", font=("TkMenuFont",25))
health2 = canvas.create_text(460, 180, text=block2_health, anchor = "center", font=("TkMenuFont",25))

ball1extrainfo = str
ball2extrainfo = str

ball_colors = {
    "Speedy" : "#ff0000",
    "Slammy" : "#bf7830",
    "Gravitron" : "#ffff00",
    "Basic Ball" : "#ffffff",
    "Spawner": "#0000ff",
    "Duplicator" : "#ff00ff"
}
balls_list = []

class Ball:
    def __init__(self,ball,xvel:float=2.5,yvel:float=0):
        self.ball = ball
        self.xvel = xvel
        self.yvel = yvel
        self.xpos = canvas.coords(self.ball)[0]
        self.ypos = canvas.coords(self.ball)[1]
        self.size = int(canvas.gettags(self.ball)[0])
        self.components = canvas.gettags(self.ball)[1]
        self.can_duplicate = False

        if self.xpos < 320: self.side = "left"
        else: self.side = "right"

        self.speed = 1
        self.damage = 1
        self.gravity = 0.25

        self.threehund = 300 - self.size

    def move_ball(self):
        canvas.move(self.ball, self.speed * self.xvel, self.speed * self.yvel)
        self.xpos = canvas.coords(self.ball)[0]
        self.ypos = canvas.coords(self.ball)[1]

        self.threehund = 300 - self.size

        # Floor collisions
        if self.ypos >= self.threehund:
            self.yvel += 0.25
            canvas.moveto(self.ball, y=self.threehund)
            self.yvel = -1 * abs(self.yvel)
            self.on_hit()

        # Block collisions
        if self.ypos >= 160 - self.size and self.block_health() > 0:
            self.yvel += 0.25
            canvas.moveto(self.ball, y=160 - self.size)
            self.yvel = -1 * abs(self.yvel)
            damage_block(self.side, self.damage)
            self.on_hit()

        # Ceiling collisions
        if self.ypos <= 60:
            self.yvel -= 0.25
            canvas.moveto(self.ball, y=60)
            self.yvel = abs(self.yvel)
            self.on_hit()

        # Inner wall collisions
        if self.xpos >= self.threehund and self.side == "left":
            canvas.moveto(self.ball, x=self.threehund)
            self.xvel = -1 * abs(self.xvel)
            self.on_hit()
        if self.xpos <= 340 and self.side == "right":
            canvas.moveto(self.ball, x=340)
            self.xvel = abs(self.xvel)
            self.on_hit()

        # Outer wall collisions
        if self.xpos <= 60:
            canvas.moveto(self.ball, x=60)
            self.xvel = abs(self.xvel)
            self.on_hit()
        if self.xpos >= 580 - self.size:
            canvas.moveto(self.ball, x=580 - self.size)
            self.xvel = -1 * abs(self.xvel)
            self.on_hit()

    def on_hit(self):
        if "Speedy" in self.components:
            self.speed += 0.01
        elif "Slammy" in self.components:
            self.damage += 1
        elif "Gravitron" in self.components:
            self.gravity += 0.0075
        elif "Spawner" in self.components:
            spawnBall(x=self.xpos, components=[ball1extrainfo if self.side == "left" else ball2extrainfo])

    def block_health(self):
        if self.side == "left":
            return block1_health
        else:
            return block2_health

def damage_block(side, damage):
    if side == "left":
        global block1_health
        block1_health -= damage
        canvas.itemconfig(health1, text=block1_health)
        if block1_health <= 0:
            canvas.delete(block1)
            canvas.delete(health1)
    else:
        global block2_health
        block2_health -= damage
        canvas.itemconfig(health2, text=block2_health)
        if block2_health <= 0:
            canvas.delete(block2)
            canvas.delete(health2)

def startBall(size=None, x=None, components=None):
    return canvas.create_oval(x, 80, x+size, 80+size,fill=ball_colors[components[0]],tags=[size,components])

def spawnBall(x, components, size:int=20):
    balls_list.append(Ball(ball=startBall(size=size, x=x, components=components)))

frames = 1

def game_loop():
    global frames
    for ball in balls_list:
        ball.yvel += ball.gravity
        ball.move_ball()
        if frames % 300 == 0 and ball.can_duplicate:
            if "Duplicator" in ball.components:
                spawnBall(x=ball.xpos, components=["Duplicator"])
        ball.can_duplicate = True
    frames += 1
    root.after(16, game_loop)

ball1 = StringVar()
ball2 = StringVar()

sob = []

def start_game():
    title.destroy()
    start_button.destroy()
    global sob
    [item.destroy() for item in sob]

    canvas.grid(row=0,column=0)
    spawnBall(x=180,components=[ball1.get()])
    spawnBall(x=460,components=[ball2.get()])

    game_loop()

def onclick(ball, side):
    global sob
    global ball1extrainfo
    global ball2extrainfo
    if ball == "Spawner":
        if side == 1:
            ball1extrainfo = askstring("Input","Ball to summon")
        else:
            ball2extrainfo = askstring("Input","Ball to summon")

title = Label(root, text="pyQuadrilateral Breakers", font=("TkMenuFont",25))
title.grid(row=0,columnspan=3)

selectable_balls = 5

def add_button(name):
    global sob
    global selectable_balls
    sob.append(ttk.Radiobutton(root, text=name, variable=ball1, value=name, command=lambda:onclick(name,1)))
    sob[len(sob)-1].grid(row=(len(sob) // 2)+1, column=0, sticky=W)
    sob.append(ttk.Radiobutton(root, text=name, variable=ball2, value=name, command=lambda:onclick(name,2)))
    sob[len(sob)-1].grid(row=(len(sob) // 2), column=2, sticky=W)

add_button("Speedy")
add_button("Slammy")
add_button("Duplicator")
add_button("Gravitron")
add_button("Basic Ball")
add_button("Spawner")

start_button = Button(root, text="    Start!    ", command=start_game, bg="#0080ff")
start_button.grid(row=(len(sob) // 2)+1,column=1)

root.mainloop()
