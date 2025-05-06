import smbus2 as smbus
import time
import requests

# LCD Constants
I2C_ADDR = 0x27
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

bus = smbus.SMBus(5)

def lcd_toggle_enable(bits):
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(0.0005)

def lcd_byte(bits, mode):
    high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(I2C_ADDR, high)
    lcd_toggle_enable(high)
    bus.write_byte(I2C_ADDR, low)
    lcd_toggle_enable(low)

def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(0.005)

def lcd_message(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)

# API setup
symbol = 'BTCUSDT'
api_url = f'https://api.api-ninjas.com/v1/cryptoprice?symbol={symbol}'
headers = {'X-Api-Key': 'mdLctKthWCR2lN6ElcChEg==WjovL7Hr7W9TGaMg'}

# Main loop
lcd_init()
lcd_message("BTC/USDT", LCD_LINE_1)

while True:
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == requests.codes.ok:
            data = response.json()
            price = "{:.2f}".format(data['price'])
            lcd_message(price, LCD_LINE_2)
        else:
            lcd_message("API Error", LCD_LINE_2)
    except Exception as e:
        lcd_message("Conn. Error", LCD_LINE_2)
    
    time.sleep(1)
