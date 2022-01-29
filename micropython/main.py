from time import sleep
from simulated_hardware import Device
from colour import Colour
from physics import Rectangle

device = Device()

player = Rectangle(0, 0, 20, 20, Colour(0x04))
enemy = Rectangle(30, 30, 20, 20, Colour(0x0F))

while True:
    
    device.screen.clear()

    device.screen.renderRectangle(player)
    device.screen.renderRectangle(enemy)

    device.screen.update()
    sleep(0.1)