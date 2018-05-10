import requests
import json
import pymysql

# koneksi database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='fleep',
                             cursorclass=pymysql.cursors.DictCursor)
cursor =connection.cursor()

r = requests.post("https://fleep.io/api/account/login",
                  headers = {"Content-Type": "application/json"},
                  data = json.dumps({"email": "jimbaraninfo@gmail.com", "password": "12345678"}))

ticket=r.json()["ticket"]
token=r.cookies["token_id"]

#mengambil conversation
r = requests.post("https://fleep.io/api/conversation/list",
    headers = {"Content-Type": "application/json"},
    cookies = {"token_id": token},
    data = json.dumps({"ticket": ticket}))

# hanya mengambil coversation id yang pertama
conv_id=r.json()['conversations'][0]['conversation_id']
print(conv_id)

#mengambil coversation sesuai coversation id
url="https://fleep.io/api/conversation/sync/"+conv_id
r = requests.post(url,
    headers = {"Content-Type": "application/json"},
    cookies = {"token_id": token},
    data = json.dumps({"ticket": ticket}))
messages=r.json()['stream']

# data=[]
for message in messages:
    try:
        pesan=message['message']
        sql_select="SELECT * FROM message where message_id='%s'"%message['message_id']

        cursor.execute(sql_select)

        item=cursor.fetchone()
        # print(item)
        if item is None:
            sql_insert="INSERT INTO message VALUES(null,'%s','%s','%s')"%(message['message_id'],message['message'],message['account_id'])
            cursor.execute(sql_insert)
            connection.commit()
        connection.rollback()
    except:
        print("bukan message")
