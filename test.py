import requests

url = "http://127.0.0.1:8080/api/update-stats"

data = {
    "username": "Чекушка228",
    "balance": 10000}

response = requests.post(url, json=data)
