import smbus
import time

# Define device parameters
I2C_ADDR  = 0x27  # Replace with your LCD's I2C address
LCD_WIDTH = 16    # Maximum characters per line

# Define some device constants
LCD_CHR = 1       # Mode - Sending data
LCD_CMD = 0       # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Initialize I2C (SMBus)
bus = smbus.SMBus(1)  # Use 0 for older Raspberry Pi versions

def lcd_init():
    lcd_byte(0x33,LCD_CMD) # Initialize
    lcd_byte(0x32,LCD_CMD) # Set to 4-bit mode
    lcd_byte(0x06,LCD_CMD) # Cursor move direction
    lcd_byte(0x0C,LCD_CMD) # Turn cursor off
    lcd_byte(0x28,LCD_CMD) # 2 line display
    lcd_byte(0x01,LCD_CMD) # Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | 0x08
    bits_low = mode | ((bits<<4) & 0xF0) | 0x08

    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | 0x04))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR,(bits & ~0x04))
    time.sleep(E_DELAY)

def lcd_string(message):
    message = message.ljust(LCD_WIDTH," ")
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

# Main program
lcd_init()
lcd_byte(LCD_LINE_1, LCD_CMD)
lcd_string("BTC")
