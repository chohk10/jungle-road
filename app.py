from cgitb import text
from lib2to3.pgen2 import driver
from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import datetime
import hashlib

app = Flask(__name__)
jwt = JWTManager(app)  # initialize JWTManager
app.config['JWT_SECRET_KEY'] = 'team5SecretKey'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(
    minutes=30)  # lifespan of access token
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(
    days=1)  # lifespan of refresh token

client = MongoClient('localhost', 27017)
db = client.jungleroad


@app.route("/")
def index():
    return render_template("index.html")


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
    if current_user != None:
        current_user_id = db.users.find_one({'username': current_user})['_id']

    restaurant_info = db.restaurants.find_one(
        {'_id': ObjectId(id)}, {"_id": False})
    review_datas = list(db.reviews.find({'restaurantId': id}))

    review_ids = []
    for review_data in review_datas:
        review_ids.append(str(review_data["_id"]))

    reviews = list(db.reviews.find({}, {"_id": False}))
    size = len(reviews)
    is_mine = []
    for review in reviews:
        userId = review['userId']
        print(userId, current_user_id)
        if str(userId) == str(current_user_id):
            is_mine.append(True)
        else:
            is_mine.append(False)
    print(is_mine)
    return jsonify({"restaurant_info": restaurant_info, "review_ids": review_ids, "reviews": reviews, "is_mine": is_mine, 'size': size}), 200


""" 
TODO : 
    - 기타 회원정보 입력받기 
    - 프론트에서 암호화된 비밀번호를 받기 
"""
@app.route("/api/v1/users", methods=["POST"])
def register():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']

    # Creating Hash of password to store in the database
    password = hashlib.sha256(
        password.encode("utf-8")).hexdigest()  # encrpt password
    # Checking if user already exists
    # check if user exist
    doc = db.users.find_one({"username": username})
    # If not exists than create one
    if not doc:
        # Creating user
        db.users.insert_one(
            {'name': name, 'username': username, 'password': password})
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409


""" TODO : 프론트에서 암호화해서 보내준 비빌번호끼리 비교"""


@app.route("/sign-up")
def signUpForm():
    return render_template("sign-up.html")


@app.route("/sign-in")
def loginForm():
    return render_template("sign-in.html")


@app.route("/api/v1/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    # Check if user exists in the databas
    user_from_db = db.users.find_one({'username': username})
    if user_from_db:  # If user exists
        # Check if password is correct
        encrpted_password = hashlib.sha256(
            password.encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            # Identity can be any data that is json serializable
            access_token = create_access_token(
                identity=user_from_db['username'])  # Create JWT Access Token
            refresh_token = create_refresh_token(
                identity=user_from_db['username'])  # Create JWT Refresh Token
            # Return Token
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
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

    restaurant = request.form['restaurant']
    rating = request.form['rating']
    text = request.form['text']

    current_restaurant = restaurant
    review_rating = rating
    review_text = text
    now = datetime.datetime.now()
    doc = {"userId": user_id, "rating": review_rating, "text": review_text,
           "created": now, "restaurantId": current_restaurant}
    db.reviews.insert_one(doc)
    return jsonify({'msg': 'Review posted successfully'}), 201


@app.route('/api/v1/reviews', methods=['PATCH'])
@jwt_required()
def editReview():
    review_id = request.form['reviewId']
    rating = request.form['rating']
    text = request.form['text']
    db.reviews.update_one({'_id': review_id}, {
        '$set': {"rating": rating, "text": text}})
    return jsonify({'msg': 'Review edited successfully'}), 201


@app.route('/api/v1/reviews', methods=['DELETE'])
@jwt_required()
def deleteReview():
    review_id = request.form['reviewId']
    db.reviews.delete_one({'_id': review_id})
    return jsonify({'msg': 'Review deleted successfully'}), 201


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
