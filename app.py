import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://test:sparta@ac-h3sofl7-shard-00-00.yyb72uo.mongodb.net:27017,ac-h3sofl7-shard-00-01.yyb72uo.mongodb.net:27017,ac-h3sofl7-shard-00-02.yyb72uo.mongodb.net:27017/?ssl=true&replicaSet=atlas-10b32e-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'bucket':bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id':False}))
    return jsonify({'buckets': buckets_list})

@app.route("/delete", methods=["POST"])
def delete_bucket():
    num_receive = request.form['num_give']
    db.bucket.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'Bucket deleted'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)