from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'user'
app.config['MONGO_URI'] = 'mongodb://0.0.0.0:2777/exceed'
mongo = PyMongo(app)

@app.route('/user', methods=['GET'])
def get_all():
    user_collection = mongo.db.user #อธิบาย

    output = []

    for i in user_collection.find():
        output.append({'name': i['name'], 'department': i['department']}) #hen pab

    #cannot return as list
    return {"data": output}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='1150', debug=True)
