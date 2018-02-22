from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from flask import abort

import json
import sqlite3


app = Flask(__name__)

@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect('mydb.db')
    print ("opened db")
    api_list = []
    cursor = conn.execute("SELECT buildtime,version,methods,links from apirelease")
    for row in cursor:
        a_dict = {}
        a_dict['version'] = row[0]
        a_dict['buildtime'] = row[1]
        a_dict['methods'] = row[2]
        a_dict['links'] = row[3]
        api_list.append(a_dict)
    conn.close()
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
        abort(400)
    user = {'username':request.json['username'],
            'email':request.json['email'],
            'name':request.json.get('name',""),
            'password':request.json['password']
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























def upd_user(user):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from users where id=?',(user['id'],))
    data = cursor.fetchall()
    if len(data) == 0:
        abort(404)
    else:
        key_list = user.keys
        for i in key_list:
            if i != 'id':
                cursor.execute(""" UPDATE users set {0}=? where id=?""".format(i),(user[i],user['id']))
        return "success"

def del_user(del_user):
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users where username=?',(del_user,))
    data = cursor.fetchall()
    if len(data) != 1:
        abort(404)
    else:
        cursor.execute('delete from users where username==?',(del_user,))
        conn.commit()
    return 'success'


def list_user(user_id):
    conn = sqlite3.connect('mydb.db')
    #api_list=[]
    #cursor = conn.connect()
    print("userid:{user_id}")
    cursor = conn.execute("SELECT * from users where id=?",(user_id,))
    data = cursor.fetchall()
 #   print("data is: "+data)
    if(len(data)!=0):
        user = {
            'username':data[0][0],
            'name':data[0][1],
            'email':data[0][2],
            'password':data[0][3],
            'id':data[0][4]
        }
    conn.close()
    return jsonify(user)


def list_users():
    conn = sqlite3.connect('mydb.db')
    api_list=[]
    cursor = conn.execute("SELECT username, full_name,emailid,password,id from users")
    for row in cursor:
        adict = {}
        adict["username"] = row[0]
        adict["name"] = row[1]
        adict["email"] = row[2]
        adict["password"] = row[3]
        adict["id"] = row[4]
        api_list.append(adict)
    conn.close()
    return jsonify({'user_list': api_list})

def add_user(new_user):
    conn = sqlite3.connect('mydb.db')
    status = "Failed"
    cursor = conn.cursor()
    cursor.execute("SELECT * from users where username=? or emailid=?",(new_user['username'],new_user['email']))
    if len(cursor.fetchall()) != 0:
        abort(409)
    else:
        cursor.execute("insert into users (username,emailid,password,full_name) values (?,?,?,?)",(new_user['username'],new_user['email'],new_user['password'],new_user['name']))
        conn.commit()
        status = "Success"
    conn.close()
    return status










@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error':'Bad Request'}),400)

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error':'Resource not found!'}),404)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)


