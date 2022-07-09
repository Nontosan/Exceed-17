from flask import Flask, request

app = Flask(__name__)

myUser = [
    {"id": 12348, "name": "Mana", "age": 20},
    {"id": 11114, "name": "Manee", "age": 19}
]

@app.route('/user', methods=['GET'])
def find():
    return {'result': myUser}

@app.route('/user/<input_id>', methods=['PUT'])
def edit_user(input_id):

    new_data = request.json
    
    for i in range(len(myUser)):
        if myUser[i]["id"] == int(input_id):
            myUser[i] = new_data
            return {"data": "OK"}

    return {"data": "Bad Request"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='1150', debug=True)
