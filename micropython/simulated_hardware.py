# This is the abstracted screen layer; interchangeable with the physical ppu
from tkinter import Tk, Canvas
from colour import Colour
import keyboard

class Device:
    def __init__(self, bgcolour=Colour(0x00)):
        self.screen = Screen(480, 320, bgcolour)

    def clear(self):
        self.screen.clear()

    def update(self):
        self.screen.update()
    
    def draw_rect(self, rect):
        self.screen.draw_rect(rect)
    
    def is_pressed(self, k):
        return keyboard.is_pressed(k)

class Screen:
    def __init__(self, width, height, bgcolour):
        self.width = width
        self.height = height
        self.bgcolour = bgcolour

        self.window = Tk()
        self.canvas = Canvas(
            self.window,
            width=width,
            height=height,
            bg=bgcolour.get_hex(),
            highlightthickness=0
        )

        self.canvas.pack()
    
    def draw_rect(self, rect):
        self.canvas.create_rectangle(
            rect.x,
            rect.y,
            rect.x + rect.width,
            rect.y + rect.height,
            fill=rect.colour.get_hex(),
            outline=rect.colour.get_hex()
        )

    def update(self):
        self.window.update()

    def clear(self):
        self.canvas.delete("all")