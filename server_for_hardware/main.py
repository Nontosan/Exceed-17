from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://adminexceed:1q2w3e4r@158.108.182.0:2277/exceed'
mongo = PyMongo(app)

@app.route('/sensor/<nisit_id>', methods=['GET'])
def find_temp_from_user(nisit_id):
    output = mongo.db.exceedHardware.find_one_or_404({"nisit_id": nisit_id})            
    return { 
        "led1": output["led1"],
        "led2": output["led2"],
        "ldr": output["ldr"]
        }

@app.route('/sensor/<nisit_id>', methods=['POST'])
def post_temp_from_user(nisit_id):
    hardwareCollection = mongo.db.exceedHardware

    led1 = request.json["led1"]
    led2 = request.json["led2"]
    ldr = request.json["ldr"]

    nisit = hardwareCollection.find_one({"nisit_id": nisit_id})

    if nisit:
        hardwareCollection.update_one({"nisit_id": nisit_id}, {"$set": { 
            'led1': led1,
            'led2': led2,
            'ldr': ldr
            }})

        return {'result' : 'Updated successfully'}
    
    else:
        hardwareCollection.insert_one({"nisit_id": nisit_id, 
            'led1': led1,
            'led2': led2,
            'ldr': ldr
        })

        return {'result' : 'Created successfully'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5567', debug=True)