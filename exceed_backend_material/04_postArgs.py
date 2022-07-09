from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def myPost():
        data = request.json
        first = data["first"]
        operator = data["operator"]
        second = data["second"]
        return {
                "first": first,
                "op": operator,
                "sec": second
               }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5006', debug=True)
