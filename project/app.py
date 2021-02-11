from flask import Flask, render_template, url_for, request, session, make_response, redirect, flash
import datetime
import requests
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcdef"

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

        response = requests.request("POST", url, headers=headers, data=payload)

        if (response.status_code == 401):
            flash("login fail!", "danger")
            return render_template("login.html")
        else:
            json = response.json()
            resp = make_response("Setting a cookie")
            resp.set_cookie('token', value = json["token"], httponly = True)
            flash("login success!", "success")
            return redirect("/")


@app.route("/balance", methods=["PUT", "GET"])
def balance():
    return render_template("balance.html", balance=True)


@app.route("/lib-store", methods=["PUT", "GET"])
def lib_store():
    return render_template("lib-store.html", lib_store=True)


@app.route("/price-cal")
def price_cal():
    #ic_res = request.get("http://158.108.182.0:3000/ic")
    ic_res = [
        {
            "Name": "Buzzer",
            "Pic_path": "../static/X-Coin.png",
            "Price": 245
        },
        {
            "Name": "Resistor",
            "Pic_path": "../static/X-Coin.png",
            "Price": 35
        },
        {
            "Name": "Breadbroad",
            "Pic_path": "../static/X-Coin.png",
            "Price": 200
        },
        {
            "Name": "LDR",
            "Pic_path": "../static/X-Coin.png",
            "Price": 50
        },
        {
            "Name": "LED",
            "Pic_path": "../static/X-Coin.png",
            "Price": 1000
        }      
    ]
    #print(ic_res.json())
    print(ic_res)
    ic = {}
    name = []
    pic_path = []
    price = []
    for i in range(len(ic_res)):
        #ic[i] = ic_res.json()[i]
        ic[i] = ic_res[i]
        name.append(ic[i]['Name'])
        pic_path.append(ic[i]['Pic_path'])
        price.append(ic[i]['Price'])
    return render_template("price-cal.html", price_cal=True, ic=ic, name=name, pic_path=pic_path, price=price)


if __name__ == "__main__":
    app.run(debug=True)