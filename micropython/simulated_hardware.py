# This is the abstracted screen layer; interchangeable with the physical ppu
from tkinter import Tk, Canvas
from colour import Colour

class Device:
    def __init__(self, width=480, height=320, bgcolour=Colour(0)):
        self.screen = Screen(width, height, bgcolour)

class Screen:
    def __init__(self, width=480, height=320, bgcolour=Colour(0)):
        self.width = width
        self.height = height
        self.bgcolour = bgcolour

        self.window = Tk()
        self.canvas = Canvas(
            self.window,
            width=width,
            height=height,
            bg=bgcolour.getHexString(),
            highlightthickness=0
        )
        self.canvas.pack()
    
    def renderRectangle(self, rect):
        self.canvas.create_rectangle(
            rect.x,
            rect.y,
            rect.x + rect.width,
            rect.y + rect.height,
            fill=rect.colour.getHexString(),
            outline=rect.colour.getHexString()
        )

    def update(self):
        self.window.update()

    def clear(self):
        self.canvas.delete("all")