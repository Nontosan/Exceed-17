from flask import Flask, request

app = Flask(__name__)

myUser = [
    {"id": 12348, "name": "Mana", "age": 20},
    {"id": 11114, "name": "Manee", "age": 19}
]

@app.route('/user', methods=['GET'])
def find():
    return {'result': myUser}

@app.route('/user', methods=['POST'])
def add_user():

    myUser.append(request.json)
            
    return {"data": "OK"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='1150', debug=True)
