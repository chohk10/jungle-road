from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungleroad


def reviewsInit():
    db.reviews.insert_one({'userId': '63fd90382a7dda08e71f0850', 'rating': 4, 'text': '정말 맛있네요',
                          'created': '2023-02-28 13:48:03.881763', 'restaurantId': '63fd813a486166b5afb4dc31'})
    db.reviews.insert_one({'userId': '63fd90382a7dda08e71f0851', 'rating': 5, 'text': '정말 최고예요!',
                          'created': '2023-02-28 13:48:03.881763', 'restaurantId': '63fd813a486166b5afb4dc31'})
    db.reviews.insert_one({'userId': '63fd90382a7dda08e71f0852', 'rating': 2, 'text': '그냥 그랬어요',
                          'created': '2023-02-28 13:48:03.881763', 'restaurantId': '63fd813a486166b5afb4dc31'})


reviewsInit()
print("DB init success")
