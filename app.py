from cgitb import text
from lib2to3.pgen2 import driver
from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright
from datetime import datetime

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.jungleroad

@app.route("/", methods=['GET'])
def home(): 
    datas = list(db.restaurants.find({}))
    ids = []
    for data in datas:
        ids.append(str(data["_id"]))
    stores = list(db.restaurants.find({}, {"_id": False}))
    
    return jsonify({"ids": ids, "data": stores})

@app.route("/api/v1/restaurants/<id>", methods=['GET'])
def read(id):
    restaurant_info = db.restaurants.find_one({'_id': ObjectId(id)}, {"_id": False})
    review_datas = list(db.reviews.find({'restaurantId': id}))

    review_ids = []
    for review_data in review_datas:
        review_ids.append(str(review_data["_id"]))
    reviews = list(db.reviews.find({}, {"_id": False}))
    return jsonify({"restaurant_info": restaurant_info, "review_ids": review_ids, "reviews": reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)