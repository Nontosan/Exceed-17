from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'user'
app.config['MONGO_URI'] = 'mongodb://0.0.0.0:27017/exceed'
mongo = PyMongo(app)

@app.route('/user', methods=['POST'])
def add():
    user_collection = mongo.db.user

    name = request.json['name']
    age = request.json['age']

    user_id = (user_collection.insert({'name': name, 'age': age}))
    new_user = user_collection.find_one({'_id': user_id})

    output = {'name': new_user['name'], 'age': new_user['age']}
    return output

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='1150', debug=True)
