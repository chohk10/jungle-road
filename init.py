from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungleroad

def init():
    db.stores.insert_one({'name': '한우곰탕', 'star': 4.55, 'junglestar': 0, 'category': '소고기구이', 'images': ['https://search.pstatic.net/common/?autoRotate=true&type=w278_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20191023_189%2F15717946190105vktc_JPEG%2FLFPvlJWAUHpZwYcHx5C6igJw.jpg']})
    db.stores.insert_one({'name': '화목한우리집', 'star': 4.57, 'junglestar': 0, 'category': '종합분식', 'images': ['https://search.pstatic.net/common/?autoRotate=true&type=w278_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20220913_111%2F1663073555626lDK1T_JPEG%2FD036DE7C-5D30-4B8C-849F-EC42AC7A4EEF.jpeg']})
    db.stores.insert_one({'name': '광세족발 본점', 'star': 4.51, 'junglestar': 0, 'category': '족발, 보쌈', 'images': ['https://search.pstatic.net/common/?autoRotate=true&type=w278_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20220913_111%2F1663073555626lDK1T_JPEG%2FD036DE7C-5D30-4B8C-849F-EC42AC7A4EEF.jpeg']})
    db.stores.insert_one({'name': '국영수떡볶이', 'star': 4.69, 'junglestar': 0, 'category': '떡볶이', 'images': ['https://search.pstatic.net/common/?autoRotate=true&type=w278_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20180715_30%2F15316329892524l4MN_JPEG%2FNUxPsjFarV4cP8lL2LyZUTo3.JPG.jpg']})
    db.stores.insert_one({'name': '스시안', 'star': 4.42, 'junglestar': 0, 'category': '초밥, 롤', 'images': ['https://search.pstatic.net/common/?autoRotate=true&type=w278_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20190324_90%2F1553355821287FJRSJ_JPEG%2FiD7jYUL3obP01Odk1sSEP1eZ.JPG.jpg']})

init()
print("DB init success")