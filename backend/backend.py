from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
import hashlib, binascii, os
import json
import jwt
import datetime
from functools import wraps


f = open('config.json')
config = json.load(f)

app = Flask(__name__)

app.config['MONGO_URI'] = config['mongo_uri']
app.config['SECRET_KEY'] = config['secret_key']

mongo = PyMongo(app)
userCollection = mongo.db.user

f.close()


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
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing'}), 403

        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/return_group_from_token')
@token_required
def returnGroup():
    token = request.args.get('token')
    decode_data = jwt.decode(token, app.config['SECRET_KEY'])
    return jsonify({
        'user': decode_data['username'],
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)