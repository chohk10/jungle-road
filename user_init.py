from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungleroad

def user_init():
    db.users.insert_one({'name': '김현지', 'username': 'D3760', 'password': '1234'})
    db.users.insert_one({'name': '김초혜', 'username': 'D3762', 'password': '1234'})
    db.users.insert_one({'name': '채상엽', 'username': 'D3764', 'password': '1234'})

user_init()
print("DB init success")