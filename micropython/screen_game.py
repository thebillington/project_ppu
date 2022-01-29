hexColourMap = ["#000", "#00f", "#0f0", "#0ff", "#f00", "#f0f", "#ff0", "#fff"]
binaryColourMap = ["000", "001", "010", "011", "100", "101", "110", "111"]
class Colour:
    def __init__(self, colourInt = 0):
        self.colourInt = colourInt
    
    def getHexString(self):
        return hexColourMap[self.colourInt % 8]
    
    def getBinaryString(self):
        return binaryColourMap[self.colourInt % 8]

from machine import Pin,SPI,PWM
import framebuf
import time
import os

LCD_DC   = 8
LCD_CS   = 9
LCD_SCK  = 10
LCD_MOSI = 11
LCD_MISO = 12
LCD_BL   = 13
LCD_RST  = 15
TP_CS    = 16
TP_IRQ   = 17

class LCD_3inch5(framebuf.FrameBuffer):

    def __init__(self):
        self.RED   =   0x07E0
        self.GREEN =   0x001f
        self.BLUE  =   0xf800
        self.WHITE =   0xffff
        self.BLACK =   0x0000
        
        self.width = 480
        self.height = 160
        
        self.cs = Pin(LCD_CS,Pin.OUT)
        self.rst = Pin(LCD_RST,Pin.OUT)
        self.dc = Pin(LCD_DC,Pin.OUT)
        
        self.tp_cs =Pin(TP_CS,Pin.OUT)
        self.irq = Pin(TP_IRQ,Pin.IN)
        
        self.cs(1)
        self.dc(1)
        self.rst(1)
        self.tp_cs(1)
        self.spi = SPI(1,60_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
              
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        #self.spi.write(bytearray([0X00]))
        self.spi.write(bytearray([buf]))
        self.cs(1)


    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep_ms(5)
        self.rst(0)
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(5)
        self.write_cmd(0x21)
        self.write_cmd(0xC2)
        self.write_data(0x33)
        self.write_cmd(0XC5)
        self.write_data(0x00)
        self.write_data(0x1e)
        self.write_data(0x80)
        self.write_cmd(0xB1)
        self.write_data(0xB0)
        self.write_cmd(0x36)
        self.write_data(0x28)
        self.write_cmd(0XE0)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x04)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x3a)
        self.write_data(0x56)
        self.write_data(0x4d)
        self.write_data(0x03)
        self.write_data(0x0a)
        self.write_data(0x06)
        self.write_data(0x30)
        self.write_data(0x3e)
        self.write_data(0x0f)
        self.write_cmd(0XE1)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x01)
        self.write_data(0x11)
        self.write_data(0x06)
        self.write_data(0x38)
        self.write_data(0x34)
        self.write_data(0x4d)
        self.write_data(0x06)
        self.write_data(0x0d)
        self.write_data(0x0b)
        self.write_data(0x31)
        self.write_data(0x37)
        self.write_data(0x0f)
        self.write_cmd(0X3A)
        self.write_data(0x55)
        self.write_cmd(0x11)
        time.sleep_ms(120)
        self.write_cmd(0x29)
        
        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x62)
        
        self.write_cmd(0x36)
        self.write_data(0x28)
    def show_up(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0xdf)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x9f)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    def show_down(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0xdf)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0xA0)
        self.write_data(0x01)
        self.write_data(0x3f)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    def bl_ctrl(self,duty):
        pwm = PWM(Pin(LCD_BL))
        pwm.freq(1000)
        if(duty>=100):
            pwm.duty_u16(65535)
        else:
            pwm.duty_u16(655*duty)

class Rectangle:
    def __init__(self,x,y,width,height,colour=Colour(1)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
    
    def has_collided(self, rect):
        return abs((self.x + self.width/2) - (rect.x + rect.width/2)) < self.width/2 + rect.width/2 and abs((self.y + self.height/2) - (rect.y + rect.height/2)) < self.height/2 + rect.height/2

from time import sleep
from random import randint

screen_width = 480
screen_height = 320

paddle_one = Rectangle(10, 140, 5, 40, Colour(0x07))
paddle_two = Rectangle(455, 140, 5, 40, Colour(0x07))
ball = Rectangle(int(screen_width/2)-2, int(screen_height/2)-2, 4, 4, Colour(0x07))

ball_y_vel = randint(-5,5)
ball_direction = 1

paddle_speed = 4

LCD = LCD_3inch5()
LCD.bl_ctrl(100)

while True:

    if ball_direction == -1:
        if paddle_one.y + paddle_one.height/2 > ball.y:
            if paddle_one.y > 0:
                paddle_one.y -= paddle_speed
        if paddle_one.y + paddle_one.height/2 < ball.y:
            if paddle_one.y + paddle_one.height < screen_height:
                paddle_one.y += paddle_speed
    else:
        if paddle_one.y + paddle_one.height/2 > screen_height/2:
            paddle_one.y -= paddle_speed
        if paddle_one.y + paddle_one.height/2 < screen_height/2:
            paddle_one.y += paddle_speed

    if ball_direction == 1:
        if paddle_two.y + paddle_two.height/2 > ball.y:
            if paddle_two.y > 0:
                paddle_two.y -= paddle_speed
        if paddle_two.y + paddle_two.height/2 < ball.y:
            if paddle_two.y + paddle_two.height < screen_height:
                paddle_two.y += paddle_speed
    else:
        if paddle_two.y + paddle_two.height/2 > screen_height/2:
            paddle_two.y -= paddle_speed
        if paddle_two.y + paddle_two.height/2 < screen_height/2:
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
    ball.x += 4 * ball_direction

    LCD.fill(LCD.BLACK)
    LCD.fill_rect(paddle_one.x,paddle_one.y,paddle_one.width,paddle_one.height,LCD.WHITE)
    LCD.fill_rect(paddle_two.x,paddle_two.y,paddle_two.width,paddle_two.height,LCD.WHITE)
    LCD.fill_rect(ball.x,ball.y,ball.width,ball.height,LCD.WHITE)
    LCD.show_up()

    LCD.fill(LCD.BLACK)
    LCD.fill_rect(paddle_one.x,paddle_one.y-160,paddle_one.width,paddle_one.height,LCD.WHITE)
    LCD.fill_rect(paddle_two.x,paddle_two.y-160,paddle_two.width,paddle_two.height,LCD.WHITE)
    LCD.fill_rect(ball.x,ball.y-160,ball.width,ball.height,LCD.WHITE)
    LCD.show_down()