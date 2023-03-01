from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungleroad

f = open("db_insertion.py", "a")

f.write('from pymongo import MongoClient'+'\n')
f.write("client = MongoClient('localhost', 27017)"+'\n')
f.write('db = client.jungleroad'+'\n')


all_data = list(db.restaurants.find({},{'_id' : False}))
for data in all_data:
    data_str = str(data)
    insertion = 'db.restaurants.insert_one(' + data_str + ")"     
    f.write(insertion+'\n')

f.close()

f = open("db_insertion.py", "r")
print(f.read())



