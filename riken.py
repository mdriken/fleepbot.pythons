import requests
import json

r = requests.post("https://fleep.io/api/account/login",
                  headers = {"Content-Type": "application/json"},
                  data = json.dumps({"email": "rikenoutsider@yahoo.com", "password": "riken12345"}))
# print(r.json())
print (r.json()["ticket"])

print (r.cookies["token_id"])
ticket=r.json()["ticket"]
token=r.cookies["token_id"]

r = requests.post("https://fleep.io/api/message/send/258036da-b60a-4465-b200-1b90a230a084",
    headers = {"Content-Type": "application/json"},
    cookies = {"token_id": token},
    data = json.dumps({"message": "Hello juga", "ticket": ticket}))