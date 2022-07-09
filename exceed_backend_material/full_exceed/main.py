from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_user:1q2w3e4r@158.108.182.0:2277/exceed_backend'
mongo = PyMongo(app)

myCollection = mongo.db.twitter

@app.route('/user', methods=['GET'])
def query_param():
    user_name = request.args.get('name')

    return { "data": user_name }

@app.route('/id/<id>', methods=['GET'])
def parameter(id):
    return {"data": id}

@app.route('/find_one', methods=['GET'])
def find_one():
    # มีแบบ filter
    # flit = {"author": "nontosan"}
    # query = myCollection.find_one(flit)

    query = myCollection.find_one()

    # query = myCollection.find_one_or_404()

    output = {
        "author": query["author"],
        "content1": query["content1"],
        "content2": query["content2"]
    }

    # return ตรง ๆ ไม่ได้ เพราะ _id
    return output


@app.route('/find_all', methods=['GET'])
def find():
    # มีแบบ filter
    # flit = {"author": "nontosan"}
    # query = myCollection.find(flit)

    query = myCollection.find()

    output = []

    for ele in query:
        output.append({
            "author": ele["author"],
            "content1": ele["content1"],
            "content2": ele["content2"]
        })

    return { "result": output }


@app.route('/create', methods=['POST'])
def insert_one():
    data = request.json

    myCollection.insert_one(data)
    return {'result': 'Created successfully'}


@app.route('/replace', methods=['PUT'])
def replace():
    data = request.json

    filt = {'author' : 'nontosan'}

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

    filt = {'author' : 'nontosan'}
    updated_content = {"$set": {'content1' : data["content1"]}}
    
    myCollection.update_one(filt, updated_content)
    
    return {'result' : 'Updated successfully'}


@app.route('/delete', methods=['DELETE'])
def delete():
    filt = {'author' : 'nontosan'}
    myCollection.delete_one(filt)
    
    return {'result' : 'Deleted successfully'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='24681', debug=True)
                                                       
