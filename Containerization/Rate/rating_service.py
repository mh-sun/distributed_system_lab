import pymongo
from flask import Flask, request

app = Flask(__name__)


@app.route("/rate", methods=["GET", "POST"])
def rating():
    data = request.json
    print("Connected")
    myclient = pymongo.MongoClient("mongodb://0.0.0.0:27017/")
    mydb = myclient["gorib_uberdb"]
    mycol = mydb["ratings"]
    print("rider %s gave rating %d to driver %s" %
          (data['rname'], data['rate'], data['dname']))
    mycol.insert_one(data)
    return "Database Updated"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
