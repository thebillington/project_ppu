hexColourMap = ["#000", "#00f", "#0f0", "#0ff", "#f00", "#f0f", "#ff0", "#fff"]
binaryColourMap = [0x0000, 0xf800, 0x001f, "011", 0x07E0, "101", "110", 0xffff]
class Colour:

    def __init__(self, colour_int):
        self.colour_int = colour_int
    
    def get_hex(self):
        return hexColourMap[self.colour_int % 8]
    
    def get_binary(self):
        return binaryColourMap[self.colour_int % 8]

Colour.BLACK = Colour(0)
Colour.BLUE = Colour(1)
Colour.GREEN = Colour(2)
Colour.RED = Colour(4)
Colour.WHITE = Colour(7)