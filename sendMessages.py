import requests
import json

r = requests.post("https://fleep.io/api/account/login",
                  headers = {"Content-Type": "application/json"},
                  data = json.dumps({"email": "jimbaraninfo@gmail.com", "password": "12345678"}))

ticket=r.json()["ticket"]
token=r.cookies["token_id"]

#messagestore
r = requests.post("https://fleep.io/api/conversation/list",
    headers = {"Content-Type": "application/json"},
    cookies = {"token_id": token},
    data = json.dumps({"ticket": ticket}))

#mendapatkan conversation id
# nb : hanya yang pertama, bisa di loop
conv_id=r.json()['conversations'][0]['conversation_id']
print(conv_id)

# send message
r = requests.post("https://fleep.io/api/message/send/"+conv_id,
    headers = {"Content-Type": "application/json"},
    cookies = {"token_id": token},
    data = json.dumps({"message": "Ini Bot brow1z!!!", "ticket": ticket}))