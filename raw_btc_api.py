import requests
symbol = 'LTCBTC'
api_url = 'https://api.api-ninjas.com/v1/cryptoprice?symbol={}'.format(symbol)
response = requests.get(api_url, headers={'X-Api-Key': 'mdLctKthWCR2lN6ElcChEg==WjovL7Hr7W9TGaMg'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)
