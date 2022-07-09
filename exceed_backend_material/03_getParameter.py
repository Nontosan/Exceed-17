from flask import Flask, request

app = Flask(__name__)

myUser = [
    {"id": "12348", "name": "Mana", "age": 20},
    {"id": "11114", "name": "Manee", "age": 19}
]

@app.route('/user/<id>', methods=['GET'])
def find_user(id):

    for i in myUser:
        if i["id"] == id:
            return i
            
    return {"data": "Not found"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='1150', debug=True)



#บอกเรื่องรับค่าเป็น string
#ถ้าอยากใช้ต้องเปลี่ยนเป็น int