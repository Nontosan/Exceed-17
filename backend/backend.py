from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
from flask_httpauth import HTTPTokenAuth
import hashlib, binascii, os
import json
import jwt
import datetime
from functools import wraps


f = open('config.json')
config = json.load(f)

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

app.config['MONGO_URI'] = config['mongo_uri']
app.config['SECRET_KEY'] = config['secret_key']

f.close()

mongo = PyMongo(app)
userCollection = mongo.db.user
groupCollection = mongo.db.group
statementCollection = mongo.db.statement
warehouseCollection = mongo.db.warehouse


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = auth.get_auth()['token']
        except:
            return jsonify({'message': 'Token is missing'}), 403

        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/')
@token_required
def tokenCheck():
    token = auth.get_auth()['token']
    decode_data = jwt.decode(token, app.config['SECRET_KEY'])
    return jsonify({
        'message': 'OK', 
        'group': decode_data['group']
        })


@app.route('/sign-up', methods=['POST'])
def createUser():
    data = request.json

    try:
        username = data['username']
        password = data['password']
        group = data['group']
    except:
        return jsonify({'message': 'Bad Request'}), 400
    
    user = userCollection.find_one({'username': data['username']})
    
    if user:
        return jsonify({'message': 'Username already exists.'}), 400

    insert_data = {
        'username': username,
        'password': hash_password(password),
        'group': group
    }
    userCollection.insert_one(insert_data)

    return jsonify({'message': 'Account successfully created.'}), 200


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    user = userCollection.find_one({'username': auth.username})
    if not user:
        return jsonify({'message': 'Incorrect username.'}), 401

    store_pw = user['password']

    if verify_password(store_pw, auth.password):
        token = jwt.encode({
            'username': auth.username,
            'group': user['group'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/balance', methods=['GET'])
@token_required
def getBalance():
    token = auth.get_auth()['token']
    decode_data = jwt.decode(token, app.config['SECRET_KEY'])

    group = decode_data['group']

    if group == 'admin':
        all_data = groupCollection.find()

        output = []

        for ele in all_data:
            output.append({
                'group': ele['group'],
                'balance': ele['balance']
            })

        return jsonify(output), 200

    else:
        data = groupCollection.find_one({'group': group})
        if not data:
            return jsonify({'data': "Can't find group's balance"}), 404

        return jsonify({"group": data["group"], "balance": data["balance"]}), 200


@app.route('/balance', methods=['PUT'])
@token_required
def putBalance():
    body = request.json
    token = auth.get_auth()['token']
    decode_data = jwt.decode(token, app.config['SECRET_KEY'])
    
    group = decode_data['group']

    try:
        methods = body['methods']
        target = body['target'] 
        value = body['value']
        description = body['description']
    except:
        return jsonify({'message': 'Bad Request'}), 400

    now = datetime.datetime.now()
    date = str(now.date())
    time = str(now.time())

    if group == 'admin':
        if methods == 'deposit':
            filt = {'group': target}
            old_balance = groupCollection.find_one(filt)['balance']
            groupCollection.update_one(filt, {"$set": {"balance": old_balance + value}})

            statementCollection.insert_one({
                "group": target,
                "transactor": "admin",
                "methods": "deposit",
                "value": value,
                "timestamp": f"{date}_{time[:8]}",
                "description": description
            })

            return jsonify({'message': f"Group {target[1:]} have received {value} XCoin!"}), 200
        else:
            return jsonify({'message': 'Bad Request'}), 400

    else:
        data = groupCollection.find_one({'group': group})
        if not data:
            return jsonify({'data': "Can't find group."}), 404
        
        if methods == 'transfer':
            src_filt = {'group': group}
            des_filt = {'group': target}

            src_old_balance = groupCollection.find_one(src_filt)['balance']

            if (src_old_balance < value):
                return jsonify({'message': 'Not enough money!'}), 406
            
            des_old_balance = groupCollection.find_one(des_filt)['balance']
            if not isinstance(des_old_balance, int):
                return jsonify({'message': "Can't find target group."}), 404

            groupCollection.update_one(des_filt, {"$set": {"balance": des_old_balance + value}})
            groupCollection.update_one(src_filt, {"$set": {"balance": src_old_balance - value}})

            # for receiver
            statementCollection.insert_one({
                "group": target,
                "transactor": group,
                "methods": "transfer received",
                "value": value,
                "timestamp": f"{date}_{time[:8]}",
                "description": description
            })

            # for sender
            statementCollection.insert_one({
                "group": group,
                "transactor": group,
                "methods": "transfer sent",
                "value": value,
                "timestamp": f"{date}_{time[:8]}",
                "description": description
            })

            return jsonify({'message': 'Transfer complete!'}), 200
        elif methods == 'deposit':
            return jsonify({'message': 'Unauthorized.'}), 401
        else:
            return jsonify({'message': 'Bad Request.'}), 400


@app.route('/statement', methods=['GET'])
@token_required
def getStatement():
    token = auth.get_auth()['token']
    decode_data = jwt.decode(token, app.config['SECRET_KEY'])

    group = decode_data['group']

    if group == 'admin':
        return jsonify({'message': 'Please see full statement at admin mongo page.'}), 200
    
    filt = {'group': group}
    group_statement = statementCollection.find(filt)

    output = []

    for statement in group_statement:
        output.append({
            "group": statement['group'],
            "transactor": statement['transactor'],
            "methods": statement['methods'],
            "value": statement['value'],
            "timestamp": statement['timestamp'],
            "description": statement['description']
        })
    
    if output:
        return jsonify(output), 200
    else:
        return jsonify({'message': "Your group's statement is empty."}), 200


@app.route('/warehouse', methods=['GET'])
def getWarehouse():
    all_data = warehouseCollection.find()
    output = []

    for ele in all_data:
        output.append({
            "sensor": ele['sensor'],
            "remain": ele['remain'],
            "price": ele['price'],
            "link": ele['link'],
            "img_src": ele['img_src']
        })
    
    return {"data": output}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
    # app.run(host='0.0.0.0', port=3000)