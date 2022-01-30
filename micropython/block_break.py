from time import sleep
from hardware import Device
from colour import Colour
from physics import Rectangle
from random import randrange, choice

screen_width = 480
screen_height = 320

device = Device(bgcolour=Colour.BLACK)

global player
global ball
global ball_direction
global ball_y_speed
global player_speed
global balls_remaining
global has_ball
global blocks

block_colours = [Colour.RED, Colour.BLUE, Colour.GREEN, Colour.PURPLE, Colour.YELLOW]
def init():

    global player
    global ball
    global ball_direction
    global ball_y_speed
    global player_speed
    global balls_remaining
    global has_ball
    global blocks

    player = Rectangle(screen_width-10, 130, 5, 60, Colour.WHITE)
    ball = Rectangle(screen_width-22, int(screen_height/2)-4, 8, 8, Colour.WHITE)

    blocks = []

    for i in range(7):
        for j in range(10):
            blocks.append(Rectangle(5 + (10*j), 5 + (45 * i), 5, 40, choice(block_colours)))

    ball_direction = -1
    ball_y_speed = 0
    player_speed = 2

    balls_remaining = 3
    has_ball = True

init()

while True:
    if device.is_pressed("l"):
        if player.y > 0:
            player.y -= player_speed
    if device.is_pressed("r"):
        if player.y + player.height < screen_height:
            player.y += player_speed

    if device.is_pressed("a"):
        if has_ball:
            has_ball = False
            if device.is_pressed("l"):
                ball_y_speed = -3
            elif device.is_pressed("r"):
                ball_y_speed = 3
            else:
                ball_y_speed = randrange(-3,4,2)
    
    if has_ball:
        ball.y = player.y + int(player.height / 2) - int(ball.height / 2)
    else:
        ball.x += 4 * ball_direction
        ball.y += ball_y_speed
        
    if ball.y < 0:
        ball.y = 0
        ball_y_speed *= -1
    if ball.y > screen_height - ball.height:
        ball.y = screen_height - ball.height
        ball_y_speed *= -1

    if ball.has_collided(player):
        ball_direction *= -1
        if device.is_pressed("l") and ball_y_speed < 5:
            ball_y_speed += 1
        elif device.is_pressed("r") and ball_y_speed > -5:
            ball_y_speed -= 1
    elif ball_direction == -1:
        for block in blocks:
            if ball.has_collided(block):
                ball_direction *= -1
                blocks.remove(block)
                break

    if ball.x < 0:
        ball_direction = 1

    if ball.x > screen_width:
        balls_remaining -= 1
        has_ball = True
        ball.x = screen_width-22
        if balls_remaining == 0:
            init()

    if len(blocks) == 0:
        init()
    
    device.clear()

    device.draw_rect(player)
    device.draw_rect(ball)
    for block in blocks:
        device.draw_rect(block)

    device.update()