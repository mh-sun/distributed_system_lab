import json
import pymongo
import flask
from flask import Flask, request
import socketio
import apscheduler.schedulers.background

app = Flask(__name__)
sio = socketio.Server()
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

avail_rider = []
avail_driver = []


def get_distance(p1, p2):
    temp = pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2)
    return pow(temp, 0.5)


def client_match():
    if not avail_driver:
        return
    for r in avail_rider:
        rider = json.loads(r)
        mini = 50000
        sel_driver = None
        sel_driverF = None
        for d in avail_driver:
            driver = json.loads(d)
            if get_distance(rider["loc"], driver["loc"]) < mini:
                sel_driverF = d
                sel_driver = driver

        fare = get_distance(rider['loc'], rider['des']) * 2

        notification = {'r_name': rider['name'], 'd_name': sel_driver['name'], 'fare': fare}
        # print(notification)
        print("Server has paired rider %s with driver %s" % (rider['name'], sel_driver['name']))
        sio.emit("notify", notification)

        avail_rider.remove(r)
        avail_driver.remove(sel_driverF)


schedule = apscheduler.schedulers.background.BackgroundScheduler()
schedule.add_job(func=client_match, trigger="interval", seconds=5)
schedule.start()


@app.route("/rider", methods=["GET", "POST"])
def rider_update():
    data = request.json
    avail_rider.append(data)
    return flask.Response(status=201)


@app.route("/driver", methods=["GET", "POST"])
def driver_update():
    data = request.json
    avail_driver.append(data)
    return flask.Response(status=201)


@app.route("/rate", methods=["GET", "POST"])
def rating():
    data = request.json
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["gorib_uberdb"]
    mycol = mydb["ratings"]
    mydict = json.loads(data)
    print("rider %s gave rating %d to driver %s" % (mydict['rname'], mydict['rate'], mydict['dname']))
    x = mycol.insert_one(mydict)

    return flask.Response(status=201)


if __name__ == "__main__":
    # sio.run(app, debug=True, port=5000, use_reloader=False)
    app.run(host="127.0.0.1", port=5000)