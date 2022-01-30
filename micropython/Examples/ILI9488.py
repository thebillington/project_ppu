from micropython import const
from machine import Pin, SPI
import time, os, ustruct

READ_DISPLAY = const(0x0f);SLEEP_OUT = const(0x11);GAMMA_SET = const(0x26);DISPLAY_ON = const(0x29)
COLUMN_ADDRESS_SET = const(0x2a);PAGE_ADDRESS_SET = const(0x2b);RAM_WRITE = const(0x2c);RAM_READ = const(0x2e)
MEMORY_ACCESS_CONTROL = const(0x36);VER_SCROLL_ADDRESS = const(0x37);NEG_GAMMA_CONTROL = const(0xe1)
PIXEL_FORMAT_SET = const(0x3a);POWER_CONTROL_A = const(0xcb);POWER_CONTROL_B = const(0xcf)
DRIVER_TIMING_CONTROL_A = const(0xe8);DRIVER_TIMING_CONTROL_B = const(0xea);POWER_ON_CONTROL = const(0xed)
PUMP_RATIO_CONTROL = const(0xf7);POWER_CONTROL_1 = const(0xc0);POWER_CONTROL_2 = const(0xc1)
VCOM_CONTROL_1 = const(0xc5);VCOM_CONTROL_2 = const(0xc7);FRAME_RATE_CONTROL = const(0xb2)
DISPLAY_FUNCTION_CONTROL = const(0xb6);ENABLE_3G = const(0xf2);POS_GAMMA_CONTROL = const(0xe0)
MEMORY_BUFFER = const(1024) # SPI Write Buffer
class ILI9488:
    def __init__(self, spi, cs, dc, rst, w, h, r):
        self.spi = spi;self.cs = cs;self.dc = dc;self.rst = rst
        self.init_width = w;self.init_height = h
        self.width = w;self.height = h;self.rotation = r
        self.cs.init(self.cs.OUT, value=1);self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.ResetDevice()
        self.Init()
        self.buffer = bytearray(MEMORY_BUFFER * 2)
        self.color_map = bytearray(b'\x00\x00\xFF\xFF') #default white foregraound, black background
        self.screen_x = 0;self.screen_y = 0
        
    def SetPosition(self,x,y):
        self.screen_x,self.screen_y = x,y

    def Init(self):
        for command, data in (
            (READ_DISPLAY, b"\x03\x80\x02"),(POWER_CONTROL_B, b"\x00\xc1\x30"),
            (POWER_ON_CONTROL, b"\x64\x03\x12\x81"),(DRIVER_TIMING_CONTROL_A, b"\x85\x00\x78"),
            (POWER_CONTROL_A, b"\x39\x2c\x00\x34\x02"),(PUMP_RATIO_CONTROL, b"\x20"),
            (DRIVER_TIMING_CONTROL_B, b"\x00\x00"),(POWER_CONTROL_1, b"\x23"),
            (POWER_CONTROL_2, b"\x10"),(VCOM_CONTROL_1, b"\x3e\x28"),(VCOM_CONTROL_2, b"\x86")):
            self.WriteDevice(command, data)
        if self.rotation == 0:                  # 0 deg
            self.WriteDevice(MEMORY_ACCESS_CONTROL, b"\x48")
            self.width,self.height = self.init_height,self.init_width
        elif self.rotation == 1:                # 90 deg
            self.WriteDevice(MEMORY_ACCESS_CONTROL, b"\x28")
            self.width,self.height = self.init_width,self.init_height
        elif self.rotation == 2:                # 180 deg
            self.WriteDevice(MEMORY_ACCESS_CONTROL, b"\x88")
            self.width,self.height = self.init_height,self.init_width
        elif self.rotation == 3:                # 270 deg
            self.WriteDevice(MEMORY_ACCESS_CONTROL, b"\xE8")
            self.width,self.height = self.init_width,self.init_height
        elif self.rotation == 4:                # Mirrored + 0 deg
            self.WriteDevice(MEMORY_ACCESS_CONTROL, b"\xC8")
            self.width,self.height = self.init_height,self.init_width
        elif self.rotation == 5:                # Mirrored + 90 deg
            self.WriteDevice(MEMORY_ACCESS_CONTROL, b"\x68")
            self.width,self.height = self.init_width,self.init_height
        elif self.rotation == 6:                # Mirrored + 180 deg
            self.WriteDevice(MEMORY_ACCESS_CONTROL, b"\x08")
            self.width,self.height = self.init_height,self.init_width
        elif self.rotation == 7:                # Mirrored + 270 deg
            self.WriteDevice(MEMORY_ACCESS_CONTROL, b"\xA8")
            self.width,self.height = self.init_width,self.init_height
        else:
            self.WriteDevice(MEMORY_ACCESS_CONTROL, b"\x08")

        for command, data in (
            (PIXEL_FORMAT_SET, b"\x55"),(FRAME_RATE_CONTROL, b"\x00\x18"),
            (DISPLAY_FUNCTION_CONTROL, b"\x02\x02\x3B"),(ENABLE_3G, b"\x00"),(GAMMA_SET, b"\x01"),
            (POS_GAMMA_CONTROL, b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"),
            (NEG_GAMMA_CONTROL, b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f")):
            self.WriteDevice(command, data)
        self.WriteDevice(SLEEP_OUT)
        time.sleep_ms(120)
        self.WriteDevice(DISPLAY_ON)

    def ResetDevice(self):
        self.rst(0);time.sleep_ms(50);self.rst(1);time.sleep_ms(50)

    def WriteDevice(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self.WriteDataToDevice(data)

    def WriteDataToDevice(self, data):
        self.dc(1);self.cs(0);self.spi.write(data);self.cs(1)

    def WriteBlock(self, x0, y0, x1, y1, data=None):
        self.WriteDevice(COLUMN_ADDRESS_SET, ustruct.pack(">HH", x0, x1))
        self.WriteDevice(PAGE_ADDRESS_SET, ustruct.pack(">HH", y0, y1))
        self.WriteDevice(RAM_WRITE, data)

    def FillRectangle(self, x, y, w, h, color=None):
        x = min(self.width - 1, max(0, x));y = min(self.height - 1, max(0, y))
        w = min(self.width - x, max(1, w));h = min(self.height - y, max(1, h))
        if color:
            color = ustruct.pack(">H", color)
        else:
            color = self.color_map[0:2] #background
        for i in range(MEMORY_BUFFER):
            self.buffer[2*i]=color[0]; self.buffer[2*i+1]=color[1]
        chunks, rest = divmod(w * h, MEMORY_BUFFER)
        self.WriteBlock(x, y, x + w - 1, y + h - 1, None)
        if chunks:
            for count in range(chunks):
                self.WriteDataToDevice(self.buffer)
        if rest != 0:
            mv = memoryview(self.buffer)
            self.WriteDataToDevice(mv[:rest*2])
            
#Initialize the onboard LED as output
led = machine.Pin(25,machine.Pin.OUT)
# Toggle LED funtionality
def BlinkLED(timer_one):
    led.toggle()
# https://forum.micropython.org/viewtopic.php?t=1420 Roberthh
@micropython.asm_thumb
def reverse(r0, r1):               # bytearray, len(bytearray)
    b(loopend)
    label(loopstart)
    ldrb(r2, [r0, 0])
    ldrb(r3, [r0, 1])
    strb(r3, [r0, 0])
    strb(r2, [r0, 1])
    add(r0, 2)
    label(loopend)
    sub (r1, 2)  # End of loop?
    bpl(loopstart)
SCR_WIDTH,SCR_HEIGHT,SCR_ROT = const(480),const(320),const(5)
TFT_CLK_PIN,TFT_MOSI_PIN,TFT_MISO_PIN,TFT_CS_PIN = const(10),const(11),const(12),const(9)
TFT_RST_PIN,TFT_DC_PIN = const(15),const(8)
spi = SPI(1,baudrate=40000000,miso=Pin(TFT_MISO_PIN),mosi=Pin(TFT_MOSI_PIN),sck=Pin(TFT_CLK_PIN))
display = ILI9488(spi,cs=Pin(TFT_CS_PIN),dc=Pin(TFT_DC_PIN),rst=Pin(TFT_RST_PIN),w=SCR_WIDTH,h=SCR_HEIGHT,r=SCR_ROT)
display.SetPosition(0,0);display.FillRectangle(0,0,480,320,0xBDF7)
# Read files.
bitmap_image_files = os.listdir("/")
#Initialize timer_one. Used for toggling the on board LED
timer_one = machine.Timer()
#Timer one initialization for on board blinking LED at 500mS interval
timer_one.init(freq=1, mode=machine.Timer.PERIODIC, callback=BlinkLED)
# Opens bitmap file. Displays the file @ 3 Sec interval
while True:
    for x in range(len(bitmap_image_files)):
        # Open file
        f = open(bitmap_image_files[x],'rb')
        
        # Check if it bitmap file
        if f.read(2) == b'BM':  #header
            dummy = f.read(8) #file size(4), creator bytes(4)
            offset = int.from_bytes(f.read(4), 'little')
            hdrsize = int.from_bytes(f.read(4), 'little')
            width = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            MEM_SIZE = 5*1024
            x = (SCR_WIDTH / 2) - (width / 2)
            y = (SCR_HEIGHT / 2) - (height / 2)
            
            if((width*height*2)>MEM_SIZE):
                no_of_read_buffer,balance_memory_size = (width*height*2)/MEM_SIZE, (width*height*2)%MEM_SIZE
            else:
                no_of_read_buffer = 0
                balance_memory_size = (width*height*2)
            x = int(x)
            y = int(y)
            no_of_read_buffer = int(no_of_read_buffer)
            balance_memory_size = int(balance_memory_size)
            if(no_of_read_buffer == 0):
                display.WriteBlock(x,y,x+width - 1, y+height - 1,None)
                dummy = f.seek(offset)
                buf = f.read(width*height*2)
                reverse(buf,width*height*2)
                display.WriteDataToDevice(buf)
                time.sleep(5)
            else:
                if(width%2 == 0x00):
                    display.WriteBlock(x,y,x+width-1, y+height - 1,None)
                else:
                    display.WriteBlock(x,y,x+width, y+height - 1,None)
                for i in range(no_of_read_buffer):
                    p = offset + (i*MEM_SIZE)
                    dummy = f.seek(p)
                    buf = f.read(MEM_SIZE)
                    reverse(buf,MEM_SIZE)
                    display.WriteDataToDevice(buf)
                p = offset + (no_of_read_buffer*MEM_SIZE)
                dummy = f.seek(p)
                buf = f.read(balance_memory_size)
                reverse(buf,balance_memory_size)
                display.WriteDataToDevice(buf)            
                time.sleep(3)
      
        # Close file
        f.close()
        display.FillRectangle(0,0,480,320,0xBDF7)