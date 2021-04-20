import json

import flask
import pymongo
from flask import Flask, request

app = Flask(__name__)


@app.route("/rate", methods=["GET", "POST"])
def rating():
    data = request.json
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["gorib_uberdb"]
    mycol = mydb["ratings"]
    mydict = json.loads(data)
    print("rider %s gave rating %d to driver %s" % (mydict['rname'], mydict['rate'], mydict['dname']))
    mycol.insert_one(mydict)
    return flask.Response(status=201)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8002, debug=True)
