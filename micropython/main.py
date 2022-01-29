from time import sleep
from simulated_hardware import Device
from colour import Colour
from physics import Rectangle

device = Device(width=480, height=320, bgcolour=Colour(0x00))

paddle_one = Rectangle(10, 140, 5, 40, Colour(0x07))
paddle_two = Rectangle(455, 140, 5, 40, Colour(0x07))

while True:

    if device.is_pressed("w"):
        paddle_one.y -= 1
    if device.is_pressed("s"):
        paddle_one.y += 1

    if device.is_pressed("Up"):
        paddle_two.y -= 1
    if device.is_pressed("Down"):
        paddle_two.y += 1
    
    device.clear()

    device.renderRectangle(paddle_one)
    device.renderRectangle(paddle_two)

    device.update()

    sleep(1/60)