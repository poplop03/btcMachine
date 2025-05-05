import requests
import time
from I2C_LCD_driver import I2CLCD

lcd = I2CLCD(addr=0x30)

symbol = 'BTCUSDT'
api_url = f'https://api.api-ninjas.com/v1/cryptoprice?symbol={symbol}'
headers = {'X-Api-Key': 'mdLctKthWCR2lN6ElcChEg==WjovL7Hr7W9TGaMg'}

while True:
    try:
        response = requests.get(api_url, headers=headers)
        lcd.clear()
        if response.status_code == 200:
            price = response.json().get('price', 'N/A')
            lcd.lcd_string(f"{symbol}", 0)
            lcd.lcd_string(f"${price:.2f}", 1)
        else:
            lcd.lcd_string("API Error", 0)
            lcd.lcd_string(str(response.status_code), 1)
    except Exception as e:
        lcd.lcd_string("Exception", 0)
        lcd.lcd_string(str(e)[:16], 1)
    
    time.sleep(5)
