import requests

url = "https://api.mantiks.io/company/search"
search = ''
headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)