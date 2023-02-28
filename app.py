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
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import datetime
import hashlib

app = Flask(__name__)
jwt = JWTManager(app)  # initialize JWTManager
app.config['JWT_SECRET_KEY'] = 'team5SecretKey'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)  # lifespan of access token
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=1)  # lifespan of refresh token

client = MongoClient('localhost', 27017)
db = client.jungleroad


@app.route("/api/v1/restaurants/", methods=['GET'])
def home():
    datas = list(db.restaurants.find({}))
    ids = []
    for data in datas:
        ids.append(str(data["_id"]))
    stores = list(db.restaurants.find({}, {"_id": False}))
    return jsonify({"ids": ids, "data": stores}), 200


@app.route("/api/v1/restaurants/<id>", methods=['GET'])
@jwt_required(optional=True)
def read(id):
    current_user = get_jwt_identity()
    current_user_id = db.users.find_one({'username': current_user})['_id']
    
    restaurant_info = db.restaurants.find_one({'_id': ObjectId(id)}, {"_id": False})
    review_datas = list(db.reviews.find({'restaurantId': id}))

    review_ids = []
    for review_data in review_datas:
        review_ids.append(str(review_data["_id"]))

    reviews = list(db.reviews.find({}, {"_id": False}))
    is_mine = []
    for review in reviews:
        userId = review['userId']
        print(userId, current_user_id)
        if str(userId) == str(current_user_id):
            is_mine.append(True)
        else:
            is_mine.append(False)
    print(is_mine)
    return jsonify({"restaurant_info": restaurant_info, "review_ids": review_ids, "reviews": reviews, "is_mine": is_mine}), 200

""" 
TODO : 
    - 기타 회원정보 입력받기 
    - 프론트에서 암호화된 비밀번호를 받기 
"""


@app.route("/api/v1/users", methods=["POST"])
def register():
    new_user = request.get_json()  # store the json body request
    # Creating Hash of password to store in the database
    new_user["password"] = hashlib.sha256(
        new_user["password"].encode("utf-8")).hexdigest()  # encrpt password
    # Checking if user already exists
    # check if user exist
    doc = db.users.find_one({"username": new_user["username"]})
    # If not exists than create one
    if not doc:
        # Creating user
        db.users.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409


""" TODO : 프론트에서 암호화해서 보내준 비빌번호끼리 비교"""


@app.route("/api/v1/login", methods=["POST"])
def login():
    login_details = request.get_json()  # Getting the login Details from payload
    # Check if user exists in the databas
    user_from_db = db.users.find_one({'username': login_details['username']})
    if user_from_db:  # If user exists
        # Check if password is correct
        encrpted_password = hashlib.sha256(
            login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            # Identity can be any data that is json serializable
            access_token = create_access_token(
                identity=user_from_db['username'])  # Create JWT Access Token
            refresh_token = create_refresh_token(
                identity=user_from_db['username'])  # Create JWT Refresh Token
            # Return Token
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    return jsonify({'msg': 'The username or password is incorrect'}), 401


@app.route('/api/v1/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token, current_user=current_user)


@app.route('/api/v1/reviews', methods=['POST'])
@jwt_required()
def postReview():
    current_user = get_jwt_identity()
    user_id = db.users.find_one({'username': current_user})['_id']
    new_review = request.get_json()
    current_restaurant = new_review['restaurant']
    review_rating = new_review['rating']
    review_text = new_review['text']
    now = datetime.datetime.now()
    doc = {"userId": user_id, "rating": review_rating, "text": review_text,
           "created": now, "restaurantId": current_restaurant}
    db.reviews.insert_one(doc)
    return jsonify({'msg': 'Review posted successfully'}), 201


@app.route('/api/v1/reviews', methods=['PATCH'])
@jwt_required()
def editReview():
    patch_details = request.get_json()
    review_id = patch_details['reviewId']
    new_rating = patch_details['rating']
    new_text = patch_details['text']
    db.reviews.update_one({'_id': review_id}, {
                          '$set': {"rating": new_rating, "text": new_text}})
    return jsonify({'msg': 'Review edited successfully'}), 201


@app.route('/api/v1/reviews', methods=['DELETE'])
@jwt_required()
def deleteReview():
    patch_details = request.get_json()
    review_id = patch_details['reviewId']
    db.reviews.delete_one({'_id': review_id})
    return jsonify({'msg': 'Review deleted successfully'}), 201


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
