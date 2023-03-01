import requests
from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
db = client.jungleroad

url = "https://m.map.naver.com/search2/search.naver?query=kaist%EB%AC%B8%EC%A7%80%EC%BA%A0%ED%8D%BC%EC%8A%A4%EB%A7%9B%EC%A7%91&sm=sug&style=v5#/list"
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(50000)
loaded_html = driver.page_source
soup = BeautifulSoup(loaded_html, "html.parser")

restaurants = soup.select('li._lazyImgContainer')

for restaurant in restaurants:
    data_id = restaurant.attrs['data-id']
    contact = restaurant.attrs['data-tel']
    url = 'https://m.place.naver.com/restaurant/' + data_id + '/home'
    name = restaurant.select_one('div.item_info > a.a_item.a_item_distance._linkSiteview > div > strong').text
    category = restaurant.select_one('div.item_info > a.a_item.a_item_distance._linkSiteview > div > em').text
    address = restaurant.select_one('div.item_info > div.item_info_inn > div > a').text.replace("주소보기","").replace(" ","")
    # img = restaurant.select_one('div.item_info > a.item_thumb._itemThumb > img').attrs['src']

    print(data_id)
    print(contact)
    print(url)
    print(name)
    print(category)
    print(address)

    doc = {
        'data_id' : data_id,
        'name' : name,
        'category' : category,
        'rating' : 0,
        'junglerating' : 0,
        'images' : [],
        'address' : address,
        'contact' : contact, 
        'url' : url
    }

    db.restaurants.insert_one(doc)

print("DB init success")
