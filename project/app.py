from flask import Flask, render_template, url_for, request, session
import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


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
    return render_template("price-cal.html", preice_cal=True)


if __name__ == "__main__":
    app.run(debug=True)