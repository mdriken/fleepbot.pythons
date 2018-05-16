import requests
import json
import pymysql
import time
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

def getConversation():
#mengambil conversation
    r = requests.post("https://fleep.io/api/conversation/list",
        headers = {"Content-Type": "application/json"},
        cookies = {"token_id": token},
        data = json.dumps({"ticket": ticket}))
# hanya mengambil coversation id yang pertama
    conversations=r.json()['conversations']

    for conversation in conversations:
        getMessages(conversation['conversation_id'])
    # print(conv_id)

#mengambil coversation sesuai coversation id

def getMessages(conversation_id):

    # get message nya
    url="https://fleep.io/api/conversation/sync/"+conversation_id
    r = requests.post(url,
        headers = {"Content-Type": "application/json"},
        cookies = {"token_id": token},
        data = json.dumps({"ticket": ticket}))
    messages=r.json()['stream']

    # data=[]

    # filter = [item for item in messages if int(item['_id']) > max and item['msg_box']=='inbox']
    for message in messages:
        try:
            pesan=message['message']
            sql_select="SELECT * FROM inbox where message_id='%s'"%message['message_id']
            # print(sql_select)
            cursor.execute(sql_select)
            #
            item=cursor.fetchone()
            # # print(item)
            if item is None and message['account_id'] != "369492cc-b4b4-4634-9510-91bab1f5f250":
                sql_insert="INSERT INTO inbox VALUES(null,'%s','%s','%s','%s')"%(conversation_id,message['message'],message['message_id'],message['account_id'])
                print(sql_insert)
                cursor.execute(sql_insert)
                connection.commit()
            connection.rollback()
        except:
            print("....")

while True:
    getConversation()
    connection.rollback()
    print("....")
    time.sleep(1)