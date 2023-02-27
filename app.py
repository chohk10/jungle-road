from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.jungleroad


@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')
