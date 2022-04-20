# back end of angular

from bson import ObjectId, json_util
from flask import Flask, jsonify, request
import pymongo as pm
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SystemIntegration2'

client = pm.MongoClient("mongodb+srv://test:test1234@demopy.8vbe5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test
col = db["user"] 
objID = ObjectId()

app.config['MONGO_DBNAME'] = 'test'

@app.route("/register/", methods=['POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        username = data['username']
        password = data['password']
        email = data['email']
        # check if username or email exists
        qry = col.find_one({"username": username})
        if qry is not None:
            return "Username already exists", 400
        qry = col.find_one({"email": email})
        if qry is None:
            col.insert_one({"username": username, "password": password, "email": email})
            return jsonify({"username": username}), 201
        else:
            return jsonify({"message": "Email already exists"}), 400

@app.route("/login/", methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        username = data['username']
        password = data['password']
        qry = col.find_one({"username": username})
        if qry is None:
            return "Username does not exist", 400
        if qry['password'] == password:
            return jsonify({"username": username}), 201
        else:
            return "Wrong password", 400

@app.route("/logout/", methods=['GET'])
def logout():
    if request.method == 'GET':
        return "Logged out", 200

@app.route("/order/", methods=['POST'])
def order():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        username = data[-1]['username']
        qry = col.find_one({"username": username})
        if qry is None:
            return "Username does not exist", 400
        else:
            for i in range(len(data)-1):
                col.update_one({"username": username}, {"$push": {"Order": {"_id": objID,"name": data[i]['name'], "price": data[i]['price']}}})
            return jsonify({"username": username}), 201

@app.route("/getOrder/<username>", methods=['GET'])
def getOrder(username):
    if request.method == 'GET':
        qry = col.find_one({"username": username})
        if qry is None:
            return "Username does not exist", 400
        else:
            if len(json.loads(json_util.dumps(qry['Order']))) == 0:
                return "No orders yet.", 400
            return jsonify({"Data": json.loads(json_util.dumps(qry['Order']))}), 201
if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
