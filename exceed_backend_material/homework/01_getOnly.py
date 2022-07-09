from flask import Flask, request

app = Flask(__name__)

@app.route('/homework', methods=['GET'])
def myGet():
    return {"nickname": "PNon",
            "department": "CPE"}

@app.route('/homework', methods=['POST'])
def myPost():
    new_data = request.json
    return {"result": new_data["first"] + new_data["second"]}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001', debug=True)
