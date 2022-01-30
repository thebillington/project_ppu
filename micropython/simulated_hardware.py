# This is the abstracted screen layer; interchangeable with the physical ppu
from tkinter import Tk, Canvas
from colour import Colour
import keyboard
from time import sleep

key_mapping = {
    "a":"a",
    "b":"b",
    "l":"Left",
    "r":"Right"
}

class Device:
    def __init__(self, bgcolour=Colour(0x00)):
        self.screen = Screen(480, 320, bgcolour)

    def clear(self):
        self.screen.clear()

    def update(self):
        self.screen.update()
        sleep(1/60)
    
    def draw_rect(self, rect):
        self.screen.draw_rect(rect)
    
    def is_pressed(self, k):
        return keyboard.is_pressed(key_mapping[k])

class Screen:
    def __init__(self, width, height, bgcolour):
        # Switch width and height because rotating isn't possible with tkinter window
        self.width = height
        self.height = width
        self.bgcolour = bgcolour

        self.window = Tk()
        self.canvas = Canvas(
            self.window,
            width=height,
            height=width,
            bg=bgcolour.get_hex(),
            highlightthickness=0
        )

        self.canvas.pack()
    
    def draw_rect(self, rect):
        self.canvas.create_rectangle(
            rect.y,
            rect.x,
            rect.y + rect.height,
            rect.x + rect.width,
            fill=rect.colour.get_hex(),
            outline=rect.colour.get_hex()
        )

    def update(self):
        self.window.update()

    def clear(self):
        self.canvas.delete("all")