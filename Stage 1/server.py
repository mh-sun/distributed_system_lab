from flask import Flask, request
from flask_socketio import SocketIO, emit
import requests
import apscheduler.schedulers.background
import pymongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)

avail_rider = []
avail_driver = []


def get_distance(p1, p2):
    temp = pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2)
    return pow(temp, 0.5)


def client_match():
    if not avail_driver:
        return
    for rider in avail_rider:
        mini = 50000
        sel_driver = None

        for driver in avail_driver:
            if get_distance(rider["loc"], driver["loc"]) < mini:
                sel_driver = driver

        fare = get_distance(rider['loc'], rider['des']) * 2

        notification = {
            'r_name': rider['name'],
            'd_name': sel_driver['name'],
            'fare': fare
        }
        print("Server has paired rider %s with driver %s" %
              (rider['name'], sel_driver['name']))
        print("message sent to comm :", notification)
        sio.emit("notify", notification)

        avail_rider.remove(rider)
        avail_driver.remove(sel_driver)


schedule = apscheduler.schedulers.background.BackgroundScheduler()
schedule.add_job(func=client_match, trigger="interval", seconds=5)
schedule.start()


@app.route("/rate", methods=["GET", "POST"])
def rating():
    data = request.json
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["gorib_uberdb"]
    mycol = mydb["ratings"]
    print("rider %s gave rating %d to driver %s" % (data['rname'], data['rate'], data['dname']))
    mycol.insert_one(data)
    return "Database Updated"


@app.route("/api/rider", methods=["POST"])
def rider_update():
    data = request.json
    print(data)
    avail_rider.append(data)
    return "Rider Api received by Server"


@app.route("/api/driver", methods=["POST"])
def driver_update():
    data = request.json
    print(data)
    avail_driver.append(data)
    return "Driver Api received by Server"


if __name__ == '__main__':
    sio.run(app, host="127.0.0.1", port=8005)
