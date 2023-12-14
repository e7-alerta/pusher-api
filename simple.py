import requests

url = "https://api.expo.dev/v2/push/send"

payload = [
    {
        "to": "ExponentPushToken[dX0rL3AiD9q90-JC7jIScI]",
        "title": "Hola Vecino",
        "body": "Alerta en Rioja 200"
    }
]
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)