from flask import Flask, render_template, url_for, request, session
import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    return "login"


@app.route("/balance", methods=["PUT", "GET"])
def balance():
    return "balance"


@app.route("/lib-store", methods=["PUT", "GET"])
def lib_store():
    return "lib. store"


@app.route("/price-cal")
def price_cal():
    return "price cal."


if __name__ == "__main__":
    app.run(debug=True)