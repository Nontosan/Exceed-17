from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_user:1q2w3e4r@158.108.182.0:2277/exceed_backend'
mongo = PyMongo(app)

myCollection = mongo.db.facebook

@app.route('/', methods=['GET'])
def hello():
    return {"data": "hello"}

@app.route('/id/<myID>', methods=['GET'])
def parameter(myID):
    return {"data": myID}

@app.route('/user', methods=['GET'])
def query_param():
    user_name = request.args.get('name')

    return { "data": user_name }

@app.route('/find_all', methods=['GET'])
def find():

    #flit = {"author": "PNon"}
    #flit = {}
    myName = request.args.get('name')
    flit = {"author": myName}

    query = myCollection.find(flit)
    output = []

    for ele in query:
        output.append({
                "author": ele["author"],
                "content1": ele["content1"],
                "content2": ele["content2"]
                })

    return { "result": output }

@app.route('/find_one', methods=['GET'])
def find_one():
    query = myCollection.find_one()

    output = {
            "author": query["author"],
            "content1": query["content1"],
            "content2": query["content2"]
            }

    return output

@app.route('/create', methods=['POST'])
def insert_one():
    data = request.json
    myInsert = {
            "author": data["author"],
            "content1": data["content1"],
            "content2": data["content2"]
            }
    myCollection.insert_one(myInsert)
    return {'result': 'Created successfully'}

@app.route('/replace', methods=['PUT'])
def replace():
    data = request.json

    filt = {'author' : 'PNon'}

    updated_content = {"$set": {
        'author': data["author"],
        'content1': data["content1"],
        'content2': data["content2"]
        }}

    myCollection.update_one(filt, updated_content)
    return {'result': 'Replace successfully'}

@app.route('/update', methods=['PATCH'])
def update_one():
    data = request.json

    filt = {'author' : 'POhm'}
    updated_content = {"$set": {'content1' : data["content1"]}}

    myCollection.update_one(filt, updated_content)

    return {'result' : 'Updated successfully'}

@app.route('/delete', methods=['DELETE'])
def delete():
    filt = {'author' : 'POhm'}
    myCollection.delete_one(filt)
    return {'result' : 'Deleted successfully'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='50008', debug=True)