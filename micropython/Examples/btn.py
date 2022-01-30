from utime import sleep_ms
from machine import Pin

led = Pin(25, Pin.OUT)
p1_left = Pin(26, Pin.IN)
p1_right = Pin(1, Pin.IN)
p2_left = Pin(28, Pin.IN)
p2_right = Pin(4, Pin.IN)

while True:
    if p1_left.value():
        print("p1_left")
        sleep_ms(10)
    elif p1_right.value():
        print("p1_right")
        sleep_ms(10)
    elif p2_left.value():
        print("p2_left")
        sleep_ms(10)
    elif p2_right.value():
        print("p2_right")
        sleep_ms(10)
