
WIDTH = 640
HEIGHT = 480

x = 320
y = 240
speed = 5

def update():
    global x, y

    if keyboard.left:
        x -= speed
    if keyboard.right:
        x += speed
    if keyboard.up:
        y -= speed
    if keyboard.down:
        y += speed

    x = max(20, min(WIDTH - 20, x))
    y = max(20, min(HEIGHT - 20, y))

def draw():
    screen.clear()
    screen.draw.filled_circle((x, y), 20, "dodgerblue")
    screen.draw.text("Move with arrows", (10, 10), color="white")