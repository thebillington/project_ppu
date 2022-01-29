hexColourMap = ["#000", "#00f", "#0f0", "#0ff", "#f00", "#f0f", "#ff0", "#fff"]
binaryColourMap = ["000", "001", "010", "011", "100", "101", "110", "111"]
class Colour:
    def __init__(self, colourInt = 0):
        self.colourInt = colourInt
    
    def getHexString(self):
        return hexColourMap[self.colourInt % 8]
    
    def getBinaryString(self):
        return binaryColourMap[self.colourInt % 8]