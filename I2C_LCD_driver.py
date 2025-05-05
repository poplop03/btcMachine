import smbus
import time

class I2CLCD:
    def __init__(self, addr=0x27, port=1):
        self.addr = addr
        self.bus = smbus.SMBus(port)
        self.lcd_init()

    def lcd_strobe(self, data):
        self.bus.write_byte(self.addr, data | 0b00000100)
        time.sleep(0.0005)
        self.bus.write_byte(self.addr, data & ~0b00000100)
        time.sleep(0.0001)

    def lcd_write(self, data, mode=0):
        high = mode | (data & 0xF0)
        low = mode | ((data << 4) & 0xF0)
        for val in [high, low]:
            self.bus.write_byte(self.addr, val | 0x08)
            self.lcd_strobe(val)

    def lcd_write_cmd(self, cmd):
        self.lcd_write(cmd, 0)

    def lcd_write_char(self, char):
        self.lcd_write(ord(char), 0x01)

    def lcd_init(self):
        cmds = [0x33, 0x32, 0x06, 0x0C, 0x28, 0x01]
        for cmd in cmds:
            self.lcd_write_cmd(cmd)
            time.sleep(0.005)

    def lcd_string(self, message, line):
        lines = [0x80, 0xC0]
        self.lcd_write_cmd(lines[line])
        for char in message.ljust(16):
            self.lcd_write_char(char)

    def clear(self):
        self.lcd_write_cmd(0x01)
        time.sleep(0.005)
