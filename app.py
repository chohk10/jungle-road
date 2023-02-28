from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import datetime
import hashlib

app = Flask(__name__)
jwt = JWTManager(app) # initialize JWTManager
app.config['JWT_SECRET_KEY'] = 'team5SecretKey'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30) # lifespan of access token
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # lifespan of refresh token


client = MongoClient('localhost', 27017)
db = client.jungleroad
users_collection = db.users
reviews_collection = db.reviews


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


""" 
TODO : 
    - 기타 회원정보 입력받기 
    - 프론트에서 암호화된 비밀번호를 받기 
"""
@app.route("/api/v1/users", methods=["POST"])
def register():
    new_user = request.get_json() # store the json body request
    # Creating Hash of password to store in the database
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt password
    # Checking if user already exists
    doc = users_collection.find_one({"username": new_user["username"]}) # check if user exist
    # If not exists than create one
    if not doc:
        # Creating user
        users_collection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409


""" TODO : 프론트에서 암호화해서 보내준 비빌번호끼리 비교"""
@app.route("/api/v1/login", methods=["post"])
def login():
    login_details = request.get_json()  # Getting the login Details from payload
    user_from_db = users_collection.find_one({'username': login_details['username']})  # Check if user exists in the databas
    if user_from_db:  # If user exists
        # Check if password is correct
        encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            # Identity can be any data that is json serializable
            access_token = create_access_token(identity=user_from_db['username'])  # Create JWT Access Token
            refresh_token = create_refresh_token(identity=user_from_db['username'])  # Create JWT Refresh Token
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200  # Return Token
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
    user_id = users_collection.find_one({'username' : current_user})['_id']
    new_review = request.get_json()
    current_restaurant = new_review['restaurant']
    review_rating = new_review['rating']
    review_text = new_review['text']
    now = datetime.datetime.now()
    doc = {"userId" : user_id, "rating" : review_rating, "text" : review_text, "created" : now, "restaurantId" : current_restaurant}
    reviews_collection.insert_one(doc)
    return jsonify({'msg': 'Review posted successfully'}), 201

@app.route('/api/v1/reviews', methods=['PATCH'])
@jwt_required()
def editReview():
    patch_details = request.get_json()
    review_id = patch_details['reviewId']
    new_rating = patch_details['rating']
    new_text = patch_details['text']
    reviews_collection.update_one({'_id' : review_id}, {'$set' : {"rating" : new_rating, "text" : new_text}})
    return jsonify({'msg': 'Review edited successfully'}), 201

@app.route('/api/v1/reviews', methods=['DELETE'])
@jwt_required()
def deleteReview():
    patch_details = request.get_json()
    review_id = patch_details['reviewId']
    reviews_collection.delete_one({'_id' : review_id})
    return jsonify({'msg': 'Review deleted successfully'}), 201


if __name__ == '__main__':
	app.run('0.0.0.0', port=5001, debug=True)