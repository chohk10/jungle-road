from pymongo import MongoClient
from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
db = client.jungleroad

target_urls = list(db.restaurants.find({},{"url":1,"_id":0}))
for target_url in target_urls:
    url = target_url['url']
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width" : 800, "height" : 600})
        page.goto(url)
        page.wait_for_selector(".K0PDV", timeout=500)
        # page.wait_for_timeout(50000)
        loaded_html = page.content()
        soup = BeautifulSoup(loaded_html, "html.parser")
        browser.close() 

    img = soup.select_one('div.K0PDV').attrs['style']
    img_url = img.split('"')[1]
    print(img_url)
    if img_url is not None:
        db.restaurants.update_one({'url' : url}, {'$set' : {'images' : [img_url]}})
    rating_tag = soup.select_one('#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm > div.dAsGb > span.PXMot.LXIwF > em')
    if rating_tag is not None:
        rating = rating_tag.text
        print(rating)
        db.restaurants.update_one({'url' : url}, {'$set' : {'rating' : rating}})

    
    
    

# width: 100%; height: 100%; background-position: 50% 0px; background-image: url("https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20200807_111%2F1596758258979MjJT5_JPEG%2FrQxa1L4oKiEFMJdbOMciFGLU.jpeg.jpg");
# width: 100%; height: 100%; background-position: 50% 0px; background-image: url("https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20211114_4%2F1636855461028g6MEJ_JPEG%2FD3FCEB0D-A22C-45AF-A99C-6955B5CA6D58.jpeg");
# width: 100%; height: 100%; background-position: 50% 0px; background-image: url("https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20220830_66%2F1661835191705pcb6L_JPEG%2F1414E4A6-6FDB-412A-BE1C-44C270BF925F.jpeg");


# url = "https://m.map.naver.com/search2/search.naver?query=kaist%EB%AC%B8%EC%A7%80%EC%BA%A0%ED%8D%BC%EC%8A%A4%EB%A7%9B%EC%A7%91&sm=sug&style=v5#/list"

# with sync_playwright() as playwright:
#     browser = playwright.chromium.launch(headless=True)
#     page = browser.new_page()
#     # page.set_viewport_size({"width" : 800, "height" : 600})
#     page.goto(url)
#     # page.wait_for_selector("div.item_info", timeout=50000)
#     page.wait_for_timeout(5000)
#     loaded_html = page.content()
#     soup = BeautifulSoup(loaded_html, "html.parser")
#     browser.close() 

# restaurants = soup.select('li._lazyImgContainer')
# # one = soup.select_one('li._lazyImgContainer')
# # img = one.select_one('div.item_info > a.item_thumb._itemThumb > img').attrs['src']
# # data_id = one.attrs['data-id']
# # print(img)
# # print(data_id)

# for restaurant in restaurants:
#     data_id = restaurant.attrs['data-id']
#     img = restaurant.select_one('div.item_info > a.item_thumb._itemThumb > img').attrs['src']
#     print(img)
#     # db.restaurants.update_one({'data_id' : data_id}, {'$set' : {'images' : [img]}})
