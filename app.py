from flask import Flask
from flask import jsonify, make_response, request,abort, render_template, session, redirect, url_for
from flask_cors import CORS, cross_origin
from datetime import datetime
import json
import sqlite3
from pymongo import MongoClient
import random


app = Flask(__name__)
app.secret_key = 'this-is-not-a-secret'
CORS(app)
connection = MongoClient("mongodb://localhost:27017/")


@app.route("/api/v1/info")
def home_index():
    api_list = []
    db = connection.cloud_native.apirelease
    print ("opened db")
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'api_version': api_list}),200


@app.route("/api/v1/users",methods=['GET'])
def get_users():
    return list_users()

@app.route("/api/v1/users/<int:user_id>",methods = ['GET'])
def get_user(user_id):
    return list_user(user_id)

@app.route('/api/v1/users',methods = ['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        print("400 error in route")
        abort(400)
    user = {'username':request.json['username'],
            'email':request.json['email'],
            'name':request.json.get('name',""),
            'password':request.json['password'],
            'id':random.randint(1,1000)
            }
    return jsonify({'status':add_user(user)}), 201

@app.route("/api/v1/users",methods=['DELETE'])
def delete_user():
    if not request.json or 'username' not in request.json:
        abort(400)
    user = request.json['username']
    return jsonify({'status': del_user(user)}) ,200


@app.route("/api/v1/users/<int:user_id>",methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
        abort(400)
    user['id'] = user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print(user)
    return jsonify({'status': upd_user(user)}),200

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet['username'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['created_at'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return jsonify({'status':add_tweet(user_tweet)}), 200

@app.route('/api/v2/tweets/<string:id>',methods=['GET'])
def get_tweet(id):
    return list_tweet(id)

@app.route('/adduser')
def add_user():
    return render_template('adduser.html')

@app.route('/addtweet')
def addtweetsjs():
    return render_template("addtweetsjs.html")

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/addname')
def addname():
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        return redirect(url_for('main'))
    else:
        return render_template('addname.html',session=session)

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('main'))












def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'cloud_native' not in dbnames:
            db = connection.cloud_native.users
            db_tweets = connection.cloud_native.tweets
            db_api = connection.cloud_native.apirelease

            db.insert({"email":"eric@google.com",
                "id":"33",
                "name":"eric",
                "password":"secr3t",
                "username":"ericsan"
                })

            db_tweets.insert({"body":"my first tweet from a json db",
                "id":"15",
                "timestamp": "2017-03-11T06:39:40Z",
                "tweetedby":"ericsan"
                })

            db_api.insert({
                "buildtime": "2017-01-01 10:00:00",
             "links": "/api/v1/users",
             "methods": "get, post, put, delete",
             "version": "v1"
                })
            db_api.insert( {
             "buildtime": "2017-02-11 10:00:00",
             "links": "api/v2/tweets",
             "methods": "get, post",
             "version": "2017-01-10 10:00:00"
                })
            print ("Database Initialize completed!")
        else:
            print ("Database already Initialized!")
    except:
        print ("Database creation failed!!")


def list_tweet(user_id):
    api_list = []
    db = connection.cloud_native.tweet
    tweet = db.find({"username":user_id})
    for i in tweet:
        api_list.append(str(i))
    if len(api_list) == 0:
        abort(404)
    return jsonify({"tweet":api_list})


def add_tweet(new_tweet):
    users = connection.cloud_native.users
    tweets = connection.cloud_native.tweet
    api_list = []
    user = users.find({"username":new_tweet['username']})
    for i in user:
        api_list.append(str(i))
    if len(api_list)==0:
        abort(404)
    else:
        tweets.insert(new_tweet)
        return "success"

def list_tweets():
    api_list = []
    db = connection.cloud_native.tweet
    for row in db.find():
        row.pop('_id')
        print(jsonify(row))
        api_list.append((row))
    return jsonify({'tweets_list':api_list})


def upd_user(user):
    api_list = []
    db_user = connection.cloud_native.users
    users = db_user.find_one({"id":user['id']})
    for i in users:
        api_list.append(str(i))
    if api_list == []:
        abort(409)
    else:
        db_user.update({'id':user['id']},{'$set':user},upsert=False)
        return "Success"


def del_user(del_user):
    db = connection.cloud_native.users
    api_list = []
    for i in db.find({"username":del_user}):
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    else:
        db.remove({'username':del_user})
        return 'success'


def list_user(user_id):
    api_list=[]
    db = connection.cloud_native.users
    print(user_id)
    result = db.find({'id':user_id})
    print(result)
    for i in result:
        api_list.append(str(i))

    if api_list == []:
        abort(404)
    return jsonify({"user_details":api_list})


def list_users():
    api_list=[]
    db = connection.cloud_native.users
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'user_list': api_list})

def add_user(new_user):
     api_list=[]
     print (new_user)
     db = connection.cloud_native.users
     user = db.find({'$or':[{"username":new_user['username']}     ,
    {"email":new_user['email']}]})
     for i in user:
       print (str(i))
       api_list.append(str(i))

     if api_list == []:
       db.insert(new_user)
       return "Success"
     else :
       abort(409)










@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error':'Bad Request'}),400)

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error':'Resource not found!'}),404)


if __name__ == "__main__":
    create_mongodatabase()
    app.run(host='0.0.0.0',port=5000,debug=True)


