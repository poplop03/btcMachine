import requests
import time

symbol = 'BTCUSDT'
api_url = f'https://api.api-ninjas.com/v1/cryptoprice?symbol={symbol}'
headers = {'X-Api-Key': 'mdLctKthWCR2lN6ElcChEg==WjovL7Hr7W9TGaMg'}

while True: 
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == requests.codes.ok:
        data = response.json()  # Convert response.text to a Python dict
        print(f"Symbol: {data['symbol']} | Price: {data['price']}")
    else:
        print("Error:", response.status_code, response.text)
    
    time.sleep(1)
