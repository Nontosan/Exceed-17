from flask import Flask, render_template, url_for, request, session, make_response, redirect, flash
from functools import wraps
import datetime
import requests
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcdef"

def token_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        header = {"Authorization":f"Bearer {request.cookies.get('token')}"}
        response = requests.get("http://158.108.182.0:3000/", headers=header)
        print(response.json())
        if response.json()["message"] == "OK":
            return func(*args, **kwargs)
        else:
            flash("login first!", "danger")
            return redirect(url_for("home"))
    return inner

def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        header = {"Authorization":f"Bearer {request.cookies.get('token')}"}
        response = requests.get("http://158.108.182.0:3000/", headers=header)
        print(response.json())
        if response.json()["group"] == "admin":
            return func(*args, **kwargs)
        else:
            flash("You need to be an admin!", "danger")
            return redirect(url_for("home"))
    return inner

@app.route("/")
def home():
    return render_template(
        "index.html", F6=True, F7=False, F13=False, F14=False, F20=False, F21=False
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html", login=True)
    else:
        url = "http://158.108.182.0:3000/login"

        payload = request.form
        usrnm = payload["username"]
        pswd = payload["passwd"]
        credentials = f"{usrnm}:{pswd}"
        cred_bytes = credentials.encode('ascii')
        cred_fin = base64.b64encode(cred_bytes).decode('ascii')
        headers = {"Authorization": f"Basic {cred_fin}"}
        print(headers)

        response = requests.request("POST", url, headers=headers, data=payload)

        if (response.status_code == 401):
            flash("login fail!", "danger")
            return render_template("login.html")
        else:
            json = response.json()
            resp = make_response(redirect("/"))
            print(json)
            resp.set_cookie('token', json["token"], httponly=True)
            flash("login success!", "success")
            return resp


@app.route("/balance", methods=["PUT", "GET"])
@token_required
def balance():
    return render_template("balance.html", balance=True)


@app.route("/lib-store", methods=["PUT", "GET"])
@token_required
def lib_store():
    return render_template("lib-store.html", lib_store=True)


@app.route("/price-cal")
@token_required
@admin_required
def price_cal():
    return render_template("price-cal.html", price_cal=True)


if __name__ == "__main__":
    app.run(debug=True)