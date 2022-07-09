from flask import Flask, request

app = Flask(__name__)

myUser = [
    {"name": "Mana", "age": 20},
    {"name": "Manee", "age": 19}
]

### First ###
#@app.route('/user', methods=['GET'])
#def find_user():
#    user_name = request.args.get('name')     
#    return {"data": user_name}

@app.route('/user', methods=['GET'])
def find_user():
    user_name = request.args.get('name')

    for i in myUser:
        if i["name"] == user_name:
            return i
            
    return {"data": "Not found"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='1150', debug=True)
