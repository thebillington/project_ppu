from time import sleep
from hardware import Device
from colour import Colour
from physics import Rectangle
from random import randint

screen_width = 480
screen_height = 320

device = Device(bgcolour=Colour.BLACK)

paddle_one = Rectangle(10, 140, 5, 40, Colour.WHITE)
paddle_two = Rectangle(455, 140, 5, 40, Colour.WHITE)
ball = Rectangle(int(screen_width/2)-2, int(screen_height/2)-2, 4, 4, Colour.WHITE)

ball_y_vel = randint(-2,2)
ball_direction = 1

paddle_speed = 2

while True:

    if device.is_pressed("b"):
        if paddle_one.y > 0:
            paddle_one.y -= paddle_speed
    if device.is_pressed("r"):
        if paddle_one.y + paddle_one.height < screen_height:
            paddle_one.y += paddle_speed

    if device.is_pressed("a"):
        if paddle_two.y > 0:
            paddle_two.y -= paddle_speed
    if device.is_pressed("l"):
        if paddle_two.y + paddle_two.height < screen_height:
            paddle_two.y += paddle_speed

    if ball.has_collided(paddle_one) or ball.has_collided(paddle_two):
        ball_direction *= -1
        
    if ball.y < 0:
        ball.y = 0
        ball_y_vel *= -1
    if ball.y > screen_height - ball.height:
        ball.y = screen_height - ball.height
        ball_y_vel *= -1

    ball.y += ball_y_vel
    ball.x += 2 * ball_direction
    
    device.clear()

    device.draw_rect(paddle_one)
    device.draw_rect(paddle_two)
    device.draw_rect(ball)

    device.update()

    sleep(1/60)