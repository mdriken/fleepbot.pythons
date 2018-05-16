import requests
import json
import pymysql
import  time
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

def sendMessage():
    cursor.execute("SELECT * FROM outbox where status=1")
    outboxes=cursor.fetchall()

    for outbox in outboxes:
        conv_id=outbox['conversation_id']
        r = requests.post("https://fleep.io/api/message/send/"+conv_id,
            headers = {"Content-Type": "application/json"},
            cookies = {"token_id": token},
            data = json.dumps({"message": outbox['message'], "ticket": ticket}))

        sql_update="UPDATE outbox set status=0 where id=%s"%(outbox['id'])
        cursor.execute(sql_update)
        connection.commit()
    connection.rollback()

while True:
    sendMessage()
    print("cek....")
    time.sleep(1)
