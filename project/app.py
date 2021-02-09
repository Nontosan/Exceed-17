from flask import Flask, render_template, url_for, request, session
import datetime

app = Flask(__name__)


@app.route("/")
def home():
    now = datetime.datetime.now()
    F6 = datetime.datetime(2021,2,6)
    F7 = datetime.datetime(2021,2,7)
    F13 = datetime.datetime(2021,2,13)
    F14 = datetime.datetime(2021,2,14)
    F20 = datetime.datetime(2021,2,20)
    F21 = datetime.datetime(2021,2,21)
    return render_template("index.html",F6=now>=F6,F7=now>=F7,F13=now>=F13,F14=now>=F14,F20=now>=F20,F21=now>=F21)


@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html", login=True)


@app.route("/balance", methods=["PUT", "GET"])
def balance():
    return render_template("balance.html", balance=True)


@app.route("/lib-store", methods=["PUT", "GET"])
def lib_store():
    return render_template("lib-store.html", lib_store=True)


@app.route("/price-cal")
def price_cal():
    return render_template("price-cal.html", price_cal=True)


if __name__ == "__main__":
    app.run(debug=True)